# Kohzu Stage EPICS DB Parameters Guide

본 문서는 `KohzuStages.pdf` 자료를 바탕으로 Kohzu 정밀 스테이지 모델별 EPICS Motor Record 필수 필드 설정값을 정리한 가이드입니다.

> **Note:** 아래 설정값은 모터 드라이버가 **Half Step (기본 설정)** 모드로 설정된 것을 가정합니다.

## 1. 모델별 상세 파라미터 (Detailed Parameters)

| 모델명 (Model) | 축 유형 (Axis) | 단위 (EGU) | 구동 범위 (Stroke) | UREV (mm,deg) | SREV (Steps) | MRES (EGU/Step) | 권장 VELO (EGU/s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **ZA10A-W2C** | Vertical (Z) | mm | -2.5 ~ 2.5 | 0.25 | 2000 | 0.000125 | 0.125 |
| **ZA16A-W2C** | Vertical (Z) | mm | -8.0 ~ 8.0 | 0.25 | 1000 | 0.00025 | 0.125 |
| **XA10A-R1** | Linear (X) | mm | -12.5 ~ 12.5 | 0.5 | 2000 | 0.00025 | 0.25 |
| **XA16A-R1** | Linear (X) | mm | -25.0 ~ 25.0 | 1.0 | 1000 | 0.001 | 0.5 |
| **RA05A-W** | Rotation | deg | -84.0 ~ 174.0 | 4.0 | 2000 | 0.002 | 0.4 |
| **SA05B-RM** (Top) | Swivel | deg | -8.0 ~ 8.0 | 1.2 | 2000 | 0.0006 | 1.2 |
| **SA05B-RB** (Bot) | Swivel | deg | -10.0 ~ 10.0 | 0.96 | 2000 | 0.00048 | 0.96 |
| **SA16A-RT** (Top) | Swivel | deg | -10.0 ~ 10.0 | 0.706 | 1000 | 0.000706 | 0.706 |
| **SA16A-RM** (Bot) | Swivel | deg | -10.0 ~ 10.0 | 0.6 | 1000 | 0.0006 | 0.6 |

## 2. 필드 설명 및 계산식

EPICS DB(`*.db` 또는 `motor.substitutions`) 작성 시 각 필드의 의미와 계산 방법은 다음과 같습니다.

### 2-1. MRES (Motor Resolution)
모터가 1 Step 움직일 때 실제 이동하는 물리적 거리입니다. 드라이버의 마이크로스텝 설정에 따라 달라집니다.
$$ MRES = \frac{UREV}{SREV \times MicroStepFactor} $$
*   **Half Step 기준:** MicroStepFactor = 1 (표의 SREV가 이미 Half Step 기준임)
*   **예시 (ZA10A-W2C):** $0.25 / 2000 = 0.000125$ mm

### 2-2. SREV (Steps per Revolution)
모터 축 1회전에 필요한 펄스(Step) 수입니다.
*   **0.36° 모터 (소형, 예: ZA10A):** Full(1000), Half(2000)
*   **0.72° 모터 (대형, 예: ZA16A):** Full(500), Half(1000)

### 2-3. UREV (Units per Revolution)
모터 축 1회전 시 스테이지 이동량입니다. 기구학적으로 고정된 값입니다.
*   **Wedge 타입(Z축):** 리드 스크류 피치 $\times$ 쐐기 비율
*   **Linear 타입(X축):** 리드 스크류 피치
*   **Rotation/Swivel:** 웜기어 비율에 따름

### 2-4. 리미트 설정 (DHLM, DLLM)
표에 명시된 구동 범위는 스펙상 최대치입니다. 안전을 위해 **소프트웨어 리미트는 스펙보다 약간 안쪽으로 설정**하는 것을 권장합니다.
*   *예: XA16A-R1 스펙이 ±25.0mm 이면, DB에는 ±24.5mm 정도로 설정*

---

## 3. 적용 예시 (Example `motor.substitutions`)

```template
file "$(MOTOR)/db/motorKohzu.db"
{
pattern
{P,      M,    DTYP,        PORT,   ADDR,  DESC,           EGU,  MRES,      SREV, UREV, VELO,  ACCL, DLLM,  DHLM}
{IOC:,   m1,   "asynMotor", KOHZU1, 0,     "Z-Axis",       mm,   0.000125,  2000, 0.25, 0.125, 0.2,  -2.4,  2.4}  # ZA10A
{IOC:,   m2,   "asynMotor", KOHZU1, 1,     "X-Axis",       mm,   0.00025,   2000, 0.5,  0.25,  0.2,  -12.0, 12.0} # XA10A
{IOC:,   m3,   "asynMotor", KOHZU1, 2,     "Rotation",     deg,  0.002,     2000, 4.0,  0.4,   0.5,  -84.0, 174.0} # RA05A
}
```
