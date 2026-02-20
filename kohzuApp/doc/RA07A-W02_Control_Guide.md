# RA07A-W02 Control Guide

본 문서는 Kohzu RA07A-W02 로테이션 스테이지와 TITAN-A2 드라이버의 EPICS 제어 설정을 위한 가이드입니다.
EPICS Motor Record의 주요 PV 기능 정의와 상세 계산 로직을 포함합니다.

---

## 1. PV 설정 테이블 (Resolution & Pitch)

RA07A-W02 스테이지의 기구학적 사양을 기반으로 EPICS Motor 레코드의 필수 필드 값을 계산합니다.

### 사양 (Specifications)
- **Model Number:** RA07A-W02
- **Mirror Model Number:** RA07A-W02-R
- **Table Size:** Φ68mm
- **Guide Mechanism:** Angular Bearing
- **Angular Range:** ±135°
- **Lead Mechanism:** Worm & Worm Wheel 1/90
- **Resolution (Full/Half Step):** 0.004° / 0.002°
- **Resolution (Micro Step 1/20 div):** 0.0002°
- **Maximum Speed:** 20°/sec
- **Key Performance Metrics:**
    - Accumulated Lead Error: ≦0.015°/360° (Ave. 0.0045°/360°)
    - Lost Motion: ≦0.006° (Ave. 0.0026°)
    - Angular Repeatability: ≦0.002° (Ave. 0.0004°)
    - Pitch Error: ≦0.01°/4° (Ave. 0.0027°/4°)
    - Backlash: ≦0.001° (Ave. 0.0001°)
    - Moment Load Stiffness: 0.51 arcsec/N cm (Ave. 0.32 arcsec/N cm)
    - Load Capacity: 58.8N (6kgf)
    - Surface Runout: ≦15μm/360° (Ave. 5.53μm/360°)
    - Eccentricity: ≦5μm/360° (Ave. 2.74μm/360°)
- **Material:** Aluminum Alloy
- **Finishing:** Clear Matt Anodizing
- **Weight:** 1.2kg
- **Electromechanical Specs:**
    - Sensor Model: F-101 (HOME, LIMIT)
    - Motor Shaft Diameter: Φ5mm (Conformance option handle: A type)
    - 5 Phase Stepper Motor: Oriental motor: PK544PMB
    - Connector: Hirose: RP13A-12JG-20PC
    - 2 Phase Stepper Option (RA07A-W02-BM):
        - Motor: Oriental motor: PKP244D15B
        - Connector: Hirose: RP13A-12JG-20PC

### MRES 설정 상세 가이드 (Resolution Calculation)
EPICS Motor Record의 `.MRES` (Motor Resolution) 필드는 모터가 1 스텝 회전할 때 스테이지가 실제로 이동하는 각도(EGU, degree)를 정의합니다.

**공식:**
$$MRES = \frac{UREV}{SREV}$$

*   **Lead Mechanism (Worm Ratio):** 1/90
    *   One Stage Revolution (360°) requires 90 Motor Revolutions.
    *   Output per 1 Motor Rev = $360 / 90 = 4.0^\circ$
*   **Motor Step Angle:** 0.36° (1000 steps/rev - Inferred from 0.004° Full Step Spec)
    *   Unlike standard 0.72° (500 steps/rev) motors, the spec resolution (0.004°) with a 1/90 gear requires a 0.36° motor (or 0.72° with 1/2 microstep base).
    *   Calculation: $4.0^\circ / 1000 = 0.004^\circ$ (Matches Full Step Spec)

*   **UREV (Units per Revolution):** 모터 1회전 당 스테이지 회전 각도 ($360 / 90 = 4.0^\circ$)
*   **SREV (Steps per Revolution):** 2000 (Half Step assuming 1000 steps/rev base).

**RA07A-W02 적용 예시 (Spec 기준):**

1.  **Full Step (0.004°):**
    *   $MRES = \mathbf{0.004}^\circ$
2.  **Half Step (0.002°) - Recommended:**
    *   $MRES = \mathbf{0.002}^\circ$
3.  **Micro Step 1/20 (0.0002°):**
    *   $MRES = \mathbf{0.0002}^\circ$

### 추천 PV 설정값 (Half Step 기준)

| PV Field | Description | Value |
| :--- | :--- | :---: |
| **(P)(M).UREV** | Units per Revolution | **4.0** |
| **(P)(M).SREV** | Steps per Revolution | **2000** |
| **(P)(M).MRES** | Motor Resolution | **0.002** |
| **(P)(M).EGU** | Engineering Units | **deg** |

---

## 2. 드라이버 설정 (TITAN-A2)

스테이지 보호를 위해 TITAN-A2 드라이버의 하드웨어 스위치를 올바르게 설정해야 합니다.

### Current Limit (전류 제한)
모터(PK544PMB)의 정격 전류를 고려하여 설정하십시오.

- **RUN Switch:** 설정값 **0.75 A/phase** (확인 필요)에 대응하는 번호 (보통 '5')
- **STOP Switch:** RUN 전류의 50~60% 설정
- **CD Switch (DIP SW 3):** **OFF** (Current Down Enable)

### Pulse Mode (펄스 모드)
- **CK Switch (DIP SW 2):** **OFF** (2-Pulse Mode: CW/CCW)
  *   Kohzu 컨트롤러 표준이며, 만약 Pulse/Dir 방식을 사용한다면 ON으로 변경해야 합니다.

---

## 3. 운용 가이드 (OPI Operation)

### 적용된 주요 파라미터 상세
- **MRES (0.002)**: 사양서 기준 Half-step 분해능입니다.
- **VELO/VMAX (5.0 / 20.0)**: 최대 속도 사양(20 deg/s)을 고려하여 안전하게 5.0 deg/s로 설정했습니다.
- **HLM/LLM (130.0 / -130.0)**: 하드웨어 리미트(±135°)보다 5° 안쪽에 여유를 둔 소프트웨어 리미트 값입니다.
- **PREC (3)**: 0.002 단위의 정밀도를 표현하기 위해 소수점 3자리까지 표시하도록 설정했습니다.

### Soft Limit 설정 (HLM, LLM)
기구적 충돌 방지를 위해 하드웨어 리미트(±135°)보다 안쪽에 소프트 리미트를 설정합니다.

| Parameter | Recommended Value | Note |
| :--- | :---: | :--- |
| **(P)(M).HLM** | **130.0 deg** | Physical Max: 135.0 deg |
| **(P)(M).LLM** | **-130.0 deg** | Physical Min: -135.0 deg |

### EPICS Motor Record OPI - PV 기능 정의표
OPI 화면(`motorx_all.opi` 등)에서 사용되는 주요 PV 필드의 기능과 역할입니다.

#### 1. 구동 및 상태 (Drive & Status)
| PV | Name | 상세 설명 | Access |
| :--- | :--- | :--- | :---: |
| **VAL** | User Desired Value | 목표 위치입니다. 값을 쓰면 이동이 시작됩니다. | R/W |
| **RBV** | User Readback Value | 현재 실제 위치(Readback)입니다. | R |
| **DMOV** | Done moving to value | 이동 완료 여부 (1: 완료, 0: 이동 중) | R |
| **STOP** | Stop | 모터를 즉시 정지시킵니다. | R/W |
| **SPMG** | Stop/Pause/Move/Go | 동작 모드 제어 (Go: 이동 가능, Stop: 이동 불가) | R/W |

#### 2. 속도 및 가속도 (Dynamics)
| PV | Name | 상세 설명 | Access |
| :--- | :--- | :--- | :---: |
| **VELO** | Velocity | 목표 주행 속도 (EGU/s) | R/W |
| **VBAS** | Base Velocity | 기동 속도 (Start Speed) | R/W |
| **ACCL** | Seconds to Velocity | 가속 시간 (초). 정지→목표속도 도달 시간 | R/W |

#### 3. 조그 및 미세 조정 (Jog & Tweak)
| PV | Name | 상세 설명 | Access |
| :--- | :--- | :--- | :---: |
| **JOGF** | Jog Forward | 1인 동안 정방향 연속 이동 | R/W |
| **JOGR** | Jog Reverse | 1인 동안 역방향 연속 이동 | R/W |
| **TWF** | Tweak Forward | TWV 만큼 정방향 이동 | R/W |
| **TWV** | Tweak Step Size | 미세 조정 이동 거리 | R/W |

#### 4. 리미트 및 캘리브레이션 (Limits & Calibration)
| PV | Name | 상세 설명 | Access |
| :--- | :--- | :--- | :---: |
| **HLM** | User High Limit | 사용자 상한 리미트 (Soft Limit) | R/W |
| **LLM** | User Low Limit | 사용자 하한 리미트 (Soft Limit) | R/W |
| **LVIO** | Limit violation | 소프트 리미트 위반 시 1 | R |
| **HLS** | High Limit Switch | 하드웨어 상한 리미트 감지 | R |
| **LLS** | Low Limit Switch | 하드웨어 하한 리미트 감지 | R |
| **SET** | Set/Use Switch | 좌표 보정 모드 (1: Set - 이동 없이 좌표만 변경) | R/W |

#### 5. 해상도 및 피드백 (Resolution & Feedback)
| PV | Name | 상세 설명 | Access |
| :--- | :--- | :--- | :---: |
| **MRES** | Motor Step Size | 모터 1 Step당 이동 거리 (위의 계산식 참조) | R/W |
| **UEIP** | Use Encoder | 엔코더 사용 여부 (Yes/No) | R/W |
| **RDBD** | Retry Deadband | 위치 도달 판단 오차 범위 | R/W |
