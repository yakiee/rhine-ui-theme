from rebuild_ui import run,snapshot
import time
run('shell','input','swipe',200,2010,1080,2010,350);time.sleep(.5)
run('shell','input','tap',140,2010);time.sleep(.5)
for _ in range(18):run('shell','input','swipe',650,2080,650,2530,80)
for _ in range(6):run('shell','input','swipe',650,2490,650,2090,450)
snapshot()
