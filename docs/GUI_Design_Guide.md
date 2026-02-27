# EPICS Web GUI (OPI) Design Guidelines

이 문서는 `motorx_all.html` 및 `motor_popup.html` 등 EPICS 웹 제어 화면(OPI)을 개발 및 수정할 때 참조해야 할 표준 디자인/레이아웃(UI/UX) 규격을 정의합니다. 새로운 GUI 요소를 추가하거나 변경할 시에는 화면의 통일성을 위해 본 문서의 규격과 속성을 우선적으로 준수하여 주시기 바랍니다.

---

## 1. 폰트 및 기본 테마 설정 (Global Settings)
* **글꼴 (Font-Family)**: `Inter`, sans-serif
* **적용 대상**: `input`, `select`, `button`, `label`, `span` 등 전체 컴포넌트
* **전체 테마 (Theme)**: 슬레이트(Slate) 계열의 다크 모드 테마를 기본으로 채택하여 눈의 피로도를 줄이고 요소 간의 경계를 뚜렷하게 구분합니다.

---

## 2. 화면 분할 및 패널 헤더 (Panels & Headers)
*제어 패널(Drive, Homing, Calibration 등)의 상단 제목 행에 적용하는 규격입니다.*

* **컨테이너 부분 (Container div)**: 
  * 적용 클래스: `bg-slate-700/50 px-2 py-1 border-b border-slate-700 flex justify-between items-center group/header`
  * 배경: 회백색 반투명(`bg-slate-700/50`), 하단 테두리(`border-b border-slate-700`)
* **타이틀 텍스트 부분 (Title span)**:
  * 적용 클래스: `text-sm font-black text-slate-300 uppercase tracking-widest`
  * 속성: `text-sm`, 볼드 집중(`font-black`), 대문자(`uppercase`), 넓은 글자 간격(`tracking-widest`)

* **서브 패널 내부 행 (Sub-panel Rows)**:
  * 항목 구분을 위한 테두리 속성: `border-b border-slate-700/30` 적용
  * 첫 번째 행 등에 불필요한 강조 배경색(`bg-slate-700/50` 등)은 지양하고, 모든 행의 배경을 기본 투명(또는 부모 요소 배경)으로 통일하여 연속성 유지

---

## 3. 버튼 (Buttons)
버튼은 목적과 역할에 따라 크기, 폰트, 상태별 색상을 엄격히 규격화합니다.

### 3.1 일반 제어 버튼 (Standard Button)
조작을 수행하는 대부분의 일반적인 버튼(예: JOG, TWR, TWF, 홈 복귀 등)에 적용합니다.

* **표준 클래스**: 
  * `w-full text-xs font-bold py-1 px-2 rounded border border-slate-600 bg-slate-700 hover:bg-slate-600 text-slate-200 transition-colors uppercase shadow-sm`
* **속성 설명**: 너비 `w-full` (그리드(grid) 공간 전체 활용), 글자 크기 `text-xs`, 폰트 두께 `font-bold`, 대문자 `uppercase`. 배경은 `bg-slate-700`, 반응형 호버 효과로 `bg-slate-600` 적용.

### 3.2 활성 상태 버튼 (Active / Selected State)
USE, SET 모드 또는 특정 상태 피드백을 사용자에게 명확히 전달해야 할 때(JS 렌더러 기반) 상태 클래스를 동적으로 주입합니다.

* **활성 덮어쓰기 요소**:
  * `!bg-green-700 !border-green-600 !text-white`
* **설명**: 모터가 해당 모드로 진입하였거나 선택된 경우, 기존 Slate 테마를 지우고 **진한 초록색**으로 눈에 띄게 강조합니다.

### 3.3 비상/정지 기능 버튼 (Emergency / Stop)
즉각적인 시각적 인지가 필요하고, 잘못 클릭되는 것을 방지하기 위해 특별한 테마를 부여합니다.

* **정지 버튼 (STOP - Warning/Alert)**:
  * 머스타드/진한 노란색 (주로 개별 조작 레이아웃 내 정지 버튼)
  * `text-[10px] font-black py-1 px-2 rounded border border-yellow-700 bg-yellow-600 hover:bg-yellow-500 text-slate-900 transition-colors shadow-sm uppercase text-center`
* **위험 상태 제어 보조 (Red Theme)**:
  * `bg-red-700 hover:bg-red-800 text-red-500 border-red-700`

---

## 4. 데이터 입력 필드 (Input Fields & Select Boxes)
모터 값 설정, 보정 계수 및 각종 PV 값을 직접 입력받는 구역입니다.

* **HTML/Tailwind 기본 속성**: 
  * `class="input-dark-tab py-0.5 text-xs text-right"`
  * 높이/패딩 최소화(`py-0.5`), 텍스트 우측 정렬(`text-right`), 가독성 확보(`text-xs`)
* **고정 너비 (Width Policy)**: 
  * 제어 화면의 안정적인 대칭 구성을 위해 모든 입력창은 기본 너비를 **`80px`**로 강제 준수합니다. (CSS 글로벌 설정 적용)
* **글로벌 강제 CSS (Dark Tab)**:
  ```css
  background-color: #0f172a !important;   /* 심해/어두운 네이비 배경 */
  border: 1px solid #334155 !important;   /* 슬레이트 경계선 */
  color: #e2e8f0 !important;              /* 가독성 높은 밝은 회색(Slate-200) 텍스트 */
  border-radius: 0.25rem;                 /* 둥근 테두리 (Rounded) */
  outline: none;
  transition: border-color 0.2s;
  
  /* 포커스(Focus) 클릭 시 */
  border-color: #3b82f6 !important;       /* 산뜻한 파란색 테두리로 전환 */
  ```

---

## 5. 텍스트 라벨 (Text Labels & Indicators)
항목명 기재 영역과, 입력란은 아니지만 그리드 자리를 차지하는 플레이스홀더 영역입니다.

* **항목명 라벨 (Title Label)**:
  * 클래스: `text-xs text-slate-400 font-bold` (또는 `text-slate-500`)
  * 정렬 방식: 기본 좌측 자간 정렬
* **보조 Indicator / 플레이스홀더 (Placeholder)**:
  * 클래스: `text-right text-xs text-yellow-500/50 pr-1 font-mono`
  * 텍스트: `-` (하이픈 사용)
  * 용도: 입력창이 없는 열(Row/Col)에 배치하여 시각적으로 빈 공간이어도 그리드 형태가 무너지지 않도록 지지대 역할을 수행합니다.

---

## 6. 레이아웃과 그리드 (Grid Alignments)
여러 개의 열을 나열할 때에는 `<div class="grid ...">` 를 통해 가로 길이를 명확히 배분하여 컴포넌트 간 들쭉날쭉한 문제를 방지합니다.

* **표준 그리드 비율 권장 구성 (모터 제어 5열 예시)**:
  * `grid grid-cols-[80px_1fr_1fr_1fr_30px] gap-2 items-center`
  * **설명**: `[라벨 80px] - [입력 1] - [입력 2] - [입력 3] - [상태 LED 30px]` 형태로 빈틈없이 짜여진 단정한 형태를 지향합니다.

* **세부 설정 패널 그리드 구성 (2열 및 3열 표준)**:
  * **라벨 + 단일 입력 (2열)**: `grid grid-cols-[80px_1fr] gap-2 items-center px-2 py-1 border-b border-slate-700/30`
  * **라벨 + 조작 버튼 다수 (3열/4열)**: `grid grid-cols-[80px_1fr_1fr]`, `grid grid-cols-[80px_1fr_1fr_1fr_1fr]`
  * **설명**: Dynamics, Backlash, Jog Control, Homing 등 하위 설정 패널들에서 좌측 라벨 크기(`80px`)를 고정하고 나머지 공간을 컴포넌트들이 `1fr` 비율로 균등하게 나눠 갖도록 설정하여 좌측/우측 정렬 밸런스를 맞춥니다.
