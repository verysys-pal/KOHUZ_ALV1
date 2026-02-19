# Kohzu ARIES EPICS Driver 개발 가이드

이 문서는 Kohzu ARIES 제어기 및 TITAN-A II 드라이브를 위한 EPICS IOC (`KOHUZ_ALV1`)의 구축 배경, 구조, 그리고 사용 방법을 설명합니다.

## 1. 배경 및 기존 문제점 해결

### 1.1 기존 문제점
일반적인 ASCII 기반 모터 제어기를 EPICS와 연동할 때 다음과 같은 문제가 자주 발생합니다.

*   **TCP/IP 통신 불안정**: ARIES 제어기는 별도의 헤더(STX) 없이 순수 ASCII 문자열과 Terminator(`\r\n`)만으로 통신하므로, 범용 드라이버 사용 시 패킷 끊김이나 동기화 오류가 발생할 수 있습니다.
*   **분해능(Resolution) 불일치**: 드라이버(TITAN-A II)의 마이크로스텝 설정과 EPICS의 위치 단위(mm/deg)가 일치하지 않아, commanded position과 actual position 간의 괴리가 발생할 위험이 높습니다.
*   **명령어 포맷 혼동**: ARIES는 모델별로 명령어 포맷(Separator가 `/` 인지 `공백`인지 등)이 다를 수 있어 표준화된 드라이버가 필요합니다.

### 1.2 해결 방안 및 구현 이유
NotebookLM 가이드를 기반으로 **`asynMotor` 기반 전용 C++ 드라이버**를 구현하여 위 문제들을 해결했습니다.

*   **전용 C++ 드라이버 (`KohzuAriesDriver`)**:
    *   `asynMotorController`를 상속받아 통신 로직을 캡슐화했습니다.
    *   **커스텀 프로토콜 처리**: Separator(`/`)와 Terminator(`\r\n`)를 명확히 처리하여 통신 신뢰성을 확보했습니다.
    *   **상태 폴링 최적화**: `poll()` 함수에서 위치(`RDP`)와 상태를 주기적으로 읽어와 EPICS 레코드에 즉각 반영합니다.

## 2. 파일 구조 및 역할

주요 파일들의 역할은 다음과 같습니다.

| 파일 경로 (Relative to `siteApp/KOHUZ_ALV1`) | 역할 |
| :--- | :--- |
| `kohzuApp/src/KohzuAriesDriver.cpp` | **드라이버 핵심 로직**. TCP/IP 통신, 명령어 변환(EPICS -> ARIES), 폴링 루틴 구현. |
| `kohzuApp/src/Makefile` | 드라이버를 라이브러리(`libKohzuAries.so`)로 빌드하고 DBD 파일을 생성하는 빌드 스크립트. |
| `iocBoot/iocKOHUZ_ALV1/st.cmd` | **IOC 시작 스크립트**. IP 설정, 드라이버 인스턴스 생성, DB 로드 순서를 정의. |
| `db/KOHZU_Motor.db` | EPICS Motor Record 템플릿. 물리적 단위(mm)와 드라이버 스텝 간의 변환 계수 정의. |

## 3. 주요 설정값 (Key Parameters)

NotebookLM 가이드에서 추출한 핵심 파라미터입니다. 현장 상황에 맞춰 `st.cmd`와 `*.db` 파일을 수정해야 합니다.

### 3.1 하드웨어 통신 (`st.cmd`)
*   **IP Address**: `192.168.1.120` (Factory Default, 변경 가능)
*   **TCP Port**: **12321** (Telnet 포트 23번이 아닌 제어 전용 포트)
*   **Poll Period**: Moving(`0.1s`), Idle(`1.0s`) - 네트워크 부하를 고려한 최적값

### 3.2 모터 레코드 (`KOHZU_Motor.db`)
| 필드 (Field) | 값 | 설명 |
| :--- | :--- | :--- |
| **DTYP** | `asynMotor` | Asyn 드라이버 사용 지정 |
| **MRES** | `0.001` | **Motor Resolution**. 1 펄스당 이동 거리 (mm). <br> *(예: Pitch 1mm / (500 step * 2 microstep))* |
| **SREV** | `500` | 모터 1회전당 스텝 수 (5상 스테핑 모터 기준) |
| **VELO** | `1` | 초당 이동 속도 (mm/sec). 드라이버의 Pulse 대역폭 내에서 설정 필요. |
| **ACCL** | `0.2` | 가속 시간 (sec). 급격한 기동 보다는 부드러운 가속 권장. |

## 4. 실행 및 검증 방법

### 4.1 빌드 (Build)
소스 코드가 수정되었다면 `KOHUZ_ALV1` 디렉토리 최상위에서 `make`를 실행합니다.

```bash
cd /usr/local/epics/EPICS_R7.0/siteApp/KOHUZ_ALV1
make
```

### 4.2 IOC 실행
IOC 부팅 스크립트가 있는 디렉토리로 이동하여 실행합니다.

```bash
cd iocBoot/iocKOHUZ_ALV1
../../bin/linux-x86_64/KOHUZ_ALV1 st.cmd
```

**성공 기준:**
1.  Console에 `iocInit` 메시지가 출력됨.
2.  `devMotorAsyn::init_record` 관련 에러가 없거나, 하드웨어 미연결 시 `Connection refused` 메시지만 출력됨.
3.  `epics>` 프롬프트가 뜸.

### 4.3 동작 검증 (Channel Access)
IOC가 실행 중일 때, 다른 터미널에서 `caget` / `caput` / `camonitor` 명령어로 제어합니다.

```bash
# 1. 현재 위치 및 상태 모니터링
camonitor KOHZU:m1.RBV KOHZU:m1.MOVN KOHZU:m1.STAT

# 2. 값 변경 (이동 명령)
# 10mm 절대 위치로 이동
caput KOHZU:m1 10

# 3. 멈춤 명령
caput KOHZU:m1.STOP 1
```

---
**작성자**: Antigravity (Powered by NotebookLM Guide)
**작성일**: 2026.02.05
