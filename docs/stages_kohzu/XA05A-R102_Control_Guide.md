# XA05A-R102 Control Guide

본 문서는 Kohzu XA05A-R102 스테이지 (선형 스테이지) 및 드라이버의 EPICS 제어 설정을 위한 가이드입니다.
EPICS Motor Record의 주요 PV 기능 정의와 상세 계산 로직을 포함합니다.

---

## 1. PV 설정 테이블 (Resolution & Pitch)

XA05A-R102 리니어 스테이지의 기구학적 사양을 기반으로 EPICS Motor 레코드의 필수 필드 값을 계산합니다.

### 사양 (Specifications)
- **Model Number:** XA05A-R102 (Mirror Model: XA05A-R102-R)
- **Table Size:** 50mm × 50mm
- **Guide Mechanism:** Cross Roller Guide
- **Motion Range:** ±7.5mm
- **Lead Mechanism:** Ground Screw, Lead 0.5mm
- **Resolution (Full/Half Step):** 0.5μm / 0.25μm
- **Resolution (Micro Step 1/20 div):** 0.025μm
- **Maximum Speed:** 2.5mm/sec
- **Key Performance Metrics:**
    - Accumulated Lead Error: ≦6μm/15mm (AVE. 1.69μm/15mm)
    - Repeatability: ≦±0.3μm (AVE. ±0.05μm)
    - Lost Motion: ≦1μm (AVE. 0.43μm)
    - Straightness (Horizontal): ≦1μm/15mm (AVE. 0.32μm/15mm)
    - Straightness (Vertical): ≦1μm/15mm (AVE. 0.21μm/15mm)
    - Backlash: ≦1μm (AVE. 0.2μm)
    - Moment Load Stiffness: 0.31 arcsec/N cm (AVE. 0.17 arcsec/N cm)
    - Load Capacity: 49N (5kgf)
- **Material:** Aluminum Alloy
- **Finishing:** Clear Matt Anodizing
- **Weight:** 0.45kg
- **Electromechanical Specs:**
    - Sensor Model: F-116 (HOME, LIMIT)
    - Motor Shaft Diameter: Φ5mm (Conformance option handle: A type)
    - 5 Phase Stepper Motor: Oriental motor PK523HPMB (Phase Current 0.75A, Basic Step 0.36°)
    - Connector: 20Pin Round (Hirose RP13A-12JG-20PC)
    - 2 Phase Stepper Option (XA05A-R102-BM):
        - Motor: Oriental motor PKP225D15B2
        - Connector: 20Pin Round (Hirose RP13A-12JG-20PC)

### MRES 설정 상세 가이드 (Resolution Calculation)
EPICS Motor Record의 `.MRES` (Motor Resolution) 필드는 모터가 1 스텝 회전할 때 스테이지가 실제로 이동하는 거리(EGU, mm)를 정의합니다.

**공식:**
$$MRES = \frac{UREV}{SREV}$$

*   **UREV (Units per Revolution):** 모터 1회전 당 선형 이동 거리 = **0.5 mm** (Lead)
*   **SREV (Steps per Revolution):** 모터 1회전 당 필요 펄스 수
    *   Basic Step 0.36°의 직결 모터를 사용하므로, 1회전에 필요한 풀 스텝 수는 360 / 0.36 = 1000 steps/rev 입니다.

**XA05A-R102 적용 예시:**

1.  **Full Step (0.5μm = 0.0005mm):**
    *   Step Angle: 0.36° (1000 steps/rev)
    *   $MRES = 0.5 / 1000 = \mathbf{0.0005}$ mm
2.  **Half Step (0.25μm = 0.00025mm) - Recommended:**
    *   Driver Setting: 2-div (Half step)
    *   Steps/Rev: $1000 \times 2 = 2000$ Steps/Rev
    *   $MRES = 0.5 / 2000 = \mathbf{0.00025}$ mm
3.  **Micro Step (1/20) (0.025μm = 0.000025mm):**
    *   Driver Setting: 20-div
    *   Steps/Rev: $1000 \times 20 = 20000$ Steps/Rev
    *   $MRES = 0.5 / 20000 = \mathbf{0.000025}$ mm

### 추천 PV 설정값 (Half Step 기준)

| PV Field | Description | Value |
| :--- | :--- | :---: |
| **(P)(M).UREV** | Units per Revolution | **0.5** |
| **(P)(M).SREV** | Steps per Revolution | **2000** |
| **(P)(M).MRES** | Motor Resolution | **0.00025** |
| **(P)(M).EGU** | Engineering Units | **mm** |
| **(P)(M).HLM** | User High Limit | **7.0** |
| **(P)(M).LLM** | User Low Limit | **-7.0** |
| **(P)(M).VELO** | Velocity (Max 2.5) | **1.5** |

---

## 2. 드라이버 설정 (TITAN-A2 등)

### Current Limit (전류 제한)
모터(PK523HPMB)의 정격 전류인 **0.75 A/phase**를 초과하지 않도록 설정하십시오.

---

## 3. 운용 가이드 (OPI Operation)

### 적용된 주요 파라미터 상세
- **MRES (0.00025)**: XA05A-R102의 리드 피치(0.5mm)와 Half-step(2000 steps/rev) 설정을 기준으로 계산된 분해능입니다.
- **VELO/VMAX (1.5 / 2.5)**: 최대 속도 사양(2.5mm/s)을 고려하여 안전 구동을 위해 1.5mm/s로 설정했습니다.
- **HLM/LLM (7.0 / -7.0)**: 실제 허용 스트로크(±7.5mm)보다 0.5mm의 여유를 둔 소프트 리미트 값입니다.
- **PREC (5)**: 0.00025 단위의 초정밀도를 표현하기 위해 소수점 5자리까지 표시하도록 설정할 수 있습니다.
