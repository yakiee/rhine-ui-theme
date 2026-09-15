from rebuild_ui import run
from rebuild_clipboard import ClipboardControl
from pathlib import Path
import time,json
run('shell','input','tap',1146,2354);time.sleep(.2);run('shell','input','tap',864,216);time.sleep(.3)
with ClipboardControl() as c:s=c.get()
n=json.loads(s.replace('##KUSTOMCLIP##',''))['clip_modules'][0]
assert n.get('internal_title')=='终端唯一入口与点击区域',n.get('internal_title')
p=Path('rhine_exact/output/dock-phone-fix-20260914');(p/'terminal-touches-before.clip.txt').write_text(s,encoding='utf8')
count=0
for child in n['viewgroup_items']:
 for shape in child.get('viewgroup_items',[]):
  for ev in shape.get('internal_events',[]):
   if ev.get('action')=='OPEN_LINK' and ev.get('url')=='$gv(wechat)$':
    ev.clear();ev.update({'type':'SINGLE_TAP','action':'LAUNCH_APP','intent':'intent:#Intent;action=android.intent.action.MAIN;category=android.intent.category.LAUNCHER;component=com.tencent.mm/com.tencent.mm.ui.LauncherUI;launchFlags=0x10200000;end'});count+=1
assert count==9,count
clip='##KUSTOMCLIP##\n'+json.dumps({'clip_version':1,'clip_modules':n['viewgroup_items']},ensure_ascii=False)+'\n##KUSTOMCLIP##'
(p/'terminal-children-wechat-fixed.clip.txt').write_text(clip,encoding='utf8')
(p/'terminal-touches-fixed.json').write_text(json.dumps(n,ensure_ascii=False,indent=2),encoding='utf8')
print('Backed up live group:',len(n['viewgroup_items']),'children; changed',count,'WeChat events; clip bytes',len(clip.encode()))
