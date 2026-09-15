from rebuild_ui import run,snapshot
import time,json
from pathlib import Path
run('shell','input','keyevent',4);time.sleep(.3)
run('shell','input','swipe',1100,2010,200,2010,350);time.sleep(.5)
snapshot()
print('FLOW SOURCE',json.dumps(json.loads(Path('rhine_exact/output/free-editor-rebuild/rebuild-plan.json').read_text(encoding='utf8'))['flows'],ensure_ascii=False))
