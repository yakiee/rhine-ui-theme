from pathlib import Path
import time
from rebuild_ui import run

out = Path('rhine_exact/output/dock-opacity-controls-20260914')
(out / 'final-opened.png').write_bytes(run('exec-out', 'screencap', '-p'))
for index in range(3):
    start, end = (1040, 160) if index % 2 == 0 else (160, 1040)
    run('shell', 'input', 'swipe', start, 1160, end, 1160, 250)
    time.sleep(.35)
    run('shell', 'input', 'swipe', end, 1160, start, 1160, 250)
    time.sleep(1)
    (out / f'final-{index + 1}-returned.png').write_bytes(run('exec-out', 'screencap', '-p'))
    run('shell', 'input', 'tap', 1020, 1967)
    time.sleep(1)
    (out / f'final-{index + 1}-opened.png').write_bytes(run('exec-out', 'screencap', '-p'))
    print(f'Captured cycle {index + 1}', flush=True)
