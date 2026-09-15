from rebuild_ui import run
from pathlib import Path
import time
out=Path('rhine_exact/output/dock-phone-fix-20260914')
(out/'terminal-open.png').write_bytes(run('exec-out','screencap','-p'))
run('shell','input','tap',190,280);time.sleep(1)
(out/'terminal-return.png').write_bytes(run('exec-out','screencap','-p'))
run('shell','am','start','-W','-a','android.settings.SETTINGS')
time.sleep(.8)
run('shell','input','keyevent',3);time.sleep(1)
(out/'return-from-app.png').write_bytes(run('exec-out','screencap','-p'))
print('Captured terminal open, return, and app return')
