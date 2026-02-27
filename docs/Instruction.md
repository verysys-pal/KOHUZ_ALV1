# 🚀 Project Control Center: kohzuApp
> **AI 가이드:** 본 문서 상단의 '표준 템플릿' 섹션은 참고용입니다. 
> 모든 신규 작업과 결과 기록은 문서의 **가장 아래(최신 날짜 섹션)**에 추가하십시오.
> 자동 기록 문서는 Todo List, Result, 변경 사항, 검증 결과 순으로 작성한다.

- 파일위치 : kohzuApp/doc/Instruction.md

---
## GUI 화면 구성시 준수할것
- docs/GUI_Design_Guide.md







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












# 2026.02.27
---
## 📋 1. 작업지시 (User Instruction)
1. motor_popup.html > 제어패널
2. Dynamics > Max speed 행 gui 규칙 준수 할 것
3. Backlash, Jog Control, Homing 행 gui 규칙 준수 할 것
4. ctrl 누르고 있을때 빨간색 pv 표시하는것 삭제

### ✅ 1.1 Todo List (AI Analysis)
- [x] **Step 1: Context Analysis** - `motor_popup.html`, `gen_dashboard.py`, `motorx_all.html` 등 관련 소스 구조 파악 및 `GUI_Design_Guide.md` 규칙 확인
- [x] **Step 2: Core Implementation** - 제어 패널(Dynamics, Backlash, Jog Control, Homing) 레이아웃에 `grid-cols-[80px_1fr]`을 적용하고 `<input>` 기본 width 강제 클래스(`.input-dark-tab`)와 호환되게 구성
- [x] **Step 3: Removing Debug Overlay** - `Control` 키 입력 시 빨간색 PV 오버레이가 나타나는 로직과 CSS 클래스 제거 (`motorx_all.html`, `gen_dashboard.py`)
- [x] **Step 4: Documentation** - `gen_dashboard.py` 실행하여 `dashboard.html`에 일괄 갱신, 문서화

### 📝 1.2 Result (Execution Summary)
요청하신 사항에 따라 `motor_popup.html`의 2열 레이아웃을 가지는 하위 세부 패널들(Dynamics, Backlash, Jog Control, Homing)에 대해 OPI 표준 GUI 디자인 라벨 고정 폭(`80px`) 그리드 규칙(`grid-cols-[80px_1fr]`)을 적용하여 정렬을 깔끔하게 맞췄습니다. 추가로 컨트롤(`Ctrl`) 키를 눌렀을 때 각 컴포넌트 위에 뜨는 빨간색 PV 이름 오버레이 표시 렌더러 동작을 완전히 제거했습니다.

### 🛠 1.3 변경 사항 (Summary of Changes)
- **수정 위치:** `kohzuApp/opi/motor_popup.html`
- **주요 수정:** 
    - Dynamics, Backlash, Jog Control, Homing 각 항목의 래퍼 `div`에 지정되어 있던 `flex justify-between`을 `grid grid-cols-[80px_1fr] gap-2 items-center`로 교체하여 OPI 라벨/입력폼 규격화 완료.
    - 조그(Jog) / 복귀(Home) 기능 조작 버튼 행의 경우 `grid-cols-[80px_1fr_1fr]` 그리드를 적용하고 라벨을 채워 넣음.
- **수정 위치:** `kohzuApp/opi/motorx_all.html`, `kohzuApp/opi/gen_dashboard.py`
- **주요 수정:** 
    - JS 내의 `Control` 단축키 감지 `addEventListener`(`keydown`/`keyup`) 삭제
    - 글로벌 CSS의 `.debug-mode` 오버레이 클래스 규칙 블록 삭제
    - 제너레이터 템플릿 코드 `gen_dashboard.py` 동기화 및 실행(`dashboard.html` 빌드 재수행)

### 🔍 검증 결과 (Validation)
- [x] HTML 템플릿 파싱 및 대시보드 재생성 성공
- [ ] OPI 적용 후 브라우저 레이아웃 테스트 (유저 직접 확인 필요)





---
## 📋 2. 작업지시 (User Instruction)
1. motor_popup.html > 제어패널
2. Dynamics > Max speed 행의 바탕색을 아래의 speed, base, accel 행처럼 동일하게 변경 할 것
3. Backlash, Jog Control, Homing 패널도 동일하게 변경 할 것

### ✅ 2.1 Todo List (AI Analysis)
- [x] **Step 1: Context Analysis** - `motor_popup.html`의 CSS 클래스 파악 (`bg-slate-700/50`)
- [x] **Step 2: Core Implementation** - Dynamics, Backlash, Jog Control, Homing 패널 최상단 행 바탕색 및 테두리 변경 (`bg-slate-700/50` 제거,  `border-b border-slate-700/30`으로 통일)
- [x] **Step 3: Validation** - 제너레이터 스크립트(`gen_dashboard.py`) 실행 후 결과 확인 및 `dashboard.html` 빌드 재수행
- [x] **Step 4: Documentation** - 변경 사항 기록

### 📝 2.2 Result (Execution Summary)
요청하신 사항에 따라 `motor_popup.html`의 Dynamics, Backlash, Jog Control, Homing 패널 최상단 행(Max Spd, Distance, Velocity, HVel)의 바탕색을 하단 행들과 동일하게 보이도록 CSS 클래스를 수정했습니다. 기존에 적용되어 있던 짙은 배경 클래스(`bg-slate-700/50`)를 제거하고 통일된 테두리 투명도(`border-slate-700/30`)로 변경하여 일관성을 맞췄습니다. 이 후 파이썬 스크립트를 재구동하여 dashboard.html을 생성 완료했습니다.

### 🛠 2.3 변경 사항 (Summary of Changes)
- **수정 위치:** `kohzuApp/opi/motor_popup.html`
- **주요 수정:**
    - Dynamics, Backlash, Jog Control, Homing 하위 패널의 첫 번째 `div` 컨테이너에서 `bg-slate-700/50` 클래스 제거 및 `border-slate-700`을 `border-slate-700/30`으로 통일화 (`Line 270`, `296`, `326`, `350` 부근)
- **수정 위치:** `kohzuApp/opi/gen_dashboard.py` (빌드 재수행)

### 🔍 검증 결과 (Validation)
- [x] HTML 템플릿 갱신 및 `gen_dashboard.py` 실행 정상 (Exit code: 0)
- [ ] OPI 적용 후 화면 레이아웃/스타일 정상 반영 유무 확인 (유저 직접 확인 필요)






---
## 📋 3. 작업지시 (User Instruction)
1. motor_popup.html > 제어패널
2. Jog Control, Homing > Action 라벨 때문에 버튼이 잘림. Action 라벨을 삭제 할 것
3. Precision (PREC) 값에 따라 Drive 패널에 표시되는 값은 PREC 값 이상의 소수점 표시 하지 말것

### ✅ 3.1 Todo List (AI Analysis)
- [x] **Step 1: Action 라벨 삭제 및 레이아웃 수정** - `motor_popup.html`의 Jog Control, Homing 패널에서 "Action" 라벨을 제거하고, 버튼들이 화면을 꽉 채울 수 있도록 컬럼을 분할(`grid-cols-2`)
- [x] **Step 2: Precision(PREC) 변수 확보 로직 구현** - `motorx_all.html` 내부 `EPICSController` 클래스를 수정하여 WebSocket으로 전달되는 `.PREC` 값을 구독 및 저장(`this.precisions[match]`)하는 로직 추가
- [x] **Step 3: 숫자 표기 포맷 정밀도 적용(.toFixed)** - 모든 요소(`input` 및 `span` 등)의 값이 화면에 표시(렌더링)될 때, 미리 저장해둔 해당 축(axis)의 `prec` (기본값 4)를 기준으로 소수점 자릿수를 자르도록(`parseFloat(val.toFixed(prec))`) 코드 수정
- [x] **Step 4: Validation 확립** - JS 코드 수정 오류 검토 후 `gen_dashboard.py` 실행 및 `dashboard.html` 동기화 업데이트 적용

### 📝 3.2 Result (Execution Summary)
요청하신 사항에 맞추어 `motor_popup.html`의 Jog Control 및 Homing 제어 버튼부에서 버튼 글씨가 잘리는 원인이었던 'Action' 라벨 텍스트를 완전히 제거했습니다. 이로 인해 잃게 된 공간은 `grid-cols-2` 속성을 통해 2개의 버튼이 균등하게 1:1 비율로 남은 너비를 꽉 채울 수 있도록 레이아웃을 최적화했습니다.
추가적으로 `EPICSController` 구동부(`motorx_all.html`의 JS 영역)에서 EPICS 모터 Record의 `PREC` 값을 지속적으로 관찰/저장하도록 코드를 업데이트했습니다. 이에 따라 수치 데이터가 화면에 출력되거나 `input` 폼에 쓰일 때, 지정된 소수점 자리수 이상의 불필요한 값은 잘려 표시됩니다. 스크립트 실행 후 Dashboard 재구성도 이상 없이 성공했습니다.

### 🛠 3.3 변경 사항 (Summary of Changes)
- **수정 위치:** `kohzuApp/opi/motor_popup.html`
    - Jog Control 및 Homing 패널 하단의 버튼 Action 래퍼에서 `span` Action 라벨 요소 자체 삭제
    - 그리드 설정을 3열(`.grid-cols-[80px_1fr_1fr]`)에서 동일한 비율의 2분할 래퍼(`.grid-cols-2`)로 교체
- **수정 위치:** `kohzuApp/opi/motorx_all.html` (및 동기화된 `dashboard.html`)
    - JavaScript `EPICSController.constructor` 내부에 각 모터별 `.PREC` 정보를 들고 있을 `precisions` 객체 추가
    - `onMessage()` 메서드에서 `.PREC` PV를 업데이트 받았을 때 정밀도를 업데이트하는 인터셉트 조건(`data.type === 'update' && data.pv.endsWith('.PREC')`) 추가
    - 표시용 값이 `typeof val === 'number'`인 경우 축의 번호를 찾은 뒤, `val.toFixed(prec)` 메서드를 통해 소수점을 자르는 포매팅 로직 전면 수정
- **실행 내역:** `python3 gen_dashboard.py` 명령 수행을 통해 위 변경사항들에 대해 일괄 반영 및 파서 갱신 성공 (Exit code: 0)

### 🔍 검증 결과 (Validation)
- [x] HTML 템플릿 갱신 및 `gen_dashboard.py` 파싱 성공
- [ ] OPI 브라우저 적용 시 PREC 값 변경에 따라 숫자가 동적으로 정밀도가 변하는 동작 상태 확인 (유저 직접 확인 필요)








---
## 📋 4. 작업지시 (User Instruction)
1. motor_popup.html > 제어패널 > Drive
2. Readback user,dial,raw 표시 창의 크기가 입력필드와 동일하게 변경 할 것
3. Readback 표시 칸(User, Dial, Raw) 내부의 폰트 우측 여백이 위/아래의 input 필드와 다름 (동일하게 맞출 것)

### ✅ 4.1 Todo List (AI Analysis)
- [x] **Step 1: CSS 클래스 분석** - `motor_popup.html`의 Drive 패널 내에 위치한 Readback 표기부 요소들의 크기와 내부 텍스트 정렬 스타일을 분석. 여백 부족 현상 확인.
- [x] **Step 2: Flex 속성 강제 주입 및 폰트 여백(Padding) 교정** - 텍스트를 감싸고 있는 `div` 컨테이너에 `flex justify-end items-center h-full` 속성을 추가하여 높이를 통일시키고, 내부 텍스트인 `span` 요소에는 `pr-1` 패딩을 주어 텍스트가 칸의 우측 모서리에 완전히 들러붙지 않게끔 다른 `input` 폼의 여백과 비슷하게 일치시킴.
- [x] **Step 3: Validation 확립** - 수정한 HTML 템플릿 검토 후 `gen_dashboard.py` 실행 및 `dashboard.html` 동기화 로직 수행.

### 📝 4.2 Result (Execution Summary)
지시 사항에 맞추어 `motor_popup.html`의 Drive 패널에 속한 세 개의 Readback 표시 칸(User, Dial, Raw) 크기 속성을 조정 및 오른쪽 여백을 일치시켰습니다.
기존 디자인 모델에서는 부모가 `text-right`만 지정하고 값(`.pv-font`) 칸에는 따로 패딩이 없어서 숫자가 프레임 우측 끝에 바짝 달라붙어 위·아래 다른 입력 칸(`input text-right`)의 내부 패딩과 정렬이 미세하게 어긋나는 문제가 있었습니다. 이를 해결하고자 내부의 숫자 `span` 요소들에 `pr-1` (오른쪽 패딩) 클래스를 각각 부여하여 텍스트 우측 여백을 여유롭게 통일했습니다. 파이프라인(`gen_dashboard.py`) 갱신 또한 성공했습니다.

### 🛠 4.3 변경 사항 (Summary of Changes)
- **수정 위치:** `kohzuApp/opi/motor_popup.html`
    - Drive 패널 내 `<span data-pv="$(P)$(M).RBV"...>` 등 Readback 값을 표시하는 `span` 요소들(User, Dial, Raw)에 개별적으로 `pr-1` 클래스 주입 (`Line 121`, `126`, `130`).
- **수정 위치:** `kohzuApp/opi/dashboard.html`
    - 파이썬 템플릿 제너레이터 실행을 통한 정적 에셋 동기화 성공 (`Exit code 0`)

### 🔍 검증 결과 (Validation)
- [x] 코드 파싱 및 `gen_dashboard.py` 정상 완료 (빌드 에러 없음)
- [ ] 브라우저 환경에서 Drive 패널 Readback 요소의 우측 정렬된 숫자들의 끝 여백이 아래위 `input` 값들과 동일한 수직선상에 오는지 여부 확인 (유저 직접 확인 필요)
