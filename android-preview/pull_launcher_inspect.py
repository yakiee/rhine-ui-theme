from pathlib import Path
from rebuild_ui import run
path=run('shell','pm','path','com.miui.home').decode().strip().split('package:')[-1]
out=Path('android-preview/apps/HyperOS-Launcher-inspect.apk')
print(run('pull',path,out).decode(errors='replace'))
