/*
 * Kohzu ARIES/LYNX EPICS Motor Driver
 * ====================================
 * Controller: Kohzu ARIES (Model 3) / LYNX
 * Stage:      XA07A-L202
 * Protocol:   TCP/IP, CRLF terminated
 *
 * 참조 문서:
 *   - ARIES 매뉴얼 (명령어 사양)
 *   - motorKohzu 모듈 (Model 1, drvSC800.cc)
 *   - Kohzu_ARIES_Driver_Troubleshooting_Report.md
 *
 * 명령어 요약:
 *   구동: APS(절대이동), RPS(상대이동), FRP(JOG), ORG(원점), STP(정지)
 *   속도: WTB(속도테이블 쓰기), RTB(속도테이블 읽기)
 *   설정: WSY(시스템파라미터 쓰기), RSY(시스템파라미터 읽기)
 *   조회: STR(상태읽기), RDP(위치읽기)
 *   응답: "C <CMD> <Axis>" (정상) / "E <CMD> <Axis> <ErrNo>" (에러)
 *
 * 원점 복귀 지원 방식 (ORG TYPE):
 *   Method 4  — NORG 센서 에지 (Kohzu 표준, 기본값)
 *   Method 7  — CW Limit 에지
 *   Method 8  — CCW Limit 에지
 */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <asynOctetSyncIO.h>
#include <epicsExport.h>
#include <epicsThread.h>
#include <iocsh.h>

#include "KohzuAriesDriver.h"

// 통신 상수
#define MAX_RESPONSE_LEN 256
#define CMD_TIMEOUT      5.0    // 일반 명령 타임아웃 (초)
#define MOVE_TIMEOUT     2.0    // 이동 명령 (즉시 응답) 타임아웃
#define TERMINATOR       "\r\n"
#define TERMINATOR_LEN   2

// ARIES 속도 제한 (pps)
#define ARIES_MIN_START_SPEED  1
#define ARIES_MAX_START_SPEED  2500000
#define ARIES_MIN_TOP_SPEED    2
#define ARIES_MAX_TOP_SPEED    5000000

// ================================================================
// Controller 생성 함수 (iocsh에서 호출)
// ================================================================
extern "C" int KohzuAriesCreateController(const char *portName,
                                          const char *KohzuAriesPortName,
                                          int numAxes, double movingPollPeriod,
                                          double idlePollPeriod) {
  new KohzuAriesController(portName, KohzuAriesPortName, numAxes,
                           movingPollPeriod, idlePollPeriod);
  return (asynSuccess);
}

// ================================================================
// Controller 생성자
// ================================================================
KohzuAriesController::KohzuAriesController(const char *portName,
                                           const char *KohzuAriesPortName,
                                           int numAxes, double movingPollPeriod,
                                           double idlePollPeriod)
    : asynMotorController(portName, numAxes,
                          NUM_MOTOR_DRIVER_PARAMS + NUM_KOHZU_PARAMS,
                          0, 0,
                          ASYN_CANBLOCK | ASYN_MULTIDEVICE,
                          1,    // autoconnect
                          0, 0) // Default priority and stack size
{
  asynStatus status;

  // ── 커스텀 파라미터 등록: 원점 복귀 방법 선택 (4/7/8) ──
  createParam(KohzuHomingMethodString, asynParamInt32, &homingMethod_);

  // TCP/IP asynOctet 포트에 연결
  status =
      pasynOctetSyncIO->connect(KohzuAriesPortName, 0, &pasynUserSelf, NULL);
  if (status) {
    asynPrint(this->pasynUserSelf, ASYN_TRACE_ERROR,
              "KohzuAriesController: cannot connect to port %s\n",
              KohzuAriesPortName);
  }

  // ARIES 프로토콜 종단 문자: CRLF (\r\n)
  pasynOctetSyncIO->setInputEos(pasynUserSelf, TERMINATOR, TERMINATOR_LEN);
  pasynOctetSyncIO->setOutputEos(pasynUserSelf, TERMINATOR, TERMINATOR_LEN);

  // 축 객체 생성 (각 축의 기본 homing method = 4)
  for (int i = 0; i < numAxes; i++) {
    new KohzuAriesAxis(this, i);
    setIntegerParam(i, homingMethod_, 4);  // Method 4 (NORG 표준) 기본값
  }

  startPoller(movingPollPeriod, idlePollPeriod, 2);
}

// ================================================================
// 명령 전송 헬퍼 (응답 있는 명령용)
// ================================================================
asynStatus KohzuAriesController::sendCommand(const char *command,
                                             char *response, size_t responseLen,
                                             double timeout) {
  size_t nwrite, nread;
  int eomReason;
  asynStatus status;

  status = pasynOctetSyncIO->writeRead(pasynUserSelf, command, strlen(command),
                                       response, responseLen, timeout, &nwrite,
                                       &nread, &eomReason);

  if (status != asynSuccess) {
    asynPrint(pasynUserSelf, ASYN_TRACE_ERROR,
              "KohzuAriesController::sendCommand: error cmd='%s' status=%d\n",
              command, status);
  }

  return status;
}

// ================================================================
// 명령 전송 헬퍼 (응답 없는 명령용 - write only)
// ================================================================
asynStatus KohzuAriesController::sendOnly(const char *command, double timeout) {
  size_t nwrite;
  asynStatus status;

  status = pasynOctetSyncIO->write(pasynUserSelf, command, strlen(command),
                                   timeout, &nwrite);

  if (status != asynSuccess) {
    asynPrint(pasynUserSelf, ASYN_TRACE_ERROR,
              "KohzuAriesController::sendOnly: error cmd='%s' status=%d\n",
              command, status);
  }

  return status;
}

// ================================================================
// Axis 생성자
// ================================================================
KohzuAriesAxis::KohzuAriesAxis(KohzuAriesController *pC, int axisNo)
    : asynMotorAxis(pC, axisNo), pC_(pC),
      homed_(false), homingActive_(false) {
  // 원점 복귀 상태를 소프트웨어로 추적
  // homed_: 원점 복귀 완료 후 전원 OFF까지 유지
  // homingActive_: ORG 실행~완료 구간 추적 (poll()에서 완료 감지)
}

// ================================================================
// WSY 명령으로 ARIES System Parameter 설정
// ================================================================
// 포맷: WSY <축>/<시스템번호>/<설정값>
// 응답: "C WSY <axis> <sysNo>" (정상) / "E WSY <axis> <errNo>" (에러)
//
// 주요 System Parameter:
//   No.1: ORG OFFSET (원점 오프셋, pulse)
//   No.2: ORG TYPE   (원점 복귀 방법, 1~15)
//   No.3: ORG SCAN SPEED (정밀 스캔 속도, pps)
// ================================================================
asynStatus KohzuAriesAxis::setSystemParam(int sysNo, int value) {
  char command[MAX_RESPONSE_LEN];
  char response[MAX_RESPONSE_LEN];
  int axisID = axisNo_ + 1;

  sprintf(command, "WSY%d/%d/%d", axisID, sysNo, value);

  asynPrint(pC_->pasynUserSelf, ASYN_TRACE_ERROR,
            "KohzuAriesAxis::setSystemParam: SENDING cmd='%s'\n", command);

  asynStatus status = pC_->sendCommand(command, response, sizeof(response),
                                       CMD_TIMEOUT);

  // 에러 응답 체크: "E WSY <axis> <errNo>"
  if (status == asynSuccess && response[0] == 'E') {
    asynPrint(pC_->pasynUserSelf, ASYN_TRACE_ERROR,
              "KohzuAriesAxis::setSystemParam: WSY error response='%s'\n",
              response);
    return asynError;
  }

  asynPrint(pC_->pasynUserSelf, ASYN_TRACE_ERROR,
            "KohzuAriesAxis::setSystemParam: WSY OK response='%s'\n",
            response);

  return status;
}

// ================================================================
// WTB 명령으로 Speed Table #0에 속도 파라미터 설정
// ================================================================
asynStatus KohzuAriesAxis::setSpeedTable(double minVelocity, double maxVelocity,
                                         double acceleration) {
  char command[MAX_RESPONSE_LEN];
  char response[MAX_RESPONSE_LEN];
  int axisID = axisNo_ + 1;

  // EPICS asynMotor 전달값:
  //   maxVelocity = VELO / MRES (steps/s = pps)
  //   minVelocity = VBAS / MRES (steps/s = pps)
  //   acceleration = ACCL (초)
  int startSpeed = (int)minVelocity;
  int topSpeed   = (int)maxVelocity;

  // 범위 클램프 (ARIES 사양)
  if (startSpeed < ARIES_MIN_START_SPEED) startSpeed = ARIES_MIN_START_SPEED;
  if (startSpeed > ARIES_MAX_START_SPEED) startSpeed = ARIES_MAX_START_SPEED;
  if (topSpeed   < ARIES_MIN_TOP_SPEED)   topSpeed   = ARIES_MIN_TOP_SPEED;
  if (topSpeed   > ARIES_MAX_TOP_SPEED)   topSpeed   = ARIES_MAX_TOP_SPEED;

  // 시작 속도는 최대 속도의 50% 이하 (ARIES 에러 605 방지)
  if (startSpeed > topSpeed / 2) startSpeed = topSpeed / 2;
  if (startSpeed < ARIES_MIN_START_SPEED) startSpeed = ARIES_MIN_START_SPEED;

  // 가속 시간 변환
  // ★ 핵심: acceleration 파라미터는 ACCL(초)가 아닌 steps/s² (가속도)
  //   acceleration = (VELO - VBAS) / (ACCL × MRES)  [steps/s²]
  //   → ACCL(초) = (topSpeed - startSpeed) / acceleration
  //   → ARIES 단위 = ACCL(초) × 100 (설정값 × 10ms)
  //
  // ARIES 속도별 가속 시간 범위:
  //   1~20 pps: 1~10 (10~100ms)
  //   21~250 pps: 1~100 (10~1000ms)
  //   251~1000 pps: 1~100 (10~1000ms)
  //   1001~250000 pps: 1~1000 (10~10000ms)
  double accelSeconds = 0.5; // 안전 기본값
  if (acceleration > 0.0) {
    accelSeconds = (double)(topSpeed - startSpeed) / acceleration;
  }
  int accelTime = (int)(accelSeconds * 100.0);  // 초 → 10ms 단위
  if (accelTime < 1) accelTime = 1;

  // 속도별 가속 시간 상한 클램프
  int maxAccelTime;
  if (topSpeed <= 20)
    maxAccelTime = 10;
  else if (topSpeed <= 1000)
    maxAccelTime = 100;
  else
    maxAccelTime = 1000;

  if (accelTime > maxAccelTime) accelTime = maxAccelTime;
  int decelTime = accelTime;

  // WTB <축>/<테이블>/<시작속도>/<최대속도>/<가속>/<감속>/<패턴>
  // 패턴 2 = 사다리꼴 구동
  sprintf(command, "WTB%d/0/%d/%d/%d/%d/2",
          axisID, startSpeed, topSpeed, accelTime, decelTime);

  // ★ 디버그: 실제 전송 명령을 ERROR 레벨로 출력 (항상 보이도록)
  asynPrint(pC_->pasynUserSelf, ASYN_TRACE_ERROR,
            "KohzuAriesAxis::setSpeedTable: SENDING cmd='%s'\n", command);

  // WTB는 응답 반환: "C WTB <axis>"
  asynStatus status = pC_->sendCommand(command, response, sizeof(response),
                                       CMD_TIMEOUT);

  // 디버그: 응답도 출력
  asynPrint(pC_->pasynUserSelf, ASYN_TRACE_ERROR,
            "KohzuAriesAxis::setSpeedTable: RESPONSE='%s' status=%d\n",
            response, status);

  // 에러 응답 체크 ("E WTB ...")
  if (status == asynSuccess && response[0] == 'E') {
    asynPrint(pC_->pasynUserSelf, ASYN_TRACE_ERROR,
              "KohzuAriesAxis: WTB ERROR! response='%s'\n", response);
    // WTB 실패해도 기존 테이블 값으로 이동은 시도
    return asynError;
  }

  return status;
}

// ================================================================
// 이동 (절대 위치)
// APS 포맷: APS <축>/<속도테이블>/<위치(pulse)>/<응답방식>
//   응답방식: 0=완료후응답, 1=즉시응답(Quick)
// 응답: "C APS <axis>"
// ================================================================
asynStatus KohzuAriesAxis::move(double position, int relative,
                                double minVelocity, double maxVelocity,
                                double acceleration) {
  char command[MAX_RESPONSE_LEN];
  char response[MAX_RESPONSE_LEN];
  int axisID = axisNo_ + 1;
  int pulse = (int)position;

  // 1. Speed Table #0에 속도 설정
  setSpeedTable(minVelocity, maxVelocity, acceleration);

  // 2. APS 명령으로 절대 이동 (Speed Table #0, 즉시 응답)
  sprintf(command, "APS%d/0/%d/1", axisID, pulse);

  asynPrint(pC_->pasynUserSelf, ASYN_TRACE_FLOW,
            "KohzuAriesAxis::move: cmd='%s' (target=%d pulses)\n",
            command, pulse);

  // 즉시 응답 모드(d=1): 컨트롤러가 "C APS <axis>" 응답 반환
  asynStatus status = pC_->sendCommand(command, response, sizeof(response),
                                       CMD_TIMEOUT);

  // 에러 응답 체크
  if (status == asynSuccess && response[0] == 'E') {
    asynPrint(pC_->pasynUserSelf, ASYN_TRACE_ERROR,
              "KohzuAriesAxis::move: APS error response: '%s'\n", response);
    return asynError;
  }

  return status;
}

// ================================================================
// 정지
// STP 포맷: STP <축>/<정지모드>
//   정지모드: 0=감속정지, 1=비상정지(즉시)
// 응답: "C STP <axis>"
// ================================================================
asynStatus KohzuAriesAxis::stop(double acceleration) {
  char command[MAX_RESPONSE_LEN];
  char response[MAX_RESPONSE_LEN];
  int axisID = axisNo_ + 1;

  // 감속 정지 (모드 0)
  sprintf(command, "STP%d/0", axisID);

  asynPrint(pC_->pasynUserSelf, ASYN_TRACE_FLOW,
            "KohzuAriesAxis::stop: cmd='%s'\n", command);

  // STP는 응답 반환: "C STP <axis>"
  asynStatus status = pC_->sendCommand(command, response, sizeof(response),
                                       CMD_TIMEOUT);

  return status;
}

// ================================================================
// JOG (연속 회전)
// FRP 포맷: FRP <축>/<속도테이블>/<방향>
//   방향: 0=CW(정방향), 1=CCW(역방향)
// STP로 정지해야 멈춤
// ================================================================
asynStatus KohzuAriesAxis::moveVelocity(double minVelocity, double maxVelocity,
                                        double acceleration) {
  char command[MAX_RESPONSE_LEN];
  char response[MAX_RESPONSE_LEN];
  int axisID = axisNo_ + 1;

  // 1. Speed Table #0에 JOG 속도 설정
  setSpeedTable(minVelocity, fabs(maxVelocity), acceleration);

  // 2. 방향 결정: maxVelocity의 부호로 판단
  //    양수 = CW(정방향, 0), 음수 = CCW(역방향, 1)
  int direction = (maxVelocity >= 0) ? 0 : 1;

  // FRP <축>/<속도테이블>/<방향>
  sprintf(command, "FRP%d/0/%d", axisID, direction);

  asynPrint(pC_->pasynUserSelf, ASYN_TRACE_FLOW,
            "KohzuAriesAxis::moveVelocity: cmd='%s' (dir=%s)\n",
            command, direction == 0 ? "CW" : "CCW");

  // FRP 즉시 응답
  asynStatus status = pC_->sendCommand(command, response, sizeof(response),
                                       CMD_TIMEOUT);

  // 에러 체크
  if (status == asynSuccess && response[0] == 'E') {
    asynPrint(pC_->pasynUserSelf, ASYN_TRACE_ERROR,
              "KohzuAriesAxis::moveVelocity: FRP error: '%s'\n", response);
    return asynError;
  }

  return status;
}

// ================================================================
// 원점 복귀 — Method 4/7/8 선택 지원
// ================================================================
// EPICS PV $(P)$(M):HomingMethod 로 사용자가 방법을 선택:
//   4 = NORG 센서 에지 (Kohzu 표준, 기본값)
//   7 = CW Limit(L+) 에지
//   8 = CCW Limit(L-) 에지
//
// 실행 순서:
//   1. PV에서 선택된 Method 읽기
//   2. WSY 명령으로 컨트롤러 System No.2 (ORG TYPE) 변경
//   3. WTB 명령으로 접근 속도 설정
//   4. ORG 명령 전송
//
// Method별 동작:
//   Method 4: CCW→NORG감지→반전→NORG에지정지→좌표0
//   Method 7: CW방향이동→CW Limit에지정지→좌표0
//   Method 8: CCW방향이동→CCW Limit에지정지→좌표0
//
// ORG 포맷: ORG <축>/<속도테이블>/<응답방식>
//   응답방식: 0=완료후응답, 1=즉시응답(Quick)
//
// ※ forwards 파라미터 미사용: ARIES가 Method에 따라
//    복귀 방향을 자동 판단함 (HOMF/HOMR 모두 동일 동작)
// ================================================================
asynStatus KohzuAriesAxis::home(double minVelocity, double maxVelocity,
                                double acceleration, int forwards) {
  char command[MAX_RESPONSE_LEN];
  char response[MAX_RESPONSE_LEN];
  int axisID = axisNo_ + 1;

  // 1. 사용자가 선택한 원점 복귀 방법 읽기 (EPICS PV)
  int method = 4;  // 기본값: Method 4 (NORG 표준)
  pC_->getIntegerParam(axisNo_, pC_->homingMethod_, &method);

  // 유효성 검증: 지원 방법은 4, 7, 8만
  const char *methodName;
  switch (method) {
    case 4:  methodName = "NORG edge (standard)"; break;
    case 7:  methodName = "CW Limit edge";        break;
    case 8:  methodName = "CCW Limit edge";       break;
    default:
      asynPrint(pC_->pasynUserSelf, ASYN_TRACE_ERROR,
                "KohzuAriesAxis::home: INVALID method=%d, "
                "falling back to Method 4\n", method);
      method = 4;
      methodName = "NORG edge (fallback)";
      break;
  }

  asynPrint(pC_->pasynUserSelf, ASYN_TRACE_ERROR,
            "KohzuAriesAxis::home: axis=%d Method=%d(%s) forwards=%d\n",
            axisID, method, methodName, forwards);

  // 2. WSY 명령으로 컨트롤러 ORG TYPE 변경
  //    WSY <축>/2/<method>  (System No.2 = ORG TYPE)
  asynStatus wsy_status = setSystemParam(2, method);
  if (wsy_status != asynSuccess) {
    asynPrint(pC_->pasynUserSelf, ASYN_TRACE_ERROR,
              "KohzuAriesAxis::home: WSY failed for Method=%d, "
              "proceeding with current controller setting\n", method);
    // WSY 실패해도 ORG 시도 (이전 설정으로 동작할 수 있음)
  }

  // 3. Speed Table #0에 원점 복귀 접근 속도 설정
  //    ※ 센서 에지 정밀 스캔 속도는 Sys No.3 (ORG SCAN SPEED)로 별도 관리
  setSpeedTable(minVelocity, maxVelocity, acceleration);

  // 4. ORG <축>/<속도테이블>/<응답방식>
  //    즉시 응답(1) → poll()에서 STR 구동상태로 완료 감지
  sprintf(command, "ORG%d/0/1", axisID);

  asynPrint(pC_->pasynUserSelf, ASYN_TRACE_ERROR,
            "KohzuAriesAxis::home: SENDING cmd='%s'\n", command);

  // ORG 즉시 응답: "C ORG <axis>"
  asynStatus status = pC_->sendCommand(command, response, sizeof(response),
                                       CMD_TIMEOUT);

  // 에러 응답 체크: "E ORG <axis> <errNo>"
  if (status == asynSuccess && response[0] == 'E') {
    asynPrint(pC_->pasynUserSelf, ASYN_TRACE_ERROR,
              "KohzuAriesAxis::home: ORG error response='%s'\n", response);
    homingActive_ = false;
    return asynError;
  }

  if (status == asynSuccess) {
    // ORG 명령 수락됨 → homing 진행 중 플래그 설정
    homingActive_ = true;
    asynPrint(pC_->pasynUserSelf, ASYN_TRACE_ERROR,
              "KohzuAriesAxis::home: homing started "
              "(Method=%d, %s)\n", method, methodName);
  }

  return status;
}

// ================================================================
// 폴링 (상태 + 위치 조회)
//
// STR 응답 포맷 (ARIES 매뉴얼):
//   "C STR <axis> <b> <c> <d> <e> <f> <g>"
//   b: 구동상태 (0=정지, 1=동작중, 2=피드백동작중)
//   c: EMG 비상정지 (0=OFF, 1=ON)
//   d: ORG/NORG 센서 (0~3, 비트마스크)
//   e: CW/CCW 리미트 (0~3, 비트마스크)
//      0=양쪽OFF, 1=CCW만ON, 2=CW만ON, 3=양쪽ON
//   f: 소프트 리미트 (0=정상, 1=+Over, 2=-Under)
//   g: 보정 허용 범위
//
// 실제 응답 예시: "C STR1 0 0 0 0 00"
//   고정 폭 포맷으로 인접 필드 연결 가능
// ================================================================
asynStatus KohzuAriesAxis::poll(bool *moving) {
  char command[MAX_RESPONSE_LEN];
  char response[MAX_RESPONSE_LEN];
  char responseCopy[MAX_RESPONSE_LEN];
  asynStatus status;
  int axisID = axisNo_ + 1;

  // ----- 1. STR: 상태 조회 -----
  sprintf(command, "STR%d", axisID);
  memset(response, 0, sizeof(response));

  size_t nwrite, nread;
  int eomReason;
  status = pasynOctetSyncIO->writeRead(
      pC_->pasynUserSelf, command, strlen(command), response, sizeof(response),
      CMD_TIMEOUT, &nwrite, &nread, &eomReason);

  if (status != asynSuccess) {
    // 통신 에러 → 안전 상태로 폴백 (DMOV 고착 방지)
    asynPrint(pC_->pasynUserSelf, ASYN_TRACE_ERROR,
              "KohzuAriesAxis::poll: STR%d comm error (status=%d)\n",
              axisID, status);
    *moving = false;
    setIntegerParam(pC_->motorStatusDone_, 1);
    setIntegerParam(pC_->motorStatusProblem_, 1);
    setIntegerParam(pC_->motorStatusCommsError_, 1);
    callParamCallbacks();
    return asynSuccess;
  }

  // 디버그: 원본 응답 보존
  strncpy(responseCopy, response, sizeof(responseCopy) - 1);
  responseCopy[sizeof(responseCopy) - 1] = '\0';
  asynPrint(pC_->pasynUserSelf, ASYN_TRACE_FLOW,
            "KohzuAriesAxis::poll: STR%d raw='%s'\n", axisID, responseCopy);

  // 통신 에러 플래그 클리어 (통신 성공했으므로)
  setIntegerParam(pC_->motorStatusCommsError_, 0);

  // ----- STR 응답 파싱 -----
  // 필드: [0]=구동상태, [1]=EMG, [2]=ORG센서, [3]=리미트(비트마스크), [4]=소프트리미트, [5]=보정
  int r_drive = 0, r_emg = 0, r_org = 0, r_limits = 0, r_softlim = 0;
  (void)r_softlim; // 향후 소프트 리미트 활용 예정
  bool parsed = false;

  static const char *delimiters = "\t ";
  char *token = strtok(response, delimiters);

  // 에러 응답 체크: "E STR ..."
  if (token && strcmp(token, "E") == 0) {
    asynPrint(pC_->pasynUserSelf, ASYN_TRACE_ERROR,
              "KohzuAriesAxis::poll: STR%d error response: '%s'\n",
              axisID, responseCopy);
    *moving = false;
    setIntegerParam(pC_->motorStatusDone_, 1);
    setIntegerParam(pC_->motorStatusMoving_, 0);
    setIntegerParam(pC_->motorStatusProblem_, 1);
    callParamCallbacks();
    return asynSuccess;
  }

  if (token && strcmp(token, "C") == 0) {
    token = strtok(NULL, delimiters); // "STR1" (명령 에코)

    // 나머지 토큰을 배열로 수집 (연결된 숫자 분리 포함)
    int fields[10] = {0};
    int nFields = 0;
    char *tok;
    while ((tok = strtok(NULL, delimiters)) != NULL && nFields < 10) {
      int len = strlen(tok);
      if (len > 1) {
        // 고정 폭 포맷: "00" → 개별 숫자 분리 (각 필드는 0~3 범위)
        for (int i = 0; i < len && nFields < 10; i++) {
          if (tok[i] >= '0' && tok[i] <= '9') {
            fields[nFields++] = tok[i] - '0';
          }
        }
      } else {
        fields[nFields++] = atoi(tok);
      }
    }

    asynPrint(pC_->pasynUserSelf, ASYN_TRACE_FLOW,
              "KohzuAriesAxis::poll: STR%d nFields=%d [%d,%d,%d,%d,%d,%d]\n",
              axisID, nFields,
              nFields > 0 ? fields[0] : -1, nFields > 1 ? fields[1] : -1,
              nFields > 2 ? fields[2] : -1, nFields > 3 ? fields[3] : -1,
              nFields > 4 ? fields[4] : -1, nFields > 5 ? fields[5] : -1);

    // ARIES 매뉴얼 기준 필드 매핑:
    // [0]=구동상태(0/1/2), [1]=EMG, [2]=ORG센서, [3]=리미트, [4]=소프트리미트, [5]=보정
    if (nFields >= 1) {
      r_drive = fields[0];
      parsed = true;
    }
    if (nFields >= 2) r_emg     = fields[1];
    if (nFields >= 3) r_org     = fields[2];
    if (nFields >= 4) r_limits  = fields[3];
    if (nFields >= 5) r_softlim = fields[4];
  }

  if (parsed) {
    // 구동 상태 (0=정지, 1=동작중, 2=피드백동작중)
    *moving = (r_drive != 0);
    setIntegerParam(pC_->motorStatusDone_, !(*moving));

    // ★ 이동 중 상태를 MSTA에 명시적으로 반영
    // 기존에 이 설정이 누락되어 이동 중 MSTA=0이 되는 문제 발생
    setIntegerParam(pC_->motorStatusMoving_, (*moving) ? 1 : 0);

    // 비상정지(EMG) → Problem 플래그
    setIntegerParam(pC_->motorStatusProblem_, (r_emg != 0));

    // 리미트 비트마스크 디코딩
    // e=0: 양쪽 OFF, e=1: CCW만 ON, e=2: CW만 ON, e=3: 양쪽 ON
    int cwLimit  = (r_limits & 0x02) ? 1 : 0; // bit 1 = CW
    int ccwLimit = (r_limits & 0x01) ? 1 : 0; // bit 0 = CCW
    setIntegerParam(pC_->motorStatusHighLimit_, cwLimit);
    setIntegerParam(pC_->motorStatusLowLimit_,  ccwLimit);

    // ── 원점 상태: Method 4 (NORG 에지) 전용 처리 ──
    // STR 'd' 필드: ORG/NORG 센서 비트마스크
    //   d=0: 양쪽 OFF, d=1: NORG ON, d=2: ORG ON, d=3: 양쪽 ON

    // motorStatusAtHome_: 현재 물리적으로 원점 위치에 있는지 (센서 실시간)
    setIntegerParam(pC_->motorStatusAtHome_, (r_org != 0) ? 1 : 0);

    // ★ homing 완료 감지: homingActive_ 중 구동 정지(r_drive==0) 시점
    //    이때 homed_를 true로 설정하고 이후 유지
    if (homingActive_ && r_drive == 0) {
      // 원점 복귀 완료: NORG 에지에서 정지 + 좌표 0 리셋 완료
      homed_ = true;
      homingActive_ = false;
      asynPrint(pC_->pasynUserSelf, ASYN_TRACE_ERROR,
                "KohzuAriesAxis::poll: axis=%d homing COMPLETE "
                "(Method 4, NORG sensor d=%d)\n", axisID, r_org);
    }

    // motorStatusHomed_: 원점 복귀를 수행했는지 (소프트웨어 래치)
    //   → 원점에서 벗어나도 유지 (전원 OFF까지 보존)
    setIntegerParam(pC_->motorStatusHomed_, homed_ ? 1 : 0);

  } else {
    // 파싱 실패 → 안전 폴백
    asynPrint(pC_->pasynUserSelf, ASYN_TRACE_ERROR,
              "KohzuAriesAxis::poll: STR%d parse FAILED raw='%s'\n",
              axisID, responseCopy);
    *moving = false;
    setIntegerParam(pC_->motorStatusDone_, 1);
    setIntegerParam(pC_->motorStatusProblem_, 1);
  }

  // ----- 2. RDP: 위치 조회 -----
  sprintf(command, "RDP%d", axisID);
  memset(response, 0, sizeof(response));
  status = pasynOctetSyncIO->writeRead(
      pC_->pasynUserSelf, command, strlen(command), response, sizeof(response),
      CMD_TIMEOUT, &nwrite, &nread, &eomReason);

  if (status == asynSuccess) {
    asynPrint(pC_->pasynUserSelf, ASYN_TRACE_FLOW,
              "KohzuAriesAxis::poll: RDP%d raw='%s'\n", axisID, response);

    // RDP 응답: "C RDP<axis> <position>"
    token = strtok(response, delimiters);

    // 에러 체크
    if (token && strcmp(token, "E") == 0) {
      asynPrint(pC_->pasynUserSelf, ASYN_TRACE_ERROR,
                "KohzuAriesAxis::poll: RDP%d error response\n", axisID);
    } else if (token && strcmp(token, "C") == 0) {
      token = strtok(NULL, delimiters); // "RDP1"
      token = strtok(NULL, delimiters); // 위치값

      if (token) {
        double pos = atof(token);
        setDoubleParam(pC_->motorPosition_, pos);
        setDoubleParam(pC_->motorEncoderPosition_, pos);
      }
    }
  }

  callParamCallbacks();
  return asynSuccess;
}

// ================================================================
// 리포트
// ================================================================
void KohzuAriesController::report(FILE *fp, int level) {
  fprintf(fp, "KohzuAriesController: port=%s\n", portName);
  if (level > 0) {
    fprintf(fp, "  Connected to ARIES/LYNX controller\n");
    fprintf(fp, "  Command timeout: %.1f sec\n", CMD_TIMEOUT);
  }
  asynMotorController::report(fp, level);
}

void KohzuAriesAxis::report(FILE *fp, int level) {
  int method = 4;
  pC_->getIntegerParam(axisNo_, pC_->homingMethod_, &method);
  fprintf(fp, "  Axis %d (ARIES axis %d)\n", axisNo_, axisNo_ + 1);
  if (level > 0) {
    fprintf(fp, "    Hardware status driven (STR command)\n");
    fprintf(fp, "    Homing: Method=%d, homed=%s, active=%s\n",
            method, homed_ ? "YES" : "NO",
            homingActive_ ? "YES" : "NO");
  }
  asynMotorAxis::report(fp, level);
}

// ================================================================
// IOC Shell 등록
// ================================================================
static const iocshArg KohzuAriesCreateControllerArg0 = {"Port name",
                                                        iocshArgString};
static const iocshArg KohzuAriesCreateControllerArg1 = {"KohzuAries port name",
                                                        iocshArgString};
static const iocshArg KohzuAriesCreateControllerArg2 = {"Number of axes",
                                                        iocshArgInt};
static const iocshArg KohzuAriesCreateControllerArg3 = {
    "Moving poll period (s)", iocshArgDouble};
static const iocshArg KohzuAriesCreateControllerArg4 = {"Idle poll period (s)",
                                                        iocshArgDouble};
static const iocshArg *const KohzuAriesCreateControllerArgs[] = {
    &KohzuAriesCreateControllerArg0, &KohzuAriesCreateControllerArg1,
    &KohzuAriesCreateControllerArg2, &KohzuAriesCreateControllerArg3,
    &KohzuAriesCreateControllerArg4};
static const iocshFuncDef KohzuAriesCreateControllerDef = {
    "KohzuAriesCreateController", 5, KohzuAriesCreateControllerArgs};
static void KohzuAriesCreateContollerCallFunc(const iocshArgBuf *args) {
  KohzuAriesCreateController(args[0].sval, args[1].sval, args[2].ival,
                             args[3].dval, args[4].dval);
}

static void KohzuAriesRegister(void) {
  iocshRegister(&KohzuAriesCreateControllerDef,
                KohzuAriesCreateContollerCallFunc);
}

extern "C" {
epicsExportRegistrar(KohzuAriesRegister);
}
