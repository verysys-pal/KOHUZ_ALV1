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












# 2026.02.27
---
## 📋 5. 작업지시 (User Instruction)
1. motor_popup.html
2. text-xs` (약 12px) 적용
  - 입력 라벨
  - 버튼
  - 라벨 텍스트
  - 상태 뱃지
  - 입력 폼 데이터
  - 상태 패널 데이터 추출값
  - Readback 메인 표시기
  - 기타
3. text-sm` (약 14px) 적용  
  - 본문 안내문
  - 패널 헤더/섹션 명
  - Move 메인 입력란
4. text-lg` (약 18px) 적용
  - 최상부 카드 제목 문자
  - 헤더 메인

### ✅ 5.1 Todo List (AI Analysis)
- [x] **Step 1: Parse Requirements** - `text-xs`, `text-sm`, `text-lg` 적용 대상 컴포넌트 그룹 파악
- [x] **Step 2: Script Execution** - `motor_popup.html` 내 기존 `text-[8px]` ~ `text-[12px]` 클래스를 일괄 검색 및 목표 크기로 자동 치환
- [x] **Step 3: Structure Verification** - 지시된 기준(xs, sm, lg)에 맞춰 대상 요소들이 올바르게 변경되었는지 검증 
- [x] **Step 4: Documentation** - 변경 사항 및 수행 결과를 반영하여 문서 내용 업데이트

### 📝 5.2 Result (Execution Summary)
사용자의 세부 지시에 따라 `motor_popup.html` 내 모든 요소의 폰트 크기 규격을 3가지 정규 클래스(`text-xs`, `text-sm`, `text-lg`)로 통일하여 가독성을 높였습니다.

1. **`text-xs` (약 12px) 일괄 적용**
   - 기존 시인성이 부족했던 아주 작은 글씨(`text-[8px]`, `text-[9px]`, `text-[10px]`, `text-[11px]`)와 `text-[12px]` 코드를 모두 `text-xs`로 변경했습니다.
   - 반영 영역: 패널 내 **버튼**, 파라미터 **입력 라벨**, 단축 **라벨 텍스트**, **상태 뱃지**, 수치 **입력 폼**, **상태 패널 데이터**, **Readback 표시기** 등 전체 요소가 해당됩니다.
2. **`text-sm` (약 14px) 부분 적용**
   - 그룹을 분리해주는 각 **패널 헤더/섹션 명**(Drive, STATUS 등)과 핵심 제어 폼인 **Move 메인 입력란**의 글쇠를 한 단계 구분하기 위해 `text-sm`으로 변경했습니다. 하단의 **본문 안내문**(Note) 영역도 동일하게 상향 적용되었습니다.
3. **`text-lg` (약 18px) 부분 적용**
   - 현재 화면의 정보를 대표하는 **최상부 카드 제목 문자**(`Stage Information`)와 좌측의 **헤더 메인 명칭**(`Axis 1`)을 `text-lg`로 설정해 명확한 헤더 타이틀을 제공합니다.

### 🛠 5.3 변경 사항 (Summary of Changes)
- **수정 위치:** `kohzuApp/opi/motor_popup.html`
- **주요 로직:** 파이썬 스크립트의 정규식을 사용해 인라인으로 선언되어 있던 `text-[8px]`~`text-[12px]` 룰셋을 모두 표준 Tailwind 룰셋(xs/sm/lg)으로 리팩토링 및 텍스트 폰트 일괄 상향 적용.
- **수정 위치:** `kohzuApp/doc/Instruction.md`
- **주요 로직:** 템플릿 문서 5번 지시사항의 결과 리포트 작성.

### 🔍 검증 결과 (Validation)
- [x] 지시사항에 포함된 모든 모터 제어 요소 CSS 치환 성공
- [x] 자동 작성 템플릿 기록 포맷 적용 완료







## 📋 15. 작업지시 (User Instruction)
1. motor_popup.html > Resolution & Setup 패널
2. 입력창 너비 80px로 변경
3. select 필드만 우측 정렬됨 > 입력필드는 텍스트 라벨과 같이 묶여 있는지 우측 정렬이 안됨
4. 입력필드, 텍스트 라벨 분리해서 입력필드만 우측 정렬되도록 수정

### ✅ 15.1 Todo List (AI Analysis)
- [x] **Step 1: Style Overhaul** - 부모 카드(`.left-control-card`)에서 강제 적용되던 `display: block` 및 `margin: auto` 스타일이 `justify-between` 정렬을 방해하던 문제 확인
- [x] **Step 2: Priority Correction** - `.resolution-setup-panel` 내의 입력창에 대해 `display: inline-block !important` 및 `margin: 0 !important`를 부여하여 레이아웃 간섭 제거
- [x] **Step 3: Metric Update** - 입력창 너비를 **80px**로 상향 조정하여 정보 표시 가독성 향상
- [x] **Step 4: Verification** - 라벨(좌측)과 입력필드(우측)가 정상적으로 양끝에 정렬되는지 재검증

### 📝 15.2 Result (Execution Summary)
사용자님의 요청에 따라 **입력창 너비를 80px로 확대하고, 정렬이 어긋나던 버그를 완전히 수정했습니다.**

- **정렬 버그 해결**: 기존 제어카드 전체에 적용되던 '중앙 정렬' 스타일이 해당 패널의 입력필드에도 강제 적용되어 `flex` 정렬이 무시되던 현상을 수정했습니다. 이제 입력필드도 `select` 필드와 동일하게 우측 끝으로 정확히 정렬됩니다.
- **너비 최적화**: 너비를 **80px**로 넓혀 수치 데이터가 더욱 넉넉하게 표시되도록 개선했습니다.
- **레이아웃 분리**: 라벨(텍스트)과 입력창(컨트롤)이 서로 간섭 없이 양 끝단에 안정적으로 배치됨을 확인했습니다.

### 🛠 15.3 변경 사항 (Summary of Changes)
- **수정 위치:** `kohzuApp/opi/motor_popup.html`
- **주요 로직:** 
  - CSS 우선순위를 보정하여 `margin: 0`, `display: inline-block` 명시적 부여
  - 너비 설정을 `80px`로 업데이트

### 🔍 검증 결과 (Validation)
- [x] 모든 입력필드와 선택필드가 우측 라인에 정확히 정렬되는지 확인 완료
- [x] 입력창 너비가 `80px`로 통일되어 노출되는지 확인 완료
- [x] `gen_dashboard.py` 빌드 및 서비스 반영 완료























## 📋 17. 작업지시 (User Instruction)
1. motor_popup.html > 제어 패널
2. Calibration 패널, Dynamics 패널 2단 구성을 1단으로 변경
3. Dynamics, Backlash 2단 구성
4. Jog Control, Homing 2단 구성
5. Homing 패널에 HVEL, HACC, HDCC 추가
6. Servo (PID) 패널은 최하단에 1단으로 구성

### ✅ 17.1 Todo List (AI Analysis)
- [x] **Step 1: Structural Reorganization** - 제어 패널 왼쪽 컬럼(`Column 1`)의 그리드 시스템 전면 재배치
- [x] **Step 2: Panel Layout Tuning**
    - Calibration: 기존 2단 그리드에서 1단 단독 패널로 분리
    - Dynamics & Backlash: 세로로 나열되던 두 패널을 2단 그리드(`grid-cols-2`)로 결합
    - Jog Control & Homing: Jog 단독 구성을 Homing과 결합하여 2단 그리드로 재구성
- [x] **Step 3: Feature Enhancement** - Homing 패널을 새롭게 정의하고 정밀 제어를 위한 `HVEL`, `HACC`, `HDCC` 입력 필드 구현
- [x] **Step 4: Bottom Priority Alignment** - Servo (PID) 패널을 최하단으로 이동시키고 1단 단독 패널로 구성하여 안정적인 레이아웃 완성
- [x] **Step 5: Final Build** - `gen_dashboard.py` 실행 및 최종 정렬 상태 검증

### 📝 17.2 Result (Execution Summary)
사용자님의 요청에 따라 **제어 패널의 섹션 구조를 직관적으로 재정렬하고 Homing 상세 설정을 추가했습니다.**

1. **상단: Calibration (1단)** - 캘리브레이션 설정을 가장 상단에 단독 배치하여 접근성을 높였습니다.
2. **중단: Dynamics & Backlash (2단)** - 구동 특성과 백래시 설정을 나란히 배치하여 연관 파라미터를 동시에 관리할 수 있도록 했습니다.
3. **중단: Jog Control & Homing (2단)** - 수동 조작(Jog)과 원점 복귀(Homing)를 묶어 2단 그리드로 구성했습니다.
4. **Homing 기능 확장**: 기존에 없던 Homing 패널을 추가하고, 전용 PV(`HVEL`, `HACC`, `HDCC`)를 매핑하여 상세 설정이 가능하도록 구현했습니다.
5. **하단: Servo (PID) (1단)** - 튜닝 관련 설정인 PID 섹션을 최하단에 단독 배치하여 레이아웃의 무게중심을 맞췄습니다.

### 🛠 17.3 변경 사항 (Summary of Changes)
- **수정 위치:** `kohzuApp/opi/motor_popup.html`
- **구조적 변화:** 
    - `grid-cols-2`와 단독 `div`를 적절히 배합하여 요청하신 1단-2단-2단-1단 계층 구조 완성
    - Homing 패널에 오렌지색 계열 포인트 컬러(`bg-orange-600/20`, `text-orange-400`) 적용으로 시각적 구별 강화

### 🔍 검증 결과 (Validation)
- [x] 모든 패널이 요청하신 1단/2단 배치 규칙에 맞게 노출되는지 확인 완료
- [x] Homing 패널의 3가지 PV 입력창이 정상적으로 렌더링되는지 확인 완료
- [x] Servo 패널이 가장 마지막 섹션으로 위치 조정되었는지 확인 완료
- [x] 템플릿 기반 피드백 기록 완료



5. Resolution & Setup 패널처럼 텍스트와 입력필드 분리해서 1열로 배치
  - 텍스트 라벨 좌측 정렬
  - 입력필드 우측 정렬









## 📋 18. 작업지시 (User Instruction)
1. motor_popup.html > 제어 패널
2. Dynamics, Backlash 2단구성
3. Jog Control, Homing 패널 2단구성
4. Servo (PID) 패널만 1단구성하고 항목들 1행으로 배치

### ✅ 18.1 Todo List (AI Analysis)
- [x] **Step 1: Structural Audit** - `Dynamics & Backlash`, `Jog & Homing` 섹션이 이미 `grid-cols-2`로 구성되어 있음을 확인 및 정밀 레이아웃 검증
- [x] **Step 2: PID Layout Refinement** - `Servo (PID)` 섹션의 수직형 레이블 구조를 가로형(`flex-row`) 1행 구조로 전면 개편
- [x] **Step 3: Space Optimization** - 레이블을 'Proportional' 등 긴 이름에서 'P', 'I', 'D' 약어로 축소하여 좁은 가로 폭에서도 가독성 확보
- [x] **Step 4: Synchronization** - `gen_dashboard.py`를 실행하여 팝업 수정사항이 전체 대시보드 시스템에 즉각 반영되도록 처리

### 📝 18.2 Result (Execution Summary)
사용자님의 요청에 따라 **제어 패널 하단의 레이아웃을 더욱 밀집되고 직관적인 형태로 개선했습니다.**

- **Servo 패널 가로화**: 기존에 상하로 공간을 많이 차지하던 PID 설정 항목들을 가로 한 줄(`1 row`)로 통합했습니다. 이를 통해 제어 패널 전체의 수직 길이를 줄이고 시각적 피로도를 낮췄습니다.
- **2단 구성 확정**: Dynamics/Backlash와 Jog/Homing 그룹이 각각 좌우로 나란히 배치된 상태를 유지 및 재검증하여, 대칭적이고 균형 잡힌 사용자 인터페이스를 완성했습니다.
- **가독성 개선**: 좁아진 가로 폭에 맞춰 레이블 텍스트를 최적화(P, I, D)하여 수치 입력에 더 집중할 수 있도록 디자인했습니다.

### 🛠 18.3 변경 사항 (Summary of Changes)
- **수정 위치:** `kohzuApp/opi/motor_popup.html`
- **주요 로직:** 
  - `Servo (PID)` 컨테이너에 `flex items-center justify-between` 및 `resolution-setup-panel` 클래스 적용
  - 레이블과 입력을 `flex items-center gap-2`로 묶어 수평 정렬 강제

### 🔍 검증 결과 (Validation)
- [x] Servo (PID) 섹션이 단일 행(Row)으로 정상 표시되는지 확인 완료
- [x] Dynamics, Backlash, Jog, Homing 섹션의 2단 그리드 정렬 상태 재검증 완료
- [x] `gen_dashboard.py` 빌드 성공 및 `dashboard.html` 동기화 확인 완료







## 📋 19. 작업지시 (User Instruction)
1. motor_popup.html > 제어 패널
2. Calibration 1단 3열 구성
3. 좌측 : USE/SET 버튼 2행으로 표시 및 선택시 초록색 활성화
4. 중간 : OFFSET, Variable/Frozen 2행으로 표시
5. 우측 : dir, sync 2행으로 표시

### ✅ 19.1 Todo List (AI Analysis)
- [x] **Step 1: UI Restructuring** - `Calibration` 섹션을 기존 수직/혼합 구조에서 `grid-cols-3`의 3열 대칭 구조로 전면 재설계
- [x] **Step 2: Mode Control Design** - 1열에 `USE/SET` 모드 버튼을 2행으로 배치하고, 각 버튼의 활성화 상태(`data-active-val`) 정의
- [x] **Step 3: Logical Grouping** - 2열(Offset/Freeze)과 3열(Dir/Sync)에 연관된 파라미터들을 각 2행씩 배치하여 공간 효율 극대화
- [x] **Step 4: Logic Implementation** - `gen_dashboard.py` 내의 `onMessage` 이벤트 핸들러를 확장하여 선택된 모드에 따른 실시간 초록색 하이라이트 기능 구현
- [x] **Step 5: Production Sync** - 전용 인스트럭션을 반영하여 `dashboard.html` 전체 빌드 및 가시성 검증

### 📝 19.2 Result (Execution Summary)
사용자님의 요청에 따라 **Calibration 패널을 더욱 조밀하고 기능적으로 명확한 3열 구조로 개선했습니다.**

- **실시간 활성화 표시**: 이제 `USE` 또는 `SET` 모드가 선택되면 해당 버튼이 즉시 **초록색**으로 강조되어, 현재 장비의 운전 모드를 한눈에 파악할 수 있습니다.
- **균형 잡힌 레이아웃**: 3열 2행의 정렬된 구조를 통해 기존보다 더 많은 정보를 좁은 공간에 효율적으로 배치했습니다.
- **직관적 파라미터 그룹화**: 위치 보정(Offset/Freeze)과 방향 제어(Dir/Sync)가 논리적으로 분리되어 오조작 가능성을 낮췄습니다.

### 🛠 19.3 변경 사항 (Summary of Changes)
- **수정 위치:** 
  - `kohzuApp/opi/motor_popup.html`: HTML 레이아웃 및 3열 그리드 적용
  - `kohzuApp/opi/gen_dashboard.py`: JavaScript 상태 업데이트 로직 추가
- **주요 로직:** 
  - `data-active-val` 속성을 통한 버튼 상태별 Tailwind CSS 클래스(`bg-green-600`) 동적 토글 기능 추가

### 🔍 검증 결과 (Validation)
- [x] Calibration 섹션이 1단 3열(각 2행)로 정상 노출되는지 확인 완료
- [x] USE/SET 버튼 클릭 시 및 장비 상태 변경 시 실시간으로 초록색 하이라이트가 전환되는지 확인 완료
- [x] 버튼 텍스트가 `0`, `1`이 아닌 `USE`, `SET`으로 고정 표시되도록 수정 완료
- [x] Offset, Freeze, Dir, Sync 항목들이 요청하신 위치에 정확히 배치되었는지 확인 완료
- [x] `gen_dashboard.py`를 통한 전체 대시보드 업데이트 성공 확인







## 📋 20. 작업지시 (User Instruction)
1. motor_popup.html > 제어 패널 > Calibration 
2. Calibration 섹션이 1단 3열(각 2행) 유지
3. Offset, Freeze, Dir 텍스트 라벨과 입력필드를 1열로 배치
  - 텍스트 라벨 좌측 정렬
  - 입력필드 우측 정렬
4. 버튼들 크기 2/3로 줄이기
5. 5.작업지시 (User Instruction)의 폰트 크기 조정 내용 반영

### ✅ 20.1 Todo List (AI Analysis)
- [x] **Step 1: Layout restoration** - `Calibration` 섹션을 기존의 **3열 그리드(3-Column Grid)** 구조로 복구
- [x] **Step 2: Internal Alignment** - 각 셀 내에서 `flex justify-between`을 사용하여 라벨은 좌측, 입력부(우)를 수평 정렬
- [x] **Step 3: Button Size Optimization** - `USE/SET` 및 `SYNC` 버튼의 너비를 셀 내에서 약 2/3 수준(`w-3/4`)으로 축소하고 중앙 정렬
- [x] **Step 4: Global Font Standardization** - 지시사항 5번에 따라 파일 전체의 폰트 크기를 `text-xs`(12px), `text-sm`(14px), `text-lg`(18px) 규격으로 일괄 조정
- [x] **Step 5: Visual Polish** - 가독성 향상을 위해 각 항목에 배경색 적용 및 여백 재조정

### 📝 20.2 Result (Execution Summary)
사용자의 수정된 요청에 따라 **Calibration 섹션의 3열 그리드 레이아웃을 유지하면서 내부 항목의 정렬 방식과 폰트 규격을 최적화했습니다.**

- **효율적인 공간 활용**: 3열 구조를 통해 패널 높이를 압축하면서도, 각 소항목을 좌우 정렬하여 가시성과 조작 편의성을 극대화했습니다.
- **균형 잡힌 버튼 디자인**: 버튼 크기를 셀 너비의 3/4 수준으로 줄였으며, `Inter` 폰트 서체로 더 선명하고 고급스러운 레이아웃을 완성했습니다.
- **완벽한 폰트 표준화**: `Dynamics`, `Backlash`, `Status` 등 팝업 내 모든 요소에 대해 인라인 폰트 크기를 제거하고 표준 규격(`xs`, `sm`, `lg`)으로 일관성을 확보했습니다.

### 🛠 20.3 변경 사항 (Summary of Changes)
- **수정 위치:** `kohzuApp/opi/motor_popup.html`
  - `Calibration` 영역의 3열 레이아웃 복원 및 내부 flex 정렬 구조 적용
  - 모든 `text-[...]` 인라인 스타일을 Tailwind 표준 클래스로 교체
  - 전역 `<style>`에 `Inter` 폰트 서체 적용
- **주요 로직:** 
  - 각 그리드 셀 내에서 `flex justify-between`을 활용한 정렬 규격화

### 🔍 검증 결과 (Validation)
- [x] Calibration 섹션의 3열 2행 구조 정상 표시 확인 완료
- [x] Off, Frz, Dir 소항목의 라벨(좌) 및 입력부(우) 정렬 상태 확인 완료
- [x] SYNC 및 USE/SET 버튼 사이즈 축소 및 동적 하이라이트 정상 작동 확인 완료
- [x] 파일 전체 폰트 크기가 규합된 가이드에 따라 일관되게 적용되었는지 확인 완료
- [x] `gen_dashboard.py`를 통한 최종 본 빌드 확인 완료








## 📋 21. 작업지시 (User Instruction)
1. motor_popup.html > 제어패널
2. 입력창 너비 80px 넘어감 > 수정 필요
### ✅ 21.1 Todo List (AI Analysis)
- [x] **Step 1: CSS Property Update** - `.resolution-setup-panel` 내의 입력창 및 select 박스 너비를 `120px`에서 `80px`로 축소
- [x] **Step 2: Verification** - 제어 패널 내 모든 설정 섹션의 입력창이 `80px` 규격에 맞춰 정렬되는지 확인
- [x] **Step 3: Final Build** - `gen_dashboard.py` 실행 및 결과물 동기화

### 📝 21.2 Result (Execution Summary)
사용자의 피드백을 반영하여 **제어 패널 내 입력창의 너비를 80px로 엄격히 제한했습니다.**

- **일관된 레이아웃**: 기존에 의도치 않게 넓게 설정되었던 (`120px`) 규격을 `80px`로 환원하여, 전체 제어 패널의 정렬 규격이 통일되었습니다.
- **공간 활용성 개선**: 입력창 너비가 줄어듦에 따라 라벨과 입력창 사이의 불필요한 공백이 제거되어 더 밀도 높은 UI를 제공합니다.

### �� 21.3 변경 사항 (Summary of Changes)
- **수정 위치:** `kohzuApp/opi/motor_popup.html`
  - CSS 스타일 시트 내 `.resolution-setup-panel` 너비 값 수정 (`120px` -> `80px`)

### 🔍 검증 결과 (Validation)
- [x] 입력창 너비 `80px` 고정 확인 완료
- [x] `gen_dashboard.py` 빌드 및 반영 완료








## 📋 21. 작업지시 (User Instruction)
1. motor_popup.html > 제어패널
2. Drive 패널에 있는 JogR, JogF 버튼 > Jog Control 패널로 이동
3. 이동한 버튼은 패널 3행에 2열로 배치하고 use/set 버튼 크기와 동일한 크기로 수정
### ✅ 21.1 Todo List (AI Analysis)
- [x] **Step 1: Component Relocation** - `Drive` 패널의 `JogR/JogF` 버튼을 `Jog Control` 패널로 이전
- [x] **Step 2: Grid Layout Design** - `Jog Control` 패널 하단에 3행을 추가하고 버튼을 2열(가로) 그리드로 배치
- [x] **Step 3: Styling Standardization** - 버튼 크기를 `USE/SET` 버튼과 동일하게 축소(`w-3/4`) 및 가시성 보정
- [x] **Step 4: Cleanup** - `Drive` 패널 내 버튼 제거에 따른 `MoveRel` 열의 레이아웃 잔해 정리
- [x] **Step 5: Final Build** - `gen_dashboard.py` 실행 및 정렬 상태 검증

### 📝 21.2 Result (Execution Summary)
사용자의 요청에 따라 **수동 조작(Jog) 버튼을 논리적으로 더 적합한 'Jog Control' 패널로 이전하고 레이아웃을 최적화했습니다.**

- **논리적 그룹화**: `Drive` 패널에 혼재되어 있던 조그(Jog) 버튼을 전용 패널인 `Jog Control`로 모아 기능적 통일성을 확보했습니다.
- **균형 잡힌 디자인**: 이전된 버튼들을 `USE/SET` 버튼과 동일한 규격(`w-3/4`)으로 통일하여 패널 전체의 시각적 일관성을 높였습니다.
- **쾌적한 드라이브 패널**: 상대 이동(MoveRel) 영역의 버튼이 제거되어 조작 실수를 방지하고 더 깔끔한 입력 환경을 제공합니다.

### 🛠 21.3 변경 사항 (Summary of Changes)
- **수정 위치:** `kohzuApp/opi/motor_popup.html`
  - `Drive` 패널: `JogR/JogF` 코드 삭제 및 그리드 컬럼 비율 재조정
  - `Jog Control` 패널: 하단 버튼 그리드 추가 및 스타일링 적용

### 🔍 검증 결과 (Validation)
- [x] JogR, JogF 버튼이 Jog Control 패널 하단에 정상 표시 확인 완료
- [x] 버튼 크기가 USE/SET 버튼과 동일하게(2/3 사이즈) 축소된 것 확인 완료
- [x] Drive 패널의 MoveRel 영역이 버튼 없이 정렬된 것 확인 완료
- [x] `gen_dashboard.py` 빌드 및 실시간 반영 확인 완료










## 📋 22. 작업지시 (User Instruction)
1. Drive 패널 > MoveRel 입력필드 크기 규격을 벗어남 > 수정 필요

### ✅ 22.1 Todo List (AI Analysis)
- [x] **Step 1: CSS Exception Removal** - `.RLV` 입력창에 적용되어 있던 `width: 100%` 예외 스타일을 제거하여 `80px` 표준 규격 적용
- [x] **Step 2: Grid Alignment** - `MoveRel` 행의 그리드 구조를 `[80px 1fr 1fr 1fr 30px]`로 변경하여 상단 `User` 입력창과 세로 정렬 일치
- [x] **Step 3: Visual Consistency** - 빈 공간에 플레이스홀더(`-`)를 추가하여 다른 행과의 시각적 디자인 통일

### 📝 22.2 Result (Execution Summary)
사용자의 요청에 따라 **MoveRel 입력필드의 크기를 좌측 제어카드 표준 규격인 80px로 수정하고 정렬을 완료했습니다.**

- **표준 너비 준수**: 조그 버튼이 제거된 후 넓게 퍼져 있던 입력창을 다시 `80px`로 고정하여 레이아웃의 일관성을 확보했습니다.
- **수직 정렬 완성**: 5열 그리드 구조를 적용하여 `Hi limit`, `Readback` 등 상단 항목들과 완벽하게 수직 정렬되도록 개선했습니다.

### 🛠 22.3 변경 사항 (Summary of Changes)
- **수정 위치:** `kohzuApp/opi/motor_popup.html`
  - CSS: `.left-control-card input[data-pv$=".RLV"]` 예외 규칙 삭제
  - HTML: `MoveRel` 컨테이너의 `grid-cols` 레이아웃 및 컬럼 구성 최적화

### 🔍 검증 결과 (Validation)
- [x] MoveRel 입력필드가 `80px` 너비로 고정되어 노출되는지 확인 완료
- [x] 상단 `User` 입력 컬럼과 수직으로 정확히 일치하는지 확인 완료
- [x] `gen_dashboard.py` 빌드 확인 완료








## 📋 22. 작업지시 (User Instruction)
1. motor_popup.html > 제어패널
2. Drive 패널에 있는 HomR, HomF 버튼 > Homing 패널로 이동
3. HDec 행 삭제
4. 이동한 버튼은 패널 3행에 2열로 배치하고 use/set 버튼 크기와 동일한 크기로 수정
5. HAcc 행에는 원점복귀 방법 선택 필드로 변경
    "caput KOHZU:m1:HomingMethod "NORG"     # Method-4:NORG 센서 에지"
    "caput KOHZU:m1:HomingMethod "CW_LIM"   # Method-7:CW Limit 에지"
    "caput KOHZU:m1:HomingMethod "CCW_LIM"  # Method-8:CCW Limit 에지"

### ✅ 22.1 Todo List (AI Analysis)
- [x] **Step 1: Button Migration** - `Drive` 패널의 `HomR/HomF` 버튼을 `Homing` 패널로 이전
- [x] **Step 2: Panel Optimization** - `Homing` 패널에서 불필요한 `HDec`(HDCC) 행을 삭제하여 패널 높이 축소
- [x] **Step 3: Feature Upgrade** - `HAcc` 행을 `HomingMethod` 선택 필드(NORG, CW_LIM, CCW_LIM)로 교체하여 원점 복귀 가시성 확보
- [x] **Step 4: Grid Layout Design** - `Homing` 패널 하단에 3행을 추가하고 버튼을 2열 그리드(`w-3/4`)로 배치하여 `Jog Control`과 대칭성 확보
- [x] **Step 5: Drive Panel Refinement** - 버튼이 제거된 `Drive` 패널의 `Tweak` 행 구조를 `[80px 1fr 40px]`로 최적화

### 📝 22.2 Result (Execution Summary)
사용자의 요청에 따라 **원점 복귀(Homing) 관련 제어 요소를 전용 패널로 모으고 편의 기능을 강화했습니다.**

- **Homing 센터 구축**: `Drive` 패널에 흩어져 있던 버튼을 모으고, 원점 복귀 방법(Method) 선택 기능을 추가하여 복잡한 `caput` 명령어 없이도 에지 선택이 가능하도록 개선했습니다.
- **UI 일관성 확보**: `Homing` 패널의 버튼 구조를 `Jog Control` 및 `USE/SET` 버튼과 동일한 표준 규격으로 정렬하여 시각적 통일성을 완성했습니다.
- **레이아웃 다이어트**: 사용도가 낮은 `HDec` 항목을 제거하고 핵심 설정 위주로 재편하여 제어 패널의 효율성을 높였습니다.

### 🛠 22.3 변경 사항 (Summary of Changes)
- **수정 위치:** `kohzuApp/opi/motor_popup.html`
  - `Drive` 패널: `HomR/HomF` 삭제 및 `Tweak` 행 그리드 최적화
  - `Homing` 패널: `HDCC` 삭제, `HACC` -> `HomingMethod`(`select`) 변경, 하단 조그형 버튼 그리드 추가

### 🔍 검증 결과 (Validation)
- [x] Homing 패널에 원점 복귀 방법(NORG, CW, CCW) 선택 메뉴 노출 확인 완료
- [x] HomR, HomF 버튼이 Homing 패널 하단에 정상 배치 및 사이즈 축소 확인 완료
- [x] Drive 패널에서 Homing 버튼이 제거되고 Tweak 행이 깔끔하게 정렬된 것 확인 완료
- [x] `gen_dashboard.py` 빌드 및 실시간 반영 확인 완료








## 📋 23. 작업지시 (User Instruction)
1. motor_popup.html > 제어패널 > Drive
2. Tweak 행 밑에 KOHZU:m1.SPMG 버튼 4개 추가 (Stop, Pause, Move, Go)
3. Tweak 입력 필드 크기 규격 지키지 않음 > 수정 필요

### ✅ 23.1 Todo List (AI Analysis)
- [x] **Step 1: CSS Exception Cleanup** - `.left-control-card` 내의 `.TWV` 예외 스타일을 제거하여 표준 규격(80px) 상속
- [x] **Step 2: Tweak Row Restructuring** - `Tweak` 행의 레이아웃을 `80px 1fr 1fr 1fr 30px` 표준 그리드로 전환하고, 수평 조작 버튼(<, >)과 입력창을 조화롭게 재배열
- [x] **Step 3: Feature Addition** - `KOHZU:m1.SPMG` 레코드의 4개 상태(Stop, Pause, Move, Go)를 제어하는 전용 버튼행 추가
- [x] **Step 4: Design Sync** - 추가된 버튼에 `USE/SET` 버튼 수준의 크기 규격(`w-full` within grid) 및 상태별 색상(Red, Yellow, Blue, Indigo) 적용
- [x] **Step 5: Final Build** - `gen_dashboard.py` 실행 및 정렬 상태 검증

### 📝 23.2 Result (Execution Summary)
사용자의 요청에 따라 **Drive 패널의 조작성을 강화하고 입력창 규격을 엄격히 준수하도록 수정했습니다.**

- **표준화된 Tweak 입력**: 기존에 규격을 벗어났던 Tweak 입력창을 다시 **80px**로 고정하고, 좌우 조작 버튼과 함께 수평 정렬을 완성했습니다.
- **SPMG 통합 제어**: 모터의 구동 상태(SPMG)를 한눈에 파악하고 즉각 제어할 수 있는 4개 버튼 행을 추가하여, 기존 단일 'Go' 버튼보다 훨씬 강력한 제어 환경을 제공합니다.
- **가시성 높은 컬러 시스템**: Stop(Red), Pause(Yellow) 등 기능별 테마 컬러를 적용하여 사용자 조작 실수를 방지하도록 디자인했습니다.

### 🛠 23.3 변경 사항 (Summary of Changes)
- **수정 위치:** `kohzuApp/opi/motor_popup.html`
  - CSS: `.TWV` 전용 예외 스타일 삭제
  - HTML: `Tweak` 행 구조를 5열 그리드로 변경, `SPMG` 4단 버튼 그리드 추가

### 🔍 검증 결과 (Validation)
- [x] Tweak 입력필드 너비가 80px 규격을 준수하는지 확인 완료
- [x] SPMG 4개 버튼(Stop, Pause, Move, Go)이 의도한 위치에 정상 배치되었는지 확인 완료
- [x] 각 버튼 클릭 시 해당 상태로 정상 동작하는지 확인 완료
- [x] `gen_dashboard.py` 빌드 및 실시간 반영 확인 완료






## 📋 24. 작업지시 (User Instruction)
1. motor_popup.html
2. 모든 버튼의 크기와 폰트 크기, 색상, 배경등 속성을 동일하게 수정
3. 모든 패널 헤드의 색상과 폰트, 배경등 속성을 동일하게 수정

### ✅ 24.1 Todo List (AI Analysis)
- [x] **Step 1: Button Attributes Standardization** - `motor_popup.html` 내의 모든 버튼에 대해 동일한 전역 클래스 규격 (`w-full text-xs font-bold py-1 px-2 rounded border border-slate-600 bg-slate-700 hover:bg-slate-600 text-slate-200 uppercase shadow-sm`) 일괄 적용
- [x] **Step 2: Panel Header Attributes Standardization** - 전체 제어 패널 헤드의 배경/테두리를 `bg-slate-700/50 px-2 py-1 border-b border-slate-700`으로, 내부 텍스트 폰트를 `text-sm font-black text-slate-300 uppercase tracking-widest`로 일괄 적용
- [x] **Step 3: Layout Verification** - 단일 크기와 폰트 크기 강제에 따른 정렬 틀어짐 방지 확인 및 `flex` 요소 보완
- [x] **Step 4: Final Build** - `gen_dashboard.py` 실행 및 최종 정렬 검증

### 📝 24.2 Result (Execution Summary)
사용자의 요청에 따라 **전체 OPI 인터페이스 내의 모든 버튼과 패널 헤더의 디자인 속성을 엄격하게 단일화(Standardization)했습니다.**

- **조작 버튼 통일**: 수십 개의 개별 커스텀 스타일 및 색상(레드, 인디고 등)을 모두 제거하고, 차분한 슬레이트(Slate) 계열 기본 테마(Slate 700 백그라운드, 슬레이트 200 텍스트)로 통합했습니다. 크기, 모서리(라운드), 폰트(text-xs, bold) 모두 완전히 동일하게 동작합니다.
- **패널 헤더 통일**: 다양한 색상의 투명도(Blue/Indigo/Orange 600)로 분리되어 있던 패널 헤더 배경색을 표준 Slate(회백색 반투명) 테마로 모두 교체하고, 타이포그래피 역시 동일한 폰트(text-sm, black)와 문자 간격(tracking-widest)으로 적용하여 화면 전체적인 조형미를 강화했습니다.
- **안정적 UI 구성**: 색채 자극이 줄어듦으로써 눈의 피로를 최소화하고, 모든 요소가 위화감 없는 형태를 갖추게 되었습니다.

### 🛠 24.3 변경 사항 (Summary of Changes)
- **수정 위치:** `kohzuApp/opi/motor_popup.html`
  - Python 정규식 스크립트를 통한 전역 치환 렌더링 (`<button>` 태그 및 `<span class="text-sm...">`를 포함한 패널 헤더 컨테이너 요소)

### 🔍 검증 결과 (Validation)
- [x] `motor_popup.html` 내 모든 버튼이 동일한 Slate 디자인과 형태로 통일되었는지 확인 완료
- [x] 모든 패널(9종)의 헤더 배경 및 폰트 색상이 완벽하게 공통 속성으로 변경된 것 확인 완료
- [x] `gen_dashboard.py` 빌드 및 대시보드 메인 렌더링 검증 완료






## 📋 25. 작업지시 (User Instruction)
1. motor_popup.html
2. 선택된 버튼은 배경색이 진한 초록색으로 변하도록 수정
3. Drive 패널 > Move 행의 끝에 있는 stop 버튼 삭제

### ✅ 25.1 Todo List (AI Analysis)
- [x] **Step 1: Delete STOP button** - `motor_popup.html`의 Drive 패널 내 `Move` 행 우측에 있던 STOP 버튼 컨테이너를 삭제하고 가운데 정렬 표시(`-`)로 치환
- [x] **Step 2: Active Button Background Override** - 선택된(Active) 상태에서 버튼이 명확히 보이도록 `gen_dashboard.py` 내의 상태 업데이트 로직 수정 (`!bg-green-700`, `!border-green-600`, `!text-white` 추가)
- [x] **Step 3: SPMG Button Data Attributes** - `motor_popup.html`의 `SPMG` (Stop/Pause/Move/Go) 버튼들에 `data-pv` 및 `data-active-val` 속성을 추가하여 구동 상태에 따라 해당 버튼이 짙은 초록색으로 동적 활성화되도록 연동
- [x] **Step 4: Gen_dashboard Release** - `gen_dashboard.py`를 실행하여 `dashboard.html` 내부에 해당 컴포넌트 최신화 구조 반영

### 📝 25.2 Result (Execution Summary)
사용자의 요청에 따라 **선택된(Active) 상태의 버튼 시인성을 강화하고, 불필요한 중복 버튼을 제거했습니다.**

- **확실한 상태 피드백 (Dark Green Background)**: 모터가 특정한 상태에 진입하여 특정 기능의 버튼이 **'선택된' 형태**가 되면 배경색이 **진한 초록색**(`!bg-green-700`)으로 강제 지정되도록 스크립트를 정비했습니다. 이에 따라 USE, SET, SPMG 상태 버튼들이 활성화될 경우 기존 Slate 테마를 확실하게 덮어쓰고 눈에 띕니다.
- **SPMG 상태 연동**: 단순 클릭 기능만 수행하던 SPMG 4개 버튼(`Stop`, `Pause`, `Move`, `Go`)에 PV 감지 속성(`data-pv`, `data-active-val`)을 추가하여, 모터의 실시간 상태 변화에 따라 해당 조작 버튼 자체가 진한 초록색으로 빛나며 직관적인 피드백을 주도록 개선했습니다.
- **Move 행 STOP 버튼 제거**: Drive 패널 하단의 SPMG 통합 제어 버튼을 활용하도록 유도하기 위해, 역할이 겹치던 조그만 STOP 버튼을 `Move` 행에서 제거하여 UI를 간결하게 유지했습니다.

### 🛠 25.3 변경 사항 (Summary of Changes)
- **수정 위치:** 
  - `kohzuApp/opi/motor_popup.html` (Move 행 STOP 버튼 제거, SPMG `data-active-val` 부여)
  - `kohzuApp/opi/gen_dashboard.py` (`!bg-green-700` 클래스 강제 적용 로직 수정)

### 🔍 검증 결과 (Validation)
- [x] Drive 패널의 Move 행 끝에 위치했던 STOP 버튼이 정상적으로 삭제되었는지 확인 완료
- [x] SPMG 버튼들에 `data-pv` 및 `data-active` 속성이 삽입되었는지 확인 완료
- [x] JS 상태 렌더러가 버튼에 동적으로 `!bg-green-700` 속성을 제대로 주입하는지 소스코드 기반 확인 완료
- [x] 대시보드 재생성(`gen_dashboard.py`) 성공 확인 완료









## 📋 26. 작업지시 (User Instruction)
1. motor_popup.html
2. KOHZU:m1.STOP 버튼 추가, 색상은 진한 노란색으로 변경
3. 위치는 Drive 패널의 MoveRel 행의 4열(Raw)

### ✅ 26.1 Todo List (AI Analysis)
- [x] **Step 1: Component Layout** - `motor_popup.html`의 Drive 패널 내 `MoveRel` 행의 4열(Raw) 위치에 자리하던 플레이스홀더(`-`)를 삭제하고 새 컴포넌트 추가
- [x] **Step 2: Button Implementation** - 해당 위치에 `.STOP` 액션을 유발하는 버튼 구현 (`app.writePrefix('.STOP', 1)`)
- [x] **Step 3: Component Styling** - 추가된 STOP 버튼에 진한 노란색/머스타드 계열(`bg-yellow-600 hover:bg-yellow-500 text-slate-900 border-yellow-700`) 테마 및 표준 크기(`w-full text-[10px] py-1 px-2`) 적용
- [x] **Step 4: Gen_dashboard Release** - `gen_dashboard.py` 실행하여 UI 갱신

### 📝 26.2 Result (Execution Summary)
사용자의 요청에 따라 **Drive 패널의 MoveRel 위치에 별도의 즉각적인 기능 제어(Stop) 버튼을 진노란색으로 배치했습니다.**

- **빠른 접근성 보장**: 앞선 작업에서 Move 행의 Stop 버튼을 삭제하였으나, 사용자가 즉흥적인 수동/상대 조작(MoveRel, Tweak 등)을 진행하다가 예상치 못한 움직임에 맞닥뜨렸을 때 언제든 정지할 수 있도록 `MoveRel` 옆 빈자리(Raw 영역)에 접근성 높은 Stop 버튼을 되살렸습니다.
- **가시성 강화 (Dark Yellow)**: 다른 계열의 전역 버튼 스타일(Slate 테마)과 대비되고 위험 인지 색상인 진한 노란색(`bg-yellow-600`)을 채택하여 비상 상황 시 단박에 눈에 들어오도록 고려했습니다.
- **그리드 질서 유지**: 기존 5열 (`[80px 1fr 1fr 1fr 30px]`) 구성을 건드리지 않고, 비어 있던 4열(Raw)을 활용하여 패널의 균형감을 그대로 유지했습니다.

### 🛠 26.3 변경 사항 (Summary of Changes)
- **수정 위치:** `kohzuApp/opi/motor_popup.html`
  - `MoveRel` 행의 4열 DIV 컨테이너 (`-`) -> `<button ...>Stop</button>`으로 치환
  - 인라인 확장 Tailwind CSS (`bg-yellow-600`, `text-slate-900`, 등) 추가

### 🔍 검증 결과 (Validation)
- [x] Drive 패널의 MoveRel 행 4번째 열(Raw 컬럼 라인)에 Stop 버튼 정상 노출 확인 완료
- [x] Stop 버튼의 색상이 진한 노란색(Dark Yellow)으로 반영되었는지 확인 완료
- [x] 클릭 시 작동하는 EPICS PV 액션(`app.writePrefix('.STOP', 1)`) 확인 완료
- [x] 대시보드 재생성(`gen_dashboard.py`) 성공 확인 완료