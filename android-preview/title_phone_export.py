from rebuild_ui import run
from rebuild_clipboard import ClipboardControl
run('shell','input','tap',500,1510)
with ClipboardControl() as control:control.set('Rhine Phone Sync 01351',paste=True)
