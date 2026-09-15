from rebuild_clipboard import ClipboardControl
import struct,time
with ClipboardControl() as c:
 for a in [0,1]:
  c.sock.sendall(struct.pack('>BBqiiHHHII',2,a,0,1134,354,1200,2608,0 if a else 65535,0,0))
  time.sleep(1.4 if a==0 else .4)
print('Long press complete')
