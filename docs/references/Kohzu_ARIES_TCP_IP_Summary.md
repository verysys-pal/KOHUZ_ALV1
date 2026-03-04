# Kohzu ARIES 제어기 및 TITAN-A II 드라이브 TCP/IP 제어 요약

본 문서는 NotebookLM의 가이드를 참조하여, ARIES 제어기와 TITAN-A II 드라이브를 TCP/IP로 제어하기 위한 필수 정보를 요약한 것입니다.

## 1. TCP/IP 통신 설정

*   **기본 포트 번호 (Default Port):** **12321**
*   **프로토콜:** TCP/IP 소켓 통신 (ASCII 기반)
*   **IP 주소 (Factory Default):** `192.168.1.120` (변경 가능)

> **참고:** Telnet 접속 시에는 23번 포트를 사용하나, 일반적인 제어 명령 전송 시에는 **12321** 포트를 사용합니다.

## 2. 명령 패킷 구조 (Command Packet Structure)

ARIES 제어기는 RS-232C와 달리 **헤더(STX)를 사용하지 않는** 순수 ASCII 포맷을 사용합니다.

### 송신 포맷 (PC -> ARIES)
*   **구조:** `<Command><Parameter 1>/<Parameter 2>/...<CRLF>`
*   **설명:**
    *   **헤더 (STX):** 없음 (사용 시 에러 발생)
    *   **Command:** 3글자 대문자 (예: `APS`, `ORG`)
    *   **Separator:** 슬래시(`/`) 사용 (공백 사용 불가)
    *   **Terminator:** **CR (0x0D) + LF (0x0A)**
*   **예시:** `APS1/0/1000/0` + `\r\n` (1축을 1000 펄스 절대 위치로 이동)

### 수신 포맷 (ARIES -> PC)
*   **구조:** `<Status><TAB><Command><TAB><Axis><TAB><Data>...<CRLF>`
*   **설명:**
    *   **Status:** `C` (정상), `E` (에러), `W` (경고)
    *   **Separator:** **TAB (0x09)**
    *   **Terminator:** **CR (0x0D) + LF (0x0A)**
*   **예시:** `C` + `\t` + `APS` + `\t` + `1` + `\r\n` (정상 응답)

## 3. EPICS Motor Record 필수 설정

Kohzu 모터 제어를 위해 반드시 설정해야 하는 핵심 레코드 필드입니다.

### 3-1. 필드 요약

| 필드명 | 설명 (Full Name) | 설정 가이드 |
| :--- | :--- | :--- |
| **DTYP** | Device Type | `asynMotor` (ASYN 드라이버 사용) |
| **OUT** | Output Link | `@asyn(PORT_NAME, AXIS_NO)` (예: `@asyn(L0, 1)`) |
| **SREV** | Steps per Rev | 모터 1회전당 스텝 수 (보통 5상 모터는 **500** 또는 마이크로스텝 적용 값) |
| **UREV** | Units per Rev | 모터 1회전당 이동 거리 (예: **1** mm) |
| **MRES** | Motor Step Size | **1 펄스당 이동 거리** (계산식 참조) |
| **VELO** | Velocity | 초당 이동 속도 (Unit/sec) |
| **VBAS** | Base Velocity | 기동 속도 (공진 회피를 위해 0보다 크게 설정 권장) |
| **ACCL** | Acceleration Time | 목표 속도 도달 시간 (초 단위, 예: 0.2) |
| **RDBD** | Retry Deadband | 위치 제어 허용 오차 (Closed-loop 제어 시 중요) |

### 3-2. MRES (Motor Resolution) 계산식

시스템의 분해능을 결정하는 가장 중요한 값입니다.

$$ MRES = \frac{UREV}{SREV \times Microstep Factor} $$

*   **UREV:** 1회전 이동 거리 (예: Lead Screw Pitch 2mm -> 2)
*   **SREV:** 모터 기본 분해능 (예: 5상 모터 -> 500)
*   **Microstep Factor:** 드라이버 설정 분할 수 (예: Full=1, Half=2)

**계산 예시:**
*   Pitch 1mm, 5상 모터(500), Half Step(2분할) 사용 시
*   $MRES = 1 / (500 \times 2) = 0.001$ mm

## 4. 기타 주의사항
*   **엔코더 사용 시:** `UEIP=Yes`로 설정하고 `ERES`(Encoder Resolution)를 정확히 입력해야 합니다.
*   **속도 테이블:** ARIES는 내부 속도 테이블을 사용하므로, EPICS의 `VELO/ACCL` 값이 드라이버가 허용하는 근사치로 매핑될 수 있습니다.
