from rebuild_ui import run,snapshot
from pathlib import Path
import time
clip=Path('rhine_exact/output/free-editor-rebuild/globals.clip.txt').resolve()
run('push',clip,'/data/local/tmp/rhine-editor-input.txt')
print(run('shell','CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard KUSTOM_GLOBAL /data/local/tmp/rhine-editor-input.txt').decode())
run('shell','input','tap',1128,216)
time.sleep(1)
snapshot()
