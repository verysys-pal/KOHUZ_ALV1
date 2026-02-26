# 🌐 EPICS Web Dashboard 사용 가이드 (Web Usage Guide)

본 문서는 KOHZU 모터 제어를 위한 EPICS Web Dashboard(`dashboard.html`)의 시스템 초기화 및 실행 절차를 안내합니다.

## 1. Linux 네트워크 접속 및 IP 할당
장비 재부팅 또는 네트워크 접속 해제 시, 컨트롤러 IP(`192.168.1.120`)와의 통신을 위해 호스트 PC의 이더넷 인터페이스에 고정 IP를 재할당해야 합니다.

```bash
# root 권한으로 접속/실행
sudo su - 

# enp3s0 네트워크 인터페이스 활성화
sudo ip link set enp3s0 up

# 해당 이더넷에 고정 IP(192.168.1.100) 할당
sudo ifconfig enp3s0 192.168.1.100 netmask 255.255.255.0 up

# 할당된 IP 상태 확인
ifconfig

# 장비(모터 컨트롤러)와 통신 테스트
ping 192.168.1.120
```

## 2. EPICS IOC 구동
통신이 확인되면 EPICS IOC 서버 프로세스를 시작하여 하드웨어와 Process Variable(PV) 간의 바인딩을 수행합니다.

```bash
# IOC 실행 디렉토리로 이동
cd ${EPICS_PATH}/siteApp/KOHUZ_ALV1/iocBoot/iocKOHUZ_ALV1

# st.cmd 스크립트를 실행하여 IOC 구동 (로그를 파일로 저장)
./st.cmd | tee "Log_stCmd.log"
```

## 3. 구동 및 상태 (Drive & Status) 터미널 명령
EPICS IOC가 구동된 상태에서 로컬 터미널 명령어를 통해 주요 변수들의 값과 모터의 피드백을 실시간 제어할 수 있습니다. (※ 1축 모터 `KOHZU:m1` 기준)

```bash
# 축 설명(Description) 확인
caget KOHZU:m1.DESC

# 상대 거리 이동 (Relative Move) : -10 또는 10 입력
caput KOHZU:m1.RLV -10
caput KOHZU:m1.RLV 10

# 모터 구동 속도 설정 (최대 4.0 mm/s)
caput KOHZU:m1.VELO 2.0

# 모터의 현재 위치 확인 (Readback Value)
caget KOHZU:m1.RBV

# 모터 이동 완료 여부 확인 (1: 완료, 0: 이동 중)
caget KOHZU:m1.DMOV

# 강제 정지 명령 (STOP)
caput KOHZU:m1.STOP 1

# 동작 모드 제어 (Go: 이동 가능, Stop: 이동 불가/정지 모드)
caget KOHZU:m1.SPMG
```

## 4. EPICS Web Gateway 서버 실행
웹사이트에서 실시간으로 EPICS PV를 구독하고 제어하기 위해 중간 다리 역할을 하는 Python 기반 웹소켓 게이트웨이 서버를 구동합니다.

```bash
# Gateway 스크립트 위치로 이동
cd ${EPICS_PATH}/siteApp/KOHUZ_ALV1/kohzuApp/opi

# 기존에 켜져 있는 백그라운드 프로세스가 있다면 종료
pkill -f web_gateway.py

# Python 웹소켓 게이트웨이 실행 (기본 포트: 8888)
python3 web_gateway.py
```

## 5. 방화벽 포트 개방 및 대시보드 접속
외부의 웹 브라우저(`dashboard.html`)에서 게이트웨이 서버로 접속할 수 있도록 방화벽 포트를 개방합니다.

```bash
# 로컬 호스트 PC의 접속용 IP 주소 확인
hostname -I

# 8888번 TCP 포트 방화벽 개방
sudo ufw allow 8888/tcp

# 방화벽 정책 재적용
sudo ufw reload
```

### 🌍 웹 페이지 연결
- 크롬(Chrome) 등의 웹 브라우저를 열고, 위에 입력했던 `IP_ADDRESS`를 포함한 URL로 접속합니다.
  - 경로: `http://[IP_ADDRESS]:8888/dashboard.html`
  - *(예시: http://192.168.1.100:8888/dashboard.html)*
