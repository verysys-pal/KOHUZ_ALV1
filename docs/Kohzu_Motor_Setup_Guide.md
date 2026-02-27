# Kohzu Motor Integration & EPICS Control Systems Guide

본 문서는 Kohzu **ARIES** 제어기와 **TITAN-A II** 모터 드라이브(**TCP/IP** 통신)를 위한 필수 EPICS 설정과 하드웨어 통신 프로토콜을 요약한 가이드입니다.

**EPICS IOC 경로:** `/usr/local/epics/EPICS_R7.0/siteApp/KOHUZ_ALV1`

---

## 1. 하드웨어 통신 프로토콜 및 결선 (Hardware Communication)

Kohzu 컨트롤러와 EPICS IOC 서버 간의 물리적/논리적 연결 설정 방법입니다.

### 1-1. 물리적 연결 (Physical Interface)
*   **TCP/IP 이용 시 (기본 권장)**
    *   **연결:** ARIES 컨트롤러의 LAN 포트를 사용하여 네트워크에 연결합니다.
    *   **설정:** 컨트롤러의 IP 주소와 포트 번호(기본값 예: 12321)를 확인합니다.
*   **RS-232C 이용 시 (보조)**
    *   **케이블:** 크로스 케이블(Null Modem Cable) 사용.

### 1-2. 통신 파라미터
TCP/IP 사용 시 별도의 Baud Rate 설정은 필요 없으나, IP 및 Port가 정확해야 합니다. RS-232C 백업 사용 시에는 ARIES 기본값인 **115200 bps**를 사용합니다.

### 1-3. 명령어 포맷 (Command Format)
*   **구조:** `헤더(STX) + 명령어 + 파라미터 + 구분자`
*   **Terminator (EOL):** **CR (0x0D) + LF (0x0A)** (반드시 2바이트 `\r\n` 사용)

---

## 2. EPICS IOC `st.cmd` 필수 설정

IOC 부팅 스크립트(`st.cmd`)에서 시리얼 포트를 Open하고 모터 드라이버 인스턴스를 생성해야 합니다.

### 2-1. 포트 구성 (ASYN - TCP/IP)
ARIES 컨트롤러와 TCP/IP 통신을 위해 `drvAsynIPPortConfigure`를 사용합니다.

```script
# drvAsynIPPortConfigure("포트명", "IP주소:포트", 우선순위, noAutoConnect, noProcessEos)
# 예: IP 192.168.0.10, Port 12321
drvAsynIPPortConfigure("L0", "192.168.0.10:12321", 0, 0, 0)
```

### 2-2. 컨트롤러 생성 (Motor Driver)
Kohzu 모터 드라이버를 로드하여 컨트롤러 인스턴스를 생성합니다.

*   **함수 원형:** `KohzuCreateController("드라이버인스턴스명", "포트명", 축수, 이동폴링주기ms, 정지폴링주기ms)`

```script
# 예시: 8축 컨트롤러 생성, 이동 시 100ms, 정지 시 500ms 폴링
KohzuCreateController("KOHZU1", "L0", 8, 100, 500)
```

---

## 3. Motor Record 필수 필드 설정 (`.db`)

Motor Record 사용 시 `motorKohzu` 모듈(DevSupport)을 활용합니다.

### 3-1. 핵심 필드 매핑

| 필드 (Field) | 설정 값 | 설명 |
| :--- | :--- | :--- |
| **DTYP** | `asynMotor` | ASYN 기반 모터 드라이버 사용 지정 |
| **OUT** | `@asyn(KOHZU1, 1)` | `st.cmd`의 인스턴스명(`KOHZU1`)과 해당 축 번호(`1`) 매핑 |

### 3-2. 제어 파라미터 확인

| 파라미터 | 필드 | 설명 및 계산 식 |
| :--- | :--- | :--- |
| **단위** | `EGU` | 사용자 공학 단위 (예: `mm`, `deg`) |
| **분해능 (Resolution)** | `MRES` | **Motor Resolution (EGU/Step)**<br>모터가 1 Step 움직일 때 실제 이동하는 거리<br>식: $\frac{UREV}{SREV \times Microstep}$ |
| **회전당 스텝** | `SREV` | Steps per Revolution (보통 200 또는 400) |
| **회전당 거리** | `UREV` | Units per Revolution (1회전에 이동하는 거리, 예: 1mm, 2mm 등) |
| **방향** | `DIR` | `Pos`(정방향) 또는 `Neg`(역방향) |

### 3-3. 속도 및 가속도 설정

| 파라미터 | 필드 | 설명 |
| :--- | :--- | :--- |
| **최대 속도** | `VELO` | 초당 이동 속도 (EGU/sec) |
| **기저 속도** | `VBAS` | 초기 기동 속도 (Base Velocity). 공진 영역 회피를 위해 설정 |
| **가속 시간** | `ACCL` | 목표 속도까지 도달하는 데 걸리는 시간 (초, sec) |

### 3-4. 리미트 및 좌표

| 파라미터 | 필드 | 설명 |
| :--- | :--- | :--- |
| **소프트웨어 리미트** | `DHLM`, `DLLM` | 하드웨어(Dial) 좌표계 기준의 상한/하한 리미트 값 |
| **오프셋** | `OFF` | User 좌표계와 Dial 좌표계 간의 오프셋 (User = Dial + OFF) |

---

## 4. 트러블슈팅 팁

### 통신 디버깅
통신이 안 되거나 명령어가 제대로 전달되는지 의심될 때, IOC 쉘에서 아래 명령어를 입력하여 로우 레벨 ASCII 통신 내용을 확인할 수 있습니다.

```script
# asynSetTraceMask("포트명", 주소, 마스크)
# 마스크: 0x1(Error), 0x2(Device), 0x4(Filter), 0x8(Driver), 0x10(Flow) ...
# 모든 입출력 보기: 255 (0xFF)
asynSetTraceMask("L0", 0, 255)

# 끄기
asynSetTraceMask("L0", 0, 1)
```

---

## 5. 실전 설정 예시: XA07A-L202 스테이지

NotebookLM에 업로드된 **XA07A-L202** (Kohzu MontBlanc Series) 사양을 바탕으로 한 권장 설정값입니다.

### 5-1. 하드웨어 스펙 요약
*   **타입:** 고정밀 전동 X축 스테이지 (Linear Guide + Ball Screw)
*   **스트로크:** ±35mm (총 70mm)
*   **모터:** 5-Phase Stepper (PK523HPMB)
    *   기본 스텝각: **0.36°** (High Resolution Type)
    *   정격 전류: **0.75A/Phase**
*   **리드 (Lead):** 1.0 mm
*   **분해능 (Full Step):** 1 μm (0.001 mm)

### 5-2. 컨트롤러 설정 (ARIES/LYNX/CRUX)
*   **구동 전류 (Run Current):** `0.75A` (System parameter No.67 = '0' for CRUX)
    *   *주의: 전류가 과하면 발열, 부족하면 탈조가 발생합니다.*

### 5-3. EPICS Motor Record 설정 권장값

| 필드 | 설정 값 (예시) | 설명 |
| :--- | :--- | :--- |
| **SREV** | `1000` | 모터 기본 스텝각이 0.36°이므로 360/0.36 = 1000 steps/rev |
| **UREV** | `1.0` | 1회전 당 이동 거리 = Lead = 1.0 mm |
| **MRES** | `0.001` | **1 μm (Full Step 기준)**<br>계산: $1.0 / 1000 = 0.001$ |
| **VELO** | `2.0` | 권장 구동 속도 2mm/s (Max 5mm/s) |
| **ACCL** | `0.5` | 가속 시간 0.5초 (부하에 따라 조정) |
| **DHLM** | `35.0` | Soft High Limit (Max Stroke) |
| **DLLM** | `-35.0` | Soft Low Limit (Min Stroke) |

### 5-4. 운영 시 주의사항
1.  **원점 복귀:** 표준적으로 **NORG (원점 근접 센서)**의 Edge를 검출하는 방식을 사용합니다.
2.  **부하 제한:** 수평 내하중 **7kgf (68.6N)**를 초과하지 않도록 주의하십시오.
3.  **결선:** 모터는 5선식 결선(Type V3)을 따릅니다.
