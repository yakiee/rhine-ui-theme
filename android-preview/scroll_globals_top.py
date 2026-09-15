from rebuild_ui import run,snapshot
import time
for _ in range(5):
 run('shell','input','swipe',650,2100,650,2520,40)
 time.sleep(.3)
snapshot()
