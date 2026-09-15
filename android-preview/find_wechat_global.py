from rebuild_ui import run,snapshot
import time
run('shell','input','tap',1060,2010);time.sleep(.4)
for _ in range(7):run('shell','input','swipe',650,2530,650,2080,180)
time.sleep(.4)
snapshot()
