from rebuild_ui import run,snapshot
import time
run('shell','input','keyevent',4)
time.sleep(.4)
run('shell','input','draganddrop',1030,2200,1185,1500,2500)
time.sleep(.8)
snapshot()
