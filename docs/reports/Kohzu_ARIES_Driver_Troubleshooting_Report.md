# Kohzu ARIES 드라이버 트러블슈팅 및 해결 보고서

## 1. 개요 (Overview)

| 항목 | 내용 |
|---|---|
| **대상 시스템** | Kohzu ARIES/LYNX 모터 컨트롤러 + XA07A-L202 스테이지 |
| **드라이버 파일** | `kohzuApp/src/KohzuAriesDriver.cpp` / `.h` |
| **IOC** | `KOHUZ_ALV1` (EPICS R7.0.7) |
| **통신 방식** | TCP/IP (`192.168.1.120:12321`), CRLF 종단 |
| **문서 목적** | 드라이버 개발 중 발생한 모든 주요 문제의 **증상 → 원인 분석 → 해결 → 교훈**을 시계열로 기록 |

본 문서는 Kohzu ARIES 모터 컨트롤러의 EPICS 드라이버 개발 과정에서 경험한 4건의 주요 장애에 대한 상세 트러블슈팅 기록입니다.
특히, `motorKohzu` 공식 모듈(Model 1)을 참조하여 `KohzuAriesDriver`(Model 3)를 리팩토링하는 과정에서 발생한 **프로토콜 불일치**, **응답 포맷 오판**, **파싱 로직 결함** 문제를 중점적으로 다룹니다.

---

## 2. 이슈 목록 (Issue Summary)

| # | 이슈 제목 | 심각도 | 상태 |
|---|---|---|---|
| 2.1 | APS 명령 타임아웃 (Command Timeout) | 🔴 Critical | ✅ 해결 |
| 2.2 | DMOV 고착 - 소프트웨어 판정 한계 (DMOV Stuck, Phase 1) | 🔴 Critical | ✅ 해결 |
| 2.3 | 이동 방향 역전 (Wrong Direction) | 🟡 Major | ✅ 해결 |
| 2.4 | DMOV 고착 - STR 응답 파싱 실패 (DMOV Stuck, Phase 2) | 🔴 Critical | ✅ 해결 |

---

## 3. 상세 이슈 분석 (Detailed Issue Analysis)

### 3.1 APS 명령 타임아웃 (Command Timeout)

#### 증상 (Symptoms)
- `APS`(절대 이동), `STP`(정지), `ORG`(원점 복귀) 명령 전송 시 **5초 타임아웃** 발생.
- IOC 콘솔에 `communication error, command=APS1/0/20000/0, status=1` 로그 반복.
- 모터는 실제로 이동하지만, EPICS 레코드에서 에러 상태로 전환됨.

#### 원인 분석 (Root Cause)
```
드라이버 코드 (변경 전):
  status = pasynOctetSyncIO->writeRead(...);  // APS 명령에 대해 응답을 대기
```

Kohzu ARIES 프로토콜 사양에 따르면:
- **조회 명령** (`STR`, `RDP`): 컨트롤러가 응답(`C STR1 ...`)을 반환함 → `writeRead()` 사용 적합.
- **동작 명령** (`APS`, `STP`, `ORG`): 컨트롤러가 **응답을 보내지 않음** → `writeRead()` 사용 시 응답 대기가 타임아웃으로 이어짐.

초기 드라이버에서 **모든 명령에 `writeRead()`를 사용**한 것이 원인이었습니다.

#### 해결 방안 (Solution)

명령 유형에 따라 통신 함수를 구분 적용:

| 명령 종류 | 명령어 | 통신 함수 | 응답 여부 |
|---|---|---|---|
| 이동 | `APS` | `pasynOctetSyncIO->write()` | ❌ 응답 없음 |
| 정지 | `STP` | `pasynOctetSyncIO->write()` | ❌ 응답 없음 |
| 원점 복귀 | `ORG` | `pasynOctetSyncIO->write()` | ❌ 응답 없음 |
| 상태 조회 | `STR` | `pasynOctetSyncIO->writeRead()` | ✅ 응답 있음 |
| 위치 조회 | `RDP` | `pasynOctetSyncIO->writeRead()` | ✅ 응답 있음 |

```cpp
// 변경 후 (move 함수)
status = pasynOctetSyncIO->write(pC_->pasynUserSelf, command, strlen(command),
                                 TIMEOUT, &nwrite);
// 응답을 대기하지 않으므로 타임아웃이 발생하지 않음
```

#### 교훈 (Lessons Learned)
> ⚠️ **프로토콜 사양서를 반드시 먼저 확인하라.** 모든 명령이 응답을 반환하는 것은 아니다. 특히 모터 컨트롤러와 같은 산업용 장비는 동작 명령에 대해 응답을 생략하는 경우가 많다.

---

### 3.2 DMOV 고착 - 소프트웨어 판정 한계 (Phase 1)

#### 증상 (Symptoms)
- 모터가 목표 위치에 정확히 도달했으나, `DMOV=0` (이동 중) 상태가 **영구적으로 유지**됨.
- `caget KOHZU:m1.DMOV` → 항상 `0` 반환.
- `verify_10mm_move.sh` 스크립트에서 이동 완료 대기 루프가 **무한 대기** 상태에 빠짐.

#### 원인 분석 (Root Cause)

**[Phase 1 원인]** 초기 드라이버는 **소프트웨어 기반 이동 판정** 로직을 사용:

```
이전 로직 (개념):
  if (abs(currentPos - lastPos) < tolerance_) {
      idleCount_++;
      if (idleCount_ > threshold) → 정지로 판정
  }
```

이 방식의 근본적 한계:
1. **Tolerance 값 설정 문제**: `tolerance_`가 너무 작으면 미세한 위치 진동에 의해 "아직 움직이는 중"으로 오판.
2. **미정의 초기값**: `tolerance_`, `idleCount_` 등이 명확하게 초기화되지 않은 경우 동작 불일치 발생.
3. **하드웨어 상태 무시**: 컨트롤러가 정확한 이동 상태 비트(`STR` 명령)를 제공함에도 이를 활용하지 않음.

#### 해결 방안 (Solution)

`motorKohzu` 모듈(Model 1, `drvSC800.cc`)의 로직을 참조하여 **하드웨어 상태 기반 판정**으로 전면 교체:

1. **소프트웨어 판정 변수 전부 제거**
   - `tolerance_`, `idleCount_`, `lastPosition_` 등 삭제.

2. **`STR` 명령 기반 상태 조회 도입**
   - `poll()` 함수에서 매 폴링마다 `STR<Axis>` 명령을 전송.
   - 응답의 Move 비트를 읽어 `motorStatusDone_`에 직접 반영.

3. **리미트 스위치 연동**
   - `STR` 응답의 `CWL`/`CCWL` 필드를 `motorStatusHighLimit_`/`motorStatusLowLimit_`에 연동.

```
변경 후 로직:
  STR1 전송 → 응답 파싱 → Move 비트 확인
  if (Move == 0) → DMOV=1 (정지)
  if (Move == 1) → DMOV=0 (이동 중)
```

#### 교훈 (Lessons Learned)
> ⚠️ **소프트웨어 Tolerance 기반 이동 감지는 신뢰할 수 없다.** 하드웨어가 상태 조회 명령을 제공하는 경우, 반드시 하드웨어 상태 비트를 기준으로 판정해야 한다.

---

### 3.3 이동 방향 역전 (Wrong Direction)

#### 증상 (Symptoms)
- `caput KOHZU:m1.RLV 10.0` (전진 +10mm) 명령 시 **-10mm 방향(원점 쪽)으로 이동**.
- 부호가 반전되어 모든 상대 이동/절대 이동이 반대 방향으로 수행됨.

#### 원인 분석 (Root Cause)

`motor.substitutions` 파일에서 `DIR`(방향) 및 `MRES`(분해능) 설정이 하드웨어 배선과 불일치:

```
# 문제가 있던 설정 예시
{MRES, "-0.0005"}  # 음수 MRES → 방향 반전 발생
# 또는
{DIR, "Neg"}       # 논리적 방향이 물리적 방향과 반대
```

EPICS 모터 레코드에서 방향 결정은 `DIR`과 `MRES` 부호의 **조합**에 의해 결정됩니다:

| DIR | MRES 부호 | 실제 이동 방향 |
|---|---|---|
| Pos | + | 정방향 ✅ |
| Pos | - | **역방향** ❌ |
| Neg | + | 역방향 |
| Neg | - | 정방향 |

#### 해결 방안 (Solution)

`motor.substitutions` 설정을 아래와 같이 확정:

```
{DIR, "Pos"},
{MRES, "0.0005"}   # 양수 (0.5 µm/pulse)
```

- 현재 하드웨어 배선 상태에서 `DIR=Pos` + `MRES=+0.0005`가 **정방향**임을 검증 완료.
- 방향 반전이 필요한 경우 `MRES` 부호를 변경하는 대신 **`DIR` 필드를 `Neg`로 변경**하는 것이 EPICS 표준 관행.

#### 교훈 (Lessons Learned)
> ⚠️ **`DIR`과 `MRES` 부호를 동시에 변경하면 혼란을 초래한다.** 방향 조정은 `DIR` 필드만으로 수행하고, `MRES`는 항상 양수(물리적 분해능)를 유지하는 것을 권장한다.

---

### 3.4 DMOV 고착 - STR 응답 파싱 실패 (Phase 2) ★ 최근 해결

#### 증상 (Symptoms)

Phase 1 해결(하드웨어 STR 기반 판정 도입) 이후에도 **동일한 `DMOV=0` 고착 현상**이 재발:

```bash
# verify_10mm_move.sh 실행 결과
Start Position: 0.0015 mm
[Step 1] Moving +10mm Relative (Forward)...
   [DEBUG] DMOV=0  RBV=10.0015  (35/120)   # ← 이미 도착했는데 DMOV=0
   [DEBUG] DMOV=0  RBV=10.0015  (40/120)   # ← 무한 대기...
   [DEBUG] DMOV=0  RBV=10.0015  (45/120)
```

IOC 콘솔에서 다음 에러 로그가 반복 출력:

```
KohzuAriesAxis::poll: STR1 parse FAILED! raw='C STR1    0       0       0       0 00' -> fallback moving=false
KohzuAriesAxis::poll: STR2 parse FAILED! raw='C STR2    0       0       0       3 00' -> fallback moving=false
```

#### 원인 분석 (Root Cause)

**두 가지 원인이 복합적으로 작용:**

##### 원인 1: 존재하지 않는 "서브커맨드" 필드 스킵 🔴

`motorKohzu` 모듈(Model 1) 문서를 참조하면서, STR 응답에 **서브커맨드 필드**(축 번호 반복)가 있다고 가정하고 파서를 작성했습니다:

```
가정한 포맷 (잘못됨):
  C  STR1  [1]  <Move>  <NOrg>  <OrgG>  <CWL>  <CCWL>  <Swing>  <Err>
            ↑
        서브커맨드 (축 번호 반복) - 실제로는 존재하지 않음!

실제 ARIES 응답 포맷:
  C  STR1  <Move>  <NOrg>  <OrgG>  <CWL>  <CCWL>  <Swing>  <Err>
           ↑
       이것이 바로 Move 비트!
```

코드에서의 동작:

```cpp
// 변경 전 (잘못된 파싱)
token = strtok(NULL, delimiters); // "STR1" ← 정상
token = strtok(NULL, delimiters); // "0"    ← ❌ 서브커맨드로 버림 (실제는 Move 비트!)
s_move = strtok(NULL, delimiters); // "0"   ← ❌ 이것을 Move로 읽지만 실제는 NOrg
// ... 이후 필드가 하나씩 밀림 → 마지막 필드(s_errr)가 NULL → parsed = false
```

##### 원인 2: 고정 폭 포맷에 의한 토큰 연결 🟡

ARIES 컨트롤러가 **고정 폭(Fixed-Width) 포맷**으로 응답을 전송하여, 인접한 단일 자릿수 필드가 연결됨:

```
실제 응답: "C STR1    0       0       0       0 00"
                                                ↑↑
                               Swing=0 + Err=0 이 "00"으로 연결
```

`strtok`으로 분리하면 `"00"`이 하나의 토큰으로 인식되어, 예상 필드 수(7개) 미달 → 파싱 조건(`s_errr != NULL`) 불충족.

##### 원인 3: 파싱 실패 시 Fallback 부재 (이전 버전) 🟡

Phase 2 디버깅 추가 전에는, `parsed == false`일 때 `*moving`과 `motorStatusDone_`을 **아무것도 설정하지 않았습니다**:

```cpp
// 변경 전 - else 블록이 사실상 비어있음
} else {
    // Fallback or Error on parse
    // setIntegerParam(pC_->motorStatusProblem_, 1);  ← 주석 처리!
}
// *moving이 미설정 → 이전 poll의 값이 잔존 → DMOV=0 영구 고착
```

#### 해결 방안 (Solution)

`poll()` 함수의 STR 파싱 로직을 **실제 ARIES 응답 포맷에 맞게 전면 재작성**:

##### 수정 1: 서브커맨드 필드 스킵 제거

```cpp
// 변경 후 - STR<n> 직후부터 데이터 필드 시작
if (token && strcmp(token, "C") == 0) {
    token = strtok(NULL, delimiters); // "STR1" (명령 에코)
    // ★ 서브커맨드 스킵 없음 - 바로 데이터 수집 시작
```

##### 수정 2: 유연한 필드 수집 + 연결 숫자 분리

```cpp
// 나머지 토큰을 배열로 수집, 연결된 숫자 분리 처리
int fields[10] = {0};
int nFields = 0;
char *tok;
while ((tok = strtok(NULL, delimiters)) != NULL && nFields < 10) {
    int len = strlen(tok);
    if (len > 1) {
        // "00" → [0, 0] 으로 분리
        for (int i = 0; i < len && nFields < 10; i++) {
            if (tok[i] >= '0' && tok[i] <= '9') {
                fields[nFields++] = tok[i] - '0';
            }
        }
    } else {
        fields[nFields++] = atoi(tok);
    }
}
```

##### 수정 3: Move 비트 우선 매핑 + 유연한 성공 조건

```cpp
// [0]=Move, [1]=NOrg, [2]=OrgG, [3]=CWL, [4]=CCWL, [5]=Swing, [6]=Err
if (nFields >= 1) {
    r_move = fields[0];   // Move 비트만 있으면 파싱 성공
    parsed = true;
}
if (nFields >= 4) r_cwlm = fields[3]; // CW Limit (있으면)
if (nFields >= 5) r_ccwl = fields[4]; // CCW Limit (있으면)
if (nFields >= 7) r_errr = fields[6]; // Error (있으면)
```

##### 수정 4: 파싱 실패 Fallback 보장

```cpp
} else {
    // 파싱 실패 시에도 DMOV 고착 방지
    *moving = false;
    setIntegerParam(pC_->motorStatusDone_, 1);
    setIntegerParam(pC_->motorStatusProblem_, 1);
}
```

##### 수정 5: 통신 에러 시에도 안전한 상태 설정

```cpp
if (status != asynSuccess) {
    *moving = false;
    setIntegerParam(pC_->motorStatusDone_, 1);    // DMOV 고착 방지
    setIntegerParam(pC_->motorStatusProblem_, 1);  // 에러 플래그
    callParamCallbacks();
    return asynSuccess;
}
```

#### 파싱 흐름 비교 (Before vs After)

```
[변경 전] "C STR1 0 0 0 0 00" 파싱:
  "C" → "STR1" → "0"(서브커맨드로 버림!) → "0" → "0" → "0" → "00"
  → 필드 부족(s_errr=NULL) → parsed=false → DMOV 미설정 → 고착 🔴

[변경 후] "C STR1 0 0 0 0 00" 파싱:
  "C" → "STR1" → fields에 수집: [0, 0, 0, 0, 0, 0]
  → nFields=6 → Move=0 → parsed=true → DMOV=1 (정지) ✅
```

#### 교훈 (Lessons Learned)
> ⚠️ **참조 모듈(motorKohzu Model 1)과 실제 대상(ARIES Model 3)의 응답 포맷이 다를 수 있다.** 반드시 실제 하드웨어 응답을 로그로 확인하고, 그에 맞게 파서를 작성해야 한다.
>
> ⚠️ **파싱 실패 시 반드시 안전한 기본값을 설정하라.** `*moving`이나 `motorStatusDone_`를 설정하지 않으면 이전 값이 잔존하여 상태 고착이 발생한다.
>
> ⚠️ **디버그 로그를 먼저 추가하라.** 실제 응답 원문을 출력하는 로그 1줄이 문제를 즉시 드러나게 해 주었다.

---

## 4. 검증 도구 (`verify_10mm_move.sh`)

검증 스크립트도 이슈 대응 과정에서 개선되었습니다:

### 4.1 스크립트 변경 이력

| 버전 | 내용 |
|---|---|
| v1 | 단방향 10mm 이동 검증. `bc`로 거리 계산. |
| v2 | 전진(+10mm) + 후진(-10mm) 양방향 검증 추가. |
| v3 (현재) | `wait_for_done()` 함수 추가 (caget 실패 처리, 디버그 출력, 타임아웃 시 STOP 명령). `python3`로 정밀 계산. `caput` 후 `sleep 1` 추가 (드라이버 시작 시간 확보). |

### 4.2 wait_for_done 함수 주요 개선점

```bash
wait_for_done() {
    # 1. caget 실패 시 재시도 (빈 값/에러 처리)
    # 2. 문자열 비교("$DMOV" = "1") 사용 → 비정상 값에도 안전
    # 3. 2.5초 간격 디버그 출력 (DMOV + RBV 동시 표시)
    # 4. 타임아웃 시 STOP 명령 전송 후 종료
}
```

---

## 5. 시스템 현황 (Current Status)

### 5.1 아키텍처

```
                    +-------------------+
                    | EPICS Motor Record|
                    |   KOHZU:m1.*      |
                    +--------+----------+
                             |
                    +--------v----------+
                    | KohzuAriesDriver  |
                    |   poll() → STR    |  ← Hardware Status Driven
                    |   move() → APS    |  ← Write-Only (no response)
                    |   stop() → STP    |  ← Write-Only
                    +--------+----------+
                             |
                    +--------v----------+
                    | asynOctetSyncIO   |
                    | TCP 192.168.1.120 |
                    | Port: 12321       |
                    | EOS: \r\n (CRLF)  |
                    +--------+----------+
                             |
                    +--------v----------+
                    | Kohzu ARIES       |
                    | Controller        |
                    +-------------------+
```

### 5.2 현재 설정 값

| 파라미터 | 값 | 비고 |
|---|---|---|
| `MRES` | 0.0005 mm/pulse | 0.5 µm 분해능 |
| `DIR` | Pos | 정방향 |
| `EGU` | mm | 밀리미터 |
| `VELO` | (느림, ~0.55 mm/s) | 추후 상향 필요 |
| `Moving Poll` | 0.2 sec | 이동 중 폴링 주기 |
| `Idle Poll` | 1.0 sec | 유휴 시 폴링 주기 |
| `Timeout` | 5.0 sec | 통신 타임아웃 |

### 5.3 통신 프로토콜 요약

| 명령 | 포맷 예시 | 방식 | 응답 예시 |
|---|---|---|---|
| 절대 이동 | `APS1/0/20000/0` | Write-Only | (없음) |
| 정지 | `STP1` | Write-Only | (없음) |
| 원점 복귀 | `ORG1/0/0/0` | Write-Only | (없음) |
| 상태 조회 | `STR1` | Write-Read | `C STR1 0 0 0 0 00` |
| 위치 조회 | `RDP1` | Write-Read | `C RDP1 <position>` |

> **주의**: `STR%d/1` 형식 사용 시 에러(Code 100)가 발생합니다. 반드시 `STR%d` (파라미터 없이) 사용해야 합니다.

### 5.4 STR 응답 필드 맵

```
실제 응답: "C STR1    0       0       0       0 00"

토큰 분리 후 필드 배열:
  fields[0] = Move   (0=정지, 1=이동 중)    → motorStatusDone_
  fields[1] = NOrg   (원점 미발견)
  fields[2] = OrgG   (원점 게이트)
  fields[3] = CWL    (CW 리미트 스위치)     → motorStatusHighLimit_
  fields[4] = CCWL   (CCW 리미트 스위치)    → motorStatusLowLimit_
  fields[5] = Swing  (스윙 상태)
  fields[6] = Err    (에러 코드)             → motorStatusProblem_

※ 고정 폭 포맷으로 인해 인접 필드가 연결될 수 있음 (예: "00" → Swing=0, Err=0)
```

---

## 6. 남은 과제 (Remaining Issues)

| # | 항목 | 우선순위 | 설명 |
|---|---|---|---|
| 1 | 모터 속도 상향 | 🟡 중간 | 현재 약 0.55 mm/s. `VELO` 설정 및 속도 테이블 검토 필요. |
| 2 | Jog 운전 미구현 | 🟢 낮음 | `moveVelocity()` 함수가 `asynError` 반환 (미구현). |
| 3 | STR2 CWL=3 확인 | 🟢 낮음 | Axis 2의 STR 응답에서 CWL=3이 반환됨. 물리적 연결 상태 확인 필요. |

---

## 7. 변경 이력 (Change Log)

| 날짜 | 버전 | 내용 |
|---|---|---|
| 2026-02-12 | v1.0 | 최초 작성. APS 타임아웃, DMOV 고착(Phase 1), 방향 역전 문제 기록. |
| 2026-02-13 | v2.0 | DMOV 고착(Phase 2, STR 파싱 실패) 이슈 추가. poll() 함수 전면 재작성 기록. 검증 스크립트 개선사항 반영. 시스템 아키텍처 다이어그램 추가. |

---
**작성일**: 2026-02-13 (v2.0)
**작성자**: MHDev / Antigravity Assistant
