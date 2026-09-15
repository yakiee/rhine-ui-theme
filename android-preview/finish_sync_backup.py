from rebuild_ui import run,snapshot
from rebuild_clipboard import ClipboardControl
import time
run('shell','input','tap',500,1450)
run('shell','input','keycombination',113,29)
with ClipboardControl() as control: control.set('Rhine Phone Sync 01351',paste=True)
time.sleep(.5)
snapshot()
