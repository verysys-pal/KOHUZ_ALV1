# ZA05A-W101 Control Guide

본 문서는 Kohzu ZA05A-W101 스테이지 (수직/Z축 스테이지) 및 드라이버의 EPICS 제어 설정을 위한 가이드입니다.
EPICS Motor Record의 주요 PV 기능 정의와 상세 계산 로직을 포함합니다.

---

## 1. PV 설정 테이블 (Resolution & Pitch)

ZA05A-W101 웨지(Wedge) 구동형 Z축 스테이지의 기구학적 사양을 기반으로 EPICS Motor 레코드의 필수 필드 값을 계산합니다.

### 사양 (Specifications)
- **Model Number:** ZA05A-W101 (Mirror Model: ZA05A-W101-R)
- **Table Size:** 50mm × 50mm
- **Guide Mechanism:** Cross Roller Guide
- **Motion Range:** ±4.0mm
- **Lead Mechanism:** 1/2 Wedge, Ground Screw, Lead 0.5mm
- **Resolution (Full/Half Step):** 0.5μm / 0.25μm
- **Resolution (Micro Step 1/20 div):** 0.025μm
- **Maximum Speed:** 2.5mm/sec
- **Key Performance Metrics:**
    - Repeatability: ≦±0.5μm (AVE. ±0.06μm)
    - Lost Motion: ≦2μm (AVE. 0.38μm)
    - Verticality: ≦5μm/8mm (AVE. 1.51μm/8mm)
    - Load Capacity: 39.2N (4kgf)
- **Material:** Aluminum Alloy
- **Finishing:** Clear Matt Anodizing
- **Weight:** 0.42kg
- **Electromechanical Specs:**
    - Sensor Model: F-115(HOME, LIMIT)
    - Motor Shaft Diameter: Φ4mm (Conformance option handle: C type)
    - 5 Phase Stepper Motor: Oriental motor PK513PB (Phase Current 0.35A, Basic Step 0.72°)
    - Connector: Hirose RP13A-12JG-20PC
    - 2 Phase Stepper Option (ZA05A-W101-BM):
        - Motor: Oriental motor PKP214D06B
        - Connector: Hirose RP13A-12JG-20PC

### MRES 설정 상세 가이드 (Resolution Calculation)
EPICS Motor Record의 `.MRES` (Motor Resolution) 필드는 모터가 1 스텝 회전할 때 스테이지가 실제로 이동하는 거리(EGU, mm)를 정의합니다.

**공식:**
$$MRES = \frac{UREV}{SREV}$$

*   **UREV (Units per Revolution):** 모터 1회전 당 테이블 수직 이동 거리.
    *   리드 정밀 나사(Lead 0.5mm)가 회전하며, 1/2 비율의 웨지(Wedge) 기구를 통해 수직 이동하므로 유효 이동거리는 절반이 됩니다.
    *   따라서 유효 리드 이동 거리(UREV) = $0.5 \times \frac{1}{2} = \mathbf{0.25}$ mm.
*   **SREV (Steps per Revolution):** 모터 1회전 당 필요 펄스 수
    *   Basic Step 0.72°의 모터를 사용하므로, 1회전에 필요한 풀 스텝 수는 360 / 0.72 = 500 steps/rev 입니다.

**ZA05A-W101 적용 예시:**

1.  **Full Step (0.5μm = 0.0005mm):**
    *   Step Angle: 0.72° (500 steps/rev)
    *   $MRES = 0.25 / 500 = \mathbf{0.0005}$ mm
2.  **Half Step (0.25μm = 0.00025mm) - Recommended:**
    *   Driver Setting: 2-div (Half step)
    *   Steps/Rev: $500 \times 2 = 1000$ Steps/Rev
    *   $MRES = 0.25 / 1000 = \mathbf{0.00025}$ mm
3.  **Micro Step (1/20) (0.025μm = 0.000025mm):**
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
| **(P)(M).HLM** | User High Limit | **3.9** |
| **(P)(M).LLM** | User Low Limit | **-3.9** |
| **(P)(M).VELO** | Velocity (Max 2.5) | **1.5** |

---

## 2. 드라이버 설정 (TITAN-A2 등)

### Current Limit (전류 제한)
모터(PK513PB)의 정격 전류인 **0.35 A/phase**를 초과하지 않도록 설정하십시오.

---

## 3. 운용 가이드 (OPI Operation)

### 적용된 주요 파라미터 상세
- **MRES (0.00025)**: 웨지 비율(1/2), 리드 피치(0.5mm), 그리고 모터의 Half-step 설정(1000 steps/rev)을 기반으로 계산된 분해능입니다.
- **VELO/VMAX (1.5 / 2.5)**: 웨지 구동 구조와 최대 속도 사양(2.5mm/s)을 고려하여 안전 구동을 위해 1.5mm/s로 설정했습니다.
- **HLM/LLM (3.9 / -3.9)**: 실제 허용 스트로크(±4.0mm)에서 충돌 방지를 위해 0.1mm의 여유를 둔 소프트 리미트 값입니다.
- **PREC (5)**: 0.00025 단위의 정밀도를 표현하기 위해 소수점 5자리까지 표시할 수 있습니다.
