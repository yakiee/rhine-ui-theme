from rebuild_ui import run
from rebuild_clipboard import ClipboardControl
from pathlib import Path
import json,time,zipfile
run('shell','input','tap',1146,2380);run('shell','input','tap',1146,2500);time.sleep(.2);run('shell','input','tap',864,216);time.sleep(.2)
with ClipboardControl() as c:s=c.get()
n=json.loads(s.replace('##KUSTOMCLIP##',''))['clip_modules'];assert len(n)==2
Path('rhine_exact/output/dock-opacity-20260914/live-top-panels.clip.txt').write_text(s,encoding='utf8')
with zipfile.ZipFile('rhine_exact/output/hyperos-klwp-v0.13.51/Rhine-UI-HyperOS-v0.13.51.klwp') as z:src=json.loads(z.read('preset.json'))['preset_root']['viewgroup_items']
for v in n:
 print('LIVE',v.get('internal_title'))
 print('CONFIG',{k:x for k,x in v.items() if k.startswith('config_')})
 for a in v.get('internal_animations',[])[:2]: print('ANIMATION',json.dumps(a,ensure_ascii=False))
 orig=next(x for x in src if x.get('internal_title')==v.get('internal_title'))
 print('anim equal',orig.get('internal_animations')==v.get('internal_animations'))
