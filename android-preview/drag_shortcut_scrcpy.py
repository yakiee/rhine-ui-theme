from rebuild_ui import run
from rebuild_clipboard import ClipboardControl
import struct,time
from pathlib import Path

def touch(control,action,x,y):
 control.sock.sendall(struct.pack('>BBqiiHHHII',2,action,-1,x,y,1200,2608,0 if action==1 else 65535,0,0))
run('shell','input','keyevent',4)
with ClipboardControl() as c:
 touch(c,0,165,1320);time.sleep(.8)
 for step in range(1,11):
  touch(c,2,165+int(235*step/10),1320-int(220*step/10));time.sleep(.05)
 time.sleep(.5)
 Path('android-preview/logs/launcher-drag.png').write_bytes(run('exec-out','screencap','-p'))
 touch(c,1,165,1320)
print('drag screenshot saved')
