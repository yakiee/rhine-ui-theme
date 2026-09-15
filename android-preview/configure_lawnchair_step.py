from rebuild_ui import run,snapshot
import time
run('shell','input','tap',1020,732)
run('shell','input','keyevent',3)
time.sleep(.6)
snapshot()
