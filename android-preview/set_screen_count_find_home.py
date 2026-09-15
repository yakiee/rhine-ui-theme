from rebuild_ui import run,snapshot
import time
run('shell','input','tap',408,1290);time.sleep(.3)
run('shell','input','tap',972,1852);time.sleep(.5)
run('shell','input','tap',1060,2010);time.sleep(.5)
for _ in range(55):run('shell','input','swipe',650,2530,650,2080,80)
for _ in range(2):run('shell','input','swipe',650,2100,650,2490,450)
snapshot()
