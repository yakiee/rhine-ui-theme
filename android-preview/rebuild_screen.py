from rebuild_ui import run
import base64
from pathlib import Path
print('ACTIVITY', '\n'.join(x for x in run('shell','dumpsys','activity','activities').decode(errors='replace').splitlines() if 'topResumedActivity' in x))
png=run('exec-out','screencap','-p');Path('android-preview/logs/rebuild-live.png').write_bytes(png)
print('IMAGE:'+base64.b64encode(png).decode())
