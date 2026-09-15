from rebuild_ui import run
from pathlib import Path
base=Path('rhine_exact/output/free-editor-rebuild/assets').resolve()
for folder in ['bitmaps','fonts']:
 print(run('push',str(base/folder),'/sdcard/Download/Rhine-KLWP/').decode(errors='replace'))
print(run('shell','ls','/sdcard/Download/Rhine-KLWP/bitmaps').decode(errors='replace'))
