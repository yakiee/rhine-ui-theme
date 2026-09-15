from rebuild_ui import run
from pathlib import Path
import time
out=Path('rhine_exact/output/dock-phone-fix-20260914/second-page-only')
run('shell','input','tap',696,216);time.sleep(1);run('shell','input','keyevent',3);time.sleep(1.2)
(out/'final-page2.png').write_bytes(run('exec-out','screencap','-p'))
run('shell','input','tap',1006,1967);time.sleep(1.5)
(out/'final-terminal.png').write_bytes(run('exec-out','screencap','-p'))
print('Saved clean theme and captured terminal opening',flush=True)
