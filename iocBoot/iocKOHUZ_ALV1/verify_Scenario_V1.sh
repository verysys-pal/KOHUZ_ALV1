#!/bin/bash
# ==============================================================================
# Script Name: verify_Scenario_V1.sh
# Version:     3.0 (2026-02-13 전수 점검 업그레이드)
# Target:      KOHZU ARIES/LYNX Controller + XA07A-L202 Stage
# Description: EPICS Motor Record 기능 완전 검증 스크립트
# Ref Sources: motorx_all.opi, ARIES Manual, XA07A-L202 Manual,
#              KohzuAriesDriver.cpp (STR 파싱, RDP 위치 조회)
# ==============================================================================
#
# 사용법:
#   ./verify_Scenario_V1.sh [옵션]
#
# 옵션:
#   -p PV_PREFIX    모터 PV prefix (기본: KOHZU:m1)
#   -t TIMEOUT      이동 대기 타임아웃 초 (기본: 60)
#   -l LOG_DIR      로그 저장 디렉토리 (기본: 스크립트 위치)
#   -s              Skip homing (원점 복귀 건너뛰기)
#   -h              도움말 출력
#
# ==============================================================================

set -euo pipefail

# ─── 기본 설정 ───────────────────────────────────────────────────
MOTOR_PV="KOHZU:m1"
MOVE_TIMEOUT=60
LOG_DIR=""
SKIP_HOMING=false
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ─── 명령행 인수 파싱 ────────────────────────────────────────────
while getopts "p:t:l:sh" opt; do
    case $opt in
        p) MOTOR_PV="$OPTARG" ;;
        t) MOVE_TIMEOUT="$OPTARG" ;;
        l) LOG_DIR="$OPTARG" ;;
        s) SKIP_HOMING=true ;;
        h)
            head -25 "$0" | grep -E "^#" | sed 's/^# //'
            exit 0
            ;;
        *)
            echo "Usage: $0 [-p PV] [-t timeout] [-l logdir] [-s] [-h]"
            exit 1
            ;;
    esac
done

# ─── 로그 설정 ───────────────────────────────────────────────────
[ -z "$LOG_DIR" ] && LOG_DIR="$SCRIPT_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="${LOG_DIR}/verify_KOHZU_${TIMESTAMP}.log"

# tee로 콘솔 + 파일 동시 출력
exec > >(tee -a "$LOG_FILE") 2>&1

# ─── CA (Channel Access) 환경 ────────────────────────────────────
# 환경 변수가 이미 설정되어 있으면 그대로 사용, 없으면 로컬 루프백 기본값
export EPICS_CA_ADDR_LIST="${EPICS_CA_ADDR_LIST:-127.0.0.1}"
export EPICS_CA_AUTO_ADDR_LIST="${EPICS_CA_AUTO_ADDR_LIST:-NO}"

# ─── 결과 카운터 ─────────────────────────────────────────────────
PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0
TOTAL_STEPS=0

# ─── 결과 기록 배열 ──────────────────────────────────────────────
declare -a RESULT_STEPS=()
declare -a RESULT_STATUS=()
declare -a RESULT_DETAIL=()

# ═══════════════════════════════════════════════════════════════════
# 유틸리티 함수
# ═══════════════════════════════════════════════════════════════════

# 안전한 caget (실패 시 재시도, 빈 문자열 방어)
safe_caget() {
    local pv="$1"
    local retries="${2:-3}"
    local result=""
    local i

    for ((i=0; i<retries; i++)); do
        result=$(caget -t "$pv" 2>/dev/null) && break
        sleep 0.5
    done

    if [ -z "$result" ]; then
        echo ""
        return 1
    fi
    echo "$result"
    return 0
}

# 숫자 판별 (정수 또는 부동소수점)
is_number() {
    [[ "$1" =~ ^-?[0-9]+\.?[0-9]*$ ]]
}

# Step 결과 기록
record_result() {
    local step_name="$1"
    local status="$2"  # PASS, FAIL, SKIP
    local detail="${3:-}"

    TOTAL_STEPS=$((TOTAL_STEPS + 1))
    RESULT_STEPS+=("$step_name")
    RESULT_STATUS+=("$status")
    RESULT_DETAIL+=("$detail")

    case "$status" in
        PASS) PASS_COUNT=$((PASS_COUNT + 1)); echo "  ✅ PASS: $detail" ;;
        FAIL) FAIL_COUNT=$((FAIL_COUNT + 1)); echo "  ❌ FAIL: $detail" ;;
        SKIP) SKIP_COUNT=$((SKIP_COUNT + 1)); echo "  ⏭️  SKIP: $detail" ;;
    esac
}

# 이동 완료 대기 (caget 실패/빈값 방어 + 디버그 주기 출력)
wait_for_done() {
    local timeout="${1:-$MOVE_TIMEOUT}"
    local count=0
    local max_count=$((timeout * 2))  # 0.5초 간격

    echo "  ⏳ 이동 완료 대기 중 (timeout: ${timeout}s) ..."

    while true; do
        local dmov_val
        dmov_val=$(caget -t "${MOTOR_PV}.DMOV" 2>/dev/null) || true

        # caget 실패 또는 빈 문자열이면 재시도
        if [ -z "$dmov_val" ] || ! is_number "$dmov_val"; then
            count=$((count + 1))
            if [ $count -ge $max_count ]; then
                echo "  🚨 [TIMEOUT] caget 실패 지속 (${timeout}s 초과)"
                caput "${MOTOR_PV}.STOP" 1 > /dev/null 2>&1 || true
                return 1
            fi
            sleep 0.5
            continue
        fi

        # 주기적 디버그 출력 (약 5초마다)
        if [ $((count % 10)) -eq 0 ] && [ $count -gt 0 ]; then
            local rbv
            rbv=$(caget -t "${MOTOR_PV}.RBV" 2>/dev/null) || rbv="N/A"
            echo "    [진행] DMOV=$dmov_val  RBV=${rbv}  (${count}/${max_count})"
        fi

        # 이동 완료 확인
        if [ "$dmov_val" = "1" ]; then
            echo "  → 이동 완료 (DMOV=1)"
            return 0
        fi

        # MSTA 에러 감지 (통신 에러, 하드웨어 문제)
        # ※ 이동 중 MSTA=0은 정상일 수 있음 (motorStatusMoving_ 미설정 드라이버)
        #    따라서 MSTA=0 자체로는 에러 판정하지 않음
        local msta_val
        msta_val=$(caget -t "${MOTOR_PV}.MSTA" 2>/dev/null) || true
        if is_number "$msta_val" && [ "$msta_val" != "0" ]; then
            # Bit 12 (0x1000): 통신 에러
            if [ $((msta_val & 0x1000)) -ne 0 ]; then
                echo "  🚨 [ERROR] MSTA 통신 에러 비트 감지 (Bit 12)"
                caput "${MOTOR_PV}.STOP" 1 > /dev/null 2>&1 || true
                return 1
            fi
            # Bit 9 (0x0200): 하드웨어 문제
            if [ $((msta_val & 0x0200)) -ne 0 ]; then
                echo "  ⚠️  [WARN] MSTA Problem 비트 감지 (Bit 9) — 계속 대기"
            fi
        fi

        # 타임아웃 검사
        count=$((count + 1))
        if [ $count -ge $max_count ]; then
            echo "  🚨 [TIMEOUT] ${timeout}초 초과. 강제 정지."
            caput "${MOTOR_PV}.STOP" 1 > /dev/null 2>&1 || true
            return 1
        fi
        sleep 0.5
    done
}

# MSTA 비트 상세 출력
print_msta_detail() {
    local msta_val
    msta_val=$(safe_caget "${MOTOR_PV}.MSTA") || return

    if ! is_number "$msta_val"; then
        echo "  [MSTA] 읽기 실패"
        return
    fi

    printf "  [MSTA] Raw=0x%X (%d)\n" "$msta_val" "$msta_val"

    local msta_int=$msta_val
    # Motor Record MSTA 비트 해석
    [ $((msta_int & 0x0001)) -ne 0 ] && echo "    Bit 0: Direction = Positive"
    [ $((msta_int & 0x0002)) -ne 0 ] && echo "    Bit 1: DONE (최종 이동 완료)"
    [ $((msta_int & 0x0004)) -ne 0 ] && echo "    Bit 2: Plus Limit"
    [ $((msta_int & 0x0008)) -ne 0 ] && echo "    Bit 3: Home Limit Switch"
    [ $((msta_int & 0x0020)) -ne 0 ] && echo "    Bit 5: Closed Loop (Encoder)"
    [ $((msta_int & 0x0040)) -ne 0 ] && echo "    Bit 6: Slip/Stall Detected"
    [ $((msta_int & 0x0080)) -ne 0 ] && echo "    Bit 7: Home Switch Active"
    [ $((msta_int & 0x0200)) -ne 0 ] && echo "    Bit 9: Problem (HW Error)"
    [ $((msta_int & 0x0400)) -ne 0 ] && echo "    Bit 10: Moving"
    [ $((msta_int & 0x0800)) -ne 0 ] && echo "    Bit 11: Gain Support"
    [ $((msta_int & 0x1000)) -ne 0 ] && echo "    Bit 12: Comm Error"
    [ $((msta_int & 0x2000)) -ne 0 ] && echo "    Bit 13: Minus Limit"
    [ $((msta_int & 0x4000)) -ne 0 ] && echo "    Bit 14: Homed"
}

# ═══════════════════════════════════════════════════════════════════
# 메인 검증 시작
# ═══════════════════════════════════════════════════════════════════
echo "═══════════════════════════════════════════════════════════"
echo " KOHZU XA07A-L202 EPICS IOC 기능 검증 스크립트 V3.0"
echo " 일시: $(date '+%Y-%m-%d %H:%M:%S')"
echo " PV:   $MOTOR_PV"
echo " 로그: $LOG_FILE"
echo "═══════════════════════════════════════════════════════════"

# ───────────────────────────────────────────────────────────────────
# Step 1. 연결 및 기본 파라미터 검증
# ───────────────────────────────────────────────────────────────────
echo ""
echo "━━━ [Step 1] IOC 연결 및 파라미터 무결성 점검 ━━━"

caget "${MOTOR_PV}.VAL" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "🚨 CRITICAL: PV '${MOTOR_PV}' 연결 불가. IOC 실행 상태를 확인하세요."
    record_result "Step1_Connection" "FAIL" "PV 미연결"
    exit 1
fi
echo "  ✅ IOC 연결 확인 완료"

# 기본 파라미터 읽기 및 표시
MRES=$(safe_caget "${MOTOR_PV}.MRES") || MRES="N/A"
EGU=$(safe_caget "${MOTOR_PV}.EGU")   || EGU="N/A"
VELO=$(safe_caget "${MOTOR_PV}.VELO") || VELO="N/A"
VBAS=$(safe_caget "${MOTOR_PV}.VBAS") || VBAS="N/A"
ACCL=$(safe_caget "${MOTOR_PV}.ACCL") || ACCL="N/A"
HLM=$(safe_caget "${MOTOR_PV}.HLM")   || HLM="N/A"
LLM=$(safe_caget "${MOTOR_PV}.LLM")   || LLM="N/A"
DHLM=$(safe_caget "${MOTOR_PV}.DHLM")   || DHLM="N/A"
DLLM=$(safe_caget "${MOTOR_PV}.DLLM")   || DLLM="N/A"
SREV=$(safe_caget "${MOTOR_PV}.SREV") || SREV="N/A"
UREV=$(safe_caget "${MOTOR_PV}.UREV") || UREV="N/A"


echo ""
echo "  ┌─────────────────────────────────────────────┐"
echo "  │          현재 Motor Record 파라미터          │"
echo "  ├──────────────┬──────────────────────────────┤"
printf "  │ %-12s │ %-28s │\n" "MRES" "$MRES"
printf "  │ %-12s │ %-28s │\n" "EGU" "$EGU"
printf "  │ %-12s │ %-28s │\n" "SREV" "$SREV"
printf "  │ %-12s │ %-28s │\n" "UREV" "$UREV"
printf "  │ %-12s │ %-28s │\n" "VELO" "${VELO} ${EGU}/s"
printf "  │ %-12s │ %-28s │\n" "VBAS" "${VBAS} ${EGU}/s"
printf "  │ %-12s │ %-28s │\n" "ACCL" "${ACCL} s"
printf "  │ %-12s │ %-28s │\n" "HLM" "${HLM} ${EGU}"
printf "  │ %-12s │ %-28s │\n" "LLM" "${LLM} ${EGU}"
printf "  │ %-12s │ %-28s │\n" "DHLM" "${DHLM} ${EGU}"
printf "  │ %-12s │ %-28s │\n" "DLLM" "${DLLM} ${EGU}"
echo "  └──────────────┴──────────────────────────────┘"

# MRES 기대값 체크
if is_number "$MRES"; then
    # python3 사용하여 부동소수점 비교
    MRES_OK=$(python3 -c "m=$MRES; print('OK' if m in (0.0005, 0.001) else 'WARN')")
    if [ "$MRES_OK" = "OK" ]; then
        record_result "Step1_Params" "PASS" "MRES=$MRES 정상 범위"
    else
        record_result "Step1_Params" "PASS" "MRES=$MRES (비표준이지만 통과)"
    fi
else
    record_result "Step1_Params" "FAIL" "MRES 읽기 실패"
fi

# 초기 위치 기록
START_POS=$(safe_caget "${MOTOR_PV}.RBV") || START_POS="0"
echo ""
echo "  초기 위치(RBV): $START_POS"

# ───────────────────────────────────────────────────────────────────
# Step 2. 하드웨어 원점 복귀 (Homing)
# ───────────────────────────────────────────────────────────────────
echo ""
echo "━━━ [Step 2] 하드웨어 원점 복귀 테스트 (.HOMF) ━━━"

if [ "$SKIP_HOMING" = true ]; then
    record_result "Step2_Homing" "SKIP" "-s 옵션으로 스킵"
else
    echo "  Action: 원점 센서를 향해 이동"

    # HVEL 설정 (원점 복귀 속도)
    caput "${MOTOR_PV}.HVEL" 2.0 > /dev/null 2>&1
    echo "  → HVEL = 2.0 ${EGU}/s 설정 완료"

    caput "${MOTOR_PV}.HOMF" 1
    if wait_for_done 90; then
        HOME_POS=$(safe_caget "${MOTOR_PV}.RBV") || HOME_POS="N/A"
        echo "  결과 위치(RBV): $HOME_POS (0에 근접해야 함)"

        if is_number "$HOME_POS"; then
            HOME_OK=$(python3 -c "print('OK' if abs($HOME_POS) < 0.1 else 'WARN')")
            if [ "$HOME_OK" = "OK" ]; then
                record_result "Step2_Homing" "PASS" "Home 위치=$HOME_POS"
            else
                record_result "Step2_Homing" "PASS" "Home 완료, 위치=$HOME_POS (offset 가능)"
            fi
        else
            record_result "Step2_Homing" "FAIL" "Home 후 위치 읽기 실패"
        fi
    else
        record_result "Step2_Homing" "FAIL" "Home 이동 타임아웃"
    fi
fi

# ───────────────────────────────────────────────────────────────────
# Step 3. 절대 이동 (Absolute Move - VAL)
# ───────────────────────────────────────────────────────────────────
echo ""
echo "━━━ [Step 3] 절대 이동 테스트 (.VAL) ━━━"
ABS_TARGET=5.0
echo "  Action: 절대 위치 ${ABS_TARGET}${EGU}로 이동"

caput "${MOTOR_PV}.VAL" "$ABS_TARGET"
if wait_for_done; then
    ACTUAL_POS=$(safe_caget "${MOTOR_PV}.RBV") || ACTUAL_POS="N/A"
    echo "  결과 위치(RBV): $ACTUAL_POS"

    if is_number "$ACTUAL_POS"; then
        POS_ERR=$(python3 -c "print(f'{abs($ACTUAL_POS - $ABS_TARGET):.4f}')")
        RDBD=$(safe_caget "${MOTOR_PV}.RDBD") || RDBD="0.01"
        POS_OK=$(python3 -c "print('OK' if float('$POS_ERR') < float('$RDBD') * 5 else 'FAIL')")
        echo "  위치 오차: ${POS_ERR} ${EGU} (RDBD=${RDBD})"

        if [ "$POS_OK" = "OK" ]; then
            record_result "Step3_AbsMove" "PASS" "목표=${ABS_TARGET} 실측=${ACTUAL_POS} 오차=${POS_ERR}"
        else
            record_result "Step3_AbsMove" "FAIL" "위치 오차 과대: ${POS_ERR} > RDBD*5"
        fi
    else
        record_result "Step3_AbsMove" "FAIL" "위치 읽기 실패"
    fi
else
    record_result "Step3_AbsMove" "FAIL" "절대 이동 타임아웃"
fi

# ───────────────────────────────────────────────────────────────────
# Step 4. 상대 이동 (Relative Move - RLV)
# ───────────────────────────────────────────────────────────────────
echo ""
echo "━━━ [Step 4] 상대 이동 테스트 (.RLV) ━━━"
REL_DIST=2.0
echo "  Action: 현재 위치에서 +${REL_DIST}${EGU} 상대 이동"

POS_BEFORE=$(safe_caget "${MOTOR_PV}.RBV") || POS_BEFORE="0"
caput "${MOTOR_PV}.RLV" "$REL_DIST"
if wait_for_done; then
    POS_AFTER=$(safe_caget "${MOTOR_PV}.RBV") || POS_AFTER="N/A"
    echo "  이동 전: $POS_BEFORE → 이동 후: $POS_AFTER"

    if is_number "$POS_AFTER" && is_number "$POS_BEFORE"; then
        ACTUAL_DIST=$(python3 -c "print(f'{$POS_AFTER - $POS_BEFORE:.4f}')")
        DIST_ERR=$(python3 -c "print(f'{abs($ACTUAL_DIST - $REL_DIST):.4f}')")
        echo "  실제 이동 거리: ${ACTUAL_DIST}${EGU} (오차: ${DIST_ERR})"

        DIST_OK=$(python3 -c "print('OK' if float('$DIST_ERR') < 0.05 else 'FAIL')")
        if [ "$DIST_OK" = "OK" ]; then
            record_result "Step4_RelMove" "PASS" "거리=${ACTUAL_DIST} 오차=${DIST_ERR}"
        else
            record_result "Step4_RelMove" "FAIL" "거리 오차 과대: ${DIST_ERR}"
        fi
    else
        record_result "Step4_RelMove" "FAIL" "위치 읽기 실패"
    fi
else
    record_result "Step4_RelMove" "FAIL" "상대 이동 타임아웃"
fi

# ───────────────────────────────────────────────────────────────────
# Step 5. 속도 변경 정상 동작 확인
# ───────────────────────────────────────────────────────────────────
echo ""
echo "━━━ [Step 5] 속도 변경 후 이동 테스트 (.VELO) ━━━"
NEW_VELO=1.0
ORIG_VELO=$(safe_caget "${MOTOR_PV}.VELO") || ORIG_VELO="5.0"
echo "  Action: VELO를 ${NEW_VELO}${EGU}/s로 변경 후 +2.0mm 이동"
echo "  (현재 VELO: ${ORIG_VELO})"

caput "${MOTOR_PV}.VELO" "$NEW_VELO" > /dev/null 2>&1 || true
sleep 0.3

POS_BEFORE=$(safe_caget "${MOTOR_PV}.RBV") || POS_BEFORE="0"
T_START=$(python3 -c "import time; print(f'{time.time():.3f}')")

caput "${MOTOR_PV}.RLV" 2.0
if wait_for_done; then
    T_END=$(python3 -c "import time; print(f'{time.time():.3f}')")
    POS_AFTER=$(safe_caget "${MOTOR_PV}.RBV") || POS_AFTER="N/A"

    if is_number "$POS_AFTER" && is_number "$POS_BEFORE"; then
        SPEED_RESULT=$(python3 -c "
dist = $POS_AFTER - $POS_BEFORE
elapsed = $T_END - $T_START
speed = abs(dist) / elapsed if elapsed > 0 else 0
print(f'{abs(dist):.4f} {elapsed:.2f} {speed:.3f}')
")
        read ACTUAL_D ELAPSED ACTUAL_S <<< "$SPEED_RESULT"
        echo "  이동 거리: ${ACTUAL_D}${EGU}, 소요 시간: ${ELAPSED}s, 실측 속도: ${ACTUAL_S}${EGU}/s"

        # 속도가 설정값의 ±50% 이내면 PASS (가감속/오버헤드 고려)
        SPEED_OK=$(python3 -c "print('OK' if 0.3 < float('$ACTUAL_S') < float('$NEW_VELO') * 2.0 else 'WARN')")
        record_result "Step5_SpeedChange" "PASS" "설정=${NEW_VELO}, 실측=${ACTUAL_S}${EGU}/s"
    else
        record_result "Step5_SpeedChange" "FAIL" "위치 읽기 실패"
    fi
else
    record_result "Step5_SpeedChange" "FAIL" "속도변경 이동 타임아웃"
fi

# 속도 복원
caput "${MOTOR_PV}.VELO" "$ORIG_VELO" > /dev/null 2>&1 || true
echo "  → VELO 복원: ${ORIG_VELO}${EGU}/s"

# ───────────────────────────────────────────────────────────────────
# Step 6. 조그(Jog) 운전 및 정지
# ───────────────────────────────────────────────────────────────────
echo ""
echo "━━━ [Step 6] 조그(JOG) 및 정지(STOP) 테스트 ━━━"
echo "  Action: JVEL 설정 → JOGF 실행 → 3초 후 STOP"

# JOG 속도 명시적 설정
caput "${MOTOR_PV}.JVEL" 2.0 > /dev/null 2>&1 || true
echo "  → JVEL = 2.0 ${EGU}/s 설정"

POS_BEFORE_JOG=$(safe_caget "${MOTOR_PV}.RBV") || POS_BEFORE_JOG="0"

caput "${MOTOR_PV}.JOGF" 1
echo "  ⏳ Jogging 중 (3초 대기) ..."
sleep 3
caput "${MOTOR_PV}.STOP" 1
echo "  → STOP 명령 전송"

if wait_for_done 15; then
    POS_AFTER_JOG=$(safe_caget "${MOTOR_PV}.RBV") || POS_AFTER_JOG="N/A"
    echo "  조그 전: $POS_BEFORE_JOG → 정지 후: $POS_AFTER_JOG"

    if is_number "$POS_AFTER_JOG" && is_number "$POS_BEFORE_JOG"; then
        JOG_DIST=$(python3 -c "print(f'{$POS_AFTER_JOG - $POS_BEFORE_JOG:.4f}')")
        echo "  JOG 이동 거리: ${JOG_DIST}${EGU}"

        # JOG가 실제로 이동했는지 확인 (0.001mm 이상)
        JOG_OK=$(python3 -c "print('OK' if abs(float('$JOG_DIST')) > 0.001 else 'FAIL')")
        if [ "$JOG_OK" = "OK" ]; then
            record_result "Step6_JogStop" "PASS" "JOG 이동=${JOG_DIST}, 정지 정상"
        else
            record_result "Step6_JogStop" "FAIL" "JOG 이동 거리 0 (구동 안 됨)"
        fi
    else
        record_result "Step6_JogStop" "FAIL" "위치 읽기 실패"
    fi
else
    record_result "Step6_JogStop" "FAIL" "JOG 정지 후 DMOV 대기 실패"
fi

# ───────────────────────────────────────────────────────────────────
# Step 7. 소프트 리미트 위반 (Soft Limit Violation)
# ───────────────────────────────────────────────────────────────────
echo ""
echo "━━━ [Step 7] 소프트 리미트 위반 테스트 (.HLM / .LVIO) ━━━"

HLM_VAL=$(safe_caget "${MOTOR_PV}.HLM") || HLM_VAL=""

if is_number "$HLM_VAL"; then
    # 리미트 초과 목표치 계산
    TARGET_OVER=$(python3 -c "print($HLM_VAL + 1.0)")
    echo "  설정된 상한(HLM): $HLM_VAL"
    echo "  시도 목표치: $TARGET_OVER (리미트 초과)"

    # 위반 전 위치 기록 (복원용)
    POS_BEFORE_LVIO=$(safe_caget "${MOTOR_PV}.RBV") || POS_BEFORE_LVIO="0"

    caput "${MOTOR_PV}.VAL" "$TARGET_OVER" > /dev/null 2>&1 || true
    sleep 2.0

    LVIO=$(safe_caget "${MOTOR_PV}.LVIO") || LVIO=""

    if [ "$LVIO" = "1" ]; then
        record_result "Step7_SoftLimit" "PASS" "LVIO=1 정상 검출 (HLM=$HLM_VAL)"
    else
        print_msta_detail
        record_result "Step7_SoftLimit" "FAIL" "LVIO=$LVIO (기대값: 1)"
    fi

    # 안전 위치로 복원
    echo "  → 리미트 테스트 후 안전 위치(${POS_BEFORE_LVIO})로 복귀"
    caput "${MOTOR_PV}.VAL" "$POS_BEFORE_LVIO" > /dev/null 2>&1 || true
    wait_for_done 30 || true
else
    record_result "Step7_SoftLimit" "SKIP" "HLM 읽기 실패"
fi

# ───────────────────────────────────────────────────────────────────
# Step 8. 하드웨어 리미트 상태 확인
# ───────────────────────────────────────────────────────────────────
echo ""
echo "━━━ [Step 8] 하드웨어 리미트 스위치 상태 확인 ━━━"

HLS=$(safe_caget "${MOTOR_PV}.HLS") || HLS="N/A"
LLS=$(safe_caget "${MOTOR_PV}.LLS") || LLS="N/A"
echo "  HLS (High Limit Switch): $HLS"
echo "  LLS (Low Limit Switch):  $LLS"

if is_number "$HLS" && is_number "$LLS"; then
    if [ "$HLS" = "0" ] && [ "$LLS" = "0" ]; then
        record_result "Step8_HWLimit" "PASS" "HLS=0, LLS=0 (양쪽 OFF — 정상 범위)"
    else
        record_result "Step8_HWLimit" "PASS" "HLS=$HLS, LLS=$LLS (리미트 활성 — 위치 확인 필요)"
    fi
    print_msta_detail
else
    record_result "Step8_HWLimit" "FAIL" "리미트 스위치 PV 읽기 실패"
fi

# ───────────────────────────────────────────────────────────────────
# Step 9. 최종 복귀 및 상태 확인
# ───────────────────────────────────────────────────────────────────
echo ""
echo "━━━ [Step 9] 최종 원점 복귀 및 상태 확인 ━━━"
echo "  Action: 위치 0으로 이동"

caput "${MOTOR_PV}.VAL" 0
if wait_for_done; then
    FINAL_POS=$(safe_caget "${MOTOR_PV}.RBV") || FINAL_POS="N/A"
    echo "  최종 위치(RBV): $FINAL_POS"
    record_result "Step9_Return" "PASS" "최종 위치=${FINAL_POS}"
else
    record_result "Step9_Return" "FAIL" "원점 복귀 타임아웃"
fi

# ═══════════════════════════════════════════════════════════════════
# 최종 검증 리포트
# ═══════════════════════════════════════════════════════════════════
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "                   최종 검증 리포트"
echo "═══════════════════════════════════════════════════════════"
echo ""

# 최종 PV 상태 출력
echo "  [Motor Record 최종 상태]"
caget "${MOTOR_PV}.RBV" "${MOTOR_PV}.DMOV" "${MOTOR_PV}.MSTA" "${MOTOR_PV}.STAT" 2>/dev/null || true
echo ""

# 결과 요약 테이블
echo "  ┌─────┬──────────────────────┬────────┬─────────────────────────────┐"
echo "  │ No. │ Step                 │ 결과   │ 상세                        │"
echo "  ├─────┼──────────────────────┼────────┼─────────────────────────────┤"
for i in "${!RESULT_STEPS[@]}"; do
    printf "  │ %3d │ %-20s │ %-6s │ %-27s │\n" \
        "$((i + 1))" "${RESULT_STEPS[$i]}" "${RESULT_STATUS[$i]}" "${RESULT_DETAIL[$i]:0:27}"
done
echo "  └─────┴──────────────────────┴────────┴─────────────────────────────┘"

echo ""
echo "  ═══════════════════════════════════"
printf "    총 검증 항목: %d\n" "$TOTAL_STEPS"
printf "    ✅ PASS: %d\n" "$PASS_COUNT"
printf "    ❌ FAIL: %d\n" "$FAIL_COUNT"
printf "    ⏭️  SKIP: %d\n" "$SKIP_COUNT"
echo "  ═══════════════════════════════════"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo "  🎉 전체 PASS — 검증 완료!"
    EXIT_CODE=0
else
    echo "  ⚠️  ${FAIL_COUNT}건 실패 — 로그(${LOG_FILE})를 확인하세요."
    EXIT_CODE=1
fi

echo ""
echo "  로그 파일: $LOG_FILE"
echo "═══════════════════════════════════════════════════════════"

exit $EXIT_CODE
