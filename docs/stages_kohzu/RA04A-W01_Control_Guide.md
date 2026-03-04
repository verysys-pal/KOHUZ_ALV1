# RA04A-W01 Control Guide

본 문서는 Kohzu RA04A-W01 스테이지 (회전 스테이지) 및 드라이버의 EPICS 제어 설정을 위한 가이드입니다.
EPICS Motor Record의 주요 PV 기능 정의와 상세 계산 로직을 포함합니다.

---

## 1. PV 설정 테이블 (Resolution & Pitch)

RA04A-W01 회전 스테이지의 기구학적 사양을 기반으로 EPICS Motor 레코드의 필수 필드 값을 계산합니다.

### 사양 (Specifications)
- **Model Number:** RA04A-W01 (Mirror Model: RA04A-W01-R)
- **Table Size:** Φ40mm
- **Guide Mechanism:** Angular bearing
- **Angular Range:** ±177°
- **Lead Mechanism:** Worm & Worm Wheel 1/90
- **Resolution (Full/Half Step):** 0.004° / 0.002°
- **Resolution (Micro Step 1/20 div):** 0.0002°
- **Maximum Speed:** 20°/sec
- **Key Performance Metrics:**
    - Accumulated Lead Error: ≦0.02°/360° (AVE. 0.0071°/360°)
    - Lost Motion: ≦0.02° (AVE. 0.0046°)
    - Angular Repeatability: ≦0.002° (AVE. 0.0006°)
    - Pitch Error: ≦0.02°/4° (AVE. 0.0045°/4°)
    - Backlash: ≦0.001° (AVE. 0.0004°)
    - Moment Load Stiffness: 0.9 arcsec/N cm (AVE. 0.46 arcsec/N cm)
    - Load Capacity: 39.2N (4kgf)
    - Surface Runout: ≦20μm/360° (AVE. 6.96μm/360°)
    - Eccentricity: ≦20μm/360° (AVE. 8.38μm/360°)
- **Material:** Aluminum Alloy
- **Finishing:** Clear Matt Anodizing
- **Weight:** 0.42kg
- **Electromechanical Specs:**
    - Sensor Model: F-113 (LIMIT)
    - Motor Shaft Diameter: Φ5mm (Conformance option handle: A type)
    - 5 Phase Stepper Motor: Oriental motor PK524HPMB (Phase Current 0.75A, Basic Step 0.36°)
    - Connector: Hirose RP13A-12JG-20PC
    - 2 Phase Stepper Option (RA04A-W01-BM):
        - Motor: Oriental motor PKP225D15B2
        - Connector: Hirose RP13A-12JG-20PC

### MRES 설정 상세 가이드 (Resolution Calculation)
EPICS Motor Record의 `.MRES` (Motor Resolution) 필드는 모터가 1 스텝 회전할 때 스테이지가 실제로 회전하는 각도(EGU, deg)를 정의합니다.

**공식:**
$$MRES = \frac{UREV}{SREV}$$

*   **UREV (Units per Revolution):** 웜기어 구동의 경우, 모터 1회전 당 테이블의 회전 이동량입니다. Worm Ratio가 1/90이므로 모터가 1회전(360°)하면 테이블은 360° / 90 = **4.0°** 회전합니다. (즉, UREV = **4.0**)
*   **SREV (Steps per Revolution):** 모터 1회전 당 필요 펄스 수
    *   Basic Step이 0.36°인 5 Phase 모터를 사용하므로, 1회전에 필요한 풀 스텝 수는 360 / 0.36 = 1000 steps/rev 입니다.

**RA04A-W01 적용 예시:**

1.  **Full Step (0.004°):**
    *   Step Angle: 0.36° (1000 steps/rev)
    *   $MRES = 4.0 / 1000 = \mathbf{0.004}^\circ$
2.  **Half Step (0.002°) - Recommended:**
    *   Driver Setting: 2-div (Half step)
    *   Steps/Rev: $1000 \times 2 = 2000$ Steps/Rev
    *   $MRES = 4.0 / 2000 = \mathbf{0.002}^\circ$
3.  **Micro Step (1/20) (0.0002°):**
    *   Driver Setting: 20-div
    *   Steps/Rev: $1000 \times 20 = 20000$ Steps/Rev
    *   $MRES = 4.0 / 20000 = \mathbf{0.0002}^\circ$

### 추천 PV 설정값 (Half Step 기준)

| PV Field | Description | Value |
| :--- | :--- | :---: |
| **(P)(M).UREV** | Units per Revolution | **4.0** |
| **(P)(M).SREV** | Steps per Revolution | **2000** |
| **(P)(M).MRES** | Motor Resolution | **0.002** |
| **(P)(M).EGU** | Engineering Units | **deg** |
| **(P)(M).HLM** | User High Limit | **176.0** |
| **(P)(M).LLM** | User Low Limit | **-176.0** |
| **(P)(M).VELO** | Velocity (Max 20.0) | **10.0** |

---

## 2. 드라이버 설정 (TITAN-A2 등)

스테이지 보호를 위해 모터 스펙에 맞는 드라이버 설정이 필요합니다.

### Current Limit (전류 제한)
모터(PK524HPMB)의 정격 전류인 **0.75 A/phase**를 초과하지 않도록 설정하십시오.

---

## 3. 운용 가이드 (OPI Operation)

### 적용된 주요 파라미터 상세
- **MRES (0.002)**: RA04A-W01의 기어비(1/90)와 Half-step(2000 steps/rev) 설정을 기준으로 계산된 분해능입니다.
- **VELO/VMAX (10.0 / 20.0)**: 최대 속도 사양(20°/s)을 고려하여 안전하게 10.0°/s로 설정할 수 있습니다.
- **HLM/LLM (176.0 / -176.0)**: 실제 회전 한계(±177°)보다 1°의 여유를 둔 소프트웨어 리미트 값입니다.
- **PREC (4)**: 회전 스테이지의 정밀도를 표현하기 위해 소수점 4자리까지 표시하도록 설정합니다.

### Soft Limit 설정 (HLM, LLM)
기구적 충돌 방지를 위해 하드웨어 리미트(±177°)보다 안쪽에 소프트 리미트를 설정합니다.

| Parameter | Recommended Value | Note |
| :--- | :---: | :--- |
| **(P)(M).HLM** | **176.0** | Physical Max: 177.0 deg |
| **(P)(M).LLM** | **-176.0** | Physical Min: -177.0 deg |

추가 OPI 설정 항목은 표준 가이드를 참조하십시오.
