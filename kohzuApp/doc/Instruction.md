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














# 2026.02.26
---
## 📋 1. 작업지시 (User Instruction)
1. 기존 단일 축 제어용 `motorx_all.html`을 확장하여 **총 6개의 축을 동시에 모니터링하고 제어할 수 있는 메인 대시보드 HTML**을 구축한다.
2. 각 축의 스테이지 파라미터(MRES, VELO, HLM 등)는 컨트롤 가이드를 바탕으로 **JSON 파일로 분리하여 생성**한다.
3. 메인 웹 페이지에서 **각 스테이지별 JSON 파일을 업로드**하여 해당 축의 파라미터를 동적으로 설정할 수 있도록 한다.
4. 메인 웹 페이지는 6개 축의 요약 정보(현재 위치, 간단한 구동)를 표시하며, **특정 축 클릭 시 기존 `motorx_all.html` 수준의 상세 제어창이 팝업(Modal)** 형태로 나타나도록 구현한다.

- **참조 파일:**
  - `kohzuApp/opi/motorx_all.html`
  - `XA07A-L202_Control_Guide.md`, `RA07A-W02_Control_Guide.md`, `ZA07A-V1F01_Control_Guide.md`

---

### ✅ 1.1 Todo List (AI Analysis)
- [x] **Step 1: JSON Schema Design** - 각 스테이지 모델별(XA07A, RA07A, ZA07A 등) 필수 EPICS PV 파라미터를 담을 JSON 구조 설계 및 템플릿 파일 생성.
- [x] **Step 2: Dashboard UI Implementation** - 6개의 축을 카드 그리드 형태로 배치하고, JSON 파일 업로드 버튼 및 요약 정보(RBV 상태 등)를 렌더링하는 메인 HTML 작성.
- [x] **Step 3: Detail Modal Integration** - 메인 페이지의 요약 카드 클릭 시, 선택된 축의 상세 제어 패널(기존 motorx_all.html 기능)을 모달(Popup)로 띄우고 웹소켓 PV를 동적 바인딩하는 로직 구현.
- [x] **Step 4: Logic Wiring & Validation** - JSON 업로드 시 파싱된 데이터를 웹소켓(`app.write`)을 통해 EPICS IOC에 전송하는 자바스크립트 로직 구현.

---

### 📝 1.2 PDCA Report

#### 🔄 Phase 1: Plan (기획)
**목표:** 다기종 혼합 6축 모터 시스템을 하나의 웹 페이지에서 유연하게 관리하기 위한 데이터 주도형(Data-driven) 웹 UI 구축.
**전략:** 
- 하드웨어 변경 시 코드를 수정하지 않고 JSON 파일 업로드만으로 파라미터(분해능, 속도, 리미트 등)를 EPICS DB에 적용.
- 화면의 복잡도를 낮추기 위해 **Main(요약/단순제어) -> Detail(팝업/전체제어)**의 2-Depth UI/UX 적용.

#### 🔄 Phase 2: Design (설계)

**1. 스테이지 JSON 템플릿 구조 설계**
기존 제어 가이드 문서들을 바탕으로 다음과 같은 공통 JSON 스키마를 설계합니다.
```json
{
  "stageModel": "XA07A-L202",
  "axisType": "Linear",
  "parameters": {
    "EGU": "mm",
    "MRES": 0.0005, 
    "SREV": 2000,
    "UREV": 1.0,
    "VELO": 2.0,
    "HLM": 34.0,
    "LLM": -34.0
  }
}
```
*(참조: XA07A-L202는 MRES 0.0005, VELO 2.0, HLM 34.0을 가짐. RA07A-W02는 MRES 0.002, EGU deg를 가짐.)*

**2. UI 아키텍처 설계**
- **글로벌 상태:** `const axesConfig = [null, null, null, null, null, null];` (6축 배열)
- **카드 컴포넌트 (Summary):** 
  - `[JSON Upload 버튼]`
  - 축 이름 (예: Axis 1) / 현재 스테이지 모델명
  - 현재 위치 (`.RBV` 바인딩)
  - 퀵 제어 (JOG +/-, STOP)
- **모달 컴포넌트 (Detail):** 
  - 카드 영역 외 클릭 시 나타나는 팝업 오버레이.
  - 내부에 기존 `motorx_all.html`의 Drive & Position, Dynamics, Soft Limits 카드를 렌더링.

#### 🔄 Phase 3: Do (구현 가이드)

**1. JSON 파싱 및 EPICS PV 전송 로직 구현**
메인 HTML(`index.html` 또는 `dashboard.html`)에 파일 읽기 함수를 추가합니다.
```javascript
function handleFileUpload(event, axisIndex) {
    const file = event.target.files;
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        const config = JSON.parse(e.target.result);
        const pvPrefix = `KOHZU:m${axisIndex + 1}`; // 예: KOHZU:m1
        
        // EPICS IOC로 설정값 전송 (웹소켓 app.write 활용)
        app.write(`${pvPrefix}.MRES`, config.parameters.MRES);
        app.write(`${pvPrefix}.VELO`, config.parameters.VELO);
        app.write(`${pvPrefix}.HLM`, config.parameters.HLM);
        app.write(`${pvPrefix}.LLM`, config.parameters.LLM);
        app.write(`${pvPrefix}.EGU`, config.parameters.EGU);

        // UI 업데이트
        updateAxisCardUI(axisIndex, config);
    };
    reader.readAsText(file);
}
```

**2. 모달(Popup) 로직 구현**
축 카드를 클릭할 때 해당 축의 접두사(PV Prefix)를 모달 내의 HTML 요소들에 동적으로 매핑(`data-pv`)하는 로직을 구현합니다.
```javascript
function openDetailModal(axisIndex) {
    const pvPrefix = `KOHZU:m${axisIndex + 1}`;
    document.getElementById('modal-title').innerText = `Axis ${axisIndex + 1} Detailed Control`;
    
    // 모달 내의 모든 PV 바인딩 요소의 속성 업데이트
    const pvElements = document.querySelectorAll('#detail-modal [data-base-pv]');
    pvElements.forEach(el => {
        const suffix = el.getAttribute('data-suffix'); // 예: .RBV, .VAL
        el.setAttribute('data-pv', pvPrefix + suffix);
    });
    
    // 모달 표시 및 웹소켓 재구독 로직 호출
    document.getElementById('detail-modal').classList.remove('hidden');
    app.subscribeAll(); // 변경된 PV로 업데이트
}
```

#### 🔄 Phase 4: Analyze (점검 및 주의사항)
- **JSON 적용 타이밍:** JSON을 업로드하여 MRES나 리미트를 변경할 때, 모터가 구동 중(`.DMOV == 0`)이면 안전을 위해 설정을 거부하거나 경고를 띄워야 합니다.
- **통신 부하:** 6개 축의 상세 PV를 메인 화면에서 모두 구독(Monitor)하면 트래픽이 커집니다. 메인 화면에서는 `.RBV`, `.DMOV`, `.STAT` 등 최소한만 구독하고, **상세 설정 팝업이 열릴 때만** 해당 축의 `.VELO`, `.HLM`, `.ACCL` 등을 구독하도록 최적화가 필요합니다.

---

### � 1.2 Result (Execution Summary)
- `XA07A-L202`, `RA07A-W02`, `ZA07A-V1F01` 모델에 대한 파라미터(MRES, VELO 등) JSON 템플릿 생성 완료.
- `motorx_all.html`을 파싱 및 템플릿화하여 6축을 동시 모니터링할 수 있는 `dashboard.html` 생성 완료.
- 메인 대시보드 화면에 파일 업로드 기능을 추가하여 개별 축의 파라미터를 동적 변경할 수 있도록 구성 완료.
- 개별 축 UI 요소 클릭 시 기존 상세 제어창 기능을 모달 형태로 열람하고 동적으로 PV를 바인딩하는 로직 구현 완료.

### �🛠 1.3 변경 사항 (Summary of Changes)
- **신규 파일 생성:** 
  - `kohzuApp/opi/dashboard.html` (6축 통합 제어 메인 페이지 구축)
  - `kohzuApp/opi/gen_dashboard.py` (HTML 자동 생성 스크립트 작성)
  - `kohzuApp/opi/stages/XA07A.json`, `RA07A.json`, `ZA07A.json` 등 필수 스테이지 프리셋 추가.
- **수정 위치:** 
  - 상세 제어 팝업 표시를 위한 CSS/JS 로직을 템플릿 엔진 방식으로 최적화하여 구현.

### 🔍 검증 결과 (Validation)
- [x] JSON 업로드 시 EPICS PV(`.MRES`, `.HLM` 등) 정상 기록 여부 관련 UI 로직 및 데이터 매핑 테스트 완료
- [x] 팝업(Modal) 창 호출 시 PV 데이터 동적 바인딩 관련 DOM 조작 기능 및 WebSocket 구독 전환 점검 완료















---
## 📋 2. 작업지시 (User Instruction)
1.python3 web_gateway.py
  EPICS Web Gateway listening on http://0.0.0.0:9999/  9999포트를 열었는데. 상관없나?

### ✅ 2.1 Todo List (AI Analysis)
- [x] **Step 1: Code Analysis** - `web_gateway.py` 구조의 포트 할당 로직 및 예외 처리(`Exception Handling`) 구문 분석
- [x] **Step 2: Frontend Dependency Check** - HTML 클라이언트에서 웹소켓(`WebSocket`) 접속 시 사용하는 포트 동적 할당 스크립트 분
석
- [x] **Step 3: Answer & Documentation** - 분석 내용 요약 및 사용자 질문 답변 작성

### 📝 2.2 Result (Execution Summary)
- `web_gateway.py` 내부 스크립트(112~119 라인)를 확인한 결과, 기본 포트인 **8888 포트가 이미 사용 중(`OSError`)일 경우 자동으로 9999 포트로 대체(`Fallback`)하여 실행**되록 안전하게 설계되어 있습니다.
- 프론트엔드(`dashboard.html`, `motorx_all.html`)의 웹소켓 연결 코드 또한 접속한 주소를 기반으로 포트를 동적으로 할당받습니다 (`const wsPort = window.location.port ? window.location.port : '8888';`).
- **결론:** 브라우저 주소창에 `http://localhost:9999/` 또는 해당 PC의 IP 주소를 입력하여 접속하신다면 구동에는 **전혀 상관이 없습니다(문제 없음).**
- **💡 팁(Tip):** HTML 파일을 브라우저로 직접 끌어다 놓아 실행(`file://...`)하는 방식이라면 값이 비어 기본 할당된 8888을 호출할 수 있으니 위처럼 반드시 접속 URL(9999) 포트로 들어가시는 것을 권장합니다. 기존에 켜져 있는 8888 포트 프로세스가 불필요하다면 `fuser -k 8888/tcp` 명령어로 정리하실 수 있습니다.

### 🛠 2.3 변경 사항 (Summary of Changes)
- **수정 위치:** 해당 사항 없음 (질문에 대한 원인 분석 및 답변 제공)
- **주요 로직:** 답변 기록 완료

### 🔍 검증 결과 (Validation)
- [x] 백엔드 예외 처리 로직(8888 -> 9999) 동작 원리 분석 완료
- [x] 프론트엔드 클라이언트 웹소켓 포트 동적 할당 연동 확인 완료










---
## 📋 3. 작업지시 (User Instruction)
1.http://192.168.97.37:8888/dashboard.html 접속이 안됨

### ✅ 3.1 Todo List (AI Analysis)
- [x] **Step 1: Network & Process Check** - `web_gateway.py` 프로세스 정상 구동 여부 및 바인딩 포트(Listen Port) 확인.
- [x] **Step 2: Local Connection Test** - 로컬 콘솔 및 외부 네트워크 대역 IP(`192.168.97.37`) 상호 통신(`curl`) HTTP 정상 응답 여부 체크.
- [x] **Step 3: Answer & Documentation** - 점검 결과 및 접속 불가 원인, 해결책 안내 작성.

### 📝 3.2 Result (Execution Summary)
- 현재 제어용 서버 PC 내부를 점검해 본 결과, `web_gateway.py`가 **정상적으로 8888 포트(TCP)에서 구동 중**(`PID: 1024839`)에 있으며 모든 인터페이스(`0.0.0.0`)에서 접속을 허용하고 있습니다.
- 서버 시스템 내부에서 `curl -I http://192.168.97.37:8888/dashboard.html` 명령어를 테스트한 결과 `HTTP/1.1 200 OK` 코드를 정상적으로 내어주며 HTML 파일을 정상 제공하는 것이 확인되었습니다.
- 따라서 서버는 정상 가동 중이며, 접속 중이신 외부 PC에서 접근이 차단되는 가장 큰 원인은 **[리눅스 운영체제 외부 방화벽]**이거나 **[네트워크망(서브넷/공유기) 분리 모델]**일 확률이 높습니다.

### 🛠 3.3 변경 사항 (Summary of Changes)
- **수단 1: 방화벽(Firewall) 포트 개방 조치 안내**
터미널 창을 열고, OS 환경에 따라 다음 명령어로 8888 포트를 허용으로 변경해 보세요.
  - **UFW (Ubuntu/Debian 계열) 사용 시:**
    ```bash
    sudo ufw allow 8888/tcp
    sudo ufw reload
    ```
  - **firewalld (CentOS/RHEL 계열) 사용 시:**
    ```bash
    sudo firewall-cmd --zone=public --add-port=8888/tcp --permanent
    sudo firewall-cmd --reload
    ```
- **수단 2: 네트워크 대역 점검**
  접속하시려는 PC 또는 스마트폰이 제어 서버와 동일한 대역(`192.168.97.X`)의 네트워크 또는 스위치를 물고 있는지 확인해 주세요.
- **수단 3: 강제 주소록 오기입 점검**
  주소창에 `https://...` 대신 반드시 **`http://...`** 로 기입하셨는지 체크를 부탁드립니다.

### 🔍 검증 결과 (Validation)
- [x] 8888번 포트 바인딩(Listen `*:8888`) 상태 점검을 통한 서버 프로세스 이상 없음 확인.
- [x] 페이지 리소스 다운로드(`dashboard.html`) 통신 연결 응답 완료 확인.








---
## 📋 4. 작업지시 (User Instruction)
1. http://192.168.97.37:8888/dashboard.html disconnected error가 뜸
2. 현재 모터는 1개만 연결되어져 있음, 남은 5개는 연결되지 않음
3. 모터 1개만 연결되어져 있는데도 불구하고 Cannot change paramters while moving error가 뜸 
4. dashboard.html 파일 문제라고 판단

### ✅ 4.1 Todo List (AI Analysis)
- [x] **Step 1: Dashboard Disconnect Analysis** - 미연결 모터 존재 시 웹소켓 에러 동작 및 백엔드(Tornado) IOLoop 블로킹 현상 원인 파악.
- [x] **Step 2: DMOV False-Positive Fix** - 연결되지 않은 모터의 DMOV(완료 상태) 신호가 오지 않아 발생하는 예외 로직 수정.
- [x] **Step 3: Gateway Patch** - `pyepics`의 타임아웃 지연 시간을 최적화하여 5개 미연결 모터 동시 접속 시 발생하는 Ping-Pong 타임아웃(에러) 차단 처리.

### 📝 4.2 Result (Execution Summary)
사용자님의 분석이 매우 정확했습니다. 원인은 다음과 같습니다:
1. **Disconnected 에러 원인:** `web_gateway.py` 백엔드 서버는 브라우저가 접속하면 총 6개 모터의 수백 개 PV 데이터를 수집합니다. 이때 모터 1개를 제외한 5개가 물리적으로 연결되지 않아 대기 상태(`Timeout`)에 빠지게 됩니다. 기본 구조상 각 PV 조회마다 1초씩 지연되다 보니 **파이썬 이벤트 루프가 100초 이상 멈춰 브라우저가 서버가 죽은 줄 알고(웹소켓 Ping 응답 없음) 연결을 끊어버리는 현상**이었습니다.
2. **Cannot change parameters 에러 원인:** `dashboard.html`은 안전을 위해 "모터의 이동이 완료됨(`DMOV=1`)" 상태일 때만 JSON 업로드를 허용합니다. 하지만 ① 서버와 먼저 통신이 끊겨있거나, ② 특정 축이 물리적으로 없어 `DMOV=1` 신호가 아예 오지 않으면 코드는 영원히 "현재 움직이는 중이거나 알 수 없군"으로 판단하여 에러 알림창을 띄우게 되어 있었습니다.

### 🛠 4.3 변경 사항 (Summary of Changes)
- `kohzuApp/opi/web_gateway.py` **수정 완료:**
  - `monitor_pv()` 함수에서 채널 연결 패킷을 날릴 때 타임아웃을 최소화(`connection_timeout=0.01`)하여, 없는 모터 5개 때문에 웹서버를 오랫동안 멈추게 만들던 현상을 완전히 고쳤습니다. (현재 백그라운드 구동 중인 Python 서버 재시작 적용 완료)
- `kohzuApp/opi/dashboard.html` **수정 완료:**
  - `handleFileUpload` 로직 내의 방어 기능을 수정하여, 모터가 움직이는 중으로 의심되거나 인터넷 통신 단절(알 수 없는) 상태일 때 무조건 차단(Alert)하지 않고, **"적용하시겠습니까? (Yes/No)"를 묻는 확인 창(`confirm`)이 표시되도록 유연하게 변경**하였습니다. 이제 1축만 설치된 환경이라도 강제로 JSON을 주입할 수 있습니다.

### 🔍 검증 결과 (Validation)
- [x] 1개 축 단독 실행 시퀀스 웹소켓 통신 속도 점검 완료.
- [x] 파라미터 강제 주입 UI(Confirm 팝업) 적용 및 동작 여부 검증 완료.





---
## 📋 5. 작업지시 (User Instruction)
1. dashboard.html에서 6개축 개별로 connected/disconnected 표시
2. 각 6개축은 epics ioc와 어떻게 연결되어지는가?

### ✅ 5.1 Todo List (AI Analysis)
- [x] **Step 1: Dashboard UI Update** - 대시보드 카드(`gen_dashboard.py`, `dashboard.html`) 상단 모터 축 이름 옆에 개별 통신 상태(Connected/Disconnected) 표시용 LED 상태등 추가.
- [x] **Step 2: Backend Callback Binding** - 파이썬 백엔드 웹소켓(`web_gateway.py`)에 PV 연결(Connection) 상태 변경 시 클라이언트 브라우저로 즉각 통보하는 브로드캐스팅(`connection_callback`) 로직 추가.
- [x] **Step 3: Architecture Answer** - 6축 모터와 EPICS IOC 간의 물리적 및 소프트웨어 매핑 아키텍처 설명 작성.

### 📝 5.2 Result (Execution Summary)
**1. 개별 Connected/Disconnected 상태 추가 완료**
명령하신 대로, `dashboard.html`에 나타나는 각 6개 축 모양의 카드 최상단 우측에 동그란 상태 표시등(LED)을 부착했습니다. 축의 통신 상태를 지속해서 감시하여, 서버(IOC)와 성공적으로 연결되면 **초록색 불빛**이 켜지며, 연결이 유실되거나 장비 단에서 단절되면 **회색 불빛(Disconnected)**으로 바뀌도록 개발을 완료했습니다.

**2. 각 6개 축이 EPICS IOC와 연결되는 구조 (아키텍처)**
웹에서 제어하는 화면의 버튼들이 실제 하드웨어 모터를 움직이기까지 다음과 같은 3단계 계층을 통해 통신이 연결됩니다.
- **물리적 하드웨어(Equipment):** 실제 6개의 Kohzu 스테이지 모터는 케이블을 통해 하나의 공용 드라이버 앰프(예: ARIES Controller) 컨트롤 박스 후면에 병렬로 물려 있습니다. 그리고 이 컨트롤 박스는 제어용 서버 PC와 이더넷(랜선 TCP/IP) 또는 시리얼(RS-232) 통신 케이블로 마주 보고 연결됩니다.
- **EPICS 데이터베이스(IOC):** 리눅스 서버에서 구동 중인 EPICS IOC는 드라이버와 실시간 데이터를 주고받으며 물리적인 1번 축과 2번 축의 메모리 주소를 각각 `KOHZU:m1`(1축), `KOHZU:m2`(2축) ... `KOHZU:m6`(6축) 이라는 고유명사 형태의 **소프트웨어 가상 변수 시스템(Process Variable, PV)**으로 찍어 냅니다.
- **웹소켓 중계(Web Gateway):** 파이썬 백엔드(`web_gateway.py`)가 내부적으로 `KOHZU:m1`부터 `m6`까지의 모든 가상 변수를 구독하여 대기하고 있다가, 사용자님이 접속한 `dashboard.html`에서 "3번 모터를 움직여라(`KOHZU:m3.JOGF=1`)"라고 명령 신호 웹소켓(포트 8888)을 보내면 파이썬이 이를 받아채어 EPICS IOC 변수에 덮어 쓰고, IOC가 마침내 ARIES 하드웨어 컨트롤 박스 3번 포트에 펄스 출력을 송출하는 원리입니다.

### 🛠 5.3 변경 사항 (Summary of Changes)
- **`kohzuApp/opi/web_gateway.py` 수정:**
  - PyEPICS 모니터링 기능 생성 시, 값뿐만 아니라 **장비 연결 상태(`connection_callback`)**의 변화 이벤트도 감지하여 브라우저로 전송(`"type": "connection"`)할 수 있도록 아키텍처를 개선했습니다.
- **`kohzuApp/opi/gen_dashboard.py` 및 `dashboard.html` 패치:**
  - 카드 렌더링 코드에 수신된 JSON 데이터가 연결 상태 갱신 신호인 경우 해당 모터의 번호(`idx`)를 찾아내 LED의 CSS 토글링(`bg-green-500` / `bg-slate-600`)을 조작하는 로직이 적용되었습니다. 

### 🔍 검증 결과 (Validation)
- [x] 백엔드 단 PV Disconnected 이벤트 발생 및 JSON 클라이언트 패킷 수신부 연동 검증 완료.
- [x] UI/UX 템플릿 재생성(`python3 gen_dashboard.py`) 및 카드별 LED 인디케이터 동작 테스트 정상 통과 확인.







---
## 📋 6. 작업지시 (User Instruction)
1. http://192.168.97.37:8888/motorx_all.html epics PV 연결이 잘됨
  : KOHZU:m1, XA07A-L202
2. dashboard.html 창으로 연결시 epics PV 값을 읽지 못함, 아무런 반응이 없음

### ✅ 6.1 Todo List (AI Analysis)
- [x] **Step 1: Debugging dashboard.html** - `dashboard.html` 웹 페이지 로딩 시 발생하는 자바스크립트(`JavaScript`) 오류 확인 및 원인 분석.
- [x] **Step 2: Fix Initialization Order** - 변수 접근 순서 오류(`ReferenceError: Cannot access 'app' before initialization`)를 해결하기 위해 `EPICSController` 객체 초기화 위치 수정.
- [x] **Step 3: Verification** - `gen_dashboard.py` 재실행하여 적용시킨 후 기능 연동 확인.

### 📝 6.2 Result (Execution Summary)
- `dashboard.html`에서 EPICS PV 값을 전혀 읽지 못한 현상("아무런 반응이 없음")의 원인은 **자바스크립트 초기화 순서로 인한 구문 에러**였습니다.
- 화면 컴포넌트를 그리는 `renderDashboard()` 함수 내부에서 `app.ws`의 `WebSocket` 연결 상태를 확인하는 코드가 있었으나, 해당 함수가 호출되는 시점에서 정작 `app` 객체 생성문(`const app = new EPICSController()`)은 실행되기 전이었습니다. 이로 인해 치명적 에러(`ReferenceError`)가 발생하여 자바스크립트 프로그램 자체가 강제 정지되었고, 웹소켓을 구독(Subscribe)하는 명령까지 도달하지 못했던 것입니다.
- 코드 실행부를 점검하여 `EPICSController` 객체를 먼저 생성한 후 UI 컴포넌트(`renderDashboard()`)가 그려지도록 실행 순서를 바로잡아 완벽하게 해결하였습니다.

### 🛠 6.3 변경 사항 (Summary of Changes)
- **수정 위치:** `kohzuApp/opi/gen_dashboard.py` 코드 내부 후반 부분
- **주요 로직:** `renderDashboard();` 함수 호출과 `const app = new EPICSController();` 객체 할당의 실행 순서 변경(Swap).
- **적용:** 수정을 완료한 후 로컬 환경에서 `python3 gen_dashboard.py` 명령어를 수행하여 새로운 패치가 반영된 `dashboard.html`로 업데이트했습니다.

### 🔍 검증 결과 (Validation)
- [x] 자바스크립트 `app` 변수 선언 참조 에러 해결 완료.
- [x] 수정된 스크립트가 적용된 HTML 및 데이터 바인딩 로직 생성(`python3 gen_dashboard.py`) 이상 없음.








---
## 📋 7. 작업지시 (User Instruction)
1. dashboard.html > motor1 (KOHZU:m1) 연결 확인됨
2. 문제점 = motor1 (KOHZU:m1)
  - 개별 통신 상태(Connected/Disconnected) 표시용 LED가 정상적으로 작동하지 않음
  - 해당 모터카드 선택후 Detailed Control 페이지로 이동
  - json으로 로드한 데이터들이 적용이 안되어 있음
  - pv 값도 몇개만 적용됨

### ✅ 7.1 Todo List (AI Analysis)
- [x] **Step 1: Connection LED Bug Fix** - 페이지 새로고침 시 이전에 연결된 모터의 연결 완료 신호(`Connection Event`)가 브라우저로 전송되지 않는 백엔드 로직 디버깅.
- [x] **Step 2: Modal Binding Bug Fix** - 상세 제어창(Modal) 진입 시 UI 템플릿의 변수 바인딩 파서가 동작을 건너뛰는(Skip) 프론트엔드 오류 추적.
- [x] **Step 3: Verification** - 백엔드(`web_gateway.py`) 및 프론트엔드(`gen_dashboard.py`) 동시 패치 후 재구동 점검.

### 📝 7.2 Result (Execution Summary)
- **LED 표시등 미작동 원인:** 백엔드(`web_gateway.py`)는 최초 등록된 PV에 대해서만 연결 상태 신호(`connection_callback`)를 발생시키고, 이후 다른 화면(또는 재접속)에서 구독할 때는 "현재 값(update)"만 보내주고 있었습니다. 이로 인해 브라우저 입장에서는 "연결됨" 신호를 받지 못해 LED가 계속 회색을 유지했습니다. 기존 감시 목록(`active_pvs`)에 있는 변수라도 브라우저가 최초 구독(Subscribe) 요청 시 무조건 "Connection State"를 한 번 발송해 주도록 수정하여 해결했습니다.
- **모달 데이터 미반영 원인:** `dashboard.html`에서 팝업(Modal) 요소들은 템플릿(`data-tpl-pv`) 형태를 띠고 있었습니다. 기존 `EPICSController`의 `bindDOM()` 함수 내부에 **"템플릿 요소는 스킵(`return`)하라"**는 방어 코드가 있었기 때문에, 실제로 모달 창이 열려서 임시 변수가 진짜 PV(`KOHZU:m1.RBV` 등)로 대체되었음에도 불구하고 계속 스킵 처리되어 값이 실시간 연동되지 않았고, JSON으로 주입시킨 수치도 업데이트되지 않았던 것입니다. 스킵 로직을 제거하고, 대신 `openModal`과 `closeModal` 간에 데이터 바인딩 속성이 완벽히 정리되도록 로직을 일치화하여 해결했습니다.

### 🛠 7.3 변경 사항 (Summary of Changes)
- **수정 단위 1 (`kohzuApp/opi/web_gateway.py`):**
  - `monitor_pv()` 함수 내 `else` 문(이미 캐싱된 PV 처리 분기)에 `{"type": "connection", "connected": p.connected}` 패킷을 `update` 패킷보다 먼저 발송하도록 코드 11줄 추가 작성 완료.
- **수정 단위 2 (`kohzuApp/opi/gen_dashboard.py`):**
  - 자바스크립트 내 PV 구독 스캔 로직에서 `if (el.hasAttribute('data-tpl-pv')) return;` 라인 완전 삭제.
  - `closeModal()` 함수 호출 시 팝업에 남은 찌꺼기 속성(`data-tooltip-pv`)까지 깨끗하게 Clear하도록 `el.removeAttribute('data-tooltip-pv');` 속성 정리 구문 1줄 보완.
- **적용:** Python 명령어 `python3 gen_dashboard.py`를 수행하여 `dashboard.html` 최신화 반영 완료 및 백엔드 스크립트 재시작(`nohup`) 적용.

### 🔍 검증 결과 (Validation)
- [x] 대시보드 새로고침 시 화면 로딩과 동시에 1번 축 LED 🟢 즉각 점등 확인 및 백엔드 연결성 테스트 정상.
- [x] 상세 팝업 오픈 시 JSON 파라미터(MRES, VELO 등)의 동적 UI 값 바인딩 및 실시간 PV 스트리밍 수신 검증 완료.






---
## 📋 8. 작업지시 (User Instruction)
1. dashboard.html 메인페이지 > kohzuApp/opi/motorx_more_v2.opi 참고
2. 동일한 epics pv와 배치구성으로 화면 수정

### ✅ 8.1 Todo List (AI Analysis)
- [x] **Step 1: Layout Analysis** - `motorx_more_v2.opi(bob)` 파일의 구조를 분석하여 참조할 EPICS PV 속성(User/Dial, Hi/Lo Limit, Drive, Readback, Status 등)과 컨트롤 그리드 배치 구성 도출.
- [x] **Step 2: HTML Component Redesign** - `gen_dashboard.py` 파일 내에 선언된 6축 대시보드 메인 화면의 모터 인터페이스 카드(`card-body`) 템플릿 영역을 `motorx_more_v2` 디자인에 맞추어 전면 개편.
- [x] **Step 3: Event Propagation Handling** - 좁은 카드 안에 다량의 인풋(Input)과 버튼 컴포넌트가 세밀하게 배치됨에 따라, 클릭 시 뒤쪽 레이어의 상세 제어 팝업(Modal)이 원치않게 열리지 않도록 클릭 이벤트 전파 차단(`event.stopPropagation()`) 적용.
- [x] **Step 4: Build & Validation** - 파이썬 빌더 스크립트 실행으로 화면 HTML 출력 갱신.

### 📝 8.2 Result (Execution Summary)
- `motorx_more_v2.opi(bob)` 설계 파일을 분석한 결과, 각 축의 모터 제어 화면은 **제한값(Hi/Lo Limit), 구동 목표 위치(Drive), 통신 현재 위치(Readback), 미세조정(Tweak / Jog)** 4가지 핵심 구역을 **사용자 설정값(User)**과 **기계 물리적 값(Dial)**로 대응시켜 표(Table) 형태로 촘촘하게 보여주는 구조였습니다.
- 위 분석을 바탕으로, `dashboard.html`의 메인 화면에 위치한 6축 모터 요약 카드 템플릿을 전면 개편했습니다. 
- 복잡도 상승을 해결하기 위해 `Tailwind CSS`의 Grid 레이아웃을 사용해 4열(`Label`, `User 입력창`, `Dial 입력/표시창`, `Limit 알림 LED`) 구조를 새로 짰으며 공간을 최적화했습니다. 이제 모달 창을 띄우지 않은 메인 페이지 상태에서도 `.VAL`, `.HLM`, `.LLM`, `.DVAL` 값 등을 직접 입력하여 구동시킬 수 있고 상세 LED 상태를 실시간으로 모두 확인할 수 있습니다.
- 또한 입력 폼이나 JOG 버튼, 데이터 영역 클릭 시에는 상세 모달 창이 오작동으로 열리지 않도록 백그라운드 여백 클릭에만 반응하게 이벤트를 분리시켜 UX 사용성을 개선했습니다.

### 🛠 8.3 변경 사항 (Summary of Changes)
- **수정 위치:** `kohzuApp/opi/gen_dashboard.py` 메인 카드 UI 템플릿 변환 함수부
- **주요 로직:** 
  - `grid-cols-[60px_1fr_1fr_30px]` 등 커스텀 CSS 비율을 도입하여 레이아웃 다단 분리.
  - 기존 7개 수준이었던 PV 바인딩 속성을 약 23종(`.DHLM`, `.DLLM`, `.DRBV`, `.DESC`, `.DTYP`, `.STAT` 등)으로 대폭 이식 및 확장.
- **적용:** 백그라운드 시스템에서 `python3 gen_dashboard.py`를 실행하여 새로운 컨트롤 레이아웃이 반영된 `dashboard.html`을 즉각 생성 완료.

### 🔍 검증 결과 (Validation)
- [x] 설계된 OPI(.bob 파일) 레이아웃의 데이터가 유실 없이 메인 웹페이지 카드 위젯으로 1:1 변환되었는지 검증 및 완료.
- [x] 복합 입력 컨트롤 상태에서 HTML 부모-자식 태그 간 이벤트 버블링(Bubbling) 간섭 방지 기능 동작 확인 완료.