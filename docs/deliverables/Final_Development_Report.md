# 📋 kohzuApp 최종 개발 보고서

> **프로젝트명:** kohzuApp — Kohzu ARIES 6-Axis Motor Control System  
> **작성일:** 2026.03.04  
> **개발 기간:** 2026.02.05 ~ 2026.03.04 (약 4주)  
> **작성자:** 4GSR/빔라인장치공학팀/제어그룹/서민호  
> **문서 버전:** v1.0

---

## 목차

1. [프로젝트 개요 및 목적](#1-프로젝트-개요-및-목적)
2. [시스템 아키텍처](#2-시스템-아키텍처)
3. [하드웨어 드라이버 개발 (C++ / EPICS IOC)](#3-하드웨어-드라이버-개발)
4. [Web Gateway 개발 (Python / Tornado)](#4-web-gateway-개발)
5. [Web GUI 개발 (HTML / JavaScript)](#5-web-gui-개발)
6. [스테이지 설정 체계 (JSON / Control Guide)](#6-스테이지-설정-체계)
7. [GUI 설계 표준 (Design Guide)](#7-gui-설계-표준)
8. [개발 과정에서의 주요 기술 결정](#8-개발-과정에서의-주요-기술-결정)
9. [주요 버그 및 해결 이력](#9-주요-버그-및-해결-이력)
10. [검증 결과](#10-검증-결과)
11. [산출물 목록](#11-산출물-목록)
12. [향후 개선 과제](#12-향후-개선-과제)
13. [부록: 개발 타임라인](#부록-개발-타임라인)

---

## 1. 프로젝트 개요 및 목적

### 1.1 배경

본 프로젝트는 방사광 빔라인(Beamline) 환경에서 **Kohzu ARIES 모터 컨트롤러**와 **TITAN-A II 드라이버**를 이용하여 
최대 6축의 정밀 스테이지를 제어하기 위한 통합 시스템을 구축하는 것을 목표로 한다.

기존에는 EPICS 표준 GUI 도구인 **Phoebus OPI (XML 기반)**를 사용하여 개별 모터를 제어했으나, 다음과 같은 한계가 존재했다:

- **접근성 제약**: Phoebus 클라이언트가 설치된 PC에서만 제어 가능
- **다축 통합 뷰 부재**: 6축을 동시에 모니터링하고 제어할 수 있는 통합 화면 미비
- **모바일 지원 불가**: 현장에서 태블릿/스마트폰으로의 접속 불가능
- **드라이버 미완성**: 속도 제어(WTB), JOG(FRP), 에러 핸들링 등 핵심 기능 미구현

### 1.2 프로젝트 목표

| 목표 | 설명 |
|------|------|
| **전용 하드웨어 드라이버** | ARIES 명령어 사양 기반 `asynMotor` C++ 드라이버 완성 |
| **Web 기반 통합 대시보드** | 6축 동시 모니터링/제어, 어디서든 Chrome 접속 |
| **실시간 양방향 통신** | WebSocket 기반 PV 구독/제어 게이트웨이 |
| **모바일 대응** | 반응형 레이아웃으로 태블릿/스마트폰 지원 |
| **JSON 기반 스테이지 관리** | 스테이지별 파라미터를 JSON으로 관리, 즉시 적용 |
| **일관된 UI 표준** | GUI Design Guide 기반 디자인 규격 통일 |

### 1.3 적용 대상 하드웨어

| 장비 | 모델 | 사양 |
|------|------|------|
| **컨트롤러** | Kohzu ARIES | TCP/IP 통신 (192.168.1.120:12321), ASCII 프로토콜 |
| **드라이버** | TITAN-A II | 5상 스테핑 모터용, 마이크로스텝 1/2~1/250 |
| **스테이지** | XA, ZA, RA, SA 시리즈 | Linear/Vertical/Rotation/Goniometer |

---

## 2. 시스템 아키텍처

### 2.1 전체 구성도

```
┌─────────────────────────────────────────────────────────────────────┐
│                        사용자 (User)                                  │
│    Chrome / Safari / Mobile Browser                                 │
│    http://192.168.x.x:8888/dashboard.html                           │
└────────────────────────────┬────────────────────────────────────────┘
                             │ HTTP + WebSocket (ws://)
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│              Web Gateway (web_gateway.py)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐     │
│  │ Tornado HTTP │  │ WebSocket    │  │ REST API               │     │
│  │ Static Files │  │ PV Subscribe │  │ /api/stages            │     │
│  │ (dashboard,  │  │ PV Write     │  │ /api/sessions          │     │
│  │  popup, CSS) │  │ Broadcast    │  │ /sessions/<file>       │     │
│  └──────────────┘  └──────┬───────┘  └────────────────────────┘     │
│                           │ Channel Access (CA)                     │
│                    pyepics.PV()                                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │ EPICS CA Protocol (TCP/UDP)
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    EPICS IOC (iocKOHUZ_ALV1)                        │
│  ┌──────────────┐  ┌──────────────────────┐  ┌───────────────────┐  │
│  │ Motor Record │  │ KohzuAriesDriver.cpp │  │ motor.substitutions│ │
│  │ KOHZU:m1~m6  │  │ (asynMotorController │  │ (6축 레코드 정의) │  │
│  │ 60+ PV/축    │  │  + asynMotorAxis)    │  │                   │  │
│  └──────────────┘  └──────────┬───────────┘  └───────────────────┘  │
│                               │ asynOctet (TCP/IP)                   │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ TCP "192.168.1.120:12321"
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│              Kohzu ARIES Controller + TITAN-A II Driver               │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ ASCII Protocol (CRLF terminated)                               │  │
│  │ Commands: APS, RPS, FRP, STP, ORG, WTB, STR, RDP ...         │  │
│  │ 6-Channel × 5-Phase Stepping Motor                            │  │
│  └────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 3계층 통신 구조

| 계층 | 프로토콜 | 구현 |
|------|----------|------|
| **Browser ↔ Gateway** | HTTP (정적 파일) + WebSocket (실시간 PV) | Tornado + JavaScript |
| **Gateway ↔ IOC** | EPICS Channel Access (CA) | pyepics `PV()` |
| **IOC ↔ Controller** | TCP/IP ASCII (`\r\n` terminated) | asynOctet Driver |

### 2.3 데이터 흐름

**읽기 (모니터링):**
```
ARIES → STR/RDP → KohzuAriesDriver.poll() → Motor Record PV 갱신
→ pyepics callback → WebSocket broadcast → JavaScript DOM 갱신
```

**쓰기 (제어):**
```
Browser input → WebSocket "write" → pyepics.caput() → Motor Record
→ KohzuAriesDriver.move() → WTB + APS 명령 → ARIES 컨트롤러
```

---

## 3. 하드웨어 드라이버 개발

### 3.1 개발 범위

| 항목 | 값 |
|------|-----|
| **소스 파일** | `kohzuApp/src/KohzuAriesDriver.cpp` (740행) |
| **헤더 파일** | `kohzuApp/src/KohzuAriesDriver.h` (79행) |
| **총 코드량** | **819행** (C++) |
| **프레임워크** | EPICS `asynMotor` (asynMotorController + asynMotorAxis 상속) |
| **통신 방식** | `asynOctetSyncIO` (TCP/IP 동기 I/O, CRLF 종단) |

### 3.2 클래스 구조

```
asynMotorController (EPICS 기본 클래스)
  └── KohzuAriesController
        ├── sendCommand()      — 응답 있는 명령 (writeRead)
        ├── sendOnly()         — 응답 없는 명령 (write only)
        ├── report()           — 드라이버 상태 리포트
        └── homingMethod_      — 커스텀 파라미터 (원점 복귀 방법 4/7/8)

asynMotorAxis (EPICS 기본 클래스)
  └── KohzuAriesAxis
        ├── move()             — 절대 위치 이동 (APS)
        ├── moveVelocity()     — JOG 연속 이동 (FRP)
        ├── home()             — 원점 복귀 (ORG, Method 4/7/8)
        ├── stop()             — 감속 정지 (STP)
        ├── poll()             — 상태+위치 폴링 (STR+RDP)
        ├── setSpeedTable()    — 속도 테이블 설정 (WTB)
        ├── setSystemParam()   — 시스템 파라미터 설정 (WSY)
        ├── report()           — 축별 상태 리포트
        ├── homed_             — 원점 복귀 완료 래치 (전원 OFF까지 유지)
        └── homingActive_      — 원점 복귀 진행 중 플래그
```

### 3.3 구현 기능 상세

#### 3.3.1 `move()` — 절대 위치 이동 (281~317행)

```
실행 순서:
  1. setSpeedTable(min, max, accel)  →  WTB 명령 전송
  2. APS<축>/0/<pulse>/1             →  즉시 응답 모드로 이동 시작
  3. poll()에서 STR 구동상태로 완료 감지
```

| 항목 | 사양 |
|------|------|
| ARIES 명령 | `APS <축>/<속도테이블>/<위치(pulse)>/<응답방식>` |
| 응답방식 | `1` = 즉시응답(Quick), `0` = 완료후응답 |
| 에러 처리 | 응답 `response[0] == 'E'` 시 `asynError` 반환 |

#### 3.3.2 `moveVelocity()` — JOG 연속 이동 (343~381행)

| 항목 | 사양 |
|------|------|
| ARIES 명령 | `FRP <축>/<속도테이블>/<방향>` |
| 방향 판별 | `maxVelocity >= 0` → CW(0), `< 0` → CCW(1) |
| 속도 절대값 | `fabs(maxVelocity)` 로 변환 후 WTB 설정 |
| 정지 방법 | STP 명령으로만 정지 가능 |

#### 3.3.3 `home()` — 원점 복귀 (383~479행)

**Method 4/7/8 선택형 원점 복귀**를 지원한다. 사용자는 EPICS PV `$(P)$(M):HomingMethod`로 방법을 런타임에 선택할 수 있다.

```
실행 순서:
  1. EPICS PV에서 Method 읽기 (getIntegerParam)
  2. 유효성 검증 (4/7/8 외 → 기본값 4로 폴백)
  3. WSY<축>/2/<method>  →  컨트롤러 ORG TYPE 변경
  4. setSpeedTable()     →  접근 속도 설정
  5. ORG<축>/0/1         →  즉시 응답으로 원점 복귀 시작
  6. homingActive_ = true  →  poll()에서 완료 감지 대기
```

| Method | 동작 | 센서 |
|--------|------|------|
| **4** (기본) | CCW→NORG감지→반전→NORG에지정지→좌표0 | NORG 센서 |
| **7** | CW방향이동→CW Limit에지정지→좌표0 | CW Limit (L+) |
| **8** | CCW방향이동→CCW Limit에지정지→좌표0 | CCW Limit (L-) |

`forwards` 파라미터는 미사용: ARIES가 Method에 따라 복귀 방향을 자동 판단함 (HOMF/HOMR 모두 동일 동작).

#### 3.3.4 `stop()` — 정지 (319~341행)

| 항목 | 사양 |
|------|------|
| ARIES 명령 | `STP <축>/<정지모드>` |
| 정지모드 | `0` = 감속정지 (기본), `1` = 비상정지(즉시) |
| 현재 구현 | 감속정지(모드 0) 고정 |

#### 3.3.5 `poll()` — 상태+위치 폴링 (481~681행, **200행**, 최대 함수)

`poll()`은 드라이버에서 가장 복잡한 함수이며, **STR(상태) + RDP(위치)** 두 명령을 매 폴링 주기마다 실행한다.

**STR 응답 파싱:**

```
응답 포맷: "C STR<축> <b> <c> <d> <e> <f> <g>"
실제 예시: "C STR1 0 0 0 0 00"
┌────────┬──────────────────────────┬────────────────────────────────┐
│ 필드   │ 의미                     │ EPICS 매핑                      │
├────────┼──────────────────────────┼────────────────────────────────┤
│ b(fields[0]) │ 구동상태 (0=정지,1=동작,2=피드백) │ motorStatusDone_, Moving_  │
│ c(fields[1]) │ EMG 비상정지 (0=OFF, 1=ON) │ motorStatusProblem_          │
│ d(fields[2]) │ ORG/NORG 센서 (비트마스크) │ motorStatusAtHome_           │
│ e(fields[3]) │ CW/CCW 리미트 (비트마스크) │ motorStatusHighLimit_, Low_  │
│ f(fields[4]) │ 소프트 리미트              │ (향후 구현 예정)               │
│ g(fields[5]) │ 보정 허용 범위             │ (미사용)                       │
└────────┴──────────────────────────┴────────────────────────────────┘
```

**핵심 파싱 로직 — 고정 폭 포맷 처리:**

ARIES 응답은 공백 구분이 아닌 **고정 폭 포맷**으로 인접 필드가 연결될 수 있다 (예: `"00"` → 필드 2개). 이를 해결하기 위해 개별 숫자 분리 로직을 구현했다:

```c++
// 고정 폭 포맷: "00" → 개별 숫자 분리 (각 필드는 0~3 범위)
if (len > 1) {
    for (int i = 0; i < len && nFields < 10; i++) {
        if (tok[i] >= '0' && tok[i] <= '9') {
            fields[nFields++] = tok[i] - '0';
        }
    }
}
```

**리미트 비트마스크 디코딩:**

```c++
// e=0: 양쪽OFF, e=1: CCW만ON, e=2: CW만ON, e=3: 양쪽ON
int cwLimit  = (r_limits & 0x02) ? 1 : 0;  // bit 1 = CW (High Limit)
int ccwLimit = (r_limits & 0x01) ? 1 : 0;  // bit 0 = CCW (Low Limit)
```

**원점 복귀 완료 감지:**

```c++
// homingActive_ 중 구동 정지(r_drive==0) → homed_ = true (래치)
if (homingActive_ && r_drive == 0) {
    homed_ = true;         // 전원 OFF까지 유지
    homingActive_ = false;
}
```

**에러 발생 시 안전 폴백:**

```
통신 에러 → moving=false, Done=1, Problem=1, CommsError=1
STR 파싱 실패 → moving=false, Done=1, Problem=1
에러 응답("E STR ...") → moving=false, Done=1, Problem=1
```

#### 3.3.6 `setSpeedTable()` — 속도 테이블 설정 (196~279행)

이동 명령(APS, FRP, ORG) 실행 전 반드시 호출되는 내부 함수이다.

```
[EPICS Motor Record]              [드라이버 변환]              [ARIES 전송]
VELO = 2.0 mm/s     →    topSpeed = 4000 pps     →    WTB1/0/200/4000/50/50/2
VBAS = 0.1 mm/s     →    startSpeed = 200 pps
ACCL = 0.5 sec      →    accelTime = 50 (×10ms)
MRES = 0.0005 mm    →    (변환 계수)
```

**가속 시간 변환 핵심 로직:**
```
acceleration 파라미터 = steps/s² (가속도, EPICS가 전달)
  → ACCL(초) = (topSpeed - startSpeed) / acceleration
  → ARIES 단위 = ACCL(초) × 100 (설정값 × 10ms)
```

**안전 클램프 (ARIES 사양 준수):**

| 파라미터 | 최소 | 최대 | 비고 |
|---------|------|------|------|
| Start Speed | 1 pps | 2,500,000 pps | `ARIES_MIN/MAX_START_SPEED` |
| Top Speed | 2 pps | 5,000,000 pps | `ARIES_MIN/MAX_TOP_SPEED` |
| Start/Top 비율 | — | Top의 50% 이하 | ARIES 에러 605 방지 |
| 가속 시간 (1~20 pps) | 1 | 10 | ×10ms (10~100ms) |
| 가속 시간 (21~1000 pps) | 1 | 100 | ×10ms (10~1000ms) |
| 가속 시간 (1001+ pps) | 1 | 1000 | ×10ms (10~10,000ms) |

#### 3.3.7 `setSystemParam()` — 시스템 파라미터 설정 (157~194행)

| 항목 | 사양 |
|------|------|
| ARIES 명령 | `WSY <축>/<시스템번호>/<설정값>` |
| 주요 용도 | System No.2 (ORG TYPE) 변경 — `home()` 에서 호출 |
| 지원 System No. | No.1: ORG OFFSET, No.2: ORG TYPE, No.3: ORG SCAN SPEED |

### 3.4 통신 프로토콜 상수

```c++
#define MAX_RESPONSE_LEN  256      // 응답 버퍼 크기
#define CMD_TIMEOUT       5.0      // 일반 명령 타임아웃 (초)
#define MOVE_TIMEOUT      2.0      // 이동 명령 타임아웃
#define TERMINATOR        "\r\n"   // CRLF 종단자
```

### 3.5 커스텀 파라미터

```c++
// KohzuAriesDriver.h
#define KohzuHomingMethodString "KOHZU_HOMING_METHOD"  // EPICS DB 연동 키
#define NUM_KOHZU_PARAMS 1                              // 커스텀 파라미터 수

// Controller 생성자에서 등록:
createParam(KohzuHomingMethodString, asynParamInt32, &homingMethod_);
setIntegerParam(i, homingMethod_, 4);  // 각 축 기본값: Method 4
```

EPICS DB에서 `$(P)$(M):HomingMethod` PV로 노출되며, 사용자가 4/7/8 중 런타임 선택 가능.

### 3.6 iocsh 등록 (708~739행)

```c++
// st.cmd에서 호출 가능한 명령 등록
KohzuAriesCreateController("PC0", "L0", 6, 0.2, 1.0)
// 인자: portName, serialPort, numAxes, movingPoll(s), idlePoll(s)
```

### 3.7 구현 상태 요약

| 기능 | ARIES 명령 | 드라이버 함수 | 행 범위 | 상태 |
|------|-----------|-------------|--------|------|
| 절대 위치 이동 | `APS a/b/c/d` | `move()` | 281~317 | ✅ |
| JOG (연속 이동) | `FRP a/b/c` | `moveVelocity()` | 343~381 | ✅ |
| 원점 복귀 (3종) | `ORG a/b/c` + `WSY` | `home()` | 383~479 | ✅ |
| 정지 (감속) | `STP a/b` | `stop()` | 319~341 | ✅ |
| 상태+위치 폴링 | `STR a` + `RDP a` | `poll()` | 481~681 | ✅ |
| 속도 테이블 설정 | `WTB a/b/c/d/e/f/g` | `setSpeedTable()` | 196~279 | ✅ |
| 시스템 파라미터 | `WSY a/b/c` | `setSystemParam()` | 157~194 | ✅ |
| 상대 이동 | `RPS a/b/c/d` | — | — | ⏸ 미구현 |
| 엔코더 읽기 | `RDE a` | — | — | ⏸ 미구현 |

### 3.8 리팩토링 성과

초기 v0.1 대비 v1.1에서 **16건의 이슈**를 해결:
- **Critical 8건**: 속도 미적용, APS 응답 미처리, ORG 파라미터 오류, JOG 미구현 등
- **Important 6건**: STP 정지모드, 비상정지 감지, 통신 에러 플래그 등
- **Minor 2건**: 헤더 중복 선언, 타임아웃 상수화

> 상세 내용: `docs/reports/Kohzu_ARIES_Driver_Refactoring_Report.md` 참조

### 3.9 IOC 설정

**st.cmd (시작 스크립트):**
```bash
# TCP/IP 포트 설정 (ARIES 컨트롤러)
drvAsynIPPortConfigure("L0", "192.168.1.120:12321", 0, 0, 0)
asynOctetSetInputEos("L0", 0, "\r\n")
asynOctetSetOutputEos("L0", 0, "\r\n")

# 6축 컨트롤러 생성 (폴링: 이동중 0.2초, 대기시 1.0초)
KohzuAriesCreateController("PC0", "L0", 6, 0.2, 1.0)
```

**motor.substitutions (6축 레코드 템플릿):**
```
pattern
{P,      M,   PORT, ADDR, DESC,      EGU, MRES,   SREV, UREV, VELO, ACCL, ...}
{KOHZU:, m1,  PC0,  0,    "Axis 1",  mm,  0.0005, 2000, 1.0,  5.0,  0.5,  ...}
{KOHZU:, m2,  PC0,  1,    "Axis 2",  mm,  0.0005, 2000, 1.0,  5.0,  0.5,  ...}
...
{KOHZU:, m6,  PC0,  5,    "Axis 6",  mm,  0.0005, 2000, 1.0,  5.0,  0.5,  ...}
```

---

## 4. Web Gateway 개발

### 4.1 개요

`kohzuApp/opi/web_gateway.py` (199행)

EPICS IOC와 웹 브라우저 사이의 중계 역할을 하는 Python 기반 WebSocket 서버이다.

### 4.2 기술 스택

| 컴포넌트 | 라이브러리 | 역할 |
|----------|-----------|------|
| HTTP 서버 | `tornado.web` | 정적 파일 서빙 (HTML, JS, CSS) |
| WebSocket | `tornado.websocket` | 실시간 양방향 PV 통신 |
| EPICS 연결 | `pyepics` | Channel Access PV 구독/쓰기 |

### 4.3 주요 구현 사항

#### WebSocket 메시지 프로토콜

```json
// 1. PV 구독 요청 (Browser → Gateway)
{"type": "subscribe", "pvs": ["KOHZU:m1.RBV", "KOHZU:m1.DMOV"]}

// 2. PV 값 갱신 (Gateway → Browser)
{"type": "update", "pv": "KOHZU:m1.RBV", "value": 12.345}

// 3. 연결 상태 변경 (Gateway → Browser)
{"type": "connection", "pv": "KOHZU:m1.RBV", "connected": true}

// 4. PV 쓰기 요청 (Browser → Gateway)
{"type": "write", "pv": "KOHZU:m1.VAL", "value": 10.0}
```

#### REST API 엔드포인트

| 경로 | 메서드 | 기능 |
|------|--------|------|
| `/ws` | WebSocket | 실시간 PV 통신 |
| `/api/stages` | GET | Stage JSON 파일 목록 반환 |
| `/api/sessions` | GET | 저장된 세션 목록 반환 |
| `/api/sessions` | POST | 세션 데이터 서버 저장 |
| `/(*)` | GET | 정적 파일 서빙 (캐시 무효화) |

#### 안정성 설계

- **스레드 안전**: PyEPICS 콜백(별도 스레드) → `IOLoop.add_callback()` → Tornado 메인 스레드
- **NonBlocking 연결**: `connection_timeout=0.01`로 미연결 PV의 IOLoop 블로킹 방지
- **포트 폴백**: 8888 포트 사용 불가 시 9999로 자동 전환
- **전역 바인딩**: `0.0.0.0` 바인딩으로 외부/모바일 접속 허용

---

## 5. Web GUI 개발

### 5.1 파일 구조

| 파일 | 역할 | 크기 |
|------|------|------|
| `dashboard.html` | **메인 6축 통합 대시보드** — 모든 기능의 집합체 | ~2,300행 |
| `motor_popup.html` | **모터 상세 제어 모달** — fetch()로 동적 로드되는 템플릿 | ~800행 |
| `motorx_all.html` | 단일축 제어 페이지 (초기 버전, 현재 대시보드로 대체) | ~1,500행 |

### 5.2 대시보드 주요 기능

#### 5.2.1 6축 모터 카드 그리드

각 축이 독립적인 카드로 표시되며, 다음 정보를 실시간으로 갱신한다:

- **상한/하한 리밋** (HLM/LLM, DHLM/DLLM) + 리밋 스위치 LED (HLS/LLS)
- **현재 위치** (RBV/DRBV) + 단위 (EGU)
- **목표 위치** (VAL/DVAL) + 이동 상태 LED (DMOV)
- **미세 이동** (Tweak: TWV, Go±, 1스텝 ±) + 개별 STOP 버튼
- **연결 상태** (Connected/Disconnected LED)
- **하드웨어 상태** (MSTA Bit Status: Done, Problem, Moving, HiLimit, LoLimit, Homing)

#### 5.2.2 모터 상세 모달 (motor_popup.html)

카드의 팝업 아이콘 클릭 시 모달이 열리며, OPI 수준의 상세 파라미터를 제어할 수 있다:

| 패널 | 포함 PV |
|------|---------|
| **Drive** | VAL, HLM, RBV, LLM, RLV, TWV, SPMG (4버튼) |
| **Calibration** | SET, OFF, FOFF, DIR, SYNC |
| **Dynamics** | VMAX, VELO, VBAS, ACCL |
| **Backlash** | BDST, BVEL, BACC, FRAC |
| **Jog Control** | JVEL, JAR, JOGR, JOGF |
| **Homing** | HVEL, HACC, HDCC, HomR, HomF |
| **Servo (PID)** | PCOF, ICOF, DCOF |
| **Resolution & Setup** | MRES, ERES, RRES, RDBD, RTRY, UEIP, DLY, PREC |
| **Status** | STAT, MOVN, ATHM, MIP, DTYP, CARD, CNEN, MSTA bits |
| **Stage Information** | Stage Select 드롭다운, 기계적 사양, 드라이버 설정 |

#### 5.2.3 실시간 차트 (Chart.js)

3개의 차트가 축 타입(axisType)별로 분리되어 위치 변화를 실시간 추적한다:

- **Linear Axes** (X축 스테이지)
- **Vertical Axes** (Z축 스테이지)
- **Rotation Axes** (R/S축 스테이지)

X축에 시간(`HH:MM:SS`), Y축에 위치 값을 표시한다.

#### 5.2.4 2D Area Scan

Raster Scan 또는 Fermat Spiral 패턴으로 2축 동시 스캔을 설정할 수 있으며, XY Scatter Plot으로 스캔 경로를 시각화한다.

#### 5.2.5 Sequence Mode

복수의 좌표 스텝을 정의하여 순차 실행하는 기능이다. 각 스텝 간 좌표 변화량이 파란색(변경)/회색(유지)으로 시각화된다.

#### 5.2.6 상태 영속화 (State Persistence)

| 계층 | 저장 대상 | 도구 |
|------|----------|------|
| **localStorage** | axesConfig, sequenceSteps, notepad | `saveAppState()` / `loadAppState()` |
| **서버 파일** | 전체 세션 (PV 값 스냅샷) | `/api/sessions` POST/GET |

### 5.3 아키텍처 변천

프로젝트 초기부터 최종 형태까지 GUI 아키텍처가 4단계로 진화했다:

| 단계 | 시기 | 구조 | 이유 |
|------|------|------|------|
| 1단계 | 02.19 | Phoebus OPI (XML) | 기존 EPICS 표준 |
| 2단계 | 02.19 | 단일 HTML `motorx_all.html` | Chrome 접근성 확보 |
| 3단계 | 02.26 | 6축 대시보드 + 하드코딩 모달 | 다축 통합 뷰 |
| **4단계** | **03.02** | **dashboard.html + fetch(motor_popup.html)** | **유지보수 분리** |

최종 4단계 아키텍처에서는 모달 템플릿(`motor_popup.html`)을 `fetch()`로 동적 로드하고, PV 접두사를 런타임에 치환(`replaceAll`)하여 6축 모두 동일 템플릿을 재사용한다.

---

## 6. 스테이지 설정 체계

### 6.1 JSON 스키마

각 스테이지의 파라미터를 JSON 파일로 관리하며, 대시보드의 Stage Select 드롭다운 또는 파일 업로드를 통해 즉시 적용할 수 있다.

```json
{
  "stageModel": "XA07A-L202",
  "axisType": "Linear",
  "parameters": {
    "EGU": "mm",
    "MRES": 0.0005,
    "SREV": 2000,
    "UREV": 1.0,
    "VELO": 5.0,
    "VBAS": 0.1,
    "ACCL": 0.5,
    "HLM": 34.0,
    "LLM": -34.0,
    "DHLM": 35.0,
    "DLLM": -35.0,
    "PREC": 3,
    "RDBD": 0.003,
    "DLY": 0.1,
    "UEIP": 0,
    "DIR": 0
  },
  "specifications": {
    "Travel Range": "±35 mm",
    "Lead Screw Pitch": "1.0 mm/rev",
    "Gear Ratio": "1:1 (Direct)"
  },
  "driverSettings": {
    "Motor Type": "5-Phase Stepping",
    "Microstep": "Half Step (1/2)",
    "Steps/Rev": "2000 (Full: 1000)"
  }
}
```

### 6.2 지원 스테이지 목록 (8종)

| JSON 파일명 | 축 타입 | EGU | MRES | 구동범위 |
|------------|---------|-----|------|---------|
| `XA07A-L202.json` | Linear | mm | 0.0005 | ±35 mm |
| `XA05A-L202.json` | Linear | mm | 0.0005 | ±25 mm |
| `XA05A-R102.json` | Linear | mm | 0.00025 | ±7.5 mm |
| `RA04A-W01.json` | Rotation | deg | 0.002 | -84°~+174° |
| `RA07A-W02.json` | Rotation | deg | 0.002 | -84°~+174° |
| `SA05A-R2B01.json` | Goniometer | deg | 0.0000637 | ±3.5° |
| `ZA05A-W101.json` | Vertical | mm | 0.00025 | ±4 mm |
| `ZA07A-V1F01.json` | Vertical | mm | 0.001 | ±10 mm |

### 6.3 파라미터 적용 프로세스

```
JSON 파일 선택/업로드
  → FileReader / fetch 파싱
  → axesConfig[i] 메모리 저장
  → 카드 UI 갱신 (모델명 뱃지, 축 타입)
  → WebSocket write → pyepics.caput() (각 PV에 값 전송)
  → 모달 열기 시 specifications/driverSettings 실시간 렌더링
  → localStorage 자동 저장 (saveAppState)
```

---

## 7. GUI 설계 표준

### 7.1 핵심 규격 요약

`docs/guides/GUI_Design_Guide.md`에 정의된 표준 규격이다.

| 요소 | 규격 |
|------|------|
| **글꼴** | `Inter`, sans-serif |
| **테마** | Slate 계열 다크 모드 |
| **패널 헤더** | `bg-slate-700/50 px-2 py-1 border-b border-slate-700` |
| **헤더 텍스트** | `text-sm font-black text-slate-300 uppercase tracking-widest` |
| **입력 필드 크기** | `w-[80px]` × `h-[22px]` 고정 |
| **입력 필드 배경** | `bg-slate-900` (`#0f172a`) |
| **Data Display 색상** | `text-green-400` (읽기 전용) |
| **Input Field 색상** | `text-white` (수정 가능) |
| **그리드 라벨** | `80px` 고정 + `1fr` 반복 |
| **STOP 버튼** | `bg-yellow-600` (머스타드/노란색) |
| **LED On** | Green (정상), Blue/Yellow (이동/경고), Red (에러) |

### 7.2 스타일링 이중 구조 (Hybrid Styling Architecture)

본 프로젝트는 **커스텀 CSS(`<style>` 태그)**와 **TailwindCSS CDN 유틸리티(인라인 `class`)**를 **의도적으로 혼합**하여 사용한다. Tailwind 단독으로 통합하지 않는 이유는 다음과 같다:

| 영역 | 담당 | 이유 |
|------|------|------|
| 구조적 뼈대 (`.card`, `.modal-overlay`) | **커스텀 CSS** | 반복 사용 클래스, 일관성 보장 |
| 상태 토글 (`.led.on/warn/error`) | **커스텀 CSS** | JS에서 `classList.add('on')` 단일 클래스 토글 |
| 애니메이션 (`@keyframes`, `box-shadow` glow) | **커스텀 CSS** | Tailwind CDN 미지원 |
| 가상 요소 (`.disconnected-card::after`) | **커스텀 CSS** | 복합 `transform` + `content` |
| 세부 레이아웃·간격·색상 | **TailwindCSS** | `grid-cols-[...]`, `gap-2` 등 미세 조정 |
| 반응형 전환 | **TailwindCSS** | `lg:flex-row`, `lg:hidden` 브레이크포인트 |

### 7.3 버튼 분류 체계

| 분류 | 대표 예시 | 스타일 방식 | 배경색 |
|------|----------|------------|--------|
| **Standard** (제어) | Go-, <, >, Go+ | Tailwind 유틸리티 | `bg-slate-700` |
| **Primary** (강조 액션) | + STEP | `.btn-primary` 커스텀 CSS | `#2563eb` (blue-600) |
| **Active** (상태 피드백) | USE, SET | JS 동적 주입 `!bg-green-700` | `bg-green-700` |
| **Emergency** (비상) | STOP, ABORT ALL | Tailwind 유틸리티 | `bg-yellow-600` |

### 7.4 UI 명칭 표준 (Nomenclature)

개발자 간 소통을 위한 표준 명칭을 정의했다:

- **Header**: 최상단 헤더 (타이틀, ABORT ALL, 연결 상태)
- **Axis Card**: 모터 개별 제어 카드
  - Card Header / Column Headers / Hi limit / Readback / Drive / Lo limit / Tweak / Bottom Status
- **Motor Detail Modal**: 상세 제어 모달
  - Left Card (Control & Setup) / Right Card (Status & Parameters)

> 상세 내용: `docs/guides/GUI_Design_Guide.md` 부록 A절 참조

---

## 8. 개발 과정에서의 주요 기술 결정

### 8.1 OPI → Web 전환 결정 (02.19)

**문제**: Phoebus OPI는 Java 기반 클라이언트에서만 실행 가능하여, 접근성이 제한됨.

**결정**: HTML + WebSocket으로 전환하여 Chrome 기반 어디서든 접속 가능하도록 변경.

**근거**:
- 추가 소프트웨어 설치 불필요
- 모바일(태블릿/스마트폰) 접속 가능
- CSS 기반 반응형 디자인 적용 용이
- 기존 OPI PV 바인딩 로직을 `data-pv` 속성으로 유사하게 구현 가능

### 8.2 모달 템플릿 분리 결정 (03.02)

**문제**: `dashboard.html` 내에 모달 HTML이 하드코딩되어, 6축분의 코드가 중복됨.

**결정**: `motor_popup.html`을 독립 파일로 분리하고, `fetch()`로 동적 로드.

**효과**:
- 모달 UI 수정 시 1개 파일만 변경하면 6축 전체에 반영
- 코드량 대폭 감소 (약 500행 → 1개 템플릿 공유)
- PV 접두사 치환(`replaceAll`)으로 축별 바인딩 자동화

### 8.3 3계층 상태 관리 결정

**문제**: 다양한 시점에서 상태를 유지해야 함 (실시간 / 세션 / 새로고침).

**결정**: 3계층 상태 관리 체계 도입.

| 계층 | 도구 | 범위 | 용도 |
|------|------|------|------|
| **EPICS PV** | IOC Motor Record | 항시 | 하드웨어 실시간 상태 |
| **localStorage** | Browser | 새로고침 간 | UI 상태 (axesConfig, 메모장) |
| **서버 파일** | `sessions/*.json` | 세션 간 | 전체 구성 백업/복원 |

### 8.4 미연결 모터의 Non-Blocking 처리 (02.26)

**문제**: 6축 중 1축만 연결된 경우, 나머지 5축의 PV 조회 타임아웃(기본 2초)으로 Tornado IOLoop이 약 10초간 블로킹됨.

**결정**: `connection_timeout=0.01`로 설정하여 미연결 PV의 타임아웃을 최소화.

**보조 대책**:
- 미연결 축의 카드를 Grayscale + 워터마크("DISCONNECTED") + 조작 차단 처리
- `connection_callback`으로 연결 상태 실시간 업데이트

### 8.5 GUI Design Guide 중심 개발 (02.28~)

**문제**: 개발자마다 입력 필드 크기, 버튼 색상, 간격 등이 달라 UI 일관성 결여.

**결정**: `GUI_Design_Guide.md`를 수립하고 모든 UI 요소의 CSS 클래스를 표준화.

**효과**:
- 신규 패널 추가 시 표준 CSS 사용으로 자동 일관성 확보
- AI 도구(Gemini/Claude)에게 가이드 참조를 지시하여 규격 준수 생성물 확보
- UI 명칭 표준(Nomenclature)으로 소통 효율 향상

---

## 9. 주요 버그 및 해결 이력

### 9.1 드라이버 레벨 버그

| # | 날짜 | 증상 | 원인 | 해결 |
|---|------|------|------|------|
| D-1 | 02.12 | DMOV 고착 (이동 완료 미감지) | STR 응답 필드 매핑 오류 | 필드 인덱스 재매핑 + 폴백 로직 |
| D-2 | 02.13 | 속도 변경 무반응 (0.5 mm/s 고정) | `move()`에서 `maxVelocity` 무시 | `WTB` + `APS` 2단계 구현 |
| D-3 | 02.13 | WTB 에러 105 (파라미터 범위 초과) | `acceleration`(steps/s²)을 ACCL(초)로 오해 | 단위 변환 수정 + 속도별 클램프 |
| D-4 | 02.12 | 리미트 스위치 잘못 감지 | CW/CCW를 개별 필드로 읽음 | 비트마스크 디코딩 (`&0x02`, `&0x01`) |

### 9.2 Web Gateway 레벨 버그

| # | 날짜 | 증상 | 원인 | 해결 |
|---|------|------|------|------|
| G-1 | 02.26 | 접속 직후 10초 프리징 | 미연결 PV 타임아웃 (5축 × 2초) | `connection_timeout=0.01` |
| G-2 | 02.20 | 모바일 접속 불가 | `localhost` 바인딩 | `0.0.0.0` 바인딩 + 방화벽 개방 |

### 9.3 Web GUI 레벨 버그

| # | 날짜 | 증상 | 원인 | 해결 |
|---|------|------|------|------|
| W-1 | 02.20 | STOP 버튼에 "0" 표시 | `data-pv` 속성으로 PV 값이 텍스트 덮어씀 | `data-pv` 제거 |
| W-2 | 02.20 | `caget DESC` 빈값 반환 | DB에 `field(DESC)` 누락 | `KOHZU_Motor.db` 수정 |
| W-3 | 02.26 | 모달 PV 데이터 미반영 | JS 초기화 순서 / `data-tpl-pv` 스킵 로직 | 순서 교정 + 스킵 제거 |
| W-4 | 03.01 | JSON 업로드 후 무반응 | DMOV 역방향 로직 (`!=1` vs `==1`) | 조건문 수정 |
| W-5 | 03.01 | 일부 파라미터만 적용 | 하드코딩 12개 필드만 전송 | `Object.entries` 동적 루프 |
| W-6 | 03.02 | MSTA LED 미작동 | 비트 번호 오류 (0~5 → 실제 1,9,10,2,13,14) | 비트 교정 + `.led` CSS 적용 |
| W-7 | 03.04 | 새로고침 시 입력 필드 흰색 | `.input-dark-tab` CSS 미정의 | 글로벌 `!important` 강제 적용 |
| W-8 | 03.04 | 카드 클릭으로 모달 오픈 | `onclick`이 카드 전체에 적용 | 전용 팝업 아이콘 버튼으로 분리 |

---

## 10. 검증 결과

### 10.1 빌드 검증

```bash
$ make 2>&1 | grep -E 'error|warning|Installing'
Installing created executable ../../../bin/linux-x86_64/KOHUZ_ALV1
Installing shared library ../../../lib/linux-x86_64/libKohzuAries.so
Installing library ../../../lib/linux-x86_64/libKohzuAries.a
# 결과: 에러 0건, 경고 0건 ✅
```

### 10.2 통신 검증

```bash
# IOC 시작 시 드라이버 초기화
KohzuAriesCreateController("PC0", "L0", 6, 0.2, 1.0)
# → iocInit 정상 완료 ✅

# Channel Access 확인
$ caget KOHZU:m1.RBV
KOHZU:m1.RBV     12.345  ✅

# 속도 설정 (WTB 명령)
SENDING cmd='WTB1/0/200/10000/50/50/2'
RESPONSE='C WTB1 0 200 10000 50 50 2 ...' status=0  ✅
```

### 10.3 Web UI 검증

| 항목 | 상태 | 비고 |
|------|------|------|
| 6축 카드 렌더링 | ✅ | Linear/Vertical/Rotation 타입별 표시 |
| 실시간 PV 갱신 | ✅ | WebSocket 경유 (~200ms 지연) |
| 모달 팝업 / 닫기 | ✅ | fetch() 동적 로드 + PV 치환 |
| JSON 파일 업로드 | ✅ | 파라미터 즉시 반영 |
| Stage Select 드롭다운 | ✅ | 서버 `/api/stages` API 연동 |
| 세션 Save/Load | ✅ | 서버 `/api/sessions` API 연동 |
| localStorage 복원 | ✅ | 새로고침 후 상태 유지 |
| 다크 테마 일관성 | ✅ | 글로벌 CSS `!important` 적용 |
| 모바일 접속 | ✅ | `192.168.x.x:8888` 경유 |
| 실시간 차트 | ✅ | 3분할 (Linear/Vertical/Rotation) |
| 리미트 LED 점등 | ✅ | HLS/LLS → Red LED |
| MSTA Bit Status | ✅ | 6종 LED (Done/Problem/Moving/Hi/Lo/Homing) |
| STOP 개별/전체 | ✅ | 축별 STOP + ABORT ALL |

---

## 11. 산출물 목록

### 11.1 소스 코드

| 파일 | 언어 | 행수 | 역할 |
|------|------|------|------|
| `kohzuApp/src/KohzuAriesDriver.cpp` | C++ | ~800 | ARIES 전용 드라이버 |
| `kohzuApp/src/KohzuAriesDriver.h` | C++ | ~80 | 드라이버 헤더 |
| `kohzuApp/opi/web_gateway.py` | Python | 199 | WebSocket Gateway |
| `kohzuApp/opi/dashboard.html` | HTML/JS | ~2,300 | 6축 통합 대시보드 |
| `kohzuApp/opi/motor_popup.html` | HTML/JS | ~800 | 상세 제어 모달 |
| `kohzuApp/opi/motorx_all.html` | HTML/JS | ~1,500 | 단일축 제어 (레거시) |

### 11.2 설정 파일

| 파일 | 역할 |
|------|------|
| `iocBoot/iocKOHUZ_ALV1/st.cmd` | IOC 시작 스크립트 |
| `iocBoot/iocKOHUZ_ALV1/motor.substitutions` | 6축 모터 레코드 템플릿 |
| `KOHUZ_ALV1App/Db/KOHZU_Motor.db` | 모터 레코드 DB |
| `kohzuApp/opi/stages/*.json` (8종) | 스테이지 파라미터 |

### 11.3 문서

| 파일 | 내용 |
|------|------|
| **최종 산출물 (`docs/deliverables/`)** | |
| `Final_Development_Report.md` | **본 문서** (최종 개발 보고서) |
| `Project_Development_History.md` | 개발 이력 종합 타임라인 |
| **가이드 (`docs/guides/`)** | |
| `GUI_Design_Guide.md` | UI 설계 표준 규격서 |
| `Web_Usage_Guide.md` | 시스템 운용 가이드 |
| `Kohzu_ARIES_Integration_Guide.md` | EPICS 연동 가이드 |
| `Kohzu_Homing_Methods_Guide.md` | 원점 복귀 방식 가이드 |
| `Kohzu_Motor_Setup_Guide.md` | 모터 셋업 가이드 |
| `Kohzu_Speed_Ramp_Verification_Guide.md` | 속도 램프 검증 가이드 |
| `Kohzu_Verification_Script_Guide.md` | 검증 스크립트 가이드 |
| `motorx_all_HTML_User_Guide.md` | 단일축 HTML 사용 가이드 |
| `motorx_all_User_Guide.md` | 단일축 사용 가이드 |
| **개발 보고서 (`docs/reports/`)** | |
| `Kohzu_ARIES_Driver_Refactoring_Report.md` | 드라이버 리팩토링 보고서 |
| `Kohzu_ARIES_Driver_Troubleshooting_Report.md` | 드라이버 트러블슈팅 보고서 |
| **참조 자료 (`docs/references/`)** | |
| `Kohzu_ARIES_TCP_IP_Summary.md` | TCP/IP 통신 프로토콜 요약 |
| `Kohzu_Stage_DB_Parameters.md` | 스테이지별 DB 파라미터 참조 |
| `CodeGuidelines_Karpathy` | AI 코딩 가이드라인 참조 |
| **스테이지 (`docs/stages_kohzu/`)** | |
| `*_Control_Guide.md` (8종) | 스테이지별 제어 가이드 |
| **프로젝트 루트** | |
| `README.md` | 빌드 및 설치 가이드 |

---

## 12. 향후 개선 과제

### 12.1 드라이버 (C++) — 높은 우선순위

| 과제 | 설명 | 예상 난이도 |
|------|------|------------|
| **RPS 상대이동 구현** | `move(relative=true)` 시 APS 대신 RPS 명령 사용 | ⭐⭐ |
| **RDE 엔코더 읽기** | `UEIP=Yes` 시 엔코더 위치를 별도 조회 | ⭐⭐ |
| **다중 축 동시이동** | MPS 명령으로 복수 축 동시 이동 지원 | ⭐⭐⭐ |
| **소프트 리미트 연동** | STR `fields[4]` 값을 EPICS 소프트 리미트에 반영 | ⭐ |
| **ORG 센서 상태 반영** | STR `fields[2]` → `motorStatusAtHome_` 매핑 | ⭐ |

### 12.2 Web Gateway (Python) — 중간 우선순위

| 과제 | 설명 | 예상 난이도 |
|------|------|------------|
| **인증(Authentication)** | 비인가 접속 차단 (토큰/패스워드) | ⭐⭐⭐ |
| **로깅 체계** | 명령 이력/에러 로깅 (파일 기반) | ⭐⭐ |
| **SSL/TLS 지원** | HTTPS/WSS 보안 통신 | ⭐⭐ |
| **다중 IOC 지원** | 복수 EPICS IOC에 대한 프록시 기능 | ⭐⭐⭐ |
| **성능 최적화** | PV 데이터 배치 전송 (throttling) | ⭐⭐ |

### 12.3 Web GUI (HTML/JS) — 중간~낮은 우선순위

| 과제 | 설명 | 예상 난이도 |
|------|------|------------|
| **2D Scan 실제 실행** | Raster/Fermat scan 알고리즘 실장 + 모터 연동 | ⭐⭐⭐⭐ |
| **Sequence Mode 실행 엔진** | 정의된 스텝 순차 실행 + 에러 핸들링 | ⭐⭐⭐ |
| **사용자 프리셋 관리** | Stage + 파라미터 묶음을 프리셋으로 저장/호출 | ⭐⭐ |
| **알람 시스템** | 리밋 도달, 에러 발생 시 시각/청각 알림 | ⭐⭐ |
| **데이터 로깅/내보내기** | 차트 데이터를 CSV/Excel로 내보내기 | ⭐⭐ |
| **다국어 지원** | 한국어/영어/일본어 UI 전환 | ⭐⭐ |
| **접근성(A11y)** | 색맹 대응 색상, 키보드 내비게이션 | ⭐⭐ |

### 12.4 인프라 및 운영

| 과제 | 설명 | 예상 난이도 |
|------|------|------------|
| **Docker 컨테이너화** | IOC + Gateway를 Docker 이미지로 패키징 | ⭐⭐⭐ |
| **systemd 서비스 등록** | web_gateway.py 자동 시작/재시작 | ⭐ |
| **모니터링 대시보드** | Gateway 연결 수, PV 갱신 빈도 등 운영 지표 | ⭐⭐⭐ |
| **자동화 테스트** | E2E 테스트 (Playwright/Selenium) | ⭐⭐⭐ |
| **CI/CD 파이프라인** | 빌드/배포 자동화 | ⭐⭐⭐ |

### 12.5 즉시 개선 권장 사항

1. **보안(Security)**: 현재 Gateway에 인증/인가 메커니즘이 없어 네트워크에 접속 가능한 누구나 모터를 제어할 수 있다. **운영 환경에서는 최소한 Basic Auth 또는 API Key 인증을 도입**해야 한다.

2. **에러 복구(Error Recovery)**: WebSocket 연결이 끊어졌을 때의 자동 재연결 및 UI 피드백을 강화해야 한다. 현재는 수동으로 페이지를 새로고침해야 한다.

3. **입력 검증(Input Validation)**: 사용자가 하드웨어 리미트를 넘는 값을 입력했을 때, 클라이언트 단에서 사전 경고하는 기능이 필요하다.

4. **구성 관리(Configuration Management)**: `motor.substitutions`의 기본값과 JSON 스테이지 설정 간의 불일치 가능성을 관리하는 메커니즘이 필요하다.

---

## 부록: 개발 타임라인

| 주차 | 기간 | 주요 마일스톤 |
|------|------|-------------|
| **1주** | 02.05~02.12 | 드라이버 초기 개발 (v0.1~v0.3), DMOV 고착 해결, 통신 프로토콜 확정 |
| **2주** | 02.13~02.19 | 드라이버 전면 리팩토링 (v1.0~v1.1, 16건 해결), OPI→HTML 전환, Web Gateway 구축 |
| **3주** | 02.20~02.26 | 단일축 HTML 완성, 모바일 지원, **6축 통합 대시보드 최초 구축**, IOC 6축 확장 |
| **4주** | 02.27~03.04 | 모달 분리 아키텍처, GUI Design Guide 수립, 실시간 차트, 세션 관리, 상태 영속화 |

> 상세 일별 기록: `docs/deliverables/Project_Development_History.md` 참조

---

*본 보고서는 kohzuApp 프로젝트의 전체 개발 과정과 최종 형태를 종합적으로 기록한 것으로, 후속 개발 및 인수인계 시 참조 문서로 활용할 수 있습니다.*
