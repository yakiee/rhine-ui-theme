from pathlib import Path
import json
base=Path('rhine_exact/output/free-editor-rebuild');dest=base/'phone-clips';dest.mkdir(exist_ok=True)
for p in [base/'globals.clip.txt',*sorted((base/'clips').glob('*.txt'))]:
 text=p.read_text(encoding='utf8').replace('kfile://org.kustom.provider/','kfile://org.kustom.sdcard/')
 (dest/p.name).write_text(text,encoding='utf8')
print('Mapped only resource authority for 13 editor batches.')
from rebuild_ui import run,snapshot
run('shell','input','tap',1146,2492)
snapshot()
