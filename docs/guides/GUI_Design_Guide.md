# EPICS Web GUI (OPI) Design Guidelines

이 문서는 `dashboard.html` 및 `motor_popup.html` 등 EPICS 웹 제어 화면(OPI)을 개발 및 수정할 때 참조해야 할 표준 디자인/레이아웃(UI/UX) 규격을 정의합니다. 새로운 GUI 요소를 추가하거나 변경할 시에는 화면의 통일성을 위해 본 문서의 규격과 속성을 우선적으로 준수하여 주시기 바랍니다.

---

## 1. 폰트 및 기본 테마 설정 (Global Settings)

### 1.1 글꼴 (Fonts)
| 용도 | 글꼴 | CDN |
|------|------|-----|
| **UI 전체** | `Inter` (400/600/700/900) | `fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900` |
| **PV 데이터 / 모노스페이스** | `JetBrains Mono` (400/700) | `fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700` |

* **적용 대상**: `body`, `input`, `select`, `button`, `label`, `span` 등 전체 컴포넌트
* **적용 방법**: `body { font-family: 'Inter', sans-serif; }`, PV 값 영역에는 `.pv-font { font-family: 'JetBrains Mono', monospace; }`

### 1.2 색상 팔레트 (Color Palette)
본 프로젝트는 **TailwindCSS Slate 계열 다크 모드**를 기준으로 합니다. 아래 색상표를 참조하여 통일성을 유지합니다.

| 역할 | TailwindCSS 클래스 | HEX 값 | 사용처 |
|------|-------------------|--------|--------|
| **페이지 배경** | `bg-slate-900` | `#0f172a` | `body`, 입력 필드 배경 |
| **카드 배경** | `bg-slate-800` | `#1e293b` | `.card`, 패널 배경 |
| **패널 헤더** | `bg-slate-700/50` | `#334155` (50% 투명) | 패널 타이틀 행 |
| **테두리** | `border-slate-700` | `#334155` | 카드, 입력 필드, 패널 |
| **테두리 (밝음)** | `border-slate-600` | `#475569` | 버튼 테두리 |
| **본문 텍스트** | `text-slate-200` | `#e2e8f0` | 기본 텍스트 |
| **라벨 텍스트** | `text-slate-400` | `#94a3b8` | 항목명, 보조 텍스트 |
| **헤더 텍스트** | `text-slate-300` | `#cbd5e1` | 패널 제목 |
| **데이터 표시** | `text-green-400` | `#4ade80` | 읽기 전용 PV 값 |
| **입력 텍스트** | `text-white` | `#ffffff` | 사용자 입력 값 |
| **정상 상태** | `bg-green-700` | `#15803d` | 활성 버튼, 정상 LED |
| **경고 상태** | `bg-yellow-600` | `#ca8a04` | STOP 버튼, 경고 LED |
| **에러 상태** | `bg-red-700` | `#b91c1c` | 에러 LED, 위험 버튼 |
| **포커스 강조** | `border-blue-500` | `#3b82f6` | 입력 필드 포커스 |
| **이동 중 강조** | `bg-blue-600` | `#2563eb` | MOVING 배지 |
| **차트-Linear** | `text-blue-400` | `#60a5fa` | X축 스테이지 |
| **차트-Vertical** | `text-purple-400` | `#c084fc` | Z축 스테이지 |
| **차트-Rotation** | `text-orange-400` | `#fb923c` | R/S축 스테이지 |

### 1.3 외부 의존성 (External Dependencies)
새 프로젝트에서 동일 GUI를 구성하려면 아래 CDN을 `<head>`에 포함해야 합니다.

```html
<!-- TailwindCSS (유틸리티 CSS 프레임워크) -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- Chart.js (실시간 그래프) -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<!-- Google Fonts (Inter + JetBrains Mono) -->
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;700;900&display=swap" rel="stylesheet">
```

### 1.4 전체 테마 (Theme)
* 슬레이트(Slate) 계열의 다크 모드 테마를 기본으로 채택
* 눈의 피로도를 줄이고 요소 간의 경계를 뚜렷하게 구분
* 글로벌 dark 강제 CSS:
```css
/* 모든 input/select에 다크 테마 강제 적용 */
input:not([type="checkbox"]):not([type="radio"]),
select {
    background-color: #0f172a !important;
    border: 1px solid #334155 !important;
    color: #f1f5f9 !important;
    border-radius: 0.25rem;
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
}
input:focus, select:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}
```

#### 1.4.1 스타일링 이중 구조 원칙 (Hybrid Styling Architecture)
본 프로젝트는 **커스텀 CSS(`<style>` 태그)**와 **TailwindCSS 유틸리티(인라인 `class`)**를 **의도적으로 혼합**하여 사용합니다. 두 방식은 각각 고유한 역할을 담당하며, Tailwind 단독으로 통합하지 않습니다.

##### 역할 분담 원칙

| 영역 | 담당 | 이유 |
|------|------|------|
| 구조적 뼈대 (카드, 모달) | **커스텀 CSS** | `.card`, `.modal-overlay` 등 반복 사용 클래스 |
| 상태 토글 (LED, 활성 버튼) | **커스텀 CSS** | JS에서 단일 클래스 토글(`classList.add('on')`)로 상태 변경 |
| 애니메이션 | **커스텀 CSS** | `@keyframes`, `box-shadow` 발광 등 Tailwind 미지원 |
| 가상 요소 (`::after`) | **커스텀 CSS** | `.disconnected-card` 워터마크 등 복합 선택자 |
| 전역 입력 리셋 | **커스텀 CSS** | `input:not(...)` 동적 생성 요소에 `!important` 강제 적용 |
| 세부 레이아웃·간격·색상 | **TailwindCSS** | `grid-cols-[...]`, `gap-2`, `text-xs` 등 미세 조정 |
| 버튼 개별 스타일 | **TailwindCSS** | 인라인 유틸리티 조합 (Go-, STOP 등) |
| 반응형 전환 | **TailwindCSS** | `lg:flex-row`, `lg:hidden` 등 브레이크포인트 |

##### Tailwind 대체 불가 영역 (커스텀 CSS 필수)

| 클래스 | 대체 불가 사유 |
|--------|---------------|
| `.disconnected-card::after` | `content` + 복합 `transform`(회전+이동) 가상 요소 |
| `@keyframes move-stripes` | 커스텀 대각선 스트라이프 애니메이션 |
| `.led.on/warn/error` | 색상 지정 `box-shadow` 발광(glow) 효과 |
| `.card.collapsed > *:not(:first-child)` | 복합 CSS 선택자 |
| `input:not([type="checkbox"])...` | 전역 셀렉터 + `!important` 강제 |

##### 신규 요소 추가 시 판단 기준 (Decision Guide)

```
신규 UI 요소 추가 시:
  ├─ JS에서 상태 토글이 필요한가? → ✅ 커스텀 CSS 클래스 정의
  ├─ @keyframes 또는 ::after 가 필요한가? → ✅ 커스텀 CSS
  ├─ 3곳 이상 동일 패턴 반복 사용인가? → ✅ 커스텀 CSS 클래스로 추출
  └─ 위 모두 아닌 단순 레이아웃/색상? → ✅ TailwindCSS 유틸리티
```


### 1.5 반응형 브레이크포인트 (Responsive Breakpoints)
TailwindCSS 기본 브레이크포인트를 따릅니다.

| 접두사 | 최소 너비 | 대상 기기 | 주요 적용 |
|--------|----------|----------|----------|
| (없음) | 0px | 모바일 | 기본 스타일 (1열 레이아웃) |
| `sm:` | 640px | 태블릿 소형 | — |
| `md:` | 768px | 태블릿 | 헤더 `flex-row` 전환 |
| `lg:` | 1024px | 데스크탑 | 2열 레이아웃, 모달 5열 그리드 |
| `xl:` | 1280px | 대형 모니터 | — |

---

## 2. 화면 분할 및 패널 헤더 (Panels & Headers)
*제어 패널(Drive, Homing, Calibration 등)의 상단 제목 행에 적용하는 규격입니다.*

* **컨테이너 부분 (Container div)**: 
  * 적용 클래스:
    * `bg-slate-700/50` — 배경: 회백색 반투명
    * `px-2 py-1` — 내부 여백 (좌우 8px, 상하 4px)
    * `border-b border-slate-700` — 하단 테두리
    * `flex justify-between items-center` — 수평 정렬 (양끝 배치, 수직 중앙)
    * `group/header` — 자식 요소 호버 그룹

* **타이틀 텍스트 부분 (Title span)**:
  * 적용 클래스:
    * `text-sm` — 폰트 크기 (14px)
    * `font-black` — 최대 굵기 (900)
    * `text-slate-300` — 밝은 회색 텍스트
    * `uppercase` — 대문자 변환
    * `tracking-widest` — 넓은 글자 간격 (0.1em)

* **서브 패널 내부 행 (Sub-panel Rows)**:
  * 항목 구분 테두리: `border-b border-slate-700/30`
  * 첫 번째 행 등에 불필요한 강조 배경색(`bg-slate-700/50` 등)은 지양하고, 모든 행의 배경을 기본 투명(또는 부모 요소 배경)으로 통일하여 연속성 유지

### 2.1 반응형 헤더 줄바꿈 규칙 (Responsive Header Wrapping)
전역 헤더 또는 각 카드/패널의 헤더에 **제목과 버튼·드롭다운·상태 표시** 등이 같은 행에 배치될 경우, 작은 화면(모바일)에서 내용이 잘리거나 넘침(overflow)이 발생합니다. 이를 방지하기 위해 다음 규칙을 적용합니다.

#### 원칙
| 화면 크기 | 동작 | 적용 클래스 |
|----------|------|------------|
| **데스크탑** (≥ 1024px) | 제목 + 컨트롤들이 **1행** 수평 배치 | `lg:flex-row lg:items-center` |
| **모바일/태블릿** (< 1024px) | 제목이 **1행**, 컨트롤들이 **2행**으로 분리 | `flex-col items-start` |

#### 적용 방법
헤더 컨테이너에 `flex flex-col lg:flex-row` 패턴을 사용합니다.

```html
<!-- 패널 헤더: 모바일=2행, 데스크탑=1행 -->
<div class="flex flex-col lg:flex-row justify-between lg:items-center gap-2 mb-2">
    <!-- 1행: 제목 (항상 존재) -->
    <div class="flex items-center justify-between">
        <span class="text-sm font-black text-slate-300 uppercase tracking-widest whitespace-nowrap">
            PANEL TITLE
        </span>
        <!-- 모바일 전용 접기 버튼 (데스크탑에서는 숨김) -->
        <button class="collapse-btn lg:hidden text-slate-500 hover:text-white">▼</button>
    </div>

    <!-- 2행: 컨트롤 그룹 (모바일에서 아래로 이동) -->
    <div class="flex flex-wrap items-center gap-2">
        <select class="bg-slate-900 border border-slate-600 rounded text-xs py-0.5 px-2">
            <option>Option</option>
        </select>
        <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-700 text-slate-400 border border-slate-600">
            READY
        </span>
        <!-- 데스크탑 전용 접기 버튼 (모바일에서는 숨김) -->
        <button class="collapse-btn hidden lg:block text-slate-500 hover:text-white">▼</button>
    </div>
</div>
```

#### 핵심 클래스 설명
* `flex flex-col` — 기본(모바일): 세로 방향, 자식 요소가 위아래로 쌓임
* `lg:flex-row` — 데스크탑: 가로 방향, 자식 요소가 좌우로 배치
* `lg:items-center` — 데스크탑에서만 수직 중앙 정렬
* `gap-2` — 행 간격 8px (모바일에서 1행과 2행 사이 여백)
* `flex-wrap` — 2행 내 컨트롤들이 공간 부족 시 자동 줄바꿈
* `whitespace-nowrap` — 제목 텍스트 줄바꿈 방지
* `lg:hidden` / `hidden lg:block` — 접기 버튼을 화면 크기별로 위치 전환

#### 적용 대상
| 대상 | 1행 (제목) | 2행 (컨트롤) |
|------|-----------|-------------|
| **전역 헤더** | "Kohzu 6-Axis Dashboard" | Session 드롭다운, SAVE, 연결 배지, ABORT ALL |
| **Readback Timeline** | "Readback Status Timeline" | Interval 드롭다운, 축 범례 배지, 접기 버튼 |
| **2D Area Scan** | "2D Area Scan" | 진행률 바, 상태 배지, 접기 버튼 |
| **Sequence Mode** | "Sequence Mode" | 세션 드롭다운, + STEP 버튼, 상태 배지, 접기 버튼 |

---

## 3. 버튼 (Buttons)
버튼은 목적과 역할에 따라 크기, 폰트, 상태별 색상을 엄격히 규격화합니다.

* **공통 사이즈 규칙**:
  * **최대 너비**: `max-w-[80px]` (입력 필드와 동일한 80px 이하)
  * **높이 고정**: `h-[22px]` (입력 필드와 동일한 22px)
  * **그리드 확장**: 버튼이 그리드(grid) 셀 내에 배치되고 최대 너비보다 작을 경우 `w-full`을 적용하여 셀 너비에 맞춰 자동 확장합니다. 이때 실제 렌더링 너비는 그리드 열 크기(`1fr` 등)에 의해 결정되므로, 80px 이하의 컴팩트한 셀 안에서 균등하게 배치됩니다.
  * **예외**: 헤더 영역의 글로벌 버튼(ABORT ALL, SAVE 등)은 텍스트 길이에 따라 `px-3` 등으로 자연 확장을 허용합니다.

### 3.1 일반 제어 버튼 (Standard Button)
조작을 수행하는 대부분의 일반적인 버튼(예: JOG, TWR, TWF, 홈 복귀 등)에 적용합니다.

* **표준 클래스**: 
  * `w-full` — 그리드 셀 전체 활용
  * `max-w-[80px]` — 최대 너비 80px 제한
  * `h-[22px]` — 높이 22px 고정
  * `text-xs` — 폰트 크기 (12px)
  * `font-bold` — 폰트 두께 (700)
  * `py-0 px-2` — 상하 0, 좌우 8px 패딩
  * `rounded` — 모서리 둥금 (4px)
  * `border border-slate-600` — 테두리 (슬레이트 600)
  * `bg-slate-700` — 기본 배경색
  * `hover:bg-slate-600` — 호버 시 배경색
  * `text-slate-200` — 밝은 텍스트 색상
  * `transition-colors` — 색상 전환 애니메이션
  * `uppercase` — 대문자 변환
  * `shadow-sm` — 미세 그림자

### 3.2 활성 상태 버튼 (Active / Selected State)
USE, SET 모드 또는 특정 상태 피드백을 사용자에게 명확히 전달해야 할 때(JS 렌더러 기반) 상태 클래스를 동적으로 주입합니다.

* **활성 덮어쓰기 요소**:
  * `!bg-green-700` — 배경: 진한 초록색 (강제 우선)
  * `!border-green-600` — 테두리: 초록색 (강제 우선)
  * `!text-white` — 텍스트: 흰색 (강제 우선)
* **설명**: 모터가 해당 모드로 진입하였거나 선택된 경우, 기존 Slate 테마를 지우고 **진한 초록색**으로 눈에 띄게 강조합니다.

### 3.3 비상/정지 기능 버튼 (Emergency / Stop)
즉각적인 시각적 인지가 필요하고, 잘못 클릭되는 것을 방지하기 위해 특별한 테마를 부여합니다.

* **정지 버튼 (STOP - Warning/Alert)**:
  * 머스타드/진한 노란색 (주로 개별 조작 레이아웃 내 정지 버튼)
  * 적용 클래스:
    * `w-full max-w-[80px]` — 너비: 그리드 셀 활용, 최대 80px
    * `h-[22px]` — 높이: 22px 고정
    * `text-[10px]` — 폰트 크기: 10px (일반보다 작음)
    * `font-black` — 폰트 두께: 최대 (900)
    * `py-0 px-2` — 상하 0, 좌우 8px 패딩
    * `rounded` — 모서리 둥금
    * `border border-yellow-700` — 테두리: 진한 노란색
    * `bg-yellow-600` — 기본 배경: 머스타드 노랑
    * `hover:bg-yellow-500` — 호버 시: 밝은 노랑
    * `text-slate-900` — 텍스트: 어두운 색 (대비 극대화)
    * `transition-colors` — 색상 전환 애니메이션
    * `shadow-sm` — 미세 그림자
    * `uppercase text-center` — 대문자, 중앙 정렬

* **위험 상태 제어 보조 (Red Theme)**:
  * `bg-red-700` — 기본 배경: 진한 빨강
  * `hover:bg-red-800` — 호버 시: 더 진한 빨강
  * `text-red-500` — 텍스트: 빨간색
  * `border-red-700` — 테두리: 진한 빨강

### 3.4 주요 동작 버튼 (Primary Action Button)
UI 상에서 **데이터 추가·생성** 등 사용자의 적극적인 행동을 유도하는 강조 버튼입니다.
대표 예시로 Sequence Mode의 `+ STEP` 버튼이 있습니다.

* **CSS 클래스 정의** (커스텀 CSS):
  ```css
  .btn-primary {
      background-color: #2563eb;    /* blue-600 — 강조 블루 */
      color: white;
  }
  .btn-primary:hover {
      background-color: #1d4ed8;    /* blue-700 — 진한 블루 */
  }
  ```

* **인라인 보조 클래스 (TailwindCSS)**:
  * `text-[10px]` — 폰트 크기: 10px
  * `py-1 px-1.5` — 상하 4px, 좌우 6px 패딩
  * `whitespace-nowrap` — 텍스트 줄바꿈 방지

* **디자인 의도**: 사용자에게 **"이곳을 눌러 새 항목을 추가하세요"** 라고 권유하는 Positive Action(긍정적 액션) 버튼으로, 주변의 중립 톤(Slate) 버튼들과 색상 대비를 통해 눈에 띄도록 설계되었습니다.

#### 3.4.1 Primary vs Standard 버튼 비교

| 구분 | Primary (`+STEP` 등) | Standard (`Go-`, `<`, `>` 등) |
|------|----------------------|-------------------------------|
| **목적** | UI 데이터 추가 (Positive Action) | 하드웨어 직접 제어 (Control Action) |
| **배경색** | `#2563eb` (blue-600) | `bg-slate-700` (`#334155`) |
| **호버색** | `#1d4ed8` (blue-700) | `hover:bg-slate-600` (`#475569`) |
| **테두리** | 없음 (배경색+그림자로 구분) | `border-slate-600` (`#475569`) |
| **텍스트색** | `white` | `text-slate-200` (`#e2e8f0`) |
| **대문자 변환** | 적용 안 됨 | `uppercase` 적용 |
| **스타일 방식** | `.btn-primary` 커스텀 CSS | Tailwind 유틸리티 클래스 조합 |

---

## 4. 데이터 디스플레이 및 입력 필드 (Data Display & Input Fields)
모터 값 설정, 보정 계수 및 각종 PV 값을 출력(읽기 전용)하거나 직접 입력(수정 가능)받는 구역입니다. 통일된 룩앤필 및 정렬을 위해 **뷰어 라벨(Data Display)**과 **입력 폼(Input Field)**은 다음과 같은 공통 디자인 속성을 적용합니다.

* **공통 규칙 (뷰어 라벨 & 입력 폼 공통)**:
  * **사이즈 고정**: `w-[80px]` (너비) 및 `h-[22px]` (높이) 고정
  * **텍스트 우측 여백 보정**: `pr-3` (HTML Input 컨트롤 기본 Spin-button 버튼과의 정렬 오차 방지)
  * **일반 텍스트 속성**: `text-xs` (폰트 크기), `text-right` (우측 정렬)
  * **기본 테마 색상**: `bg-slate-900` / `#0f172a` (배경 색상), `border-slate-700` (테두리 색상)
  * **내부 패딩 규칙**: `px-1.5` (좌우 여백), `py-0.5` (상하 여백)

* **뷰어 라벨 (Data Display - 읽기 전용) 전용 속성**:
  * **폰트 색상**: 그린 포인트 색상 **`text-green-400`** 적용
  * 설명: 사용자 입력 요소와 헷갈리지 않도록 고유의 포인트 컬러(Green)를 유지합니다.

* **입력 폼 (Input Field - 직접 입력 가능) 전용 속성**:
  * **폰트 색상**: 직관적인 하얀색 **`text-white`** (혹은 밝은 회색 `text-slate-200`) 적용
  * 포커스(Focus) 시 `border-blue-500` 형태의 파란색 선 활성화 디자인 연계

---

## 5. 텍스트 라벨 (Text Labels & Indicators)
항목명 기재 영역과, 입력란은 아니지만 그리드 자리를 차지하는 플레이스홀더 영역입니다.

* **항목명 라벨 (Title Label)**:
  * 적용 클래스:
    * `text-xs` — 폰트 크기 (12px)
    * `text-slate-400` — 중간 밝기 회색 (또는 `text-slate-500`)
    * `font-bold` — 폰트 두께 (700)
  * 정렬 방식: 기본 좌측 자간 정렬

* **보조 Indicator / 플레이스홀더 (Placeholder)**:
  * 적용 클래스:
    * `text-right` — 우측 정렬
    * `text-xs` — 폰트 크기 (12px)
    * `text-yellow-500/50` — 반투명 노란색 텍스트
    * `pr-1` — 우측 여백 (4px)
    * `font-mono` — 고정폭 폰트
  * 텍스트: `-` (하이픈 사용)
  * 용도: 입력창이 없는 열(Row/Col)에 배치하여 시각적으로 빈 공간이어도 그리드 형태가 무너지지 않도록 지지대 역할을 수행합니다.

---

## 6. LED 상태 표시등 (LED Indicators)
모터의 구동 상태나 에러 상황을 가장 직관적으로 보여주는 작고 둥근 마커(`.led`) 컴포넌트의 다이나믹 색상 규격입니다. 각 상황에 알맞은 CSS 보조 클래스(`on`, `warn`, `error`)를 사용하여 점등 효과를 부여합니다.

* **완료 및 정상 상태 (Done / Safe)**:
  * 클래스: `on`
  * 시각 특성: **초록색 (Green)** 베이스, 시각적 안정감 및 정상 작동/도달 완료를 알림.
* **이동 및 경고 상태 (Moving / Warn)**:
  * 클래스: `warn`
  * 시각 특성: **파란색/노란색 (Blue/Yellow)** 혼합, 현재 모터가 조작에 의해 이동 중이거나 일시적인 주의가 필요할 때 사용.
* **에러 및 한계 도달 (Problem / Limit Error)**:
  * 클래스: `error`
  * 시각 특성: **강렬한 빨간색 (Red)**, 한계 스위치(Hi/Lo Limit)를 치거나 드라이버에 치명적 결함(Problem)이 발생했음을 경고.

---

## 7. 레이아웃과 그리드 (Grid Alignments)
여러 개의 열을 나열할 때에는 `<div class="grid ...">` 를 통해 가로 길이를 명확히 배분하여 컴포넌트 간 들쭉날쭉한 문제를 방지합니다.

* **표준 그리드 비율 권장 구성 (모터 제어 5열 예시)**:
  * 적용 클래스:
    * `grid` — CSS Grid 레이아웃 활성화
    * `grid-cols-[80px_1fr_1fr_1fr_30px]` — 5열 정의: 라벨 80px / 입력×3 / LED 30px
    * `gap-2` — 셀 간격 8px
    * `items-center` — 수직 중앙 정렬
  * **배치 형태**: `[라벨 80px] - [입력 1] - [입력 2] - [입력 3] - [상태 LED 30px]`

* **세부 설정 패널 그리드 구성 (2열 및 3열 표준)**:
  * **라벨 + 단일 입력 (2열)**:
    * `grid grid-cols-[80px_1fr]` — 2열: 라벨 80px / 입력 자동
    * `gap-2 items-center` — 간격 8px, 수직 중앙
    * `px-2 py-1` — 행 내부 여백
    * `border-b border-slate-700/30` — 하단 구분선
  * **라벨 + 조작 버튼 다수 (3열/4열)**:
    * `grid grid-cols-[80px_1fr_1fr]` — 3열: 라벨 80px / 버튼×2
    * `grid grid-cols-[80px_1fr_1fr_1fr_1fr]` — 5열: 라벨 80px / 버튼×4
  * **원칙**: 좌측 라벨 크기(`80px`)를 고정하고 나머지 공간을 `1fr` 비율로 균등 분배하여 좌우 정렬 밸런스를 유지합니다.

---


## 8. 카드 컴포넌트 (Card Components)
페이지를 구성하는 기본 블록 단위입니다. 모든 패널과 컨트롤 그룹은 카드 형태로 감싸집니다.

### 8.1 기본 카드 (.card)
```css
.card {
    background-color: #1e293b;    /* bg-slate-800 */
    border: 1px solid #334155;    /* border-slate-700 */
    border-radius: 0.75rem;       /* rounded-xl (12px) */
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1),
                0 2px 4px -1px rgba(0,0,0,0.06);
}
```

### 8.2 반응형 카드 (.card-responsive)
모터 개별 제어 카드용. 좌측 열에 배치됩니다.
* `width: 100%` — 부모 컨테이너 전체 사용
* `min-width: 0` — flex/grid 축소 허용
* `max-width: 510px` — 최대 너비 제한
* `margin: 0 auto` — 수평 중앙 정렬

### 8.3 와이드 카드 (.card-wide-responsive)
우측 열의 차트/스캔/시퀀스/메모장 패널용.
* `max-width: 700px` — 카드보다 넓은 최대 너비

### 8.4 카드 헤더 (.card-header)
```css
.card-header {
    padding: 0.5rem 0.75rem;       /* py-2 px-3 */
    border-bottom: 1px solid #334155;
    display: flex;
    align-items: center;
    gap: 0.5rem;                   /* gap-2 */
    background-color: rgba(51, 65, 85, 0.5); /* bg-slate-700/50 */
}
```

### 8.5 카드 호버 효과 (.axis-card)
```css
.axis-card:hover {
    transform: translateY(-2px);   /* 위로 2px 부상 */
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
    border-color: #3b82f6;         /* 파란색 테두리 강조 */
}
```

---

## 9. 상태 배지 (Status Badges)
장비의 현재 상태를 텍스트+색상으로 요약 표시하는 소형 라벨입니다.

| 상태 | 배경색 | 텍스트색 | 사용처 |
|------|--------|----------|--------|
| **IDLE** | `bg-slate-700` | `text-slate-400` | 모터 대기 중 |
| **MOVING** | `bg-blue-600 animate-pulse` | `text-white` | 모터 이동 중 (깜빡임) |
| **READY** | `bg-slate-700` | `text-slate-400` | 스캔/시퀀스 대기 |
| **SCANNING** | `bg-blue-600` | `text-white` | 스캔 실행 중 |
| **DONE** | `bg-green-700` | `text-white` | 작업 완료 |
| **Connected** | `bg-green-500` (LED) | — | 서버 연결 정상 |
| **Disconnected** | `bg-red-500` (LED) | — | 서버 연결 끊김 |

* **공통 클래스**: `px-2 py-0.5 rounded text-[10px] font-bold border border-slate-600`
* **모델명 배지**: `ml-4 px-2 py-0.5 rounded text-xs bg-slate-700 text-slate-300`

---

## 10. 모달 및 오버레이 (Modal & Overlay)
상세 제어 화면 등 전체 화면을 덮는 팝업 구조의 표준 규격입니다.

### 10.1 오버레이 (.modal-overlay)
```css
.modal-overlay {
    background-color: rgba(0, 0, 0, 0.75);  /* 75% 불투명 검정 */
    backdrop-filter: blur(4px);               /* 배경 블러 */
}
```

### 10.2 모달 컨테이너
* **위치**: `fixed inset-0 z-[100]` (전체 화면, 최상위 레이어)
* **정렬**: `flex justify-center items-start pt-10 pb-10` (상단 여백 40px)
* **스크롤**: `overflow-y-auto` (내용 넘칠 시 스크롤)

### 10.3 모달 본체
* **배경**: `bg-slate-900`
* **테두리**: `border border-slate-700 rounded-xl`
* **최대 너비**: `max-w-7xl` (80rem = 1280px)
* **그림자**: `shadow-2xl`

### 10.4 모달 헤더
* **배경**: `bg-slate-800 rounded-t-xl`
* **고정**: `sticky top-0 z-10` (스크롤 시에도 상단 고정)
* **닫기 버튼**: 우상단 원형 버튼 (`rounded-full p-1 bg-slate-700 hover:bg-slate-600`)

---

## 11. 접이식 패널 (Collapsible Panels)
우측 열의 패널들은 접기/펼치기를 지원하여 화면 공간을 효율적으로 사용합니다.

### 11.1 접기 버튼 (.collapse-btn)
* **아이콘**: 하향 화살표(▼) SVG, `h-4 w-4`
* **색상**: `text-slate-500 hover:text-white transition-colors`
* **회전**: 접힌 상태에서 180° 회전 (`transform: rotate(-180deg)`)

### 11.2 접힌 상태 (.card.collapsed)
```css
.card.collapsed {
    min-height: 0 !important;
    height: auto !important;
    padding-bottom: 0.5rem !important;
}
/* 첫 번째 자식(헤더) 외 모든 요소 숨김 */
.card.collapsed > *:not(:first-child) {
    display: none !important;
}
/* 화살표 회전 */
.card.collapsed .collapse-btn svg {
    transform: rotate(-180deg);
}
```

### 11.3 미연결 카드 (.disconnected-card)
```css
.disconnected-card {
    opacity: 0.6;                  /* 반투명 */
    filter: grayscale(1);          /* 회색조 */
    position: relative;
}
.disconnected-card::after {
    content: "DISCONNECTED";       /* 워터마크 텍스트 */
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%) rotate(-15deg);
    font-weight: 900; font-size: 1.5rem;
    color: rgba(239, 68, 68, 0.4); /* 반투명 빨강 */
    border: 4px solid rgba(239, 68, 68, 0.3);
    padding: 0.5rem 1rem;
    pointer-events: none; z-index: 10;
}
.disconnected-card .card-body {
    pointer-events: none;          /* 조작 차단 */
}
```

---

## 12. 퀵스타트 코드 스니펫 (Quick Start Snippets)
새 프로젝트에서 본 가이드를 즉시 적용하기 위한 복사/붙여넣기용 HTML 예제입니다.

### 12.1 패널 헤더 + 2열 입력 행
```html
<!-- 패널 헤더 -->
<div class="bg-slate-700/50 px-2 py-1 border-b border-slate-700 flex justify-between items-center">
    <span class="text-sm font-black text-slate-300 uppercase tracking-widest">DRIVE</span>
</div>

<!-- 2열 입력 행 (라벨 80px + 입력) -->
<div class="grid grid-cols-[80px_1fr] gap-2 items-center px-2 py-1 border-b border-slate-700/30">
    <span class="text-xs text-slate-400 font-bold">VELO</span>
    <input type="number" class="w-[80px] h-[22px] bg-slate-900 border border-slate-700 rounded px-1.5 text-xs text-right text-white outline-none focus:border-blue-500">
</div>
```

### 12.2 표준 버튼 그룹 (3열)
```html
<div class="grid grid-cols-[80px_1fr_1fr] gap-2 items-center px-2 py-1">
    <span class="text-xs text-slate-400 font-bold">MODE</span>
    <button class="w-full max-w-[80px] h-[22px] text-xs font-bold py-0 px-2 rounded border border-slate-600 bg-slate-700 hover:bg-slate-600 text-slate-200 transition-colors uppercase shadow-sm">USE</button>
    <button class="w-full max-w-[80px] h-[22px] text-xs font-bold py-0 px-2 rounded border border-slate-600 bg-slate-700 hover:bg-slate-600 text-slate-200 transition-colors uppercase shadow-sm">SET</button>
</div>
```

### 12.3 LED 상태 표시등
```html
<!-- 기본(Off) -->
<div class="led"></div>

<!-- 정상(On) -->
<div class="led on"></div>

<!-- 경고(Warn) -->
<div class="led warn"></div>

<!-- 에러(Error) -->
<div class="led error"></div>

<style>
.led {
    width: 1rem; height: 1rem;
    border-radius: 50%;
    background-color: #334155;
    border: 1px solid #475569;
    transition: background-color 0.3s;
}
.led.on    { background-color: #22c55e; box-shadow: 0 0 8px #22c55e; border-color: #16a34a; }
.led.warn  { background-color: #eab308; box-shadow: 0 0 8px #eab308; border-color: #ca8a04; }
.led.error { background-color: #ef4444; box-shadow: 0 0 8px #ef4444; border-color: #dc2626; }
</style>
```

### 12.4 데이터 표시 (읽기 전용) + 입력 필드 비교
```html
<!-- 읽기 전용 (Data Display) — 초록색 텍스트 -->
<span class="w-[80px] h-[22px] bg-slate-900 border border-slate-700 rounded px-1.5 pr-3 text-xs text-right text-green-400 inline-block leading-[22px]">12.345</span>

<!-- 입력 가능 (Input Field) — 흰색 텍스트 -->
<input type="number" class="w-[80px] h-[22px] bg-slate-900 border border-slate-700 rounded px-1.5 pr-3 text-xs text-right text-white outline-none focus:border-blue-500" value="10.000">
```

### 12.5 상태 배지
```html
<!-- IDLE 상태 -->
<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-700 text-slate-400 border border-slate-600">IDLE</span>

<!-- MOVING 상태 (깜빡임) -->
<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-600 text-white border border-blue-500 animate-pulse">MOVING</span>

<!-- STOP 버튼 -->
<button class="w-full max-w-[80px] h-[22px] text-[10px] font-black py-0 px-2 rounded border border-yellow-700 bg-yellow-600 hover:bg-yellow-500 text-slate-900 transition-colors shadow-sm uppercase text-center">STOP</button>
```

---
---

# 부록 A. UI 명칭 표준안 (UI Nomenclature Reference)

> 이 부록은 `dashboard.html` 및 `motor_popup.html`의 구성 요소 명칭을 참조 목적으로 정리한 것입니다.
> 화면 수정 요청 시 이 명칭을 활용하면 AI 도구 및 개발자 간의 소통이 원활해집니다.
>
> **범례**: `[대괄호]` = 구조 블록, **(볼드)** = PV 필드명 또는 ID, `코드폰트` = CSS 클래스 또는 HTML ID

## A.1 메인 대시보드 구조 (dashboard.html)

대시보드는 **2열(Columns) 레이아웃**으로 구성되며, 좌측 열에 모터 카드들, 우측 열에 차트·스캔·시퀀스·메모장 패널이 배치된다.

### A.1.1 [Header] 최상단 헤더
전체 화면 상단에 고정(`sticky`)되는 글로벌 네비게이션 바.

- **Title 라벨**: "Kohzu 6-Axis Dashboard" (`text-sm md:text-xl font-bold`)
- **Session 관리 영역**
  - 세션 드롭다운 (`#session-select`): 서버 저장 세션 목록 선택/로드
  - SAVE 버튼: 현재 세션을 서버에 저장 (`saveSessionToServer()`)
- **연결 상태 배지** (`#conn-status`): Connected (초록) / Disconnected (빨강) LED + 텍스트
- **ABORT ALL 버튼**: 전체 축 비상정지 (`app.abortAll()`), 노란색 경고 테마
- **반응형 헤더**: 모바일에서 `flex-col`, 데스크탑에서 `flex-row` 전환 (`md:flex-row`)

### A.1.2 [Left Column] 모터 카드 그리드
좌측 열에 6장의 Axis Card가 `flex-wrap` 레이아웃으로 배치된다.

#### [Axis Card] 모터 개별 제어 카드
각 축(m1~m6)에 대응하는 독립적 제어 카드. 미연결 시 `disconnected-card` 클래스 적용.

- **카드 헤더 (Card Header)** — `.card-header`
  - 축 타이틀 라벨 ("Motor 1" 등)
  - 모델명 배지 (JSON 스테이지 설정 시 표시, 예: "XA07A-L202")
  - 연결 상태 인디케이터 (둥근 `.led`)
  - **팝업 아이콘 버튼** (⧉): 모달 열기 전용 버튼 (`openModal(i)`)
- **데이터 열 헤더 (Column Headers)** — 4열: Desc / User / Dial / Limit
- **1행: 상한 리밋 (Hi limit)**: **HLM** (입력) / **DHLM** (뷰어) / **HLS** (LED)
- **2행: 현재 위치 (Readback)**: **RBV** / **DRBV** / **EGU**
- **3행: 목표 이동 제어 (Drive)**: **VAL** (입력) / **DVAL** (뷰어) / **DMOV** (LED)
- **4행: 하한 리밋 (Lo limit)**: **LLM** (입력) / **DLLM** (뷰어) / **LLS** (LED)
- **5행: 미세 이동 조작 (Tweak)**: Go- / < / **TWV** / > / Go+ — 5열 대칭
- **하단 상태창**: **DTYP** / IDLE·MOVING 배지 / **STOP** 버튼

### A.1.3 [Right Column] 분석·운용 패널
우측 열에 배치되는 4개의 접이식 패널.

- **[Readback Status Timeline]**: Chart.js 3분할 시계열 차트 (Linear / Vertical / Rotation)
- **[2D Area Scan]**: Raster/Fermat 탭 + XY Plot + 축 선택 + 실행/정지
- **[Sequence Mode]**: 세션 스텝 테이블 + 반복 설정 + 실행/정지
- **[Notepad]**: 자유 메모 (localStorage 자동 저장)

### A.1.4 [Detail Modal] 모터 상세 제어 모달
Axis Card ⧉ 클릭 시. `motor_popup.html`을 `fetch()`로 동적 로드.

## A.2 모터 상세 제어 모달 (motor_popup.html)

PV 접두사(`${pvPrefix}`)를 런타임 치환. `lg:grid-cols-5` — 좌3열(Control) : 우2열(Status).

### A.2.1 [Left Card] 제어 및 상세 설정 — `lg:col-span-3`

| 패널 | 주요 PV / 요소 |
|------|---------------|
| **Drive** | HLM, DHLM, HLS, RBV, DRBV, VAL, DVAL, DMOV, LLM, DLLM, LLS, RLV, TWV, SPMG |
| **Calibration** | USE/SET 버튼, OFF, FOFF, DIR, SYNC |
| **Dynamics** | VMAX, VELO, VBAS, ACCL |
| **Backlash** | BDST, BVEL, BACC, FRAC |
| **Jog Control** | JVEL, JAR, JogR, JogF |
| **Homing** | HVEL, HACC, HDCC, HomingMethod, HomR, HomF |
| **Servo (PID)** | PCOF, ICOF, DCOF |

### A.2.2 [Right Card] 상태 열람 및 파라미터 — `lg:col-span-2`

| 패널 | 주요 PV / 요소 |
|------|---------------|
| **STATUS** | STAT, MOVN, ATHM, MIP, DIFF, DTYP, CARD, STUP, FLNK, CNEN |
| **MSTA Bits** | Done(1), Problem(9), Moving(10), HiLimit(2), LoLimit(13), Homing(14) |
| **Resolution & Setup** | MRES, ERES, RRES, RDBD, RTRY, UEIP, URIP, DLY, PREC, PREM, POST |
| **Stage Information** | Stage Select 드롭다운, Mechanical Specs, Driver Settings |
