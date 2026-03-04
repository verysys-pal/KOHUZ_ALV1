# SA05A-R2B01 Control Guide

본 문서는 Kohzu SA05A-R2B01 스테이지 (고니오미터/Swivel 스테이지) 및 드라이버의 EPICS 제어 설정을 위한 가이드입니다.
EPICS Motor Record의 주요 PV 기능 정의와 상세 계산 로직을 포함합니다.

---

## 1. PV 설정 테이블 (Resolution & Pitch)

SA05A-R2B01 기울기 스테이지의 기구학적 사양을 기반으로 EPICS Motor 레코드의 필수 필드 값을 계산합니다.

### 사양 (Specifications)
- **Model Number:** SA05A-R2B01 (Mirror Model: SA05A-R2B01-R)
- **Table Size:** 50mm × 50mm
- **Guide Mechanism:** Cross Roller Guide
- **Angular Range:** ±3.5°
- **Lead Mechanism:** Ball Screw, Lead 1.0mm
- **Resolution (Full/Half Step):** ≈0.001274° / 0.000637°
- **Resolution (Micro Step 1/20 div):** ≈0.0000637°
- **Maximum Speed:** 9.6°/sec (Half 15kpps)
- **Key Performance Metrics:**
    - Repeatability: ≦±0.001° (AVE.±0.0001°)
    - Lost Motion: ≦0.003° (AVE. 0.0006°)
    - Backlash: ≦0.003° (AVE. 0.0006°)
    - Moment Load Stiffness: 0.41 arcsec/N cm (AVE. 0.295 arcsec/N cm)
    - Load Capacity: 29.4N (3kgf)
    - Work Distance: 86mm ±0.2mm
    - Rotation Center Error: φ0.05mm/±3.5°
- **Material:** Aluminum Alloy
- **Finishing:** Clear Matt Anodizing
- **Weight:** 0.27kg
- **Electromechanical Specs:**
    - Sensor Model: F-116 (HOME, LIMIT)
    - Motor Shaft Diameter: Φ4mm (Conformance option handle: C type)
    - 5 Phase Stepper Motor: Oriental motor PK513PB (Phase Current 0.35A, Basic Step 0.72°)
    - Connector: Hirose RP13A-12JG-20PC
    - 2 Phase Stepper Option (SA05A-R2B01-BM):
        - Motor: Oriental motor PKP214D06B
        - Connector: Hirose RP13A-12JG-20PC

### MRES 설정 상세 가이드 (Resolution Calculation)
EPICS Motor Record의 `.MRES` (Motor Resolution) 필드는 모터가 1 스텝 구동할 때 스테이지가 실제로 회전하는 각도(EGU, deg)를 정의합니다.

**공식:**
$$MRES = \frac{UREV}{SREV}$$

*   **UREV (Units per Revolution):** 볼스크류의 선형 운동을 각도 운동으로 변환하므로 동작은 비선형적 특성을 띠지만 중심 부근에서의 등가 유효 각도 변화율을 사용합니다. 사양 상 Full Step (0.72°) 1회전(500 steps) 시 이동 각도는 약 $500 \times 0.001274^\circ \approx 0.637^\circ$ 입니다.
    * 즉, 기준 UREV $\approx$ **0.637** 로 산정할 수 있습니다.
*   **SREV (Steps per Revolution):** 모터 1회전 당 필요 펄스 수
    *   Basic Step이 0.72°인 5 Phase 모터를 사용하므로, 1회전에 필요한 풀 스텝 수는 360 / 0.72 = 500 steps/rev 입니다.

**SA05A-R2B01 적용 예시:**

1.  **Full Step (≈0.001274°):**
    *   Step Angle: 0.72° (500 steps/rev)
    *   $MRES = 0.637 / 500 = \mathbf{0.001274}^\circ$
2.  **Half Step (0.000637°) - Recommended:**
    *   Driver Setting: 2-div (Half step)
    *   Steps/Rev: $500 \times 2 = 1000$ Steps/Rev
    *   $MRES = 0.637 / 1000 = \mathbf{0.000637}^\circ$

### 추천 PV 설정값 (Half Step 기준)

| PV Field | Description | Value |
| :--- | :--- | :---: |
| **(P)(M).UREV** | Units per Revolution | **0.637** |
| **(P)(M).SREV** | Steps per Revolution | **1000** |
| **(P)(M).MRES** | Motor Resolution | **0.000637** |
| **(P)(M).EGU** | Engineering Units | **deg** |
| **(P)(M).HLM** | User High Limit | **3.4** |
| **(P)(M).LLM** | User Low Limit | **-3.4** |
| **(P)(M).VELO** | Velocity (Max 9.6) | **5.0** |

---

## 2. 드라이버 설정 (TITAN-A2 등)

### Current Limit (전류 제한)
모터(PK513PB)의 정격 전류인 **0.35 A/phase**를 초과하지 않도록 설정하십시오.

---

## 3. 운용 가이드 (OPI Operation)

### 적용된 주요 파라미터 상세
- **MRES (0.000637)**: 볼스크류 메커니즘을 반영하여 계산된 1 스텝당 유효 각도 변화량입니다.
- **VELO/VMAX (5.0 / 9.6)**: 최대 회전 속도 (9.6°/s)에 대해 여유로운 동작을 위해 5.0°/s 를 권장합니다.
- **HLM/LLM (3.4 / -3.4)**: 허용 스트로크 내 (±3.5°) 안전한 구동을 위해 소프트 리미트를 ±3.4°로 설정합니다.
