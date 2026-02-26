import epics
import time

def on_conn(pvname=None, conn=None, **kwargs):
    print(f"PV {pvname} connected: {conn}")

p1 = epics.PV("KOHZU:m1.RBV", connection_callback=on_conn, connection_timeout=0.01)
p2 = epics.PV("KOHZU:m2.RBV", connection_callback=on_conn, connection_timeout=0.01)

time.sleep(1)
