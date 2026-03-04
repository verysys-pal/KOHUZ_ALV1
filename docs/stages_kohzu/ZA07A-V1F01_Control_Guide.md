# ZA07A-V1F01 Control Guide

본 문서는 Kohzu ZA07A-V1F01 Z축(Vertical) 스테이지와 TITAN-A2 드라이버의 EPICS 제어 설정을 위한 가이드입니다.
EPICS Motor Record의 주요 PV 기능 정의와 상세 계산 로직을 포함합니다.

---

## 1. PV 설정 테이블 (Resolution & Pitch)

ZA07A-V1F01 스테이지의 기구학적 사양을 기반으로 EPICS Motor 레코드의 필수 필드 값을 계산합니다.

### 사양 (Specifications)
- **Model Number:** ZA07A-V1F01
- **Table Size:** 70mm × 70mm
- **Guide Mechanism:** Tetrahedral Flat Roller
- **Motion Range:** ±10mm (Hardware Limit)
- **Lead Mechanism:** Ground Screw, Lead 0.5mm, 1/2 belt drive
- **Resolution (Full/Half Step):** 0.5μm / 0.25μm
- **Resolution (Micro Step 1/20 div):** 0.025μm
- **Maximum Speed:** 2.5 mm/sec
- **Key Performance Metrics:**
    - Repeatability: ≦±0.2μm (Ave. ±0.05μm)
    - Lost Motion: ≦2μm (Ave. 0.48μm)
    - Verticality: ≦6μm/20mm (Ave. 1.62μm/20mm)
    - Load Capacity: 117.6N (12kgf)
- **Material:** Aluminum Alloy
- **Finishing:** Clear Matt Anodizing
- **Weight:** 1.8kg
- **Electromechanical Specs:**
    - Sensor Model: F-115 (HOME, LIMIT)
    - Motor Shaft Diameter: Φ5mm (Conformance option handle: A type)
    - 5 Phase Stepper Motor: Oriental motor: C090P-9015P
    - Connector: Hirose: RP13A-12JG-20PC
    - 2 Phase Stepper Option (ZA07A-V1F01-BM):
        - Motor: Oriental motor: PKP244D15B2
        - Connector: Oriental motor: RP13A-12JG-20PC

### MRES 설정 상세 가이드 (Resolution Calculation)
EPICS Motor Record의 `.MRES` (Motor Resolution) 필드는 모터가 1 스텝 회전할 때 스테이지가 실제로 이동하는 거리(EGU, mm)를 정의합니다.

**공식:**
$$MRES = \frac{UREV}{SREV}$$

*   **UREV (Units per Revolution):** 모터 1회전 당 스테이지 이동 거리
    *   Lead: 0.5 mm (Screw 1회전 당 이동 거리)
    *   Reduction Ratio: 1/2 (모터 2회전 = 스크류 1회전)
    *   $UREV = 0.5 / 2 = \mathbf{0.25}$ mm (모터 1회전 당 이동 거리)
*   **SREV (Steps per Revolution):** 모터 1회전 당 필요 펄스 수
    *   5-phase Standard Motor (0.72°/step): 500 steps/rev

**ZA07A-V1F01 적용 예시:**

1.  **Full Step (기본):**
    *   Spec Resolution: 0.5 μm (0.0005 mm)
    *   $MRES = 0.25 / 500 = \mathbf{0.0005}$ mm
2.  **Half Step (추천 - 일반적):**
    *   Spec Resolution: 0.25 μm (0.00025 mm)
    *   Driver Setting: 2-div (Half step)
    *   Steps/Rev: $500 \times 2 = 1000$ Steps/Rev
    *   $MRES = 0.25 / 1000 = \mathbf{0.00025}$ mm
3.  **Micro Step (1/20):**
    *   Spec Resolution: 0.025 μm (0.000025 mm)
    *   Driver Setting: 20-div
    *   Steps/Rev: $500 \times 20 = 10000$ Steps/Rev
    *   $MRES = 0.25 / 10000 = \mathbf{0.000025}$ mm

### 추천 PV 설정값 (Half Step 기준)

| PV Field | Description | Value |
| :--- | :--- | :---: |
| **(P)(M).UREV** | Units per Revolution | **0.25** |
| **(P)(M).SREV** | Steps per Revolution | **1000** |
| **(P)(M).MRES** | Motor Resolution | **0.00025** |
| **(P)(M).EGU** | Engineering Units | **mm** |
| **(P)(M).HLM** | User High Limit | **9.5** |
| **(P)(M).LLM** | User Low Limit | **-9.5** |
| **(P)(M).VELO** | Velocity (Max 2.5) | **1.0** |

---

## 2. 드라이버 설정 (TITAN-A2)

스테이지 보호를 위해 TITAN-A2 드라이버의 하드웨어 스위치를 올바르게 설정해야 합니다.

### Current Limit (전류 제한)
모터(C090P-9015P)의 정격 전류를 고려하여 설정하십시오.

- **RUN Switch:** 설정값 **0.75 A/phase** (확인 필요)에 대응하는 번호 (보통 '5')
- **STOP Switch:** RUN 전류의 50~60% 설정
- **CD Switch (DIP SW 3):** **OFF** (Current Down Enable)

### Pulse Mode (펄스 모드)
- **CK Switch (DIP SW 2):** **OFF** (2-Pulse Mode: CW/CCW)
  *   Kohzu 컨트롤러 표준이며, 만약 Pulse/Dir 방식을 사용한다면 ON으로 변경해야 합니다.

---

## 3. 운용 가이드 (OPI Operation)

### 적용된 주요 파라미터 상세
- **MRES (0.00025)**: 사양서 기준 Half-step 분해능입니다.
- **VELO/VMAX (1.0 / 2.5)**: 최대 속도 사양(2.5 mm/s)을 고려하여 안전하게 1.0 mm/s로 설정했습니다.
- **HLM/LLM (9.5 / -9.5)**: 하드웨어 리미트(±10mm)보다 0.5mm 안쪽에 여유를 둔 소프트웨어 리미트 값입니다.
- **PREC (4)**: 0.00025 단위의 정밀도를 표현하기 위해 소수점 4자리까지 표시하도록 설정했습니다.

### Soft Limit 설정 (HLM, LLM)
기구적 충돌 방지를 위해 하드웨어 리미트(±10mm)보다 안쪽에 소프트 리미트를 설정합니다.

| Parameter | Recommended Value | Note |
| :--- | :---: | :--- |
| **(P)(M).HLM** | **9.5 mm** | Physical Max: 10.0 mm |
| **(P)(M).LLM** | **-9.5 mm** | Physical Min: -10.0 mm |

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
