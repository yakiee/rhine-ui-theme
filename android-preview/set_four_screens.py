from rebuild_ui import run,snapshot
import time
for _ in range(2):run('shell','input','tap',408,1620);time.sleep(.5)
snapshot()
run('shell','input','tap',972,1852)
time.sleep(.5)
