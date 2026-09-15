from rebuild_ui import run,snapshot
import time
for _ in range(2):
 run('shell','input','tap',408,1245);time.sleep(.4)
run('shell','input','tap',972,1805)
time.sleep(.4)
run('shell','input','tap',1060,1915)
time.sleep(.4)
snapshot()
