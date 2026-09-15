from rebuild_ui import run,snapshot
from rebuild_clipboard import ClipboardControl
import time
run('shell','input','tap',500,680)
run('shell','input','keycombination',113,29)
with ClipboardControl() as c:c.set('SCREEN=$si(screen)$ HOME=$gv(homepg)$ VIEW=$gv(view)$ ORIGIN=$gv(origin)$',paste=True)
time.sleep(.7)
root=snapshot()
