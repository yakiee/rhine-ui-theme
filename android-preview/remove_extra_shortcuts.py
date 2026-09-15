from rebuild_ui import run,snapshot
from rebuild_clipboard import ClipboardControl
import struct,time

def touch(c,a,x,y):c.sock.sendall(struct.pack('>BBqiiHHHII',2,a,-1,x,y,1200,2608,0 if a==1 else 65535,0,0))
def drag(c,x,y,tx,ty):
 touch(c,0,x,y);time.sleep(.8)
 for s in range(1,21):
  touch(c,2,round(x+(tx-x)*s/20),round(y+(ty-y)*s/20));time.sleep(.04)
 time.sleep(.4);touch(c,1,tx,ty);time.sleep(.8)
with ClipboardControl() as c:
 drag(c,165,1310,410,325)
 drag(c,456,2240,410,325)
snapshot()
