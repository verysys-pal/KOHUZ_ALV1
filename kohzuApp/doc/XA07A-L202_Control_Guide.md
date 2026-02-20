# XA07A-L202 Control Guide

본 문서는 Kohzu XA07A-L202 스테이지와 TITAN-A2 드라이버의 EPICS 제어 설정을 위한 가이드입니다.
EPICS Motor Record의 주요 PV 기능 정의와 상세 계산 로직을 포함합니다.

---

## 1. PV 설정 테이블 (Resolution & Pitch)

XA07A-L202 스테이지의 기구학적 사양을 기반으로 EPICS Motor 레코드의 필수 필드 값을 계산합니다.

### 사양 (Specifications)
- **Model Number:** XA07A-L202
- **Mirror Model Number:** XA07A-L202-R
- **Table Size:** 70mm × 70mm
- **Guide Mechanism:** Linear Guide
- **Motion Range:** ±35mm
- **Lead Mechanism:** Ball Screw, Lead 1.0mm
- **Resolution (Full/Half Step):** 1μm / 0.5μm
- **Resolution (Micro Step 1/20 div):** 0.05μm
- **Maximum Speed:** 5mm/sec
- **Key Performance Metrics:**
    - Accumulated Lead Error: ≦8μm/70mm (Ave. 2.31μm/70mm)
    - Repeatability: ≦±0.5μm (Ave. ±0.06μm)
    - Lost Motion: ≦1μm (Ave. 0.41μm)
    - Straightness (Horizontal): ≦3μm/70mm (Ave. 1.18μm/70mm)
    - Straightness (Vertical): ≦3μm/70mm (Ave. 0.73μm/70mm)
    - Backlash: ≦1μm (Ave. 0.16μm)
    - Moment Load Stiffness: 0.18 arcsec/N cm (Ave. 0.09 arcsec/N cm)
    - Load Capacity: 68.6N (7kgf)
- **Material:** Aluminum Alloy
- **Finishing:** Clear Matt Anodizing
- **Weight:** 1.15kg
- **Electromechanical Specs:**
    - Sensor Model: F-107 (LIMIT), F-108 (HOME)
    - Motor Shaft Diameter: Φ5mm (Conformance option handle: A type)
    - 5 Phase Stepper Motor: Oriental motor: PK523HPMB
    - Connector: 20Pin Round (Hirose: RP13A-12JG-20PC)
    - 2 Phase Stepper Option (XA07A-L202-BM):
        - Motor: Oriental motor: PKP225D15B2
        - Connector: 20Pin Round (Hirose: RP13A-12JG-20PC)

### MRES 설정 상세 가이드 (Resolution Calculation)
EPICS Motor Record의 `.MRES` (Motor Resolution) 필드는 모터가 1 스텝 회전할 때 스테이지가 실제로 이동하는 거리(EGU, mm)를 정의합니다.

**공식:**
$$MRES = \frac{UREV}{SREV}$$

*   **UREV (Units per Revolution):** 모터 1회전 당 이동 거리 = **1.0 mm** (Lead)
*   **SREV (Steps per Revolution):** 모터 1회전 당 필요 펄스 수
    *   5-phase Standard Motor (0.72°/step): 500 steps/rev
    *   (Full Step Res 1um -> 1.0mm / 500 = 0.002mm? No. Spec says Full Step = 1um.)
    *   Means Motor must be **1000 steps/rev** (High Res 0.36°) OR 500 steps/rev with half-step driver as "Full".
    *   Given Spec: "Resolution Full/Half Step : 1μm/0.5μm"
    *   Wait, Lead 1.0mm.
    *   If 1000 steps/rev (0.36°): 1.0 / 1000 = 0.001mm = 1μm. (Matches Spec).
    *   So the base motor is likely 0.36 deg/step (High Resolution type).

**XA07A-L202 적용 예시:**

1.  **Full Step (1μm):**
    *   Step Angle: 0.36° (1000 steps/rev)
    *   $MRES = 1.0 / 1000 = \mathbf{0.001}$ mm
2.  **Half Step (0.5μm) - Recommended:**
    *   Driver Setting: 2-div (Half step)
    *   Steps/Rev: $1000 \times 2 = 2000$ Steps/Rev
    *   $MRES = 1.0 / 2000 = \mathbf{0.0005}$ mm
3.  **Micro Step (1/20) (0.05μm):**
    *   Driver Setting: 20-div
    *   Steps/Rev: $1000 \times 20 = 20000$ Steps/Rev
    *   $MRES = 1.0 / 20000 = \mathbf{0.00005}$ mm

### 추천 PV 설정값 (Half Step 기준)

| PV Field | Description | Value |
| :--- | :--- | :---: |
| **(P)(M).UREV** | Units per Revolution | **1.0** |
| **(P)(M).SREV** | Steps per Revolution | **2000** |
| **(P)(M).MRES** | Motor Resolution | **0.0005** |
| **(P)(M).EGU** | Engineering Units | **mm** |
| **(P)(M).HLM** | User High Limit | **34.0** |
| **(P)(M).LLM** | User Low Limit | **-34.0** |
| **(P)(M).VELO** | Velocity (Max 5.0) | **2.0** |

---

## 2. 드라이버 설정 (TITAN-A2)

스테이지 보호를 위해 TITAN-A2 드라이버의 하드웨어 스위치를 올바르게 설정해야 합니다.

### Current Limit (전류 제한)
모터(PK523HPMB)의 정격 전류(Rated Current)인 **0.75 A/phase**를 초과하지 않도록 설정하십시오.

- **RUN Switch:** 설정값 **0.75 A/phase**에 대응하는 번호 (보통 '5' 또는 매뉴얼 표 참조)
- **STOP Switch:** RUN 전류의 50~60% 설정
- **CD Switch (DIP SW 3):** **OFF** (Current Down Enable)

### Pulse Mode (펄스 모드)
- **CK Switch (DIP SW 2):** **OFF** (2-Pulse Mode: CW/CCW)
  *   Kohzu 컨트롤러 표준이며, 만약 Pulse/Dir 방식을 사용한다면 ON으로 변경해야 합니다.

---

## 3. 운용 가이드 (OPI Operation)

### 적용된 주요 파라미터 상세
- **MRES (0.0005)**: XA07A-L202의 리드 피치(1.0mm)와 Half-step(2000 steps/rev) 설정을 기준으로 계산된 분해능입니다.
- **VELO/VMAX (2.0 / 5.0)**: 최대 속도 사양(5mm/s)을 고려하여 안전하게 2.0mm/s로 설정했습니다.
- **HLM/LLM (34.0 / -34.0)**: 실제 스트로크(±35mm)보다 1mm의 여유를 둔 소프트웨어 리미트 값입니다.
- **PREC (4)**: 0.0005 단위의 정밀도를 표현하기 위해 소수점 4자리까지 표시하도록 설정했습니다.

### Soft Limit 설정 (HLM, LLM)
기구적 충돌 방지를 위해 하드웨어 리미트(±35mm)보다 안쪽에 소프트 리미트를 설정합니다.

| Parameter | Recommended Value | Note |
| :--- | :---: | :--- |
| **(P)(M).HLM** | **34.0 mm** | Physical Max: 35.0 mm |
| **(P)(M).LLM** | **-34.0 mm** | Physical Min: -35.0 mm |

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
