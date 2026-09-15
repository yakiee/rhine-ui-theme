from rebuild_ui import run,snapshot
from pathlib import Path
import time
out=Path('rhine_exact/output/dock-phone-fix-20260914')
(out/'page4-after.png').write_bytes(run('exec-out','screencap','-p'))
for _ in range(2):
 run('shell','input','swipe',160,1160,1040,1160,550);time.sleep(.6)
snapshot()
(out/'page2-after.png').write_bytes(run('exec-out','screencap','-p'))
