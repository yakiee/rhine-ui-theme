from rebuild_ui import run
from rebuild_clipboard import ClipboardControl
from pathlib import Path
run('shell','input','tap',840,216)
with ClipboardControl() as c:
 text=c.get();print(text);Path('rhine_exact/output/free-editor-rebuild/flow-format.txt').write_text(text,encoding='utf8')
