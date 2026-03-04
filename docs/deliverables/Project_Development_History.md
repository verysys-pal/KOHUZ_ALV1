# 📊 kohzuApp 프로젝트 개발 이력 종합 정리
> **생성일:** 2026.03.04  
> **최종 갱신:** 2026.03.04  

---

## 🗂️ 프로젝트 개요

| 항목 | 내용 |
|------|------|
| **프로젝트명** | kohzuApp (Kohzu 6-Axis Motor Control System) |
| **경로** | `/usr/local/epics/EPICS_R7.0/siteApp/KOHUZ_ALV1/` |
| **기술 스택** | EPICS IOC (C++) + Python Web Gateway (Tornado/PyEPICS) + HTML/JS/TailwindCSS |
| **개발 기간** | 2026.02.19 ~ 2026.03.04 (약 2주) |

---

## 📈 개발 진행 흐름 (Evolution)

```
[Phase 1] Phoebus OPI (XML) — 기존 EPICS 제어기 GUI
    ↓ Task 12 (02.19) : OPI → HTML 변환 시도
[Phase 2] 단일축 HTML (motorx_all.html) — Chrome 기반 제어 UI
    ↓ Task 13~15 (02.19) : WebSocket Gateway 구축
[Phase 3] WebSocket 실시간 연동 + 현대화 UI (TailwindCSS)
    ↓ Task 1 (02.26a) : 6축 통합 설계
[Phase 4] 6축 통합 Dashboard (dashboard.html) — JSON 기반 스테이지 관리
    ↓ Task 10 (02.26a) : IOC 백엔드 확장
[Phase 5] IOC 6축 확장 (st.cmd + motor.substitutions)
    ↓ Task 1 (03.02a) : 아키텍처 분리
[Phase 6] 모달 분리 아키텍처 (fetch + 템플릿 동적 로드)
    ↓ Task 13 (03.02a) : 분석/백업 기능 추가
[Phase 7] 실시간 차트 + 세션 Save/Load 시스템
    ↓ Task 1~11 (03.04) : 고급 기능 및 UX 개선
[Phase 8] 2D Area Scan + 모바일 최적화 + localStorage 영속화
```

---

## 📅 날짜별 주요 작업 내역

### 📌 2026.02.19 (`Instruction_260219.md`) — 16개 Task

| Task | 핵심 내용 | 분류 |
|------|----------|------|
| 1~4 | `verify_Scenario_V2.sh` 소프트/하드 리미트 양방향 테스트 개선 및 디버깅 (`unbound variable` 오류 수정 포함) | 🔧 테스트 |
| 5~6 | Phoebus OPI 실행 및 PV 매크로(`$(P)`, `$(M)`) 접두사 활용법 가이드 | 📖 가이드 |
| 7 | `motorx_all.opi` 사용 가이드 문서 작성 (PV 설명, Calibration, HLM/DHLM 차이, scanParam) | 📖 가이드 |
| 10~11 | OPI XML 파일의 Grouping Container 리팩토링 (Python `refactor_opi.py` 스크립트 활용, Row Clustering) | 🛠️ 리팩토링 |
| **12~13** | **⭐ 전환점:** OPI → Chrome용 HTML 변환(`opi_to_web.py`), EPICS Web Gateway (`web_gateway.py`) 최초 구축 | 🚀 신규 |
| 14 | HTML 내 매크로(`$(P)$(M)`) 치환 로직 추가 (URL 파라미터 또는 기본값 적용) | 🔧 수정 |
| 15 | `motorx_all.html` 아키텍처 현대화 (TailwindCSS Dark Mode, `EPICSController` Class 기반 WebSocket 바인딩) | 🛠️ 리팩토링 |
| 16 | Drive & Position 카드에 Advanced/Scan 카드 병합 | 🎨 UI |

---

### 📌 2026.02.20a (`Instruction_260220a.md`) — 19개 Task

| Task | 핵심 내용 | 분류 |
|------|----------|------|
| 1~2 | SPMG 버튼 UI 개선 (Select → Button Group), Hidden Element WebSocket 구독 방식 수정 | 🎨 UI |
| **3** | **모바일 접속 지원**: `web_gateway.py` → `0.0.0.0` 바인딩 + `StaticFileHandler` 정적 파일 서빙 + `window.location.hostname` 동적 WebSocket URL | 🚀 신규 |
| 4~6 | 카드 min/max 크기 제한(350~400px), `NoCacheStaticFileHandler` 캐시 방지, `.card-responsive` 클래스 도입 | 🎨 UI |
| 7~11 | 카드 중앙정렬(`margin: 0 auto`), 그리드 최적화(`4cols→3cols`), gap 조정(`12px`), `repeat(N, minmax())` 사용 | 🎨 레이아웃 |
| 12 | 카드 내부 2열 구조: Dynamics/Backlash, Soft Limits User/Dial 분리, Resolution 2열 그리드 | 🎨 UI |
| 13~15 | 전역 헤더 반응형(모바일) 레이아웃 개선 (flex-col/flex-row 전환), PV.DESC 추가 | 📱 반응형 |
| **16** | **EPICS DB 수정**: `KOHZU_Motor.db`에 누락된 `field(DESC, "$(DESC)")` 추가, `make` 빌드 및 IOC 재시작 | 🔧 백엔드 |
| 17 | 그리드 컬럼 고정(`repeat(3, minmax(350px, 400px))`), `justify-center` 중앙 정렬 | 🎨 레이아웃 |
| 18~19 | Set Position 버튼 테두리/초록색 활성화, STOP 버튼 `data-pv` 제거(텍스트 덮어쓰기 버그 수정) | 🐛 버그 |

---

### 📌 2026.02.20b (`Instruction_260220b.md`)

| 내용 | 상세 | 분류 |
|------|------|------|
| SET 버튼 색상 미변경 | PV `.SET` 구독 누락으로 `onMessage` 미실행 → Hidden `data-pv` span 추가, Enum 문자열 대응 | 🐛 버그 |

---

### 📌 2026.02.24 (`Instruction_260224.md`)

| 내용 | 상세 | 분류 |
|------|------|------|
| NotebookLM | "kohzuApp Documentation" 노트 생성(ID: `590ff233-...`), `Instruction.md`, `Kohzu_ARIES_Driver_Refactoring_Report.md`, `Kohzu_Stage_DB_Parameters.md` 업로드 | 📖 문서화 |

---

### 📌 2026.02.25 (`Instruction_260225.md`) — 5개 Task

| Task | 핵심 내용 | 분류 |
|------|----------|------|
| 1~2 | **bkit 확장앱** 사용법 분석: PDCA 워크플로우 장단점 비교, 다중 에이전트 vs 병렬 도구 실행 방식 차이 설명 | 📖 가이드 |
| 3~4 | `frozen(FOFF)` 기능 분석: OPI 구현 확인(Select 드롭다운), EPICS Motor Record 내장 기능 확인 | 📖 분석 |
| 5 | FOFF ↔ ARIES 커맨드 매핑 분석: 직접 매핑 없음(EPICS 소프트웨어 전용 플래그), `setPosition()` 미구현 우려 | 📖 분석 |

---

### 📌 2026.02.26a (`Instruction_260226a.md`) — 16개 Task ⭐ **가장 큰 전환점**

| Task | 핵심 내용 | 분류 |
|------|----------|------|
| **1** | **⭐ 6축 통합 대시보드** (`dashboard.html`) 최초 구축: JSON 스키마 설계, 카드 그리드, 모달 팝업, `gen_dashboard.py` 자동 생성 스크립트 | 🚀 신규 |
| 2~3 | 서버 포트(8888/9999) 폴백 로직 확인, 방화벽/네트워크 대역 트러블슈팅 | 📖 가이드 |
| **4** | **Disconnected 에러 해결**: 5개 미연결 모터의 PV 조회 타임아웃으로 IOLoop 블로킹 → `connection_timeout=0.01` 최적화, `confirm()` 팝업으로 유연화 | 🐛 버그 |
| 5 | 6축 개별 Connected/Disconnected LED 추가, `connection_callback` 브로드캐스팅, EPICS IOC 3계층 아키텍처 설명 | 🚀 신규 |
| 6~7 | `dashboard.html` JS 초기화 순서 `ReferenceError` 수정, 모달 `data-tpl-pv` 스킵 로직 제거 | 🐛 버그 |
| 8 | `motorx_more_v2.opi` 참조 카드 리디자인: 4열 그리드(`60px_1fr_1fr_30px`), 23종 PV 바인딩 확장, `event.stopPropagation()` 적용 | 🎨 UI |
| 9 | **Web Usage Guide** 작성: IP 할당, IOC 실행, caget/caput 테스트, Web Gateway, 방화벽 개방 | 📖 가이드 |
| **10** | **IOC 6축 확장**: `KohzuAriesCreateController("PC0","L0",6,0.2,1.0)`, `motor.substitutions` 파일 생성, `dbLoadTemplate` 적용 | 🔧 백엔드 |
| 11 | 미연결 축 비활성화: `.disconnected-card` CSS(반투명, Grayscale, "DISCONNECTED" 워터마크), 조작 차단 | 🎨 UI |
| 12 | **MSTA 기반 HW 헬스체크**: Bit 9(`RA_PROBLEM`) 감지 → 3색 LED(Green/Red/Gray) 상태 천이 | 🚀 신규 |
| 13 | JSON 스키마 확장: `specifications`(기계 사양), `driverSettings`(드라이버 전류), `DHLM/DLLM` 추가, 모달 4컬럼 확장 | 🛠️ 개선 |
| 14~15 | 모터 팝업 OPI 스타일 이식(`JVEL`, `JAR` 추가, `MOVN` 애니메이션), `motor_popup.html` 독립 템플릿 생성 | 🚀 신규 |
| 16 | PID 계수, 백래시, 분해능 파라미터 추가, 스테이지 JSON 렌더링 ID 불일치 수정 | 🐛 수정 |

---

### 📌 2026.02.27a (`Instruction_260227a.md`) — 19개 Task

| Task | 핵심 내용 | 분류 |
|------|----------|------|
| 1 | `motorx_all.opi` PV 매칭 검증: OPI 69종 vs HTML 60종, 비핵심 9종(ATHM, CARD 등) 제외 확인 | 📖 분석 |
| 2~3 | `motor_popup.html` 다크모드 적용(`.input-dark-tab`), 카드 비율 3:2(`lg:col-span-3/2`), 입력 필드 50% 축소 | 🎨 UI |
| 4~6 | 폰트 크기 전수 조사 및 3단계 규칙 통일: `text-xs`(라벨/버튼/뱃지), `text-sm`(패널 헤더/Move), `text-lg`(타이틀) | 🎨 표준화 |
| 7~11 | Resolution & Setup 패널: 위치 이동(Column2 하단), 수직 배치 → 가로 배치, 2단 컬럼 구조 복구, 태그 누락 수정 | 🎨 레이아웃 |
| 12~16 | 입력창 너비 최적화: `w-24(96px)` → `w-16(64px)` → `70px` → **`80px` 최종 확정**, CSS `!important` 우선순위 충돌 해결 | 🎨 표준화 |
| **17** | **제어 패널 구조 최종 확정**: Calibration(1단) → Dynamics+Backlash(2단) → Jog+Homing(2단, `HVEL/HACC/HDCC` 추가) → Servo PID(1단) | 🎨 UI |
| 18~19 | `README.md` 빌드 가이드 업데이트, `DEPEND_DIRS` 의존성 규칙 추가로 빌드 순서 자동화 | 📖 문서화 |

---

### 📌 2026.02.27b (`Instruction_260227b.md`)

| 내용 | 상세 | 분류 |
|------|------|------|
| Readback 패딩 | `motor_popup.html` 뷰어 라벨(User, Dial, Raw) 우측 패딩 정렬 보정 | 🎨 UI |
| Drive 패널 | 51번째 라인 지시사항 기반 Tweak 행 5열 그리드 구성, SPMG 4버튼(Stop/Pause/Move/Go) 추가 | 🎨 UI |

---

### 📌 2026.02.28 (`Instruction_260228.md`)

| 내용 | 상세 | 분류 |
|------|------|------|
| GUI Design Guide | 그리드 규격(80px 라벨 너비) 추가, Tweak 6열 그리드 표준, STOP 노란색 테마 | 📖 표준화 |
| JSON 적용 Q&A | 파라미터 적용 범위 설명, 브라우저 새로고침 필요성 안내 | 📖 가이드 |

---

### 📌 2026.03.01 (`Instruction_260301.md`) — 13개 Task

| Task | 핵심 내용 | 분류 |
|------|----------|------|
| 1~2 | Upload JSON 버튼 위치 이동(Stage Information 패널 우측 상단), `motor_popup.html` 독립 파싱 스크립트 추가 | 🎨 UI |
| 3~5 | JSON FileReader 메커니즘 상세 설명, **DMOV 역방향 로직 버그 수정**(정상=1인데 `!=1`로 오구현), 동적 파라미터 전송(`Object.entries` 루프) | 🐛 버그 |
| **6** | **모달 즉시 갱신 블록(45줄)**: `handleFileUpload` 내 `modal-stage-badge`, `modal-specs-list`, `modal-driver-list` 실시간 렌더링, `data-actual-pv` 입력 반영 | 🚀 신규 |
| **7** | **서버 Stage Select 시스템**: `web_gateway.py`에 `StageListHandler`(GET `/api/stages`) 추가, `dashboard.html`에 `populateStageDropdown()` + `loadServerStage()` 함수 구현 | 🚀 신규 |
| **8** | **GUI Design Guide 대규모 적용**: 패널 헤더(bg-slate-700/50), 입력 필드(border-slate-700, rounded-0.25rem), STOP 버튼(노란색 bg-yellow-600), 라벨 80px 그리드 | 🎨 표준화 |
| 9 | **RA04A-W01 가이드 생성**: 회전형 스테이지(Worm 1/90, EGU=deg, MRES=0.002°) | 📖 문서 |
| 9 | **SA05A-R2B01 가이드 생성**: 고니오미터(Ball Screw, ±3.5°, MRES=0.0000637°) | 📖 문서 |
| 9 | **XA05A-R102 가이드 생성**: 선형 스테이지(Ground Screw 0.5mm, ±7.5mm, MRES=0.00025mm) | 📖 문서 |
| 10 | **JSON 3종 생성**: `RA04A.json`, `SA05A.json`, `XA05A.json` (16가지 PV 파라미터 포함) | 🚀 신규 |
| 11 | **XA05A-L202 가이드+JSON 생성**: Ball Screw 1.0mm, ±25mm, MRES=0.0005mm | 📖 문서 |
| 12 | JSON 파일명 변경: 모델번호 중복 방지를 위해 `stageModel` 기반으로 리네이밍 (예: `XA07A.json` → `XA07A-L202.json`) | 🛠️ 정리 |
| 13 | **ZA05A-W101 가이드+JSON 생성**: 1/2 Wedge 구조, UREV=0.25mm, ±4mm 수직 이동 | 📖 문서 |

---

### 📌 2026.03.02a (`Instruction_260302a.md`) — 15개 Task

| Task | 핵심 내용 | 분류 |
|------|----------|------|
| **1** | **⭐ 아키텍처 리팩토링**: `dashboard.html`이 `motor_popup.html`을 `fetch()`로 동적 로드 → 하드코딩 모달 제거, PV 치환(`replaceAll`), 캐싱 적용 | 🛠️ 리팩토링 |
| 2~3 | 누락된 Stage Select 드롭다운 복구, Upload JSON 버튼 제거, GUI Design Guide 준수 패널 생성(Mechanical Specifications, Driver & Switching Settings) | 🎨 UI |
| **4** | **MSTA Bit Status 미작동 해결**: 비트 번호 오류(0-5 → 1,9,10,2,13,14), `led-tiny` → 표준 `.led` 교체, `data-led-color` 다이나믹 색상 연동 | 🐛 버그 |
| 5 | GUI Design Guide에 LED 상태 표시등 규칙 추가: `on`(Green), `warn`(Blue/Yellow), `error`(Red) | 📖 표준화 |
| **6** | **UI 명칭 표준 용어집(Nomenclature)** 작성: Header, Card Header, 데이터 열 헤더, Hi/Lo limit, Readback, Drive, Tweak, Bottom Status, Modal 제어 패널, STATUS 패널 등 | 📖 문서화 |
| 7~8 | 뷰어 라벨(Data Display) 명칭 정의: "입력창 룩앤필의 ReadOnly 박스", 사이즈 분석(`80px` 고정 vs `1fr` 가변) | 📖 분석 |
| **9** | **뷰어 라벨 규격화**: `w-[80px]`, `h-[22px]`, `pr-3`(스피너 보정), `bg-slate-900`, `text-green-400` → 입력 폼과 완전 동일 외형 | 🎨 표준화 |
| 10 | GUI Design Guide 업데이트: 공통 속성(80px, 22px, pr-3, px-1.5, py-0.5), 개별 색상(Data Display: green-400, Input: white) | 📖 표준화 |
| **11** | **Axis Card 2열 분리 레이아웃**: 좌(데이터: Hi/RBV/Drive/Lo) / 우(Tweak: 1행 방향 + 2행 Go/STOP), 헤더에 DTYP/상태 뱃지 이동 | 🎨 UI |
| 12 | Flexbox 레이아웃 전환: `grid` → `flex flex-wrap justify-center gap-6`, 고정 간격 24px 보장 | 🎨 레이아웃 |
| **13** | **대시보드 2열 분할**: 좌(모터 카드) / 우(실시간 차트 + 메모장), `Chart.js` 추가, **세션 Save/Load 시스템** (JSON 직렬화 → PV 일괄 Write 복원) | 🚀 신규 |
| 14~15 | 실시간 차트 3분할(Linear/Vertical/Rotation by `axisType`), X축 시간 표시, 타입별 데이터 분배 로직 수정 | 🎨 차트 |

---

### 📌 2026.03.02b / 03.03a (`Instruction_260302a.md` 후속, `Instruction_260303a.md`)

| 내용 | 상세 | 분류 |
|------|------|------|
| 서버 세션 관리 | `kohzuApp/opi/sessions/` 디렉토리 생성, `web_gateway.py`에 API 엔드포인트 추가(`/api/sessions`, `/sessions/:filename`), Dashboard에 드롭다운/Save 버튼 UI | 🚀 신규 |
| Sequence Mode | 접이식 카드(Collapse), 좌표 변화값 시각화(파란색=변경, 회색=유지) | 🎨 UI |

---

### 📌 2026.03.03b (`Instruction_260303b.md`)

| 내용 | 상세 | 분류 |
|------|------|------|
| 2D Scan Panel | Raster/Fermat 스캔 설정 UI 정비, GUI Design Guide 준수(60px 라벨, 그리드 정렬) | 🎨 UI |

---

### 📌 2026.03.04 (`Instruction_260304.md`) — 11개 Task

| Task | 핵심 내용 | 분류 |
|------|----------|------|
| 1~3 | **2D Area Scan XY 그래프**: `scatter` 차트(Planned Path 점선 + Scanned 초록 도트), 좌/우 2열 분리(`auto_1fr`), 캔버스 오버플로우 수정(`min-w-0`) | 🚀 신규 |
| 4~6 | **모바일 최적화**: 접속 가이드(`192.168.97.59:8888`), `.card-responsive` min-width 제거, 전역 헤더 반응형(`flex-col md:flex-row`) 변환, 패널 헤더 2행 배치 | 📱 반응형 |
| 7~8 | GUI Design Guide 준수: Tweak 버튼 그리드(`1fr_80px_1fr` 확장), 전역 헤더 버튼 표준화(`text-xs py-1 px-2 rounded`) | 🎨 표준화 |
| **9** | **입력 필드 색상 버그**: 새로고침 시 흰색 → 글로벌 `input, select` 다크 테마 CSS `!important` 강제 적용, `.input-dark-tab` 클래스 정의 추가 | 🐛 버그 |
| 10~11 | **팝업 아이콘 버튼** 추가(External Link 아이콘), 카드/헤더 `onclick` 제거 → 전용 버튼으로 모달 진입 경로 한정 | 🎨 UX |

---

### 📌 현재 세션 (2026.03.04 후속)

| 내용 | 상세 | 분류 |
|------|------|------|
| **localStorage 상태 영속화** | `saveAppState()` / `loadAppState()` 구현: `axesConfig`, `sequenceSteps`, `notepad` 자동 저장/복원, notepad `oninput` 자동 저장 | 🚀 신규 |

---

## 🏗️ 주요 산출물 목록

### 핵심 소스 파일

| 파일 | 역할 | 최초 생성 |
|------|------|----------|
| `kohzuApp/opi/dashboard.html` | **메인 6축 통합 대시보드** (모든 기능의 집합체) | 02.26 |
| `kohzuApp/opi/motor_popup.html` | **모터 상세 제어 모달 템플릿** (fetch로 동적 로드) | 02.26 |
| `kohzuApp/opi/web_gateway.py` | **Python WebSocket Gateway** (EPICS ↔ 브라우저 중계, API 서버) | 02.19 |
| `kohzuApp/opi/motorx_all.html` | 단일 축 제어용 페이지 (Phase 2, 현재 dashboard로 대체) | 02.19 |
| `kohzuApp/opi/gen_dashboard.py` | Dashboard HTML 자동 생성 스크립트 (Phase 4~5, 이후 직접 수정으로 전환) | 02.26 |

### 스테이지 설정 파일 (8종)

`kohzuApp/opi/stages/` 폴더:

| 파일명 | 타입 | EGU | MRES |
|--------|------|-----|------|
| `XA07A-L202.json` | Linear | mm | 0.0005 |
| `XA05A-L202.json` | Linear | mm | 0.0005 |
| `XA05A-R102.json` | Linear | mm | 0.00025 |
| `RA04A-W01.json` | Rotation | deg | 0.002 |
| `RA07A-W02.json` | Rotation | deg | 0.002 |
| `SA05A-R2B01.json` | Goniometer | deg | 0.0000637 |
| `ZA05A-W101.json` | Vertical | mm | 0.00025 |
| `ZA07A-V1F01.json` | Vertical | mm | 0.001 |

### 문서 (`docs/`)

| 파일 | 내용 |
|------|------|
| `GUI_Design_Guide.md` | UI 설계 표준 규격서 (패널 헤더, 버튼, 입력 필드, LED, 그리드 등) |
| `Web_Usage_Guide.md` | 시스템 운용 가이드 (IP, IOC, Gateway, 방화벽) |
| `README.md` | 빌드 및 설치 가이드 |
| `Project_Development_History.md` | 본 문서 (개발 이력 종합 정리) |
| `Instruction.md` | 작업지시 메인 문서 (표준 템플릿 포함) |
| `Instruction_daily/` | 일별 상세 기록 14개 파일 |
| `XA07A-L202_Control_Guide.md` | 스테이지 제어 가이드 (기준 템플릿) |
| `RA04A-W01_Control_Guide.md` | 회전 스테이지 제어 가이드 |
| `SA05A-R2B01_Control_Guide.md` | 고니오미터 제어 가이드 |
| `XA05A-R102_Control_Guide.md` | 선형 스테이지 제어 가이드 |
| `XA05A-L202_Control_Guide.md` | 선형 스테이지 제어 가이드 |
| `ZA05A-W101_Control_Guide.md` | 수직 스테이지 제어 가이드 |

### EPICS IOC 설정

| 파일 | 내용 |
|------|------|
| `iocBoot/iocKOHUZ_ALV1/st.cmd` | IOC 시작 스크립트 (6축 확장) |
| `iocBoot/iocKOHUZ_ALV1/motor.substitutions` | 6축 레코드 템플릿 |
| `KOHUZ_ALV1App/Db/KOHZU_Motor.db` | 모터 레코드 DB 템플릿 |

---

## 🔑 핵심 기술 결정 사항

### 1. 아키텍처 변천

| 시점 | 아키텍처 | 이유 |
|------|----------|------|
| 초기 | Phoebus OPI (XML) | EPICS 표준 GUI 도구 |
| 02.19 | 단일 HTML + WebSocket | Chrome 접근성, 모바일 지원 |
| 02.26 | `gen_dashboard.py` 자동 생성 | 6축 템플릿 일괄 관리 |
| 03.02 | `fetch()` 동적 로드 | 모달 템플릿 유지보수 분리 |

### 2. 상태 관리 체계

| 계층 | 도구 | 용도 |
|------|------|------|
| EPICS IOC | PV (Process Variable) | 실시간 하드웨어 상태 |
| 서버 | `sessions/` 파일 | 전체 세션 백업/복원 |
| 클라이언트 | `localStorage` | 페이지 새로고침 간 상태 영속화 |
| 클라이언트 | `axesConfig[]` 배열 | 런타임 스테이지 설정 메모리 |

### 3. 연결 상태 감지 3단계

| 상태 | 감지 방법 | LED 색상 |
|------|----------|----------|
| 정상 (Connected) | WebSocket 연결 + MSTA 정상 | 🟢 Green |
| HW 장애 (Problem) | `MSTA` Bit 9 (`RA_PROBLEM`, 512) | 🔴 Red |
| 통신 단절 | WebSocket 끊김 / CA 미연결 | ⚪ Gray |

### 4. GUI Design Guide 핵심 규격

| 항목 | 표준값 |
|------|--------|
| 패널 헤더 배경 | `bg-slate-700/50` |
| 입력 필드 너비 | `80px` 고정 |
| 입력 필드 높이 | `22px` 고정 |
| 입력 필드 배경 | `#0f172a` (bg-slate-900) |
| 텍스트 정렬 | `text-right` |
| 뷰어 라벨 색상 | `text-green-400` |
| 입력 폼 색상 | `text-white` |
| 버튼 표준 | `text-xs font-bold py-1 px-2 rounded uppercase` |
| STOP 버튼 | `bg-yellow-600` |
| 그리드 라벨 폭 | `80px` |

---

## 🐛 주요 버그 해결 이력

| 날짜 | 증상 | 원인 | 해결 |
|------|------|------|------|
| 02.19 | Step 8 `$4: unbound variable` | `check_hw_limit` 함수의 미사용 4번째 인자 참조 | 주석 처리 |
| 02.20a | STOP 버튼에 "0" 표시 | `data-pv` 속성으로 PV 값이 텍스트를 덮어씀 | `data-pv` 제거 |
| 02.20a | `caget DESC` 빈값 | DB 템플릿에 `field(DESC)` 누락 | DB 파일 수정 + make |
| 02.26a | 접속 직후 Disconnected | 5개 미연결 모터 PV 타임아웃으로 IOLoop 블로킹 | 타임아웃 0.01초 최적화 |
| 02.26a | 모달 PV 안 읽힘 | JS 초기화 순서 → `ReferenceError` | `EPICSController` 선 생성 |
| 02.26a | 모달 데이터 미반영 | `data-tpl-pv` 스킵 로직 | 스킵 제거 |
| 03.01 | JSON 업로드 무반응 | DMOV 역방향 로직 (`!=1` vs `==1`) | 조건문 수정 |
| 03.01 | 일부 파라미터 미적용 | 하드코딩 12개 필드만 전송 | `Object.entries` 동적 루프 |
| 03.02a | MSTA LED 미작동 | 비트 번호 오류(0-5 vs 1,9,10), CSS 미정의 | 표준 비트 교정 + `.led` 사용 |
| 03.04 | 입력 필드 새로고침 시 흰색 | `.input-dark-tab` 클래스 미정의 | 글로벌 CSS `!important` 강제 |

---

## 📊 통계 요약

| 항목 | 수치 |
|------|------|
| 총 작업 일수 | 14일 (주말 포함) |
| 총 Task 수 | 약 120+ 건 |
| 생성된 소스 파일 | 5개 (HTML 3, Python 2) |
| 생성된 JSON 설정 | 8개 |
| 생성된 문서 | 12+ 개 |
| 수정된 EPICS 설정 | 3개 (st.cmd, Motor.db, substitutions) |
| 해결된 주요 버그 | 10+ 건 |
| GUI Design Guide 규칙 | 8개 섹션 |
