from rebuild_clipboard import ClipboardControl
from rebuild_ui import run
import struct,time
with ClipboardControl() as c:
 for x,y in [(972,1852),(840,216)]:
  for a in [0,1]:
   c.sock.sendall(struct.pack('>BBqiiHHHII',2,a,0,x,y,1200,2608,0 if a else 65535,0,0));time.sleep(.12)
  time.sleep(1)
run('shell','input','keyevent',3)
time.sleep(.7)
