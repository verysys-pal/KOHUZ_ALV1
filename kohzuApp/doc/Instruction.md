# 🚀 Project Control Center: kohzuApp
> **AI 가이드:** 본 문서 상단의 '표준 템플릿' 섹션은 참고용입니다. 
> 모든 신규 작업과 결과 기록은 문서의 **가장 아래(최신 날짜 섹션)**에 추가하십시오.
> 자동 기록 문서는 Todo List, Result, 변경 사항, 검증 결과 순으로 작성한다.

- 파일위치 : kohzuApp/doc/Instruction.md

---
# Instruction.md 표준 템플릿 (참고용)
## 📋 1. 작업지시 (User Instruction)
1. 
2. 
- **참조 파일:** - `kohzuApp/src/motor_control.c`
    - `kohzuApp/include/config.h`

### ✅ 1.1 Todo List (AI Analysis)
- [ ] **Step 1: Context Analysis** - 기존 코드의 의존성 및 제어 흐름 파악
- [ ] **Step 2: Core Implementation** - 요구사항에 따른 로직 수정 및 최적화
- [ ] **Step 3: Validation** - 빌드 확인 및 에러 핸들링 검증
- [ ] **Step 4: Documentation** - 변경 사항 주석 및 결과 보고


### 📝 1.2 Result (Execution Summary)

### 🛠 1.3  변경 사항 (Summary of Changes)
- **수정 위치:** `Line XX` in `file_path`
- **주요 로직:** ### 🔍 검증 결과 (Validation)
- [x] 컴파일 성공 여부
- [ ] 런타임 테스트 (시뮬레이션/실기기)

### 💡 사용예시
- Instruction.md : ?? 라인의 지시사항을 반영하여 수행해.





# 2026.02.20
---
## 📋 1. 작업지시 (User Instruction)
1. 현재 모터 스테이지가 1개만 제어하고 있음
2. 모터 스테이지 2개 이상 제어하도록 하려면 어떻게 하는지 설명해줘

### ✅ 1.1 Todo List (AI Analysis)
- [x] **Step 1: Configuration Analysis**
  - **`st.cmd`**: `KohzuAriesCreateController("PC0", "L0", 2, 0.2, 1.0)`
    - 3번째 인자가 `2`로 설정되어 있어, 이미 컨트롤러 레벨에서는 **2축(Axis 0, Axis 1)**까지 제어 가능하도록 구성되어 있음. 별도의 드라이버 소스 수정이나 `st.cmd` 수정은 불필요함.
  - **`motor.substitutions`**: 현재 `ADDR=0`인 `m1` 레코드만 정의되어 있음.
- [x] **Step 2: Guide Documentation**
  - `motor.substitutions` 파일에 `ADDR=1`인 두 번째 모터(`m2`) 레코드를 추가하는 방법 설명.
  - OPI(`motorx_all.html`)에서 두 번째 모터를 제어하기 위해 URL 파라미터(`?M=m2`)를 사용하는 방법 설명.

### 📝 1.2 가이드 (How to Add 2nd Motor)

현재 컨트롤러 설정(`st.cmd`)상 이미 2개의 축(Axis)을 사용할 준비가 되어 있습니다. 따라서 `motor.substitutions` 파일에 두 번째 모터에 대한 정의만 추가하면 됩니다.

#### 1. `motor.substitutions` 파일 수정
`/usr/local/epics/EPICS_R7.0/siteApp/KOHUZ_ALV1/iocBoot/iocKOHUZ_ALV1/motor.substitutions` 파일을 열고, 아래와 같이 두 번째 줄을 추가하십시오.

```diff
 file "../../db/KOHZU_Motor.db"
 {
 pattern
 {P,      M,   PORT, ADDR, DESC,           EGU, DIR,  VELO, VBAS, ACCL, MRES,   SREV, UREV, PREC, HLM,  LLM,   DHLM,  DLLM,  UEIP, RDBD, DLY}
 {KOHZU:, m1,  PC0,  0,    XA07A-L202,   mm,  Pos,  5.0,  0.1,  0.5,  0.0005, 2000, 1.0,  3,    34.0, -34.0, 35.0,  -35.0, No,   0.003, 0.1}
+{KOHZU:, m2,  PC0,  1,    SECOND_AXIS,  deg, Pos,  10.0, 0.5,  0.2,  0.001,  1000, 1.0,  3,    180.0, -180.0, 185.0, -185.0, No,   0.01,  0.1}
 }
```
> **주의:** `ADDR` 값을 반드시 `1`로 설정해야 합니다. (첫 번째 모터는 `0`, 두 번째는 `1`)

#### 2. IOC 재시작
설정 변경 사항을 적용하려면 IOC를 재시작해야 합니다.
```bash
cd /usr/local/epics/EPICS_R7.0/siteApp/KOHUZ_ALV1/iocBoot/iocKOHUZ_ALV1/
../../bin/linux-x86_64/KOHUZ_ALV1 st.cmd
```

#### 3. 두 번째 모터 제어 (Web OPI)
웹 브라우저에서 `motorx_all.html`을 열 때, 주소 뒤에 파라미터를 변경하여 두 번째 모터에 접속할 수 있습니다.
- **기본(1축):** `motorx_all.html?P=KOHZU:&M=m1`
- **추가(2축):** `motorx_all.html?P=KOHZU:&M=m2`

### 🛠 1.3 변경 사항 (Summary of Changes)
- **문서화:** 다축 제어를 위한 설정 파일 수정 및 접속 방법 가이드 작성 완료.




























