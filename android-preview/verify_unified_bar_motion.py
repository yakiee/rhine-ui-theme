from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import time
from rebuild_ui import run

out = Path('rhine_exact/output/unified-bar-motion-20260914')
events = []

def assert_launcher():
    activity = next(line for line in run('shell', 'dumpsys', 'activity', 'activities').splitlines() if b'topResumedActivity' in line)
    assert b'com.miui.home/.launcher.Launcher' in activity, activity

def capture(name):
    (out / (name + '.png')).write_bytes(run('exec-out', 'screencap', '-p'))

def drag(name, start, end):
    assert_launcher()
    capture(name + '-start')
    began = time.monotonic()
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(run, 'shell', 'input', 'swipe', start, 1160, end, 1160, 1800)
        for index, target in enumerate((.3, .8, 1.3)):
            time.sleep(max(0, began + target - time.monotonic()))
            capture(name + f'-moving-{index}')
        future.result()
    time.sleep(.7)
    capture(name + '-end')
    events.append(name)
    print(name, 'captured', flush=True)

drag('closed-away', 1040, 160)
drag('closed-return', 160, 1040)
assert_launcher()
run('shell', 'input', 'tap', 1020, 1967)
time.sleep(1)
drag('opened-away', 1040, 160)
drag('opened-return', 160, 1040)
(out / 'capture-events.json').write_text(json.dumps(events), encoding='utf-8')
