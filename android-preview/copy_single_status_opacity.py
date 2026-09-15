from rebuild_ui import run
from rebuild_clipboard import ClipboardControl
from pathlib import Path
import time,json
run('shell','input','swipe',650,2470,650,2230,600);time.sleep(.3)
run('shell','input','tap',1146,2380);time.sleep(.3);run('shell','input','tap',864,216);time.sleep(.3)
with ClipboardControl() as c:s=c.get()
n=json.loads(s.replace('##KUSTOMCLIP##',''))['clip_modules'];assert len(n)==1 and n[0].get('internal_title')=='主菜单 · 设备状态',[v.get('internal_title') for v in n]
Path('rhine_exact/output/dock-opacity-20260914/live-status.clip.txt').write_text(s,encoding='utf8')
v=n[0];print('CONFIG',{k:x for k,x in v.items() if k.startswith('config_')});print('ANIM',json.dumps(v.get('internal_animations'),ensure_ascii=False))
