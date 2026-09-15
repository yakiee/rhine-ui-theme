from rebuild_ui import run,snapshot
import time
run('shell','input','tap',84,216)
time.sleep(.4)
run('shell','input','keyevent',3)
time.sleep(.7)
run('shell','input','swipe',1020,1150,160,1150,600)
time.sleep(.7)
snapshot()
