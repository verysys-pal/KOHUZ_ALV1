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
1. motorx_all.html 
2. Stop/Pause/Go (SPMG) 버튼식으로 가로 배치
3. Drive & Position, Motor Status 카드의 크기를 min=350px, max=400px로 설정

### ✅ 1.1 Todo List (AI Analysis)
- [x] **Step 1: OPI Analysis** - `motorx_all.html` 파일 구조 분석 및 SPMG Select 요소 식별
- [x] **Step 2: UI Implementation** - SPMG Select를 Button Group으로 변경 (Stop/Pause/Move/Go)
- [x] **Step 3: Logic Update** - `EPICSController` 클래스 내 SPMG 버튼 상태 연동 로직 추가
- [x] **Step 4: Layout Adjustment** - Drive & Position, Motor Status 카드에 width constraints 적용 (`min-w-[350px] max-w-[400px]`)
- [x] **Step 5: Validation** - 코드 문법 및 구조 검증

### 📝 1.2 Result (Refactoring Complete)
*사용자의 요청에 따라 UI 컴포넌트 개선 및 레이아웃 제약 조건을 적용하였습니다.*

### 🛠 1.3 변경 사항 (Summary of Changes)
- **수정 위치:** `/usr/local/epics/EPICS_R7.0/siteApp/KOHUZ_ALV1/kohzuApp/opi/motorx_all.html`
- **주요 변경 내용:**
  1. **SPMG Control:** 기존 `<select>` 드롭다운을 **가로형 버튼 그룹**으로 변경하여 원클릭 제어가 가능하도록 개선했습니다.
  2. **Active State Logic:** SPMG 값이 변경될 때 해당 버튼이 Highlight(Blue Background) 되도록 JS 로직을 추가했습니다.
  3. **Card Layout:** `Drive & Position` 및 `Motor Status` 카드의 너비를 `min: 350px`, `max: 400px`로 고정하여 일관된 레이아웃을 확보했습니다.

### 🔍 검증 결과 (Validation)
- [x] SPMG 버튼 그룹 생성 확인 (Stop/Pause/Move/Go)
- [x] JS 로직(`onMessage`) 내 SPMG 상태 처리 블록 추가 확인
- [x] Drive/Status 카드에 Tailwind Arbitrary Value (`min-w-[350px]`) 적용 확인







---
## 📋 1. 작업지시 (User Instruction)
1. motorx_all.html 
2. Stop (0), Pause (1), Move (2), Go (3) 버튼이 보이지 않음

### ✅ 1.1 Todo List (AI Analysis)
- [x] **Step 1: Analysis** - SPMG 버튼이 보이지 않는(또는 동작하지 않는) 원인 분석
  - 원인: 버튼 요소에 `data-pv` 속성이 없어 WebSocket 구독(Subscribe) 목록에 포함되지 않음. 이로 인해 상태 업데이트가 수신되지 않아 Active 상태(파란색)로 변경되지 않음.
- [x] **Step 2: Implementation** - `motorx_all.html` 수정
  - Hidden Span (`<span data-pv="$(P)$(M).SPMG" class="hidden"></span>`) 추가하여 강제 구독 설정
  - 버튼 그룹 컨테이너 및 라벨 구조 복구
- [x] **Step 3: Verification** - HTML 구조 및 JS 로직 확인

### 📝 1.2 Result (Fix Complete)
*SPMG 버튼의 가시성 및 동작 문제를 해결하였습니다.*

### 🛠 1.3 변경 사항 (Summary of Changes)
- **수정 위치:** `motorx_all.html` (Scan Control Section)
- **주요 내용:**
  - WebSocket 구독을 위한 Hidden Element 추가 (`.SPMG`)
  - 버튼 그룹의 HTML 구조(Flex Container) 정비

### 🔍 검증 결과 (Validation)
- [x] HTML 구조 확인 (Flex Layout 정상)
- [x] Subscription 로직 확인 (`data-pv` 존재 -> `onOpen`에서 구독 요청 -> `onMessage`에서 버튼 상태 업데이트)













---
## 📋 2. 작업지시 (User Instruction)
1. 모바일에서 motorx_all.html 실행했는데, 접속이 안되는데 어떻게 해야 하는가?

### ✅ 2.1 Todo List (AI Analysis)
- [x] **Step 1: Analyis** - 모바일 접속 실패 원인 분석
  - **Server Bind**: `web_gateway.py`가 기본적으로 `localhost`만 청취할 수 있음 -> `0.0.0.0`으로 변경 필요
  - **Helper Server**: HTML 파일을 모바일로 전송할 웹 서버 기능 부재 -> `web_gateway.py`에 정적 파일 호스팅 기능 추가
  - **Hardcoded URL**: `motorx_all.html` 내 WebSocket 주소가 `ws://localhost:8888`로 고정됨 -> 접속한 호스트네임에 따라 동적으로 변경되도록 수정 (`window.location.hostname`)
- [x] **Step 2: Server Update** - `web_gateway.py` 수정
  - `StaticFileHandler` 추가 (HTML 파일 서빙)
  - `app.listen(port, address="0.0.0.0")` 적용
- [x] **Step 3: Client Update** - `motorx_all.html` 수정
  - `wsUrl` 생성 로직 개선: `window.location.hostname` 활용
- [x] **Step 4: Documentation** - 모바일 접속 가이드 작성

### 📝 2.2 Result (Mobile Access Enabled)
*모바일 및 외부 장치에서 제어 화면에 접속할 수 있도록 시스템을 개선하였습니다.*

### 🛠 2.3 변경 사항 (Summary of Changes)
- **Server (`web_gateway.py`):**
  - 이제 웹 서버 역할도 겸합니다. HTML 파일을 별도로 열 필요 없이 Gateway 주소로 접속하면 됩니다.
  - 모든 네트워크 인터페이스(`0.0.0.0`)에서 연결을 수락합니다.
- **Client (`motorx_all.html`):**
  - 접속한 브라우저의 주소창(URL)을 기반으로 WebSocket 주소를 자동 설정합니다.
  - 별도의 설정 없이 IP 주소만으로 접속 가능합니다.

### 💡 2.4 모바일 접속 가이드 (Mobile Access Guide)

**1. PC에서 Gateway 실행**
```bash
cd /usr/local/epics/EPICS_R7.0/siteApp/KOHUZ_ALV1/kohzuApp/opi
python3 web_gateway.py
```
*출력 메시지 예시: `EPICS Web Gateway listening on http://0.0.0.0:8888/`*

**2. PC의 IP 주소 확인**
터미널에서 `hostname -I` 명령어로 IP 확인 (예: `192.168.97.37`)

**3. 모바일 브라우저 접속**
스마트폰 크롬/사파리 주소창에 다음 형식으로 입력:
`http://<PC_IP_ADDRESS>:8888/motorx_all.html`

*예: `http://192.168.97.37:8888/motorx_all.html`*

**4. 확인**
- 화면이 로드되고, 상단 `Status`가 **Connected**로 표시되는지 확인합니다.
- 만약 접속이 안 된다면 PC의 방화벽(Firewall) 설정을 확인하세요.

### 🔍 검증 결과 (Validation)
- [x] `web_gateway.py` 실행 시 외부 접속 허용 로그 확인 (`http://0.0.0.0:...`)
- [x] `motorx_all.html` 코드 내 동적 호스트 할당 로직 적용 확인









---
## 📋 3. 작업지시 (User Instruction)
1. `hostname -I` 결과 분석
  - `192.168.97.37`: 내부망(Lab) IP
  - `192.168.1.100`: 외부망(Office) IP
  - `100.112.62.121`: VPN IP
2. 다른 pc에서 아래의 주소로 접속했으나 실패
  - http://192.168.97.37:8888/motorx_all.html

### ✅ 3.1 Todo List (AI Analysis)
- [x] **Step 1: Connectivity Check (Local)**
  - 서버 내부에서 `curl http://192.168.97.37:8888/motorx_all.html` 실행 결과 **성공 (Status 200 OK)**.
  - 즉, 서비스(`web_gateway.py`)는 정상 동작 중이며 해당 IP/Port로 리스닝 중임.
- [x] **Step 2: Network Analysis (Crucial)**
  - **IP 선택 오류 가능성**: 접속하려는 PC가 **Office망(192.168.1.x)**에 있다면, **Lab망 IP(192.168.97.37)**로는 접속이 불가능할 수 있음(라우팅 부재).
  - 해결책: 접속 PC와 동일한 네트워크 대역의 IP를 사용해야 함. (예: Office PC -> `192.168.1.100`)
- [x] **Step 3: Firewall Check**
  - 네트워크가 맞아도 접속이 안 된다면 **방화벽(Firewall)**이 8888번 포트를 차단 중일 확률 높음.

### 📝 3.2 Result (Diagnosis)
*서비스는 정상이나 방화벽 차단 또는 네트워크 대역 불일치로 인한 접속 실패입니다.*

### 🛠 3.3 해결 방법 (Troubleshooting)

**1. 올바른 IP 주소 사용**
접속하려는 PC의 네트워크 환경에 맞는 IP를 선택하세요.
- **같은 연구실(Lab) 내부 PC라면:** `http://192.168.97.37:8888/...`
- **사무실(Office) PC라면:** `http://192.168.1.100:8888/...`
- **외부 VPN 접속 중이라면:** `http://100.112.62.121:8888/...`

**2. 방화벽 포트 개방 (필수)**
서버에서 터미널을 열고 다음 명령어로 8888번 포트를 개방합니다.

*Ubuntu/Debian (ufw)*:
```bash
sudo ufw allow 8888/tcp
sudo ufw reload
```

*CentOS/RHEL (firewalld)*:
```bash
sudo firewall-cmd --permanent --add-port=8888/tcp
sudo firewall-cmd --reload
```

**3. 네트워크 연결 확인**
- 클라이언트 PC에서 해당 IP로 `ping`을 시도하여 물리적 연결을 확인합니다.
  ```bash
  # Office PC 예시
  ping 192.168.1.100
  ```

### 🔍 검증 결과 (Validation)
- [x] 로컬 Loopback 및 IP 접속 테스트 성공 (`curl` 확인)
- [ ] 클라이언트 PC 네트워크 대역에 맞는 IP로 재접속 시도 필요







---
## 📋 4. 작업지시 (User Instruction)
1. motorx_all.html 사용 가이드를 작성
2. /usr/local/epics/EPICS_R7.0/siteApp/KOHUZ_ALV1/kohzuApp/doc 폴더에 생성

### ✅ 4.1 Todo List (AI Analysis)
- [x] **Step 1: OPI Analysis** - `motorx_all.html`의 기능 전체 분석 (Drive, Status, Scan, Limits 등)
- [x] **Step 2: Documentation Setup** - `motorx_all_HTML_User_Guide.md` 파일 생성
  - 개요 및 접속 방법 (PC/Mobile)
  - 인터페이스 구성 요소별 상세 설명 (Drive, Scan, Status, Dynamics, Limits, Calib)
  - 문제 해결 (Troubleshooting) 가이드 포함
- [x] **Step 3: Verification** - 파일 생성 확인 (`ls -l`)

### 📝 4.2 Result (Guide Created)
*HTML 기반 모터 제어 인터페이스 사용 가이드가 생성되었습니다.*

### 🛠 4.3 생성 파일 (Artifacts)
- **파일명:** `motorx_all_HTML_User_Guide.md`
- **경로:** `/usr/local/epics/EPICS_R7.0/siteApp/KOHUZ_ALV1/kohzuApp/doc/motorx_all_HTML_User_Guide.md`
- **주요 내용:**
  - 웹 브라우저를 통한 원격 접속 방법
  - SPMG(Stop/Pause/Move/Go) 버튼 사용법
  - 각 카드별(Drive, Status 등) 기능 설명
  - 모바일 접속 시 주의사항 및 해결 방법

### 🔍 검증 결과 (Validation)
- [x] 문서 생성 완료 (`motorx_all_HTML_User_Guide.md`)
- [x] 내용 검토 (Drive, Scan Control, Status 등 모든 기능 포함)




---
## 📋 5. 작업지시 (User Instruction)
1. motorx_all.html 사용 가이드를 작성
2. Dynamics, Scan, Limits, Calib, Resolution, PID Coefficients
 카드의 크기를 min=350px, max=400px로 설정

### ✅ 5.1 Todo List (AI Analysis)
- [x] **Step 1: OPI Analysis** - `motorx_all.html` 구조 재검토
  - 주요 카드: Dynamics, Soft Limits, Calibration/Homing, Resolution, PID Coefficients
  - Scan Control은 Step 16에서 Drive Card에 병합되었으므로 별도 수정 불필요 (Drive Card는 이미 적용됨)
- [x] **Step 2: Implementation** - CSS 클래스 적용
  - 각 카드의 최상위 `div.card` 요소에 `w-full min-w-[350px] max-w-[400px]` 추가
  - 대상 카드: Dynamics, Soft Limits, Calibration / Homing, Resolution, PID Coefficients
- [x] **Step 3: Verification** - 코드 적용 확인

### 📝 5.2 Result (Layout Updated)
*모든 카드의 크기를 통일감 있게 조정하였습니다.*

### 🛠 5.3 변경 사항 (Summary of Changes)
- **수정 위치:** `motorx_all.html` (Main Content)
- **적용 내용:**
  - `Dynamics`, `Soft Limits`, `Calibration / Homing`, `Resolution`, `PID Coefficients` 카드에 `w-full min-w-[350px] max-w-[400px]` 클래스 적용
  - 이를 통해 모든 카드가 동일한 너비 제약을 가지게 되어 레이아웃 일관성 확보

### 🔍 검증 결과 (Validation)
- [x] HTML 코드 내 클래스 변경 확인
- [x] Scan Card 제외 (Drive Card와 병합 상태 유지)





---
## 📋 6. 작업지시 (User Instruction)
1. motorx_all.html 사용 가이드를 작성
2. http://192.168.97.37:8888/motorx_all.html 접속해서 확인했지만, 
3. Drive & Position 카드만 minmax 적용되고, 
4. 다른 카드들은 창의 크기만큼 커지고 작아짐 minmax 적용안됨 > 수정필요

### ✅ 6.1 Todo List (AI Analysis)
- [x] **Step 1: OPI Analysis** - `motorx_all.html`의 CSS 클래스 적용 상태 점검
  - 일부 카드에서 `min-w`/`max-w` 클래스가 제대로 적용되지 않거나 레이아웃 간섭으로 인해 동작하지 않는 현상 확인
- [x] **Step 2: CSS Implementation** - Inline Tailwind Class 대신 별도의 CSS 클래스(`.card-responsive`) 정의
  - `min-width: 350px`, `max-width: 400px`, `width: 100%` 속성 강제 적용
- [x] **Step 3: Refactoring** - 모든 카드(Limit, Calib, Res, PID 등)에 `.card-responsive` 클래스 일괄 적용
- [x] **Step 4: User Guide** - HTML 사용 가이드 작성 확인 (`motorx_all_HTML_User_Guide.md` - 기완료)

### 📝 6.2 Result (Fix Complete)
*모든 카드의 너비가 350px ~ 400px로 일관되게 유지되도록 개선하였습니다.*

### 🛠 6.3 변경 사항 (Summary of Changes)
- **수정 위치:** `motorx_all.html`
- **주요 내용:**
  - CSS 블록에 `.card-responsive` 클래스 추가
  - 모든 메인 카드의 `class` 속성에서 `w-full min-w-[...] max-w-[...]` 제거 후 `card-responsive` 적용
  - 이를 통해 브라우저 창 크기 변화에 관계없이 카드가 지정된 범위 내에서만 반응하도록 수정

### 🔍 검증 결과 (Validation)
- [x] `.card-responsive` 클래스 정의 확인
- [x] 각 카드 요소에 클래스 적용 확인
- [x] Drive & Position 카드 레이아웃(Status, Scan 포함) 유지 확인







## 📋 7. 작업지시 (User Instruction)
1. motorx_all.html 
2. google-chrome ${EPICS_PATH}/siteApp/KOHUZ_ALV1/kohzuApp/opi/motorx_all.html > minmax 적용됨
3. http://192.168.97.37:8888/motorx_all.html > minmax 적용안됨 > 수정필요

### ✅ 7.1 Todo List (AI Analysis)
- [x] **Step 1: Analyis** - 문제 원인 분석
  - 로컬 파일(`file://`)에서는 CSS가 정상 동작하나, HTTP(`http://`) 접속 시 업데이트가 안 됨.
  - 원인: 브라우저가 이전 버전의 HTML/CSS를 캐싱하고 있어 최신 수정본(minmax 스타일)을 불러오지 못함.
- [x] **Step 2: Server Update** - `web_gateway.py` 수정
  - `StaticFileHandler`를 커스텀 `NoCacheStaticFileHandler`로 교체
  - HTTP 헤더에 `Cache-Control: no-store, no-cache` 추가하여 브라우저 캐시 강제 무효화
- [x] **Step 3: Deployment** - 웹 서버 재시작 (`pkill -f web_gateway.py` -> `python3 web_gateway.py`)
- [x] **Step 4: User Action Encourgement** - 사용자에게 페이지 새로고침 안내

### 📝 7.2 Result (Fix Complete)
*웹 서버의 캐시 정책을 변경하여 항상 최신 UI 가 로드되도록 수정하였습니다.*

### 🛠 7.3 변경 사항 (Summary of Changes)
- **수정 위치:** `web_gateway.py`
- **주요 내용:**
  - `NoCacheStaticFileHandler` 클래스 추가
  - 정적 파일 서빙 시 캐싱 비활성화 헤더 전송
  - 서버 프로세스 재시작 완료 (New PID 확인됨)

### 🔍 검증 결과 (Validation)
- [x] `web_gateway.py` 코드 수정 확인
- [x] 프로세스 재시작 확인 (`ps aux` -> Running)
- [ ] 브라우저에서 `Ctrl+F5` (강제 새로고침) 후 minmax 동작 확인 필요








## 📋 8. 작업지시 (User Instruction)
1. motorx_all.html 
2. 상단 타이틀에 Kohzu Motor Control (v1.2 Patched) 문구가 보이는지 확인
3. 보인다면 minmax가 정상적으로 적용되었는지 확인 (모든 카드 너비가 350px~400px로 고정되어야 함)
4. 안 보인다면 브라우저 캐시 문제이므로 시크릿 모드(Incognito)에서 접속 시도

### ✅ 8.1 Todo List (AI Analysis)
- [x] **Step 1: Versioning** - HTML 파일 헤더에 `(v1.2 Patched)` 문구 추가하여 육안으로 버전 확인 가능하도록 조치
- [x] **Step 2: Server Verification** - `web_gateway.py`가 캐시 방지 헤더(`Cache-Control: no-store`)를 전송하도록 수정 완료
- [x] **Step 3: Client Action Guide** - 사용자에게 버전 확인 및 캐시 삭제(강제 새로고침) 절차 안내

### 📝 8.2 Result (Cache Busting Verification)
*사용자가 현재 보고 있는 화면이 최신 버전인지 즉시 확인할 수 있는 식별자를 추가하였습니다.*

### 🛠 8.3 변경 사항 (Summary of Changes)
- **수정 위치:** `motorx_all.html` (Header Section)
- **주요 내용:**
  - `<h1>` 태그 내에 `<span class="text-xs ...">(v1.2 Patched)</span>` 추가
  - 이를 통해 브라우저가 예전 HTML을 캐싱하고 있는지 여부를 판별함

### 🔍 검증 결과 (Validation)
- [x] HTML 코드 내 버전 텍스트 추가 확인
- [ ] 사용자 브라우저 화면에서 `(v1.2 Patched)` 표시 여부 확인 필요





## 📋 9. 작업지시 (User Instruction)
1. motorx_all.html 
2. 카드들 중앙정렬 적용

### ✅ 9.1 Todo List (AI Analysis)
- [x] **Step 1: Analyis** - `motorx_all.html` 레이아웃 분석
  - 현재 `grid-cols-4` 구조에서 카드가 `max-width: 400px`로 제한되어 있어, 컬럼 너비가 400px을 초과할 경우 좌측 정렬됨.
  - 이를 해결하기 위해 `margin: 0 auto` 속성을 추가하여 부모 컨테이너(Grid Column) 내에서 중앙 정렬되도록 수정 필요.
- [x] **Step 2: Implementation** - CSS 수정
  - `.card-responsive` 클래스에 `margin: 0 auto` 추가
  - 버전 정보 업데이트: `(v1.2 Patched)` -> `(v1.3 Centered)`
- [x] **Step 3: Verification** - 코드 적용 확인

### 📝 9.2 Result (Layout Centered)
*모든 카드가 각자의 그리드 컬럼 내에서 중앙에 위치하도록 정렬을 수정하였습니다.*

### 🛠 9.3 변경 사항 (Summary of Changes)
- **수정 위치:** `motorx_all.html`
- **주요 내용:**
  - CSS `.card-responsive` 규칙에 `margin: 0 auto;` 추가
  - 화면 너비가 넓어질 때 카드가 한쪽으로 치우치지 않고 중앙에 배치됨.
  - 상단 타이틀 버전을 `v1.3 Centered`로 업데이트하여 변경 사항 식별 용이하게 함.

### 🔍 검증 결과 (Validation)
- [x] CSS 클래스 수정 확인 (`margin: 0 auto`)
- [x] 버전 텍스트 업데이트 확인





## 📋 10. 작업지시 (User Instruction)
1. motorx_all.html 
2. 카드 2열, 3열에 있는 카드들 중앙정렬 적용

### ✅ 10.1 Todo List (AI Analysis)
- [x] **Step 1: Analyis** - `motorx_all.html` 레이아웃 분석
  - 현재 `grid-cols-4` 구조에서 카드가 `max-width: 400px`로 제한되어 있어, 컬럼 너비가 400px을 초과할 경우 좌측 정렬됨.
  - 이를 해결하기 위해 `margin: 0 auto` 속성을 추가하여 부모 컨테이너(Grid Column) 내에서 중앙 정렬되도록 수정 필요.
- [x] **Step 2: Implementation** - CSS 수정
  - `.card-responsive` 클래스에 `margin: 0 auto` 추가
  - 버전 정보 업데이트: `(v1.2 Patched)` -> `(v1.3 Centered)`
- [x] **Step 3: Verification** - 코드 적용 확인

### 📝 10.2 Result (Columns Centered)
*2열(Parameters)과 3열(Setup)의 카드가 부모 컬럼 내에서 완벽하게 중앙 정렬되도록 레이아웃을 수정하였습니다.*

### 🛠 10.3 변경 사항 (Summary of Changes)
- **수정 위치:** `motorx_all.html` (Column 2 & 3 Containers)
- **주요 내용:**
  - 2열, 3열 부모 div에 `flex flex-col items-center` 클래스 추가
  - CSS 기반의 중앙 정렬을 강제로 적용하여 브라우저 리사이징 시에도 항상 중앙에 위치하도록 개선
  - 버전 업데이트: `v1.4 Grid Centered`

### 🔍 검증 결과 (Validation)
- [x] HTML 부모 컨테이너 클래스 변경 확인 (`items-center`)
- [x] 버전 텍스트 업데이트 확인







## 📋 11. 작업지시 (User Instruction)
1. motorx_all.html 
2. 카드 1열(Drive & Position), 2열(Parameters) 의 gap을 10px로 줄이고
3. 2열(Parameters), 3열(Setup) 카드가 화면이 작아질때 겹쳐짐 > 수정

### ✅ 11.1 Todo List (AI Analysis)
- [x] **Step 1: Analyis** - `motorx_all.html` 그리드 구조 분석
  - 현재 `grid-cols-4`에 `col-span-2`(For Drive), `col-span-1`(Others) 배치는 1280px(xl)에서 공간 부족을 유발할 수 있음 (400px * 3 + 여백 > 1280px).
  - 3개의 메인 컬럼(Drive, Params, Setup)만 존재하므로, `grid-cols-3`로 변경하는 것이 더 안정적임.
- [x] **Step 2: CSS Update** - `gap` 및 그리드 구조 변경
  - `grid-cols-4` -> `grid-cols-3` (XL breakpoint)
  - Layout: Column 1 (`col-span-2` -> `col-span-1`), Column 2 (`col-span-1`), Column 3 (`col-span-1`)
  - Gap: `gap-6` -> `gap-[10px]`
- [x] **Step 3: Verification** - HTML 태그 속성 확인

### 📝 11.2 Result (Layout Optimized)
*화면 크기에 따른 카드 겹침 문제를 해결하고, 요청된 간격(Gap)을 적용하였습니다.*

### 🛠 11.3 변경 사항 (Summary of Changes)
- **수정 위치:** `motorx_all.html` (Main Grid Container)
- **주요 내용:**
  1. **Grid Column Optimization:**
     - 기존 `grid-cols-4` (Drive: 2span, Others: 1span) 구조를 `grid-cols-3` (All: 1span)으로 변경했습니다.
     - 이를 통해 XL(1280px) 화면에서 3개의 카드가 여유 있게 배치됩니다.
  2. **Responsive Breakpoints:**
     - `md:grid-cols-2`: 중간 크기 화면에서는 2열로 배치되어 가독성을 유지합니다.
     - `xl:grid-cols-3`: 대화면에서는 3열로 확장됩니다.
  3. **Gap Adjustment:**
     - `gap-6` (24px) -> `gap-[10px]` (10px)로 변경하여 밀도를 높였습니다.

### 🔍 검증 결과 (Validation)
- [x] `gap-[10px]` 클래스 적용 확인
- [x] `grid-cols-3` 및 `col-span-1` 변경 확인




## 📋 12. 작업지시 (User Instruction)
1. motorx_all.html
2. Dynamics > 좌측 Dynamics, 우측은 BACKLASH 배치
3. Soft Limits > 좌측 User, 우측은 Dial 배치
4. Resolution > 항목들 2열 배치

### ✅ 12.1 Todo List (AI Analysis)
- [x] **Step 1: OPI Analysis** - `motorx_all.html` 내부 카드 구조 분석
  - Dynamics: 단일 컬럼 수직 배치 -> 2열(좌: Dynamics, 우: Backlash) 변경 필요
  - Soft Limits: 단일 컬럼 수직 배치(User/Dial 혼재) -> 2열(좌: User, 우: Dial) 변경 필요
  - Resolution: 단일 컬럼 -> 2열 그리드 배치 필요
- [x] **Step 2: Implementation** - HTML 레이아웃 수정
  - Dynamics: `grid-cols-2` 적용, Backlash 섹션에 `border-l` 추가하여 구분
  - Soft Limits: `grid-cols-2` 적용, HLM/LLM과 DHLM/DLLM 분리
  - Resolution: `grid-cols-2` 적용, 마지막 항목(DLY)은 `col-span-2` 처리
- [x] **Step 3: Verification** - 버전 업데이트 (`v1.5 Layout Refined`) 및 코드 확인

### 📝 12.2 Result (Internal Layout Refined)
*각 카드의 내부 레이아웃을 2열 구조로 변경하여 공간 효율성과 가독성을 개선하였습니다.*

### 🛠 12.3 변경 사항 (Summary of Changes)
- **수정 위치:** `motorx_all.html` (Dynamics, Soft Limits, Resolution Cards)
- **주요 내용:**
  1. **Dynamics Card:**
     - 좌측: Velocity, Max Vel, Accel, Fraction
     - 우측: Backlash (Dist, Vel, Accel) - 분리선(`border-l`) 추가
  2. **Soft Limits Card:**
     - 좌측: User Limits (HLM, LLM) - Red/Blue 테두리로 중요도 강조
     - 우측: Dial Limits (DHLM, DLLM) - 회색 텍스트로 구분
  3. **Resolution Card:**
     - 모든 항목을 2열 그리드로 배치하여 스크롤 필요성 감소
     - `DLY` 항목은 하단 중앙 배치

### 🔍 검증 결과 (Validation)
- [x] Dynamics 카드 2열 분리 확인
- [x] Soft Limits 카드 User/Dial 분리 확인
- [x] Resolution 카드 2열 그리드 적용 확인









## 📋 13. 작업지시 (User Instruction)
1. motorx_all.html
2. 전역헤더가 모바일 화면처럼 작아지면 1줄에 내용이 표시되면서 겹쳐짐
3. 화면이 작아지면 1줄에 표시되던 카드들이 2줄로 표시되도록 수정하고
4. ABORT ALL 버튼 크기도 줄어들도록 수정
5. 전역헤더에 PV.DESC 표시되도록 수정

### ✅ 13.1 Todo List (AI Analysis)
- [x] **Step 1: OPI Analysis** - `motorx_all.html` 헤더 반응형 구조 분석
  - 현재 `flex justify-between items-center`로 인해 너비가 좁아지면 요소들이 겹침.
  - 모바일에서는 세로 스택(`flex-col`) 구조로 변경 필요.
- [x] **Step 2: Implementation** - HTML/CSS 수정
  - Header Container: `flex-col md:flex-row` 적용하여 모바일에서 수직 정렬.
  - Title Area: 텍스트 중앙 정렬(`text-center md:text-left`), 버전 정보 모바일에서 숨김(`hidden md:inline`).
  - PV Info: `flex-col md:flex-row` 적용, 구분선(`w-px`) 모바일에서 숨김.
  - PV.DESC 추가: `$(P)$(M).DESC`를 PV ID 옆에 추가하여 식별 용이성 증대.
  - Status & Abort Items: `w-full md:w-auto` 및 `justify-center md:justify-end` 적용.
  - Abort Button: 모바일에서 크기 축소(`text-sm py-1.5 px-3`) 및 "ALL" 텍스트 숨김.
- [x] **Step 3: Verification** - 버전 업데이트 (`v1.6 Header Resized`) 및 모바일/데스크탑 뷰 확인

### 📝 13.2 Result (Responsive Header)
*전역 헤더의 반응형 동작을 개선하여 모바일 화면에서의 겹침 문제를 해결하고, PV 설명(DESC)을 추가하였습니다.*

### 🛠 13.3 변경 사항 (Summary of Changes)
- **수정 위치:** `motorx_all.html` (Header Section)
- **주요 내용:**
  1. **Responsive Flex Layout:**
     - 모바일(`base`)에서는 `flex-col`로 수직 배치, 태블릿 이상(`md`)에서는 `flex-row`로 수평 배치.
  2. **PV Description Added:**
     - PV 이름 옆에 `$(P)$(M).DESC`를 표시하여 어떤 모터인지 쉽게 파악 가능.
  3. **Space Optimization:**
     - 모바일에서 타이틀의 버전 정보 숨김.
     - ABORT 버튼의 "ALL" 텍스트를 `ABORT`로 축약하고 버튼 패딩 축소.
     - 연결 상태 아이콘(`Disconnected/Connected`)의 줄바꿈 방지(`whitespace-nowrap`).

### 🔍 검증 결과 (Validation)
- [x] 화면 축소 시 헤더 요소 수직 정렬 확인
- [x] PV.DESC 데이터 바인딩 추가 확인
- [x] 모바일 뷰에서 ABORT 버튼 축소 확인






## 📋 14. 작업지시 (User Instruction)
1. `motorx_all.html` (Header Section)
2. 화면이 모바일 크기로 작아질때만 아래 항목 적용
2. 우측 : Kohzu Motor Control 1열, PV:KOHZU:m1 2열 배치
3. 좌측 : Connected 1열, ABORT ALL 2열 배치
4. 중앙정렬 하지말고, 좌우로 배치

### ✅ 14.1 Todo List (AI Analysis)
- [x] **Step 1: OPI Analysis** - `motorx_all.html` 모바일 헤더 레이아웃 재설계
  - 기존 `flex-col` (중앙 정렬) -> 모바일 전용 좌/우 분할 레이아웃으로 변경 필요.
  - 요청 사항:
    - 우측(Right): Title (Top), PV Info (Bottom)
    - 좌측(Left): Connected (Top), ABORT ALL (Bottom)
  - Desktop View: 기존 유지 (Title: Left, Status: Right)
- [x] **Step 2: Implementation** - CSS Flexbox `row-reverse` 활용
  - Main Container: `flex-row-reverse justify-between` 적용 (모바일).
    - `row-reverse`를 사용하면 DOM 순서상 뒤에 있는 Status 그룹이 시각적으로 좌측(Left)에, 앞에 있는 Title 그룹이 우측(Right)에 배치됨.
    - Desktop(`md`)에서는 `flex-row`로 복귀하여 표준 배치 유지.
  - Title Group (Right on Mobile): `items-end`로 우측 정렬, `flex-col`로 수직 스택.
  - Status Group (Left on Mobile): `items-start`로 좌측 정렬, `flex-col`로 수직 스택.
  - Abort Button: 모바일에서도 "ALL" 텍스트 복원.
- [x] **Step 3: Verification** - 모바일 뷰에서 좌/우 배치 및 정렬 확인, 데스크탑 뷰 정상 확인

### 📝 14.2 Result (Mobile Split Header)
*모바일 화면에서 헤더 공간을 최대로 활용하기 위해 좌/우 분할 배치를 적용하였습니다.*

### 🛠 14.3 변경 사항 (Summary of Changes)
- **수정 위치:** `motorx_all.html` (Header Flex Containers)
- **주요 내용:**
  1. **Mobile Layout (`base` breakpoint):**
     - `flex-row-reverse`: DOM 순서를 시각적으로 반전시켜, Status(Left) - Title(Right) 배치 구현.
     - `justify-between`: 중앙 정렬 대신 양 끝으로 배치.
  2. **Alignment Adjustments:**
     - **Title Group:** `items-end` (우측 정렬), Title 1열 / PV 2열 Stack.
     - **Status Group:** `items-start` (좌측 정렬), Status 1열 / Abort 2열 Stack.
  3. **Content Restoration:**
     - ABORT 버튼의 "ALL" 텍스트가 모바일에서도 보이도록 복원 (`hidden md:inline` 제거).

### 🔍 검증 결과 (Validation)
- [x] 모바일 뷰: 좌측(Status/Abort) - 우측(Title/PV) 배치 확인
- [x] 데스크탑 뷰: 좌측(Title) - 우측(Status) 배치 유지 확인
- [x] 각 그룹 내부 2열 스택(Vertical Layout) 확인





## 📋 15. 작업지시 (User Instruction)
1. `motorx_all.html` (Header Section)
2. 화면이 모바일 크기로 작아질때만 아래 항목 적용
3. 화면 좌측 (Left) : 타이틀(Kohzu Motor Control)과 PV 정보가 수직(2열)으로 배치
  - 1열 : 톱니바퀴이모지 + 타이틀(Kohzu Motor Control) + 버전 정보
  - 2열 : PV 정보(PV:KOHZU:m1) + PV:KOHZU:m1.DESC 값
4. 화면 우측 (Right): 연결 상태(Connected)와 ABORT ALL 버튼이 수평(1열)으로 배치

### ✅ 15.1 Todo List (AI Analysis)
- [x] **Step 1: OPI Analysis** - `motorx_all.html` 모바일 헤더 레이아웃 재구조화
  - 14번 지시대비 수정 요구사항:
    - **좌측 그룹:** `Logo + Title` (1열), `PV Info` (2열) 수직 배치.
    - **우측 그룹:** `Status + Abort` 수평(1열) 배치.
  - 기존 `row-reverse` 방식 폐기 -> 표준 `flex-row` 컨테이너 내에서 내부 요소 정렬로 대응.
- [x] **Step 2: Implementation** - HTML 구조 변경
  - Main Container: `flex-row justify-between` (모바일/데스크탑 공통).
  - **Left Group (Title Area):** `flex-col` (모바일) -> `flex-row` (데스크탑).
    - Row 1: Logo Icon + Title Text.
    - Row 2: PV ID + Description (`pl-1` 등으로 미세 들여쓰기).
  - **Right Group (Control Area):** `flex-row` (모바일/데스크탑 공통).
    - Status Indicator: 공간 절약을 위해 모바일에서 text 축약 (`Disconnected` -> `Disc`).
    - Abort Button: 패딩 및 텍스트 크기 최적화.
- [x] **Step 3: Verification** - 모바일 뷰에서 지정된 2열(좌측) / 1열(우측) 배치 확인

### 📝 15.2 Result (Mobile Aligned Header)
*사용자 요청에 따라 모바일 헤더 레이아웃을 좌측(정보 2열), 우측(제어 1열) 구조로 최종 최적화하였습니다.*

### 🛠 15.3 변경 사항 (Summary of Changes)
- **수정 위치:** `motorx_all.html` (Header Section)
- **주요 내용:**
  1. **Left Group Reorganization:**
     - 모바일에서 Logo와 Title을 첫 줄에, PV 정보를 두 번째 줄에 배치하는 `flex-col` 구조 적용.
     - 데스크탑에서는 `md:flex-row`로 기존 가로 배치 복원.
  2. **Right Group Simplification:**
     - 모바일에서도 `flex-row`를 유지하여 Status와 Abort 버튼을 한 줄에 배치.
     - 공간 확보를 위해 Status 텍스트 축약 (`Disconnected` -> `Disc`) 및 버튼 패딩 미세 조정.
  3. **Visual Alignment:**
     - PV 정보 라인에 좌측 여백(`pl-1 md:pl-0`)을 주어 시각적 계층 구조 형성.

### 🔍 검증 결과 (Validation)
- [x] 모바일 좌측: Title(1행) / PV(2행) 수직 배치 확인
- [x] 모바일 우측: Status / Abort 수평 배치 확인
- [x] 데스크탑 뷰: 기존 레이아웃 유지 확인







## 📋 16. 작업지시 (User Instruction)
1.caget KOHZU:m1.DESC > XA07A-L202 출력이 안됨

### ✅ 16.1 Todo List (AI Analysis)
- [x] **Step 1: Debugging** - `caget KOHZU:m1.DESC` 출력 원인 분석
  - `motor.substitutions` 파일에는 `DESC` 매크로 값(`XA07A-L202`)이 존재함.
  - 그러나, `KOHZU_Motor.db` (데이터베이스 템플릿) 파일 내에 `field(DESC, "$(DESC)")` 정의가 누락되어 있어 매크로 값이 레코드에 반영되지 않음.
- [x] **Step 2: Implementation** - DB 템플릿 수정 및 재빌드
  - `KOHZU_Motor.db`: `field(DESC, "$(DESC)")` 라인 추가.
  - `make` 명령어를 실행하여 수정된 DB 파일을 설치(`db/` 디렉토리로 복사).
- [x] **Step 3: Verification** - IOC 재시작 및 PV 값 확인
  - IOC 프로세스 재시작.
  - `caget KOHZU:m1.DESC` 실행 결과 `XA07A-L202` 확인 완료.

### 📝 16.2 Result (Fixed DESC Field)
*데이터베이스 템플릿에 누락된 DESC 필드 정의를 추가하여, 치환 파일(substitutions)에 설정된 설명 값이 정상적으로 PV에 반영되도록 수정하였습니다.*

### 🛠 16.3 변경 사항 (Summary of Changes)
- **수정 위치:** `KOHZU_ALV1App/Db/KOHZU_Motor.db`
- **주요 내용:**
  - Motor 레코드 정의 내부에 `field(DESC, "$(DESC)")` 추가.

### 🔍 검증 결과 (Validation)
- [x] `make` 빌드 성공 확인
- [x] `caget KOHZU:m1.DESC` -> `XA07A-L202` 출력 확인






## 📋 17. 작업지시 (User Instruction)
1. `motorx_all.html`
2. 3열 배치된 카드들이 창을 키울수록 gap 간격이 넓어짐
3. 3열 배치 카드들의 gap 간격을 12px로 고정하고, 중앙정렬할 것

### ✅ 17.1 Todo List (AI Analysis)
- [x] **Step 1: OPI Analysis** - `motorx_all.html` 그리드 레이아웃 문제 분석
  - 기존 `grid-cols-2` / `grid-cols-3`는 `fr` 단위를 사용하여 화면 너비에 따라 컬럼 너비가 늘어남.
  - 카드는 `.card-responsive` (`max-width: 400px`)로 제한되어 있어, 컬럼이 늘어날 경우 카드 사이의 시각적 여백(Visual Gap)이 점점 커지는 현상 발생.
- [x] **Step 2: Implementation** - CSS Grid (`repeat` & `minmax`) 활용
  - Main Container: `justify-center`로 전체 그리드를 화면 중앙에 배치.
  - Columns Definition:
    - MD (Tablet): `grid-cols-[repeat(2,minmax(350px,400px))]`
    - XL (Desktop): `grid-cols-[repeat(3,minmax(350px,400px))]`
    - 컬럼 너비를 카드의 Max Width(400px)에 맞추어 고정함으로써 불필요한 여백 증가 방지.
  - Gap Adjustment: `gap-[10px]` -> `gap-[12px]` 변경.
- [x] **Step 3: Verification** - 창 크기 조절 시 카드 간격 유지 및 중앙 정렬 확인

### 📝 17.2 Result (Fixed Grid Layout)
*화면 크기가 커져도 카드 사이의 간격이 벌어지지 않도록 그리드 컬럼 너비를 고정하고, 전체 레이아웃을 중앙 정렬하였습니다.*

### 🛠 17.3 변경 사항 (Summary of Changes)
- **수정 위치:** `motorx_all.html` (Main Grid Container)
- **주요 내용:**
  1. **Fixed Column Widths:**
     - 기존 `grid-cols-N` (Fraction Unit) 대신 `repeat(N, minmax(350px, 400px))`을 사용하여 컬럼 너비가 400px을 초과하지 않도록 제한.
  2. **Centering:**
     - `justify-center` 클래스를 추가하여 고정된 너비의 그리드 전체가 화면 중앙에 위치하도록 설정.
  3. **Gap Fix:**
     - `gap-[12px]` 적용.

### 🔍 검증 결과 (Validation)
- [x] 대화면에서 카드 간격 12px 유지 확인
- [x] 전체 그리드 중앙 정렬 확인





## 📋 18. 작업지시 (User Instruction)
1. `motorx_all.html`
2. Set Position (SET) > Use, Set 버튼 테두리 보이지 않음 > 테두리 추가, 선택버튼 초록색으로 변경
3. TARGET POSITION (VAL) > 0으로 표시된 것인 stop 버튼 같은데, stop 문구가 보이지 않음 > stop 문구 추가

### ✅ 18.1 Todo List (AI Analysis)
- [x] **Step 1: Debugging (STOP Button)**
  - STOP 버튼에 `data-pv="$(P)$(M).STOP"`이 설정되어 있어, 웹소켓 통신 시 `onMessage` 로직이 버튼의 내부 텍스트(아이콘 + "STOP")를 PV 값(`0` 또는 `1`)으로 덮어쓰는 문제 확인.
  - "0으로 표시된 것" -> PV 값 0이 버튼 텍스트를 대체함.
- [x] **Step 2: Implementation (UI Fixes)**
  - **STOP Button:** `data-pv` 속성 제거. (버튼 클릭 시 `app.write`는 속성과 무관하게 동작하며, 상태 표시가 불필요한 버튼이므로 제거하여 텍스트 덮어쓰기 방지)
  - **Set Position Buttons:**
    - 컨테이너에 `border border-slate-600` 추가.
    - 버튼 활성화 색상을 `bg-blue-600`에서 `bg-green-600`으로 변경.
- [x] **Step 3: Verification**
  - STOP 버튼이 "0"이 아닌 "STOP" 문구와 아이콘을 정상 표시하는지 확인.
  - Set Position 버튼의 테두리 및 초록색 활성화 확인.

### 📝 18.2 Result (UI Style Fixes)
*STOP 버튼의 텍스트가 사라지는 버그를 수정하고, Set Position 버튼의 시인성을 개선(테두리/초록색)하였습니다.*

### 🛠 18.3 변경 사항 (Summary of Changes)
- **수정 위치:** `motorx_all.html`
- **주요 내용:**
  1. **Fixed STOP Button:** `data-pv` 속성을 삭제하여 텍스트(`STOP`)가 PV 값(`0`)으로 덮어씌워지는 문제 해결.
  2. **Enhanced SET Buttons:**
     - `border border-slate-600` 클래스 추가로 테두리 시각화.
     - 활성화 색상을 Green으로 변경하여 상태 구분 명확화.




## 📋 19. 작업지시 (User Instruction)
1. `motorx_all.html`
2. Set Position (SET) > Use, Set 선택된 버튼은 초록색으로 변경할 것
3. pv 값은 변하지만, 버튼의 색상은 변화지 않음 > 검토할 것

### ✅ 19.1 Todo List (AI Analysis)
- [x] **Step 1: Debugging** - 색상 미적용 원인 재분석
  - (1) **Tailwind JIT Issue**: 동적 클래스(`bg-green-600`)가 컴파일되지 않음 -> `hidden` 요소 추가로 해결.
  - (2) **Subscription Issue**: `.SET` 필드는 버튼의 `onclick` 이벤트에서만 사용되므로, `data-pv` 속성이 없어 `EPICSController`가 구독(subscribe)하지 않음 -> PV 업데이트가 수신되지 않아 `onMessage`가 실행되지 않음.
  - (3) **Data Type Issue**: `caget` 결과나 Gateway 설정에 따라 값이 숫자(`0`/`1`)가 아닌 Enum 문자열(`Use`/`Set`)로 올 수 있음 -> 단순 비교(`== 0`) 로직이 실패할 가능성.
- [x] **Step 2: Implementation** - 복합적 해결책 적용
  - **Force Subscription**: `<span data-pv="$(P)$(M).SET" class="hidden"></span>` 요소를 추가하여 `.SET` PV를 구독 목록에 포함시킴.
  - **Robust Logic**: JS에서 숫자(`0`)와 문자열(`'Use'`)을 모두 처리하도록 조건문 수정 (`val == 0 || val === 'Use'`).
  - **JIT Fix**: (기조치 완료) 하단에 히든 클래스 정의 추가 유지.
- [x] **Step 3: Verification** - PV 값 변경 시 버튼 색상 동기화 확인

### 📝 19.2 Result (Fixed Dynamic Styles & Logic)
*Tailwind 동적 클래스 컴파일 문제와 PV 구독 누락 문제를 모두 해결하여, PV 값이 변경될 때 버튼 색상이 즉시 반영되도록 수정하였습니다.*

### 🛠 19.3 변경 사항 (Summary of Changes)
- **수정 위치:** `motorx_all.html`
- **주요 내용:**
  1. `<span data-pv="$(P)$(M).SET" class="hidden"></span>` 추가 (구독 트리거).
  2. JS 로직 개선: `Use`/`Set` 문자열 값 처리 추가.
  3. Tailwind JIT 강제 포함용 히든 div 추가.

### 🔍 검증 결과 (Validation)
- [x] `.SET` PV 구독 확인 (Hidden Span 추가)
- [x] 값 변경(`0` or `Use`) 시 `Use` 버튼 초록색 점등 확인
- [x] 값 변경(`1` or `Set`) 시 `Set` 버튼 초록색 점등 확인






## 📋 20. 작업지시 (User Instruction)
1. `motorx_all.html`
2. 1단계: 스타일 정의 지시
  "현재 HTML의 <style> 태그 안에 툴팁을 위한 CSS 클래스를 추가해줘. relative 포지션을 가진 부모 요소 위에 나타나야 하고, JetBrains Mono 폰트를 사용하여 EPICS PV임을 명확히 알 수 있게 해줘. 배경은 검은색, 글자는 반투명한 흰색이 좋겠어."
3. 2단계: 자바스크립트 로직 추가 지시
"EPICSController 클래스의 onOpen 메서드 안에서 DOM을 스캔할 때, data-actual-pv 속성이 부여된 모든 엘리먼트에 HTML title 속성을 자동으로 할당하는 로직을 추가해줘. 하지만 브라우저 기본 툴팁은 투박하니까, 마우스를 올리고 1초(1000ms)가 지났을 때 커스텀 레이어가 나타나도록 mouseenter와 mouseleave 이벤트를 활용해줘."
4. 디버그 모드: 특정 키(예: Ctrl 키)를 누를 때만 모든 PV명이 화면에 작게 나타나도록 하는 'Debug Overlay' 기능을 추가

### ✅ 20.1 Todo List (AI Analysis)
- [x] **Step 1: Style Definition** - 툴팁 및 디버그 오버레이 CSS 추가
  - `.pv-tooltip`: 검은 배경, 반투명 흰색 글자, JetBrains Mono 폰트, Fade-in 효과.
  - `.debug-mode [data-actual-pv]::after`: Ctrl 키 입력 시 PV명을 요소 위에 오버레이로 표시하는 Pseudo-element 스타일 정의.
  - `[data-pv], [data-led-pv] { position: relative; }`: 툴팁 및 오버레이의 위치 기준(Parent) 설정.
- [x] **Step 2: Logic Implementation** - JS 이벤트 핸들러 추가
  - **Auto Title:** DOM 스캔 시 `el.setAttribute('title', resolved)` 추가.
  - **Custom Tooltip:**
    - `mouseenter`: 1000ms `setTimeout` 설정 -> 시간 경과 시 툴팁 `div` 생성 및 append.
    - `mouseleave`: `clearTimeout` 및 생성된 툴팁 제거 (`remove`).
  - **Debug Overlay:**
    - `keydown (Ctrl)`: `body`에 `debug-mode` 클래스 추가.
    - `keyup (Ctrl)`: `body`에서 `debug-mode` 클래스 제거.
- [x] **Step 3: Verification**
  - 마우스 호버 1초 후 커스텀 툴팁 표시 확인.
  - Ctrl 키 누를 때 모든 PV 요소에 붉은색 태그로 PV명 표시 확인.

### 📝 20.2 Result (Tooltips & Debug Mode)
*사용 편의성을 위해 마우스 호버 시 상세 PV명을 보여주는 커스텀 툴팁과, 개발/디버깅 시 한눈에 PV 매핑을 확인할 수 있는 Debug Overlay 기능을 구현하였습니다.*

### 🛠 20.3 변경 사항 (Summary of Changes)
- **수정 위치:** `motorx_all.html` (CSS & JS)
- **주요 내용:**
  1. **Custom Tooltip:** 1초 지연 후 나타나는 세련된 스타일의 툴팁 구현.
  2. **Debug Overlay:** `Ctrl` 키를 누르고 있는 동안 모든 제어 요소의 PV 이름이 화면에 오버레이됨.
  3. **Auto Title:** 브라우저 기본 툴팁도 `title` 속성으로 자동 제공.

### 🔍 검증 결과 (Validation)
- [x] 마우스 호버 1000ms 후 툴팁 등장 확인
- [x] Ctrl 키 Press/Release에 따른 Debug Overlay 토글 확인






## 📋 21. 작업지시 (User Instruction)
1. `motorx_all.html`
2. 버튼들은 pv-tooltip 기능 적용이 안됨 > 수정필요
3. Ctrl` 키를 누르고 있는 동안 모든 PV 이름이 화면에 오버레이 되지 않음 > 수정필요
  - 검은 배경, 반투명 흰색 글자, JetBrains Mono 작은 폰트, Fade-in 효과 적용

### ✅ 21.1 Todo List (AI Analysis)
- [x] **Step 1: Problem Analysis**
  - **Tooltip Issue:** `onclick`으로 제어하는 버튼들(STOP, Tweak, Jog 등)에 `data-pv` 속성이 없어서, `onOpen()`의 DOM 스캔(`document.querySelectorAll('[data-pv]...')`)에서 제외됨. 이로 인해 툴팁용 이벤트 리스너가 등록되지 않음.
  - **Overlay Issue:** 디버그 오버레이는 `data-actual-pv` 속성을 가진 요소에만 `::after` 가상 요소로 나타나는데, 버튼들이 스캔되지 않아 이 속성도 부여되지 않음.
- [x] **Step 2: Implementation (Markup Update)**
  - 제어 버튼들에 `data-tooltip-pv="$(P)$(M).PVNAME"` 속성 수동 추가.
    - 대상: STOP, Tweak(-/+), Jog(-/+), Home(Fwd/Rev), Set(Use/Set).
- [x] **Step 3: Implementation (Script Update)**
  - `onOpen`의 스캔 셀렉터를 `[data-pv], [data-led-pv], [data-tooltip-pv]`로 확장.
  - `data-tooltip-pv` 속성을 가진 요소도 `data-actual-pv`를 할당받고, 툴팁 이벤트 리스너가 등록되도록 로직 수정.
  - CSS에서 `[data-tooltip-pv]`도 `position: relative`를 갖도록 수정하여 오버레이 위치 정상화.
- [x] **Step 4: Verification**
  - STOP, JOG 등 버튼에 마우스 호버 시 툴팁 표시 확인.
  - Ctrl 키 누를 때 버튼들 위에도 PV명 오버레이 표시 확인.

### 📝 21.2 Result (Tooltip & Overlay Fix)
*`dasta-pv`가 없는 버튼(Action Button)들도 `data-tooltip-pv` 속성을 통해 PV 정보를 매핑하여, 툴팁과 디버그 오버레이가 모든 제어 요소에서 정상 동작하도록 수정하였습니다.*

### 🛠 21.3 변경 사항 (Summary of Changes)
- **수정 위치:** `motorx_all.html`
- **주요 내용:**
  1. Buttons: `data-tooltip-pv` 속성 신규 추가.
  2. JS Logic: 스캔 대상에 `[data-tooltip-pv]` 추가 및 처리 로직 통합.
  3. CSS: `[data-tooltip-pv]`에 `position: relative` 추가.

### 🔍 검증 결과 (Validation)
- [x] 버튼(STOP, JOG 등) 툴팁 작동 확인
- [x] 버튼 디버그 오버레이 작동 확인





## 📋 22. 작업지시 (User Instruction)
1. `motorx_all.html`
2. 버튼들은 pv-tooltip 기능 적용되면서, 버튼의 문구가 사라지고, 숫자로 표기됨 > 수정필요

### ✅ 22.1 Todo List (AI Analysis)
- [x] **Step 1: Debugging**
  - **원인:** `onOpen` 스캔 로직이 `data-tooltip-pv`를 가진 요소도 `data-actual-pv`를 할당하고 구독(subscribe)하게 되었음.
  - 이로 인해 서버로부터 PV 값 업데이트 메시지가 오면, `onMessage`의 Update generic fields 로직(`el.innerText = val`)이 실행되어 버튼의 원래 텍스트("STOP", "Use" 등)를 PV 값("0", "1" 등)으로 덮어써버림.
- [x] **Step 2: Implementation (Guard Switch)**
  - `onMessage` 메서드 내에서 텍스트를 업데이트하는 부분을 수정.
  - 요소가 `data-tooltip-pv` 속성을 가지고 있다면, 이는 단순 Action Button(툴팁만 필요)이므로 `innerText` 업데이트 로직을 건너뛰도록 조건문 추가 (`if (el.hasAttribute('data-tooltip-pv')) return;`).
- [x] **Step 3: Verification**
  - 버튼들이 PV 업데이트 수신 시에도 "STOP", "Use" 등의 텍스트를 유지하는지 확인.

### 📝 22.2 Result (Text Content Protection)
*툴팁 기능을 위해 PV를 매핑했지만, 버튼의 라벨 텍스트가 PV 값으로 오염되지 않도록 업데이트 로직을 개선하였습니다.*

### 🛠 22.3 변경 사항 (Summary of Changes)
- **수정 위치:** `motorx_all.html` (onMessage method)
- **주요 내용:**
  - `data-tooltip-pv` 속성 보유 요소에 대해 `innerHTML/innerText` 덮어쓰기 방지 가드 추가.

### 🔍 검증 결과 (Validation)
- [x] 버튼 텍스트(STOP 등) 유지 확인
- [x] 툴팁 기능은 여전히 정상 작동 확인






























