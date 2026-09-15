from rebuild_ui import run
from pathlib import Path
import time
out=Path('rhine_exact/output/dock-opacity-20260914');out.mkdir(exist_ok=True)
(out/'before.png').write_bytes(run('exec-out','screencap','-p'))
run('shell','input','tap',190,280);time.sleep(2)
run('shell','input','tap',1020,1967);time.sleep(3)
(out/'reopened.png').write_bytes(run('exec-out','screencap','-p'))
print('Captured before and after reopening.')
