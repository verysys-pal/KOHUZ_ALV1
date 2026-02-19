TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = KOHUZ_ALV1
# KOHUZ_ALV1.dbd will be created and installed
DBD += KOHUZ_ALV1.dbd

# KOHUZ_ALV1.dbd will be made up from these files:
KOHUZ_ALV1_DBD += base.dbd
KOHUZ_ALV1_DBD += asyn.dbd
KOHUZ_ALV1_DBD += motorSupport.dbd
KOHUZ_ALV1_DBD += drvAsynIPPort.dbd
KOHUZ_ALV1_DBD += KohzuAries.dbd

# Include dbd files from all support applications:
#KOHUZ_ALV1_DBD += xxx.dbd

# Add all the support libraries needed by this IOC
#KOHUZ_ALV1_LIBS += xxx

# KOHUZ_ALV1_registerRecordDeviceDriver.cpp derives from KOHUZ_ALV1.dbd
KOHUZ_ALV1_SRCS += KOHUZ_ALV1_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
KOHUZ_ALV1_SRCS_DEFAULT += KOHUZ_ALV1Main.cpp
KOHUZ_ALV1_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#KOHUZ_ALV1_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
KOHUZ_ALV1_LIBS += KohzuAries
KOHUZ_ALV1_LIBS += KohzuMotor
KOHUZ_ALV1_LIBS += motor
KOHUZ_ALV1_LIBS += asyn
KOHUZ_ALV1_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

