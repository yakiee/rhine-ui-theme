from rebuild_ui import run
import time
run('shell','input','tap',600,1100)
run('shell','input','touchscreen','motionevent','DOWN',165,2240)
time.sleep(.8)
run('shell','input','touchscreen','motionevent','MOVE',165,2000)
time.sleep(.3)
run('shell','input','touchscreen','motionevent','MOVE',10,1600)
time.sleep(2)
run('shell','input','touchscreen','motionevent','MOVE',170,1400)
time.sleep(.4)
run('shell','input','touchscreen','motionevent','UP',170,1400)
time.sleep(.6)
