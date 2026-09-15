from rebuild_ui import run
from rebuild_clipboard import ClipboardControl
import time
run('shell','input','tap',450,658)
run('shell','input','keycombination',113,29)
with ClipboardControl() as c:c.set('2',paste=True)
time.sleep(.6)
run('shell','input','tap',1128,216)
time.sleep(.8)
run('shell','input','tap',840,216)
time.sleep(2)
