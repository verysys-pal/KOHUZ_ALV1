#!../../bin/linux-x86_64/KOHUZ_ALV1

#- You may have to change KOHUZ_ALV1 to something else
#- everywhere it appears in this file

#< envPaths

## Register all support components
dbLoadDatabase "../../dbd/KOHUZ_ALV1.dbd"
KOHUZ_ALV1_registerRecordDeviceDriver(pdbbase)

## Load record instances
dbLoadTemplate("motor.substitutions")

# 1. IP 포트 구성 (noProcessEos를 1로 설정하여 수동 EOS 간섭 배제)
drvAsynIPPortConfigure("L0", "192.168.1.120:12321", 0, 0, 0)

# 2. [필수] Kohzu 컨트롤러를 위한 종단 문자 설정
# Kohzu ARIES/LYNX는 표준 CRLF(\r\n)를 사용합니다.
asynOctetSetInputEos("L0", 0, "\r\n")
asynOctetSetOutputEos("L0", 0, "\r\n")

# 3. 디버깅 활성화 (초기화 과정을 보기 위해 iocInit 전 배치)
asynSetTraceIOMask("L0", 0, 0x2)
asynSetTraceMask("L0", 0, 0x1) # Error(0x1) only to avoid noise

# 4. Controller 생성
# MovingPoll을 0.1s로 설정했으므로 통신 부하가 발생할 수 있습니다. 
# 통신이 불안정하면 0.2~0.5 정도로 조절하십시오.
KohzuAriesCreateController("PC0", "L0", 2, 0.2, 1.0)

iocInit()
