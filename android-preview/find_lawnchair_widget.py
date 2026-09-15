from rebuild_ui import run,snapshot
from rebuild_clipboard import ClipboardControl
import time
run('shell','input','tap',500,550)
with ClipboardControl() as control:control.set('Lawnchair',paste=True)
time.sleep(.5)
snapshot()
