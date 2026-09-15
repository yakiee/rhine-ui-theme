from rebuild_ui import run,snapshot
from pathlib import Path
import sys,time
clip=Path(sys.argv[1]).resolve();label=sys.argv[2] if len(sys.argv)>2 else 'KUSTOM_MODULES'
run('push',clip,'/data/local/tmp/rhine-editor-input.txt')
print(run('shell',f'CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard {label} /data/local/tmp/rhine-editor-input.txt').decode())
time.sleep(.5)
run('shell','input','tap',1128,216)
time.sleep(1)
try:snapshot()
except RuntimeError:print('UI tree temporarily unavailable; inspect screen before continuing.')
