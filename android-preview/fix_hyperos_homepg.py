from rebuild_ui import run,snapshot
from rebuild_clipboard import ClipboardControl
import time
run('shell','input','tap',450,658)
run('shell','input','keycombination',113,29)
with ClipboardControl() as c:c.set('$si(screen)$',paste=True)
time.sleep(.5)
root=snapshot()
preview=next(n.get('text') for n in root.iter('node') if n.get('resource-id','').endswith('/preview'))
print('NATIVE PAGE 3, KLWP SCREEN=',preview)
assert preview=='1',preview
run('shell','input','tap',1128,216);time.sleep(.5)
snapshot()
