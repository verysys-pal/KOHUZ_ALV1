# KOHZU 모터 검증 스크립트 사용 가이드

> **스크립트**: `verify_Scenario_V1.sh`  
> **대상 시스템**: KOHZU ARIES/LYNX Controller + XA07A-L202 Stage  
> **최종 업데이트**: 2026-02-13

---

## 목차

1. [개요](#1-개요)
2. [사전 요구사항](#2-사전-요구사항)
3. [설치 및 준비](#3-설치-및-준비)
4. [사용법](#4-사용법)
5. [검증 시나리오 상세](#5-검증-시나리오-상세)
6. [출력 해석](#6-출력-해석)
7. [MSTA 비트 해석표](#7-msta-비트-해석표)
8. [트러블슈팅](#8-트러블슈팅)
9. [커스터마이징](#9-커스터마이징)
10. [관련 파일 목록](#10-관련-파일-목록)

---

## 1. 개요

`verify_Scenario_V1.sh`는 Kohzu ARIES/LYNX 모터 컨트롤러와 XA07A-L202 스테이지가 EPICS IOC를 통해 정상적으로 동작하는지 **전 기능을 자동으로 검증**하는 스크립트입니다.

### 주요 특징

| 특징 | 설명 |
|------|------|
| **9단계 검증** | 연결 → 원점복귀 → 절대이동 → 상대이동 → 속도변경 → 조그/정지 → 소프트리미트 → 하드웨어리미트 → 최종복귀 |
| **자동 판정** | 각 Step을 PASS/FAIL/SKIP으로 자동 판정 |
| **자동 로그** | 검증 결과를 타임스탬프 포함 로그 파일로 자동 저장 |
| **안전 설계** | caget 실패 시 재시도, 타임아웃 방어, MSTA 통신에러/Problem 비트 감지 |
| **CLI 옵션** | PV prefix, 타임아웃, 로그 디렉토리 등을 명령행에서 설정 가능 |

---

## 2. 사전 요구사항

### 시스템 환경

- **EPICS Base**: R7.0 이상
- **EPICS IOC**: `KOHUZ_ALV1` IOC가 실행 중이어야 합니다.
- **Python 3**: 부동소수점 연산 및 시간 측정에 사용
- **bash**: 4.0 이상 (배열 및 `set -euo pipefail` 지원)

### EPICS 도구

아래 명령어가 `$PATH`에 포함되어 있어야 합니다:

| 명령어 | 용도 |
|--------|------|
| `caget` | PV 값 읽기 |
| `caput` | PV 값 쓰기 |

### PV 확인

스크립트 실행 전 아래 PV에 접근 가능한지 확인합니다:

```bash
# IOC 연결 확인
caget KOHZU:m1.VAL

# 연결 안 되면 IOC를 먼저 실행
cd /usr/local/epics/EPICS_R7.0/siteApp/KOHUZ_ALV1/iocBoot/iocKOHUZ_ALV1
../../bin/linux-x86_64/KOHUZ_ALV1 st.cmd
```

---

## 3. 설치 및 준비

### 스크립트 위치

```
/usr/local/epics/EPICS_R7.0/siteApp/KOHUZ_ALV1/
└── iocBoot/
    └── iocKOHUZ_ALV1/
        ├── st.cmd                        # IOC 시작 스크립트
        ├── motor.substitutions           # Motor Record 설정
        ├── verify_Scenario_V1.sh   # ← 이 검증 스크립트
        ├── verify_10mm_move.sh           # 단순 이동 검증
        └── verify_20mm_speed_ramp.sh     # 속도 증가 반복 검증
```

### 실행 권한 설정

```bash
chmod +x verify_Scenario_V1.sh
```

### CA 환경 설정 (필요시)

IOC가 로컬에서 실행 중이면 기본 설정으로 동작합니다. 원격 IOC에 연결하려면:

```bash
# 방법 1: 환경 변수 직접 설정
export EPICS_CA_ADDR_LIST="192.168.1.100"
export EPICS_CA_AUTO_ADDR_LIST=NO

# 방법 2: 스크립트 옵션 사용 시 자동으로 기본 로컬 설정 적용
```

---

## 4. 사용법

### 기본 실행

```bash
./verify_Scenario_V1.sh
```

### 명령행 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `-p PV_PREFIX` | 모터 PV prefix | `KOHZU:m1` |
| `-t TIMEOUT` | 이동 대기 타임아웃 (초) | `60` |
| `-l LOG_DIR` | 로그 파일 저장 디렉토리 | 스크립트 위치 |
| `-s` | 원점 복귀(Homing) 건너뛰기 | - |
| `-h` | 도움말 출력 | - |

### 사용 예시

```bash
# 기본 실행 (KOHZU:m1, 타임아웃 60초)
./verify_Scenario_V1.sh

# 다른 PV에 대해 실행
./verify_Scenario_V1.sh -p KOHZU:m2

# 원점 복귀 건너뛰기 (이미 원점에 있을 때)
./verify_Scenario_V1.sh -s

# 타임아웃 120초, 로그를 /tmp에 저장
./verify_Scenario_V1.sh -t 120 -l /tmp

# 원격 IOC에 대한 검증 (환경 변수 지정 후)
export EPICS_CA_ADDR_LIST="192.168.1.100"
./verify_Scenario_V1.sh -p REMOTE:m1
```

---

## 5. 검증 시나리오 상세

### Step 1: IOC 연결 및 파라미터 무결성 점검

| 항목 | 내용 |
|------|------|
| **검증 대상** | **`.VAL`**, **`.MRES`**, **`.EGU`**, **`.VELO`**, **`.ACCL`**, **`.HLM`**, **`.LLM`** |
| **판정 기준** | PV 연결 가능 + **MRES** 읽기 성공 |
| **기대값** | **MRES** = `0.0005` 또는 `0.001` |
| **에러 시** | IOC 미실행 → 즉시 종료 |

### Step 2: 하드웨어 원점 복귀 (.HOMF)

| 항목 | 내용 |
|------|------|
| **검증 대상** | **`.HOMF`**, **`.HVEL`**, **`.RBV`** |
| **동작** | **HVEL** = 2.0 mm/s 설정 → **HOMF** = 1로 원점 이동 |
| **판정 기준** | DMOV=1 + RBV ≈ 0 (0.1 이내) |
| **스킵** | `-s` 옵션으로 건너뛸 수 있음 |
| **타임아웃** | 90초 (원점복귀는 스트로크 전체 이동 가능성) |

### Step 3: 절대 이동 (.VAL)

| 항목 | 내용 |
|------|------|
| **검증 대상** | **`.VAL`**, **`.RBV`**, **`.RDBD`** |
| **동작** | **VAL** = 5.0mm로 절대 이동 |
| **판정 기준** | 위치 오차 < **RDBD** × 5 |
| **검증 의미** | APS 명령을 통한 절대 위치 지정 이동 확인 |

### Step 4: 상대 이동 (.RLV)

| 항목 | 내용 |
|------|------|
| **검증 대상** | **`.RLV`**, **`.RBV`** |
| **동작** | 현재 위치에서 +2.0mm 상대 이동 |
| **판정 기준** | 실제 이동 거리 오차 < 0.05mm |
| **검증 의미** | Motor Record의 상대 이동 연산 + APS 절대 변환 정확도 |

### Step 5: 속도 변경 후 이동 (.VELO)

| 항목 | 내용 |
|------|------|
| **검증 대상** | **`.VELO`**, **`.RBV`**, 실측 속도 |
| **동작** | VELO = 1.0mm/s로 변경 → +2.0mm 이동 → 속도 복원 |
| **판정 기준** | 이동 완료 + 실측 속도 출력 |
| **검증 의미** | WTB 속도 테이블 업데이트가 정상 반영되는지 확인 |

### Step 6: 조그(JOG) 및 정지(STOP)

| 항목 | 내용 |
|------|------|
| **검증 대상** | **`.JOGF`**, **`.STOP`**, **`.JVEL`** |
| **동작** | JVEL = 2.0mm/s 설정 → JOGF 시작 → 3초 후 STOP |
| **판정 기준** | 정지 성공 + JOG 이동 거리 > 0.001mm |
| **검증 의미** | FRP 연속 회전 + STP 감속 정지 동작 확인 |

### Step 7: 소프트 리미트 위반 (.LVIO)

| 항목 | 내용 |
|------|------|
| **검증 대상** | **`.HLM`**, **`.LVIO`**, **`.VAL`** |
| **동작** | HLM + 1.0 위치로 이동 시도 → LVIO 감지 → 원래 위치 복원 |
| **판정 기준** | **LVIO** = 1 |
| **검증 의미** | Motor Record의 소프트웨어 리미트 보호 기능 |

### Step 8: 하드웨어 리미트 상태 확인

| 항목 | 내용 |
|------|------|
| **검증 대상** | **`.HLS`**, **`.LLS`**, **`.MSTA`** |
| **동작** | HLS/LLS 현재 상태 읽기 + MSTA 비트 상세 출력 |
| **판정 기준** | PV 읽기 성공 |
| **검증 의미** | STR 응답의 리미트 비트마스크(e 필드)가 정상 파싱되는지 확인 |

### Step 9: 최종 원점 복귀

| 항목 | 내용 |
|------|------|
| **검증 대상** | **`.VAL`**, **`.RBV`**, **`.DMOV`** |
| **동작** | VAL = 0 으로 복귀 이동 |
| **판정 기준** | 이동 완료 (DMOV=1) |
| **의미** | 테스트 종료 후 장비를 안전한 위치로 복원 |

---

## 6. 출력 해석

### 콘솔 출력 예시

```
═══════════════════════════════════════════════════════════
 KOHZU XA07A-L202 EPICS IOC 기능 검증 스크립트 V3.0
 일시: 2026-02-13 15:30:00
 PV:   KOHZU:m1
 로그: /path/to/verify_KOHZU_20260213_153000.log
═══════════════════════════════════════════════════════════

━━━ [Step 1] IOC 연결 및 파라미터 무결성 점검 ━━━
  ✅ IOC 연결 확인 완료
  ...
  ✅ PASS: MRES=0.0005 정상 범위
  
  ...
  
═══════════════════════════════════════════════════════════
                   최종 검증 리포트
═══════════════════════════════════════════════════════════

  ┌─────┬──────────────────────┬────────┬─────────────────────────────┐
  │ No. │ Step                 │ 결과   │ 상세                        │
  ├─────┼──────────────────────┼────────┼─────────────────────────────┤
  │   1 │ Step1_Params         │ PASS   │ MRES=0.0005 정상 범위       │
  │   2 │ Step2_Homing         │ PASS   │ Home 위치=0.000             │
  │   3 │ Step3_AbsMove        │ PASS   │ 목표=5.0 실측=5.000 오차=0  │
  │ ... │ ...                  │ ...    │ ...                         │
  └─────┴──────────────────────┴────────┴─────────────────────────────┘

    총 검증 항목: 9
    ✅ PASS: 8
    ❌ FAIL: 0
    ⏭️  SKIP: 1
  
  🎉 전체 PASS — 검증 완료!
```

### 결과 상태 아이콘

| 아이콘 | 상태 | 의미 |
|--------|------|------|
| ✅ | PASS | 해당 검증 항목 통과 |
| ❌ | FAIL | 해당 검증 항목 실패 — 원인 확인 필요 |
| ⏭️ | SKIP | 옵션에 의해 건너뜀 (예: `-s` 사용) |
| 🚨 | ERROR/TIMEOUT | 심각한 오류 (통신 두절, 타임아웃 등) |
| ⏳ | 대기중 | 이동 완료를 기다리는 중 |

### 로그 파일

- 파일명 형식: `verify_KOHZU_YYYYMMDD_HHMMSS.log`
- 위치: 스크립트 실행 디렉토리 (또는 `-l` 옵션 지정 디렉토리)
- 콘솔 출력과 동일한 내용이 기록됩니다.

---

## 7. MSTA 비트 해석표

스크립트 내 `print_msta_detail()` 함수가 출력하는 **MSTA** (Motor Status) 비트 해석 기준입니다.

| 비트 | 16진 마스크 | 필드명 | 의미 |
|------|------------|--------|------|
| 0 | `0x0001` | RA_DIRECTION | 마지막 이동 방향 (1=양방향) |
| 1 | `0x0002` | RA_DONE | 이동 완료 |
| 2 | `0x0004` | RA_PLUS_LS | + 방향 리미트 스위치 활성 |
| 3 | `0x0008` | RA_HOME | Home 스위치 활성 |
| 5 | `0x0020` | EA_POSITION | 인코더 위치 사용 |
| 6 | `0x0040` | EA_SLIP_STALL | 슬립/스톨 감지 |
| 7 | `0x0080` | EA_HOME | Home 센서 활성 |
| 9 | `0x0200` | RA_PROBLEM | 하드웨어 에러 |
| 10 | `0x0400` | RA_MOVING | 이동 중 |
| 11 | `0x0800` | GAIN_SUPPORT | 게인(서보) 지원 |
| 12 | `0x1000` | CNTRL_COMM_ERR | 통신 에러 |
| 13 | `0x2000` | RA_MINUS_LS | - 방향 리미트 스위치 활성 |
| 14 | `0x4000` | RA_HOMED |원점복귀 완료 |

### MSTA와 드라이버의 관계

KOHZU ARIES 드라이버(`KohzuAriesDriver.cpp`)의 `poll()` 함수는 **STR** 명령으로 하드웨어 상태를 읽어서 MSTA에 반영합니다:

| STR 필드 | 드라이버 매핑 | MSTA 비트 |
|----------|-------------|-----------|
| b (구동상태) | `motorStatusDone_` | Bit 1 (RA_DONE) |
| b (구동상태) | `motorStatusMoving_` | Bit 10 (RA_MOVING) |
| c (EMG) | `motorStatusProblem_` | Bit 9 (RA_PROBLEM) |
| d (ORG센서) | `motorStatusAtHome_` / `motorStatusHomed_` | Bit 7 / Bit 14 |
| e (CW/CCW 리미트) | `motorStatusHighLimit_` / `motorStatusLowLimit_` | Bit 2 / Bit 13 |

> **참고 (v3.0 수정 사항)**: 이전 버전에서는 `motorStatusMoving_`이 설정되지 않아
> 이동 중 MSTA=0이 되는 문제가 있었습니다. 이로 인해 스크립트의 Zombie State 감지가
> false positive를 발생시켰습니다. 드라이버 수정 후 이동 중 MSTA에
> RA_MOVING(Bit 10, 0x0400) 비트가 정상적으로 설정됩니다.

---

## 8. 트러블슈팅

### 자주 발생하는 문제

| 증상 | 원인 | 해결 방법 |
|------|------|-----------|
| `PV 연결 불가` | IOC 미실행 또는 네트워크 문제 | IOC 실행 확인: `../../bin/linux-x86_64/KOHUZ_ALV1 st.cmd` |
| `Channel connect timed out` | CA 주소 설정 오류 | `EPICS_CA_ADDR_LIST` 확인, IOC과 같은 서브넷인지 체크 |
| `MSTA 통신 에러 (Bit 12)` | 컨트롤러 통신 두절 | 컨트롤러 전원/네트워크 확인, `st.cmd` IP 주소 확인 |
| `MSTA Problem (Bit 9)` | EMG 비상정지 또는 하드웨어 에러 | 컨트롤러 전면 패널 확인, EMG 해제 후 재시도 |
| `TIMEOUT` 반복 | 이동 거리 대비 속도가 너무 느림 | **VELO** 증가 또는 `-t` 옵션으로 타임아웃 연장 |
| `LVIO` 미검출 | **HLM**/**LLM** 미설정 | `motor.substitutions`에서 **HLM**, **LLM** 값 확인 |
| `JOG 이동 거리 0` | **JVEL** = 0 또는 FRP 명령 실패 | asyn 트레이스 활성화하여 FRP 응답 확인 |
| `Home 후 위치 ≠ 0` | **OFF** (Offset) 값이 설정됨 | `caget KOHZU:m1.OFF`로 확인, 필요시 0으로 리셋 |

### asyn 디버그 트레이스 활성화

IOC 실행 중인 상태에서 디버그 레벨을 높여 ARIES 통신 내용을 확인할 수 있습니다:

```bash
# IOC shell에서 실행
asynSetTraceMask("L0", 0, 0x9)    # Error + Flow
asynSetTraceIOMask("L0", 0, 0x2)  # Hex dump
```

### 컨트롤러 직접 통신 테스트

네트워크 연결 자체를 확인하려면:

```bash
# 직접 TCP 연결 (ARIES 기본 포트: 12321)
echo "STR1" | nc -w 2 192.168.1.120 12321
```

정상 응답 예시: `C STR1 0 0 0 0 00`

---

## 9. 커스터마이징

### PV prefix 변경

`motor.substitutions` 파일의 `P`(prefix)와 `M`(motor 번호)을 변경 시:

```bash
# 예: BEAMLINE:m2로 변경
./verify_Scenario_V1.sh -p BEAMLINE:m2
```

### 검증 Step 비활성화

특정 Step만 건너뛰고 싶다면 스크립트 내 해당 Step 블록을 주석 처리하면 됩니다:

```bash
# Step 5 (속도 변경)을 건너뛰려면:
# echo "━━━ [Step 5] ..."
# ... 해당 블록 전체를 주석 처리
record_result "Step5_SpeedChange" "SKIP" "수동 비활성화"
```

### 이동 목표값 변경

스크립트 상단부의 Step별 목표값을 프로젝트에 맞게 수정합니다:

| 변수 | 위치 | 기본값 | 설명 |
|------|------|--------|------|
| `ABS_TARGET` | Step 3 | `5.0` | 절대 이동 목표 위치 (mm) |
| `REL_DIST` | Step 4 | `2.0` | 상대 이동 거리 (mm) |
| `NEW_VELO` | Step 5 | `1.0` | 속도 변경 테스트 값 (mm/s) |

---

## 10. 관련 파일 목록

| 파일 | 경로 | 설명 |
|------|------|------|
| **검증 스크립트** | `iocBoot/iocKOHUZ_ALV1/verify_Scenario_V1.sh` | 본 가이드 대상 스크립트 |
| **10mm 이동 검증** | `iocBoot/iocKOHUZ_ALV1/verify_10mm_move.sh` | 단순 전/후진 이동 검증 |
| **속도 증가 검증** | `iocBoot/iocKOHUZ_ALV1/verify_20mm_speed_ramp.sh` | 속도 단계적 증가 반복 검증 |
| **IOC 시작** | `iocBoot/iocKOHUZ_ALV1/st.cmd` | IOC 시작 스크립트 |
| **Motor 설정** | `iocBoot/iocKOHUZ_ALV1/motor.substitutions` | Motor Record 파라미터 |
| **Motor DB** | `db/KOHZU_Motor.db` | Motor Record 템플릿 |
| **드라이버 소스** | `kohzuApp/src/KohzuAriesDriver.cpp` | ARIES 드라이버 구현체 |
| **드라이버 헤더** | `kohzuApp/src/KohzuAriesDriver.h` | 드라이버 헤더 파일 |
| **시스템 가이드** | `kohzuApp/doc/KOHZU_System_Verification_Guide.md` | 통합 기술 지침서 |
| **리팩토링 보고서** | `kohzuApp/doc/Kohzu_ARIES_Driver_Refactoring_Report.md` | 드라이버 리팩토링 이력 |

---

## 부록: motor.substitutions 현재 설정

참고로, 현재 `motor.substitutions`에 설정된 파라미터는 아래와 같습니다:

```
file "../../db/KOHZU_Motor.db"
{
pattern
{P,      M,   PORT, ADDR, DESC,           EGU, DIR,  VELO, VBAS, ACCL, MRES,   SREV, UREV, PREC, HLM,  LLM,   DHLM,  DLLM,  UEIP, RDBD, DLY}
{KOHZU:, m1,  PC0,  0,    "XA07A-L202",   mm,  Pos,  5.0,  0.1,  0.5,  0.0005, 2000, 1.0,  3,    34.0, -34.0, 35.0,  -35.0, No,   0.003, 0.1}
}
```

| 파라미터 | 값 | 의미 |
|----------|-----|------|
| **MRES** | 0.0005 mm/step | 모터 분해능 (0.5μm) |
| **SREV** | 2000 steps/rev | 1회전 당 스텝 수 |
| **UREV** | 1.0 mm/rev | 1회전 당 이동 거리 |
| **VELO** | 5.0 mm/s | 최대 주행 속도 |
| **VBAS** | 0.1 mm/s | 기동 속도 |
| **ACCL** | 0.5 s | 가속 시간 |
| **HLM** | 34.0 mm | 사용자 좌표 상한 |
| **LLM** | -34.0 mm | 사용자 좌표 하한 |
| **RDBD** | 0.003 mm | 이동 완료 판정 기준 (3μm) |
| **DLY** | 0.1 s | 이동 완료 후 지연 시간 |

---

*이 문서는 `verify_Scenario_V1.sh` v3.0 기준으로 작성되었습니다.*
