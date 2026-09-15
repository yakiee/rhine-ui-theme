from pathlib import Path
from rebuild_ui import run
import sys,time
raw=run('shell','dumpsys','activity','activities')
assert any(b'topResumedActivity' in s and b'com.miui.home/.launcher.Launcher' in s for s in raw.splitlines())
run('shell','input','tap',1010,1971);time.sleep(.6)
sys.argv=['check','right-unconditional']
source=Path('android-preview/check_open_dock_swipe.py').read_text(encoding='utf-8')
source=source.replace("1040,1150,160,1150", "TEMP").replace("160,1150,1040,1150","1040,1150,160,1150").replace('TEMP','160,1150,1040,1150')
source=source.replace("1100);time.sleep(1)", "1100);time.sleep(1);guard();(out/(label+'-away.png')).write_bytes(run('exec-out','screencap','-p'))",1)
exec(compile(source,__file__,'exec'))
