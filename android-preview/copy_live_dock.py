from rebuild_ui import run,snapshot
from rebuild_clipboard import ClipboardControl
from pathlib import Path
import time,json
run('shell','input','tap',864,216);time.sleep(.5)
with ClipboardControl() as c: clip=c.get()
out=Path('rhine_exact/output/dock-phone-fix-20260914');out.mkdir(exist_ok=True)
(out/'dock-before.clip.txt').write_text(clip,encoding='utf8')
p=json.loads(clip.replace('##KUSTOMCLIP##',''))
print('keys',p.keys())
n=p['clip_modules'][0]
print('Dock conditions:',json.dumps({k:v for k,v in n.items() if k not in ['viewgroup_items']},ensure_ascii=False))
for c in n.get('viewgroup_items',[]):
 if 'config_visible' in c.get('internal_formulas',{}):print('CHILD',c.get('internal_title'),c['internal_formulas']['config_visible'])
run('shell','input','tap',1060,2010)
time.sleep(.5)
snapshot()
