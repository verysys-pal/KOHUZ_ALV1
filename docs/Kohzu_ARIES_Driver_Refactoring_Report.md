# KohzuAriesDriver 리팩토링 완료 보고서

**최종 수정**: 2026-02-13 15:05  
**대상**: `kohzuApp/src/KohzuAriesDriver.cpp`, `KohzuAriesDriver.h`  
**검증 기준**: ARIES/LYNX 컨트롤러 매뉴얼 (NotebookLM 소스)  
**빌드 결과**: ✅ 에러 0건 / 경고 0건  
**실기 검증**: ✅ WTB 명령 성공 확인 (`C WTB1 ... status=0`)

---

## 1. 리팩토링 배경

### 1.1 발단

속도 검증 테스트(`verify_20mm_speed_ramp.sh`)에서 **VELO를 0.5~4.1 mm/s로 변경해도 실제 이동 속도가 ~0.5 mm/s로 고정**되는 문제가 발견되었다. 원인 분석 결과, 드라이버의 `move()` 함수가 EPICS의 `maxVelocity` 파라미터를 완전히 무시하고 있었다.

이를 계기로 NotebookLM에서 ARIES 컨트롤러 전체 명령어 사양을 조회하여 **현재 드라이버 코드를 사양 기준으로 전수 점검**하였으며, 총 14건의 이슈를 발견하고 수정하였다.

### 1.2 참조 자료

| 자료 | 출처 |
|---|---|
| ARIES 명령어 전체 사양 | NotebookLM → Kohzu Motor Integration Guide |
| motorKohzu 모듈 (drvSC800.cc) | EPICS synApps motorKohzu |
| Troubleshooting Report | `doc/Kohzu_ARIES_Driver_Troubleshooting_Report.md` |

---

## 2. 수정 이슈 목록 (16건)

### 🔴 Critical (8건)

| # | 이슈 | Before | After |
|---|---|---|---|
| 1 | **속도 미적용 (핵심 버그)** | `maxVelocity` 무시, Speed Table 고정 | `setSpeedTable()` 분리, WTB → APS 2단계 전송 |
| 2 | **APS 응답 미처리** | `write()` (응답 무시) | `writeRead()` + 에러 응답 체크 |
| 3 | **ORG 파라미터 오류** | `ORG%d/0/0/0` (4개 인수) | `ORG%d/0/1` (3개: 축/테이블/응답) |
| 4 | **JOG(FRP) 미구현** | `return asynError` | FRP `<축>/<테이블>/<방향>` 완전 구현 |
| 5 | **STR 필드 매핑 오류** | CWL/CCWL 개별 필드로 분리 읽기 | 비트마스크 디코딩 (`&0x02` / `&0x01`) |
| 6 | **APS 포맷 혼동** | 2번째 파라미터를 "Mode"로 오해 | "Speed Table 번호"로 정정 |
| 7 | **WTB 에러 105** *(v1.1 추가)* | 가속시간 범위 초과 (클램프 없음) | 속도별 가속시간 상한 클램프 적용 |
| 8 | **acceleration 단위 오해** *(v1.1 추가)* | ACCL(초)로 오해 → 가속 10초 | steps/s² 단위로 올바르게 변환 → 500ms |

### 🟡 Important (6건)

| # | 이슈 | Before | After |
|---|---|---|---|
| 9 | **STP 정지모드 누락** | `STP%d` (모드 미지정) | `STP%d/0` (감속정지) |
| 10 | **STP 응답 미처리** | `write()` (응답 무시) | `sendCommand(writeRead)` 사용 |
| 11 | **ORG 속도 설정 없음** | 기본 테이블 고정 | WTB로 원점 복귀 속도 설정 |
| 12 | **EMG 비상정지 미감지** | STR에서 EMG 필드 무시 | `fields[1]` → `motorStatusProblem_` |
| 13 | **에러 응답 파싱 없음** | "E ..." 무시 | `response[0]=='E'` 체크 전 함수 적용 |
| 14 | **통신 에러 플래그 미설정** | 없음 | `motorStatusCommsError_` 설정/클리어 |

### ⚪ Minor (2건)

| # | 이슈 | Before | After |
|---|---|---|---|
| 15 | **헤더 `friend class` 2중 선언** | 24행과 22행 중복 | 단일 선언으로 정리 |
| 16 | **TIMEOUT 상수** | `2.0` 하드코딩 | `CMD_TIMEOUT(5.0)` / `MOVE_TIMEOUT(2.0)` 분리 |

---

## 3. 핵심 변경 사항 상세

### 3.1 속도 설정 — WTB 명령 도입

#### 변경 전 (속도 무시)

```cpp
// move() 함수 - maxVelocity 파라미터 완전 무시
sprintf(command, "APS%d/0/%d/0", axisNo_ + 1, pulse);
// 두 번째 파라미터 '0'을 "Mode"로 오해했으나, 실제로는 Speed Table 번호
```

#### 변경 후 (WTB + APS 2단계)

```cpp
// 1) setSpeedTable(): VELO/VBAS/ACCL → WTB 명령
//    WTB <축>/<테이블>/<시작pps>/<최대pps>/<가속×10ms>/<감속×10ms>/<패턴>
sprintf(command, "WTB%d/0/%d/%d/%d/%d/2",
        axisID, startSpeed, topSpeed, accelTime, decelTime);
pC_->sendCommand(command, response, sizeof(response), CMD_TIMEOUT);

// 2) APS: Speed Table #0 참조하여 이동
sprintf(command, "APS%d/0/%d/1", axisID, pulse);
pC_->sendCommand(command, response, sizeof(response), CMD_TIMEOUT);
```

#### 변환 로직 *(v1.1 수정: acceleration 단위 정정)*

```
EPICS 설정:
  VELO = 2.0 mm/s, VBAS = 0.1 mm/s, ACCL = 0.5s, MRES = 0.0005 mm/step

asynMotor 변환 (자동):
  maxVelocity = VELO / MRES = 2.0 / 0.0005 = 4000 steps/s (pps)
  minVelocity = VBAS / MRES = 0.1 / 0.0005 = 200 pps
  acceleration = (VELO - VBAS) / (ACCL × MRES)
               = (2.0 - 0.1) / (0.5 × 0.0005)
               = 7600 steps/s²  ← 가속도! (ACCL 초가 아님)

드라이버 변환 (v1.1 수정):
  startSpeed   = 200 pps
  topSpeed     = 4000 pps
  accelSeconds = (topSpeed - startSpeed) / acceleration
               = (4000 - 200) / 7600
               = 0.5초  ← ACCL 원래 값 복원
  accelTime    = 0.5 × 100 = 50 (× 10ms = 500ms)

전송 명령:
  WTB1/0/200/4000/50/50/2
  APS1/0/<target_pulse>/1
```

> ⚠️ **v1.0 버그**: `acceleration`을 ACCL(초)로 오해하여
> `accelTime = 7600 × 100 = 760,000`이 되었고, 클램프 후 1000(=10초 가속)이
> 적용되어 속도가 정상 반영되지 않았음. v1.1에서 수정 완료.

### 3.2 JOG 구현 — FRP 명령

```cpp
// FRP <축>/<속도테이블>/<방향>
// 방향: 0=CW(정방향), 1=CCW(역방향)
// maxVelocity의 부호로 방향 결정
int direction = (maxVelocity >= 0) ? 0 : 1;
sprintf(command, "FRP%d/0/%d", axisID, direction);
```

EPICS OPI에서 JOGF/JOGR 버튼 사용 가능.

### 3.3 STP 포맷 수정

```cpp
// Before: STP1 (정지모드 누락 → 컨트롤러 동작 불명)
// After:  STP1/0 (감속정지)
sprintf(command, "STP%d/0", axisID);

// 참고: STP <축>/<모드>
//   모드 0 = 감속정지 (안전)
//   모드 1 = 비상정지 (즉시)
//   축 0 = 전체 축 정지
```

### 3.4 ORG 포맷 수정

```cpp
// Before: ORG1/0/0/0 (4개 인수 - 잘못된 포맷)
// After:  ORG1/0/1   (3개: 축/속도테이블/응답방식)
sprintf(command, "ORG%d/0/1", axisID);
```

### 3.5 STR 필드 재매핑

```
ARIES 매뉴얼 기준:
  "C STR <axis> <b> <c> <d> <e> <f> <g>"

  b: 구동상태 (0=정지, 1=동작중, 2=피드백)  → motorStatusDone_
  c: EMG 비상정지 (0=OFF, 1=ON)             → motorStatusProblem_
  d: ORG/NORG 센서 (0~3)                    → (향후 motorStatusAtHome_)
  e: CW/CCW 리미트 비트마스크                 → motorStatusHighLimit_ / LowLimit_
  f: 소프트 리미트 (0/1/2)                   → (향후 확장)
  g: 보정 허용 범위                           → (향후 확장)
```

#### 리미트 비트마스크 디코딩 (핵심 수정)

```
Before: CWL=fields[3], CCWL=fields[4] (개별 필드로 분리 — 오류)

After:  e 값 하나에서 비트 연산으로 추출
  e=0: 양쪽 OFF           → CW=0, CCW=0
  e=1: CCW만 ON           → CW=0, CCW=1
  e=2: CW만 ON            → CW=1, CCW=0
  e=3: 양쪽 ON            → CW=1, CCW=1

코드:
  int cwLimit  = (r_limits & 0x02) ? 1 : 0;  // bit 1
  int ccwLimit = (r_limits & 0x01) ? 1 : 0;  // bit 0
```

---

### 3.6 WTB 에러 105 트러블슈팅 *(v1.1 추가)*

#### 증상
```
E   WTB1    105
→ 5번째 파라미터(가속 시간)가 설정 범위를 벗어남
```

#### 원인
ARIES 에러 코드 `10n` = "n번째 파라미터 범위 초과".
`acceleration` 파라미터를 ACCL(초)로 오해하여, 실제 steps/s² 값(7600)에
×100을 적용 → 760,000이 되어 범위 초과.

#### ARIES 속도별 가속 시간 유효 범위

| 최대 속도 (pps) | 가속 시간 범위 (설정값) | 실제 시간 범위 |
|---|---|---|
| 1 ~ 20 | 1 ~ 10 | 10 ~ 100 ms |
| 21 ~ 250 | 1 ~ 100 | 10 ~ 1,000 ms |
| 251 ~ 1,000 | 1 ~ 100 | 10 ~ 1,000 ms |
| 1,001 ~ 250,000 | 1 ~ 1,000 | 10 ~ 10,000 ms |

#### 해결
1. `acceleration`(steps/s²)에서 올바른 ACCL(초) 역산:
   ```cpp
   accelSeconds = (topSpeed - startSpeed) / acceleration;
   ```
2. 속도별 가속 시간 상한 클램프 적용
3. 에러 발생 시에도 기존 테이블 값으로 이동 시도

#### 실기 검증 결과
```
SENDING cmd='WTB1/0/200/10000/50/50/2'
RESPONSE='C WTB1 0 200 10000 50 50 2 ...' status=0  ← 성공!
```

---

## 4. 아키텍처 변경

### 4.1 함수 구조 비교

```
═══════════════════════════════════════════════════════════════
                        Before
═══════════════════════════════════════════════════════════════

move()          ──► APS (write only, 속도 무시)
stop()          ──► STP (write only, 모드 없음)
moveVelocity()  ──► return asynError (미구현)
home()          ──► ORG (write only, 4 인수)
poll()          ──► STR + RDP (필드 매핑 오류)

═══════════════════════════════════════════════════════════════
                        After
═══════════════════════════════════════════════════════════════

move()          ──► setSpeedTable() ──► WTB (writeRead)
                └──► APS (writeRead + 에러 체크)

stop()          ──► STP (writeRead + 모드 0)

moveVelocity()  ──► setSpeedTable() ──► WTB (writeRead)
                └──► FRP (writeRead + 방향)

home()          ──► setSpeedTable() ──► WTB (writeRead)
                └──► ORG (writeRead + 3 인수)

poll()          ──► STR (EMG + 비트마스크 + 에러 응답 체크)
                └──► RDP (에러 응답 체크)
```

### 4.2 헬퍼 함수 추가

| 함수 | 설명 |
|---|---|
| `sendCommand()` | writeRead — 응답 있는 명령용 (기존) |
| `sendOnly()` | write only — 응답 없는 명령용 (신규) |
| `setSpeedTable()` | WTB 명령으로 Speed Table #0 설정 (신규) |

### 4.3 상수 정의 개선

| 상수 | 값 | 용도 |
|---|---|---|
| `CMD_TIMEOUT` | 5.0초 | 일반 명령 타임아웃 |
| `MOVE_TIMEOUT` | 2.0초 | 이동 명령 (즉시 응답) |
| `ARIES_MIN_START_SPEED` | 1 pps | 시동 속도 하한 |
| `ARIES_MAX_START_SPEED` | 2,500,000 pps | 시동 속도 상한 |
| `ARIES_MIN_TOP_SPEED` | 2 pps | 최대 속도 하한 |
| `ARIES_MAX_TOP_SPEED` | 5,000,000 pps | 최대 속도 상한 |

---

## 5. ARIES 명령어 매핑 (사양 ↔ 구현)

| 명령 | ARIES 포맷 | 드라이버 함수 | 상태 |
|---|---|---|---|
| **APS** | `APS a/b/c/d` | `move()` | ✅ 구현 |
| **RPS** | `RPS a/b/c/d` | (APS로 대체) | ⏸ 미사용 |
| **FRP** | `FRP a/b/c` | `moveVelocity()` | ✅ 신규 |
| **STP** | `STP a/b` | `stop()` | ✅ 수정 |
| **ORG** | `ORG a/b/c` | `home()` | ✅ 수정 |
| **WTB** | `WTB a/b/c/d/e/f/g` | `setSpeedTable()` | ✅ 신규 |
| **STR** | `STR a` → `C STR a b c d e f g` | `poll()` | ✅ 수정 |
| **RDP** | `RDP a` → `C RDP a <pos>` | `poll()` | ✅ 수정 |
| **RTB** | `RTB a/b` | — | ⏸ 미구현 |
| **RST** | `RST` | — | ⏸ 미구현 |
| **MPS** | `MPS ...` (다축이동) | — | ⏸ 미구현 |
| **RDE** | `RDE a` (엔코더 읽기) | — | ⏸ 미구현 |

---

## 6. 빌드 검증

```bash
$ make 2>&1 | grep -E 'error|warning|Installing'
Installing created executable ../../../bin/linux-x86_64/KOHUZ_ALV1
Installing shared library ../../../lib/linux-x86_64/libKohzuAries.so
Installing library ../../../lib/linux-x86_64/libKohzuAries.a

# 결과: 에러 0건, 경고 0건
```

---

## 7. 향후 과제

| 우선순위 | 과제 | 설명 | 상태 |
|---|---|---|---|
| ~~🔴~~ | ~~**WTB 속도 설정**~~ | ~~WTB 명령으로 속도 테이블 설정~~ | ✅ v1.1 해결 |
| ~~🔴~~ | ~~**acceleration 단위 변환**~~ | ~~steps/s² → ACCL(초) 올바른 변환~~ | ✅ v1.1 해결 |
| 🔴 | **실기 속도 램프 검증** | `verify_20mm_speed_ramp.sh` 실행하여 속도별 시간 변화 확인 | 🔄 진행 중 |
| 🔴 | **검증 스크립트 업그레이드** | `verify_KOHZU_Scenario_V2.sh` 전수 점검 및 리팩토링 | 🔄 진행 중 |
| 🟡 | **RPS 상대이동** | `move()` 에서 `relative` 플래그 시 RPS 명령 사용 | ⏸ |
| 🟡 | **RTB 속도 확인** | 설정된 Speed Table 값을 읽어서 검증하는 기능 | ⏸ |
| 🟡 | **RDE 엔코더 위치** | UEIP=Yes 시 엔코더 위치를 별도로 읽는 기능 | ⏸ |
| ⚪ | **소프트 리미트 활용** | STR `fields[4]` (r_softlim) 값을 EPICS 레코드에 반영 | ⏸ |
| ⚪ | **ORG 센서 상태** | STR `fields[2]` 를 `motorStatusAtHome_`에 반영 | ⏸ |

---

## 8. 변경 이력

| 일자 | 버전 | 변경 내용 |
|---|---|---|
| 2026-02-05 | v0.1 | 초기 드라이버 작성 (APS/STP/ORG/STR/RDP) |
| 2026-02-12 | v0.2 | DMOV 고착 해결 (STR 파싱 수정, 폴백 로직) |
| 2026-02-12 | v0.3 | 통신 프로토콜 수정 (CRLF, write/writeRead 분리) |
| 2026-02-13 | v0.4 | WTB 속도 설정 추가 (속도 미적용 버그 수정) |
| 2026-02-13 | v1.0 | 전면 리팩토링 (14건 이슈 해결) |
| **2026-02-13** | **v1.1** | **WTB 에러 105 해결, acceleration 단위 수정 (+2건, 총 16건)** |

### v1.1 변경 세부 (2026-02-13 15:05)

1. **WTB 에러 105 해결**
   - 원인: `acceleration`(steps/s²)을 ACCL(초)로 오해 → 가속시간 760,000 (범위 초과)
   - 수정: `accelSeconds = (topSpeed - startSpeed) / acceleration` 변환 적용
   - 결과: `WTB1/0/200/10000/50/50/2` → `C WTB1 ... status=0` (성공)

2. **속도별 가속 시간 클램프 추가**
   - ARIES 사양에 따른 속도 구간별 상한/하한 적용
   - 범위 초과 시 자동 클램프 (에러 방지)

3. **WTB 디버그 로깅 강화**
   - 전송 명령과 응답을 `ASYN_TRACE_ERROR` 레벨로 출력
   - 실기 디버그 시 `asynSetTraceMask` 변경 없이 확인 가능

---

*본 보고서는 ARIES 매뉴얼 사양(NotebookLM 조회)을 기준으로 드라이버 코드를 전수 점검한 결과를 기록한 것입니다.*
