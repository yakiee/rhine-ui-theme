from rebuild_ui import run
from rebuild_clipboard import ClipboardControl
from pathlib import Path
run('shell','input','tap',720,216)
with ClipboardControl() as c:
 print(c.get())
