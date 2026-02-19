#!/bin/bash
# ==============================================================================
# 20mm 전/후진 속도 증가 반복 검증 스크립트
# - 전진(+20mm) + 후진(-20mm)을 1 사이클로 총 10회 반복
# - 매 사이클마다 VELO(속도)를 단계적으로 증가시켜 검증
# - 각 사이클의 이동 거리, 소요 시간, 실제 속도를 기록
# ==============================================================================

MOTOR_PV="KOHZU:m1"
MOVE_DIST=20.0          # 이동 거리 (mm)
TOTAL_CYCLES=5          # 총 반복 횟수
BASE_VELO=0.5           # 시작 속도 (mm/s)
VELO_STEP=1.0           # 매 사이클 속도 증가량 (mm/s) → 최종 4.1 mm/s (VMAX=4.0 이내 안전 범위)
TIMEOUT_SEC=120         # 이동 대기 타임아웃 (초)

echo "================================================================="
echo " [20mm Speed Ramp Test] Target: $MOTOR_PV"
echo " 이동 거리: ±${MOVE_DIST}mm × ${TOTAL_CYCLES}회"
echo " 속도 범위: ${BASE_VELO} ~ $(python3 -c "print(${BASE_VELO} + ${VELO_STEP} * (${TOTAL_CYCLES} - 1))") mm/s"
echo "================================================================="

# ---------------------------------------------------------------
# 1. 연결 확인
# ---------------------------------------------------------------
caget ${MOTOR_PV}.VAL > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "🚨 ERROR: IOC에 연결할 수 없습니다. IOC 상태를 확인하세요."
    exit 1
fi
echo "✅ IOC 연결 확인 완료."

# ---------------------------------------------------------------
# 이동 완료 대기 함수
# ---------------------------------------------------------------
wait_for_done() {
    local timeout=$TIMEOUT_SEC
    local count=0
    local max_count=$((timeout * 2))  # 0.5초 간격
    while true; do
        DMOV=$(caget -t ${MOTOR_PV}.DMOV 2>/dev/null)
        CAGET_STATUS=$?

        # caget 실패 시 재시도
        if [ $CAGET_STATUS -ne 0 ] || [ -z "$DMOV" ]; then
            count=$((count+1))
            if [ $count -ge $max_count ]; then
                echo "   🚨 Timeout! (caget 실패 지속)"
                return 1
            fi
            sleep 0.5
            continue
        fi

        # 주기적 디버그 출력 (약 5초 간격)
        if [ $((count % 10)) -eq 0 ] && [ $count -gt 0 ]; then
            RBV=$(caget -t ${MOTOR_PV}.RBV 2>/dev/null)
            echo "   [진행] DMOV=$DMOV  RBV=${RBV}mm  (${count}/${max_count})"
        fi

        # 이동 완료 확인
        if [ "$DMOV" = "1" ]; then
            return 0
        fi

        # 타임아웃 처리
        count=$((count+1))
        if [ $count -ge $max_count ]; then
            echo "   🚨 Timeout! (${timeout}초 초과)"
            caput ${MOTOR_PV}.STOP 1 > /dev/null 2>&1
            return 1
        fi
        sleep 0.5
    done
}

# ---------------------------------------------------------------
# 시간 측정 함수 (밀리초 정밀도)
# ---------------------------------------------------------------
get_time_ms() {
    python3 -c "import time; print(f'{time.time():.3f}')"
}

# ---------------------------------------------------------------
# 2. 초기 상태 기록
# ---------------------------------------------------------------
ORIGIN_POS=$(caget -t ${MOTOR_PV}.RBV)
ORIG_VELO=$(caget -t ${MOTOR_PV}.VELO)
echo "초기 위치: ${ORIGIN_POS} mm"
echo "원래 속도: ${ORIG_VELO} mm/s"
echo ""

# 결과 테이블 헤더
echo "================================================================="
printf "%-6s %-10s %-8s %-8s %-10s %-10s %-8s %s\n" \
       "Cycle" "VELO" "방향" "거리(mm)" "시간(s)" "실속도" "오차(mm)" "결과"
echo "-----------------------------------------------------------------"

# ---------------------------------------------------------------
# 3. 반복 검증 루프
# ---------------------------------------------------------------
PASS_COUNT=0
FAIL_COUNT=0

for i in $(seq 1 $TOTAL_CYCLES); do
    # 현재 사이클의 속도 계산
    CURRENT_VELO=$(python3 -c "print(round(${BASE_VELO} + ${VELO_STEP} * ($i - 1), 1))")

    # 속도 설정
    caput -w 5 ${MOTOR_PV}.VELO $CURRENT_VELO > /dev/null 2>&1

    # === 전진 (+20mm) ===
    POS_BEFORE=$(caget -t ${MOTOR_PV}.RBV)
    T_START=$(get_time_ms)

    caput ${MOTOR_PV}.RLV $MOVE_DIST > /dev/null 2>&1
    sleep 0.5  # 드라이버 시작 대기

    if wait_for_done; then
        T_END=$(get_time_ms)
        POS_AFTER=$(caget -t ${MOTOR_PV}.RBV)

        # 이동 거리, 소요 시간, 실측 속도, 오차 계산
        RESULT=$(python3 -c "
before=$POS_BEFORE; after=$POS_AFTER; t0=$T_START; t1=$T_END; target=$MOVE_DIST
dist = after - before
elapsed = t1 - t0
speed = abs(dist) / elapsed if elapsed > 0 else 0
error = abs(dist) - target
status = 'PASS' if abs(error) < 0.01 else 'FAIL'
print(f'{abs(dist):.4f} {elapsed:.2f} {speed:.3f} {error:.4f} {status}')
")
        read DIST ELAPSED SPEED ERROR STATUS <<< "$RESULT"

        if [ "$STATUS" = "PASS" ]; then
            PASS_COUNT=$((PASS_COUNT+1))
            MARK="✅"
        else
            FAIL_COUNT=$((FAIL_COUNT+1))
            MARK="❌"
        fi

        printf "%-6s %-10s %-8s %-8s %-10s %-10s %-8s %s\n" \
               "#$i" "${CURRENT_VELO}" "전진" "$DIST" "$ELAPSED" "$SPEED" "$ERROR" "$MARK"
    else
        FAIL_COUNT=$((FAIL_COUNT+1))
        printf "%-6s %-10s %-8s %-8s %-10s %-10s %-8s %s\n" \
               "#$i" "${CURRENT_VELO}" "전진" "---" "TIMEOUT" "---" "---" "❌"
    fi

    # === 후진 (-20mm) ===
    POS_BEFORE=$(caget -t ${MOTOR_PV}.RBV)
    T_START=$(get_time_ms)

    caput ${MOTOR_PV}.RLV -${MOVE_DIST} > /dev/null 2>&1
    sleep 0.5

    if wait_for_done; then
        T_END=$(get_time_ms)
        POS_AFTER=$(caget -t ${MOTOR_PV}.RBV)

        RESULT=$(python3 -c "
before=$POS_BEFORE; after=$POS_AFTER; t0=$T_START; t1=$T_END; target=$MOVE_DIST
dist = before - after
elapsed = t1 - t0
speed = abs(dist) / elapsed if elapsed > 0 else 0
error = abs(dist) - target
status = 'PASS' if abs(error) < 0.01 else 'FAIL'
print(f'{abs(dist):.4f} {elapsed:.2f} {speed:.3f} {error:.4f} {status}')
")
        read DIST ELAPSED SPEED ERROR STATUS <<< "$RESULT"

        if [ "$STATUS" = "PASS" ]; then
            PASS_COUNT=$((PASS_COUNT+1))
            MARK="✅"
        else
            FAIL_COUNT=$((FAIL_COUNT+1))
            MARK="❌"
        fi

        printf "%-6s %-10s %-8s %-8s %-10s %-10s %-8s %s\n" \
               "#$i" "${CURRENT_VELO}" "후진" "$DIST" "$ELAPSED" "$SPEED" "$ERROR" "$MARK"
    else
        FAIL_COUNT=$((FAIL_COUNT+1))
        printf "%-6s %-10s %-8s %-8s %-10s %-10s %-8s %s\n" \
               "#$i" "${CURRENT_VELO}" "후진" "---" "TIMEOUT" "---" "---" "❌"
    fi
done

# ---------------------------------------------------------------
# 4. 최종 결과 출력
# ---------------------------------------------------------------
echo "================================================================="
echo ""

# 최종 위치 확인
FINAL_POS=$(caget -t ${MOTOR_PV}.RBV)
TOTAL_DRIFT=$(python3 -c "print(f'{$FINAL_POS - $ORIGIN_POS:.4f}')")

echo "==============================="
echo "       최종 검증 리포트"
echo "==============================="
echo "총 이동 횟수: $((TOTAL_CYCLES * 2))회 (전진 ${TOTAL_CYCLES} + 후진 ${TOTAL_CYCLES})"
echo "  ✅ PASS: ${PASS_COUNT}건"
echo "  ❌ FAIL: ${FAIL_COUNT}건"
echo ""
echo "초기 위치:  ${ORIGIN_POS} mm"
echo "최종 위치:  ${FINAL_POS} mm"
echo "누적 드리프트: ${TOTAL_DRIFT} mm"
echo ""

# 속도 원복
caput -w 5 ${MOTOR_PV}.VELO $ORIG_VELO > /dev/null 2>&1
echo "속도 원복: VELO=${ORIG_VELO} mm/s"

if [ $FAIL_COUNT -eq 0 ]; then
    echo ""
    echo "🎉 전 사이클 PASS — 검증 완료!"
else
    echo ""
    echo "⚠️ ${FAIL_COUNT}건 실패 — 로그를 확인하세요."
fi
echo "==============================="
