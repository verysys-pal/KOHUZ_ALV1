# XA05A-L202 Control Guide

본 문서는 Kohzu XA05A-L202 스테이지 (선형 스테이지) 및 드라이버의 EPICS 제어 설정을 위한 가이드입니다.
EPICS Motor Record의 주요 PV 기능 정의와 상세 계산 로직을 포함합니다.

---

## 1. PV 설정 테이블 (Resolution & Pitch)

XA05A-L202 리니어 스테이지의 기구학적 사양을 기반으로 EPICS Motor 레코드의 필수 필드 값을 계산합니다.

### 사양 (Specifications)
- **Model Number:** XA05A-L202 (Mirror Model: XA05A-L202-R)
- **Table Size:** 50mm × 50mm
- **Guide Mechanism:** Linear Guide
- **Motion Range:** ±25mm
- **Lead Mechanism:** Ball Screw, Lead 1.0mm
- **Resolution (Full/Half Step):** 1μm / 0.5μm
- **Resolution (Micro Step 1/20 div):** 0.05μm
- **Maximum Speed:** 5mm/sec
- **Key Performance Metrics:**
    - Accumulated Lead Error: ≦8μm/50mm (AVE. 2.24μm/50mm)
    - Repeatability: ≦±0.5μm (AVE. ±0.05μm)
    - Lost Motion: ≦1μm (AVE. 0.4μm)
    - Straightness (Horizontal): ≦3μm/50mm (AVE. 0.98μm/50mm)
    - Straightness (Vertical): ≦3μm/50mm (AVE. 0.7μm/50mm)
    - Backlash: ≦0.5μm (AVE. 0.13μm)
    - Moment Load Stiffness: 0.20 arcsec/N cm (AVE. 0.11 arcsec/N cm)
    - Load Capacity: 49N (5kgf)
- **Material:** Aluminum Alloy
- **Finishing:** Clear Matt Anodizing
- **Weight:** 0.75kg
- **Electromechanical Specs:**
    - Sensor Model: F-107(LIMIT), F-108(HOME)
    - Motor Shaft Diameter: Φ5mm (Conformance option handle: A type)
    - 5 Phase Stepper Motor: Oriental motor PK523HPMB (Phase Current 0.75A, Basic Step 0.36°)
    - Connector: 20Pin Round (Hirose RP13A-12JG-20PC)
    - 2 Phase Stepper Option (XA05A-L202-BM):
        - Motor: Oriental motor PKP225D15B2
        - Connector: 20Pin Round (Hirose RP13A-12JG-20PC)

### MRES 설정 상세 가이드 (Resolution Calculation)
EPICS Motor Record의 `.MRES` (Motor Resolution) 필드는 모터가 1 스텝 회전할 때 스테이지가 실제로 이동하는 거리(EGU, mm)를 정의합니다.

**공식:**
$$MRES = \frac{UREV}{SREV}$$

*   **UREV (Units per Revolution):** 모터 1회전 당 선형 이동 거리 = **1.0 mm** (Lead)
*   **SREV (Steps per Revolution):** 모터 1회전 당 필요 펄스 수
    *   Basic Step 0.36°의 직결 모터를 사용하므로, 1회전에 필요한 풀 스텝 수는 360 / 0.36 = 1000 steps/rev 입니다.

**XA05A-L202 적용 예시:**

1.  **Full Step (1μm = 0.001mm):**
    *   Step Angle: 0.36° (1000 steps/rev)
    *   $MRES = 1.0 / 1000 = \mathbf{0.001}$ mm
2.  **Half Step (0.5μm = 0.0005mm) - Recommended:**
    *   Driver Setting: 2-div (Half step)
    *   Steps/Rev: $1000 \times 2 = 2000$ Steps/Rev
    *   $MRES = 1.0 / 2000 = \mathbf{0.0005}$ mm
3.  **Micro Step (1/20) (0.05μm = 0.00005mm):**
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
| **(P)(M).HLM** | User High Limit | **24.0** |
| **(P)(M).LLM** | User Low Limit | **-24.0** |
| **(P)(M).VELO** | Velocity (Max 5.0) | **2.0** |

---

## 2. 드라이버 설정 (TITAN-A2 등)

### Current Limit (전류 제한)
모터(PK523HPMB)의 정격 전류인 **0.75 A/phase**를 초과하지 않도록 설정하십시오.

---

## 3. 운용 가이드 (OPI Operation)

### 적용된 주요 파라미터 상세
- **MRES (0.0005)**: XA05A-L202의 리드 피치(1.0mm)와 Half-step(2000 steps/rev) 설정을 기준으로 계산된 분해능입니다.
- **VELO/VMAX (2.0 / 5.0)**: 최대 속도 사양(5.0mm/s)을 고려하여 안전 구동을 위해 2.0mm/s로 권장 설정했습니다.
- **HLM/LLM (24.0 / -24.0)**: 실제 허용 스트로크(±25mm)에서 충돌 방지를 위해 1.0mm의 여유를 둔 소프트 리미트 값입니다.
- **PREC (4)**: 0.0005 단위의 정밀도를 표현하기 위해 소수점 4자리까지 표시하도록 설정할 수 있습니다.
