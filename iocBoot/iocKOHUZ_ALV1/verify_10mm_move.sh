#!/bin/bash
# 10mm Forward/Backward Move Verification Script

MOTOR_PV="KOHZU:m1"

echo "=========================================="
echo " [10mm Move Verification] Target: $MOTOR_PV"
echo "=========================================="

# 1. Connection Check
caget ${MOTOR_PV}.VAL > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: IOC is not running or PV is disconnected."
    exit 1
fi

# 이동 완료 대기 함수 (caget 실패 및 타임아웃 처리 포함)
wait_for_done() {
    local timeout=60
    local count=0
    local max_count=$((timeout * 2))  # 0.5초 간격이므로 x2
    echo "   ... Waiting for move completion (timeout: ${timeout}s) ..."
    while true; do
        DMOV=$(caget -t ${MOTOR_PV}.DMOV 2>/dev/null)
        CAGET_STATUS=$?

        # caget 실패 또는 빈 값이면 재시도
        if [ $CAGET_STATUS -ne 0 ] || [ -z "$DMOV" ]; then
            echo "   [DEBUG] caget failed (status=$CAGET_STATUS). Retrying..."
            count=$((count+1))
            if [ $count -ge $max_count ]; then
                echo "🚨 [ERROR] Timeout! (caget keeps failing)"
                exit 1
            fi
            sleep 0.5
            continue
        fi

        # 디버그 출력 (5회마다 = 약 2.5초 간격)
        if [ $((count % 5)) -eq 0 ]; then
            RBV=$(caget -t ${MOTOR_PV}.RBV 2>/dev/null)
            echo "   [DEBUG] DMOV=$DMOV  RBV=$RBV  (${count}/${max_count})"
        fi

        # 이동 완료 확인
        if [ "$DMOV" = "1" ]; then
            echo "   -> Move Complete (DMOV=1)."
            break
        fi

        # 타임아웃 처리
        count=$((count+1))
        if [ $count -ge $max_count ]; then
            echo "🚨 [ERROR] Timeout waiting for move completion!"
            caput ${MOTOR_PV}.STOP 1
            exit 1
        fi
        sleep 0.5
    done
}

# 2. Get Start Position
START_POS=$(caget -t ${MOTOR_PV}.RBV)
echo "Start Position: $START_POS mm"

# 3. Step 1: Move +10mm Relative (Forward)
echo -e "\n[Step 1] Moving +10mm Relative (Forward)..."
caput ${MOTOR_PV}.RLV 10.0
sleep 1  # 드라이버가 이동을 시작할 시간 확보
wait_for_done

# 4. Check Forward Result
MID_POS=$(caget -t ${MOTOR_PV}.RBV)
echo "Position after Forward: $MID_POS mm"
DIFF_FWD=$(python3 -c "print($MID_POS - $START_POS)")
echo "Forward Distance: $DIFF_FWD mm"

# 5. Step 2: Move -10mm Relative (Backward)
echo -e "\n[Step 2] Moving -10mm Relative (Backward)..."
caput ${MOTOR_PV}.RLV -10.0
sleep 1  # 드라이버가 이동을 시작할 시간 확보
wait_for_done

# 6. Check Backward Result
END_POS=$(caget -t ${MOTOR_PV}.RBV)
echo "Final Position: $END_POS mm"
DIFF_TOTAL=$(python3 -c "print($END_POS - $START_POS)")
echo "Total displacement from start: $DIFF_TOTAL mm"

echo -e "\nVerification Done."

