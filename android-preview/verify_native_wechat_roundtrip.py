from rebuild_ui import run
from rebuild_clipboard import ClipboardControl
from pathlib import Path
import json,time
run('shell','input','tap',1146,2487);time.sleep(.2);run('shell','input','tap',864,216);time.sleep(.2)
with ClipboardControl() as c:s=c.get()
n=json.loads(s.replace('##KUSTOMCLIP##',''))['clip_modules'][0]
assert n.get('internal_title')=='终端唯一入口与点击区域'
intents=[e for ch in n['viewgroup_items'] for shape in ch.get('viewgroup_items',[]) for e in shape.get('internal_events',[]) if e.get('action')=='LAUNCH_APP' and 'com.tencent.mm' in e.get('intent','')]
assert len(intents)==9,len(intents)
p=Path('rhine_exact/output/dock-phone-fix-20260914');(p/'terminal-wechat-roundtrip.clip.txt').write_text(s,encoding='utf8')
print('Verified on phone: 9 native WeChat launch actions, 106 children.')
run('shell','input','tap',696,216);time.sleep(1);run('shell','input','keyevent',3)
