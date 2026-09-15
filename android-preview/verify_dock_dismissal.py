from pathlib import Path
import json
import time
from rebuild_ui import run

out = Path('rhine_exact/output/dock-dismissal-20260914')

def shot(name):
    (out / (name + '.png')).write_bytes(run('exec-out', 'screencap', '-p'))

def tap(x, y):
    activity = next(line for line in run('shell', 'dumpsys', 'activity', 'activities').splitlines() if b'topResumedActivity' in line)
    assert b'com.miui.home/.launcher.Launcher' in activity, activity
    run('shell', 'input', 'tap', x, y)
    time.sleep(1)

shot('01-opened-no-header')
tap(80, 1100)
shot('02-outside-tap')
tap(1020, 1967)
shot('03-reopened')
tap(1070, 1520)
activity = next(line.decode(errors='replace') for line in run('shell', 'dumpsys', 'activity', 'activities').splitlines() if b'topResumedActivity' in line)
(out / 'wechat-check.json').write_text(json.dumps({'activity': activity, 'native_wechat': 'com.tencent.mm/.ui.LauncherUI' in activity}), encoding='utf-8')
print(activity, flush=True)
assert 'com.tencent.mm/.ui.LauncherUI' in activity
run('shell', 'input', 'keyevent', 3)
time.sleep(1)
shot('04-app-return')
tap(1020, 1967)
run('shell', 'input', 'swipe', 1040, 1160, 160, 1160, 600)
time.sleep(.7)
run('shell', 'input', 'swipe', 160, 1160, 1040, 1160, 600)
time.sleep(1)
shot('05-page-return')
print('Captured outside tap, native app return, and page return.', flush=True)
