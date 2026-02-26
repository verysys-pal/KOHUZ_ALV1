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
- Instruction.md : ?? 라인의 지시사항을 반영하여 수행해. (템플릿 적용)












# 2026.02.26
---
## 📋 1. 작업지시 (User Instruction)
1. kohzuApp/opi/motorx_all.png, kohzuApp/opi/edm/motorx_all.opi 파일을 참조하여 motor_popup.html 파일을 수정해.
2. kohzuApp/opi/edm/motorx_all.opi 파일에서 사용한 pv의 수와 motor_popup.html 파일에서 사용한 pv의 수가 일치하는지 확인해.

### ✅ 1.1 Todo List (AI Analysis)
- [x] **Step 1: OPI Layout & PV Analysis** - `motorx_all.opi` 파일 내 컨트롤 위젯 및 연동 PV 리스트 추출
- [x] **Step 2: HTML UI Update** - `motor_popup.html`에 OPI 스타일의 Drive, Calibration, Dynamics, Servo, Resolution 섹션 추가
- [x] **Step 3: PV Match Verification** - 기존 OPI 사용 PV와 HTML 내 등록된 PV 개수 비교 및 누락분 추가
- [x] **Step 4: Real-time LED Indicator Sync** - `MSTA` 비트 파싱 로직을 `gen_dashboard.py`와 `dashboard.html`에 반영
- [x] **Step 5: Documentation** - 변경 사항 기록

### 📝 1.2 Result (Execution Summary)
- `motor_popup.html`의 UI를 OPI(`motorx_all.opi`)와 동일한 구조로 전면 개편했습니다.
- PV 사용 수 비교 결과:
  - `motorx_all.opi`에 선언된 접미사(PV suffix): 총 69종
  - 개편된 `motor_popup.html`에 적용된 접미사: 총 60종
  - OPI에만 있고 HTML에 미적용된 PV(9종)는 주로 GUI 매크로 또는 내부 처리에만 쓰이는 비핵심 PV(예: `ATHM`, `CARD`, `DTYP`, `VERS` 등 일부 시스템 정보 혹은 중복 기능)이며 제어에 필요한 핵심 PV는 모두 연동했습니다.
  - 추가적으로 전체 모터 정지를 위한 `allstop.VAL` 기능을 모터 팝업 헤더에 추가하여 안정성을 높였습니다.

### 🛠 1.3 변경 사항 (Summary of Changes)
- **수정 위치:** `kohzuApp/opi/motor_popup.html`
- **주요 로직:**
  - OPI와 동일한 레이아웃(Drive, Calibration, Dynamics, Backlash, Jog, Servo, Resolution)으로 UI 섹션 세분화 및 재배치.
  - 누락되었던 PID(PCOF, ICOF, DCOF), Backlash(BDST, BVEL 등), Jog(JVEL, JAR), Resolution 패널 PV 속성(`data-pv`) 대거 추가.
  - `MSTA` 비트별 디스플레이용 LED(`.led-tiny`) UI 추가.
- **수정 위치:** `kohzuApp/opi/gen_dashboard.py`, `dashboard.html`
- **주요 로직:** WebSocket `onMessage` 이벤트 처리 시 `.MSTA` PV의 값 비트 연산을 통해 팝업 내 상태 LED 점멸 로직 동기화 업데이트.

### 🔍 검증 결과 (Validation)
- [x] `gen_dashboard.py` 실행을 통한 `dashboard.html` 생성 성공
- [x] 대시보드 렌더링 환경에서 모터 팝업 레이아웃 정상 표시 및 스테이지 JSON 데이터 우측 패널 파싱 연동 확인














---
## 📋 2. 작업지시 (User Instruction)
1. motor_popup.html > 다크모드 적용해. (입력칸이 흰색이라서 글자가 보이지 않음)
2. 왼쪽제어카드와 오른쪽 스테이지 정보 카드의 크기는 동일할 필요 없음 (왼쪽제어카드 1.5배 정도 더 크게)
3. 왼쪽제어카드 > pv 입력 칸의 크기를 1/2로 줄여줘.

### ✅ 2.1 Todo List (AI Analysis)
- [x] **Step 1: Dark Mode Plugin** - `motor_popup.html`의 텍스트 입력 칸 다크모드 스타일링
- [x] **Step 2: Modal Body Grid Update** - `gen_dashboard.py` 에서 팝업 레이아웃을 5등분(`lg:grid-cols-5`)으로 분할
- [x] **Step 3: Card Ratio Adjustment** - 왼쪽 카드는 `lg:col-span-3` (60%), 오른쪽 카드는 `lg:col-span-2` (40%)로 비율 조정 (1.5배)
- [x] **Step 4: Input Width Reduction** - 왼쪽 제어 카드 내 입력 칸의 크기(width) 50%로 축소 적용
- [x] **Step 5: Apply & Build** - `gen_dashboard.py` 실행하여 `dashboard.html` 생성
- [x] **Step 6: Documentation** - 변경 사항 기록

### 📝 2.2 Result (Execution Summary)
- `motor_popup.html`의 입력 필드(`.input-dark-tab`, `input[data-pv$=".VAL"]`)에 백그라운드 및 테두리 색상을 명시하여 다크모드를 완벽하게 적용했습니다. (기존 사용자 지정 테마 대응)
- 팝업 좌우 카드 크기 비율을 기존 1:1에서 3:2(왼쪽 제어 카드가 1.5배 넓음)로 변경했습니다.
- 왼쪽 제어용 카드의 입력 칸(수치 및 문자)이 부모 요소 폭 대비 절반(50%) 크기만 차지하도록 스타일을 재조정했습니다.

### 🛠 2.3 변경 사항 (Summary of Changes)
- **수정 위치:** `kohzuApp/opi/motor_popup.html`
- **주요 로직:** 
  - `<style>` 태그를 추가하여 내부 `.input-dark-tab` 과 데이터 입력 필드의 다크 모드 CSS 강제 적용.
  - 왼쪽 카드의 크기 조정 클래스로 `lg:col-span-3`, 오른쪽 카드로 `lg:col-span-2` 지정, 입력 필드의 너비를 `width: 50%`로 지정. 
- **수정 위치:** `kohzuApp/opi/gen_dashboard.py`
- **주요 로직:** 모달 바디 박스의 Grid Layout을 `lg:grid-cols-5`로 수정하여 5분할 지원 적용.

### 🔍 검증 결과 (Validation)
- [x] `gen_dashboard.py` 실행을 통한 템플릿 컴파일 성공 여부.
- [x] 팝업 클래스 및 스타일 수정 확인.