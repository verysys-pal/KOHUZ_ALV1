#ifndef KOHZU_ARIES_DRIVER_H
#define KOHZU_ARIES_DRIVER_H

/*
 * Kohzu ARIES/LYNX EPICS Motor Driver
 *
 * 지원 명령: APS, RPS, FRP, ORG, STP, WTB, WSY, RSY, STR, RDP
 * 프로토콜: TCP/IP, CRLF terminated
 *
 * 원점 복귀 지원 방식:
 *   Method 4  — NORG 센서 에지 (Kohzu 표준)
 *   Method 7  — CW Limit 에지
 *   Method 8  — CCW Limit 에지
 */

#include "asynMotorController.h"
#include "asynMotorAxis.h"

// 커스텀 파라미터 문자열 (EPICS DB 연동용)
#define KohzuHomingMethodString "KOHZU_HOMING_METHOD"

// 커스텀 파라미터 개수
#define NUM_KOHZU_PARAMS 1

class epicsShareClass KohzuAriesAxis : public asynMotorAxis {
public:
    KohzuAriesAxis(class KohzuAriesController *pC, int axisNo);

    // asynMotorAxis 인터페이스 구현
    void report(FILE *fp, int level);
    asynStatus move(double position, int relative,
                    double minVelocity, double maxVelocity, double acceleration);
    asynStatus moveVelocity(double minVelocity, double maxVelocity,
                            double acceleration);
    asynStatus home(double minVelocity, double maxVelocity,
                    double acceleration, int forwards);
    asynStatus stop(double acceleration);
    asynStatus poll(bool *moving);

private:
    KohzuAriesController *pC_;

    // ── 원점 복귀 상태 추적 ──
    bool homed_;          // 원점 복귀 완료 플래그 (전원 OFF까지 유지)
    bool homingActive_;   // 원점 복귀 진행 중 플래그 (poll()에서 완료 감지)

    // Speed Table #0에 속도 파라미터 설정 (WTB 명령)
    asynStatus setSpeedTable(double minVelocity, double maxVelocity,
                             double acceleration);

    // WSY 명령으로 ARIES System Parameter 설정
    asynStatus setSystemParam(int sysNo, int value);

    friend class KohzuAriesController;
};

class epicsShareClass KohzuAriesController : public asynMotorController {
public:
    KohzuAriesController(const char *portName, const char *KohzuAriesPortName,
                         int numAxes, double movingPollPeriod,
                         double idlePollPeriod);
    void report(FILE *fp, int level);

    // 명령 전송 (응답 있음: writeRead)
    asynStatus sendCommand(const char *command, char *response,
                           size_t responseLen, double timeout);
    // 명령 전송 (응답 무시: write only)
    asynStatus sendOnly(const char *command, double timeout);

protected:
    // 커스텀 파라미터 인덱스
    int homingMethod_;    // KOHZU_HOMING_METHOD: 4, 7, 8
#define FIRST_KOHZU_PARAM homingMethod_

    friend class KohzuAriesAxis;
};

#endif // KOHZU_ARIES_DRIVER_H
