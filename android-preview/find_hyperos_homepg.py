from rebuild_ui import run,snapshot
import time
run('shell','input','tap',1060,2010);time.sleep(.5)
for _ in range(55):run('shell','input','swipe',650,2530,650,2080,70)
for _ in range(2):run('shell','input','swipe',650,2080,650,2470,450)
snapshot()
