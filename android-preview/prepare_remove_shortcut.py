from rebuild_ui import run
import time
run('shell','input','keyevent',3)
time.sleep(.5)
run('shell','input','touchscreen','motionevent','DOWN',165,1320)
time.sleep(.8)
run('shell','input','touchscreen','motionevent','MOVE',400,1100)
time.sleep(.5)
