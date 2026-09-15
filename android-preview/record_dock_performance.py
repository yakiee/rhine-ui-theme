from pathlib import Path
import sys
import time
import subprocess
from rebuild_ui import run, ADB, SERIAL

def require_launcher():
    activity = run('shell','dumpsys','activity','activities').decode(errors='replace')
    if not any('topResumedActivity' in line and 'com.miui.home/.launcher.Launcher' in line for line in activity.splitlines()):
        raise RuntimeError('Foreground changed; stopped before next touch')

label = sys.argv[1]
out = Path('rhine_exact/output/animation-performance-20260915')
out.mkdir(parents=True, exist_ok=True)
foreground = run('shell', 'dumpsys', 'activity', 'activities').decode(errors='replace')
if not any('topResumedActivity' in line and 'com.miui.home/.launcher.Launcher' in line for line in foreground.splitlines()):
    raise RuntimeError('Phone must remain on theme page 2 before the controlled gesture test')
remote = '/sdcard/Download/rhine-performance-' + label + '.mp4'
record = subprocess.Popen([ADB, '-s', SERIAL, 'shell', 'screenrecord', '--size', '720x1564', '--bit-rate', '5000000', '--time-limit', '9', remote], stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
time.sleep(.8)
require_launcher()
run('shell', 'input', 'tap', '1020', '1967')
time.sleep(1.1)
require_launcher()
run('shell', 'input', 'swipe', '1040', '1150', '160', '1150', '900')
time.sleep(.55)
require_launcher()
run('shell', 'input', 'swipe', '160', '1150', '1040', '1150', '900')
time.sleep(.8)
require_launcher()
run('shell', 'input', 'tap', '1020', '1967')
time.sleep(.8)
require_launcher()
run('shell', 'input', 'tap', '140', '1100')
stdout, stderr = record.communicate(timeout=15)
if record.returncode:
    raise RuntimeError(stderr.decode(errors='replace'))
target = out / (label + '.mp4')
run('pull', remote, target.resolve())
print('Recorded', target, target.stat().st_size)
