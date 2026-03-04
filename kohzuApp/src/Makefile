TOP=../..

include $(TOP)/configure/CONFIG

LIBRARY_IOC = KohzuAries

DBD += KohzuAries.dbd

KohzuAries_DBD += base.dbd
KohzuAries_DBD += asyn.dbd
KohzuAries_DBD += motorSupport.dbd
KohzuAries_DBD += KohzuAriesDriver.dbd

# Source files
KohzuAries_SRCS += KohzuAriesDriver.cpp

KohzuAries_LIBS += motor asyn
KohzuAries_LIBS += $(EPICS_BASE_IOC_LIBS)

include $(TOP)/configure/RULES
