from rebuild_ui import run,snapshot
from rebuild_clipboard import ClipboardControl
run('shell','input','keycombination',113,29)
with ClipboardControl() as c:c.set('$si(screen)$',paste=True)
run('shell','input','keyevent',4)
snapshot()
