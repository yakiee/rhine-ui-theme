import json,time,re
from pathlib import Path
from toolbar_native import tree,click,run,ClipboardControl
out=Path('rhine_exact/output/opacity-repair-20260915');out.mkdir(exist_ok=True)
root=tree()
for n in list(root.iter('node')):
    if n.get('resource-id','').endswith('/checkbox') and n.get('checked')=='true':click(n)
root=tree()
target=next(n for n in root.iter('node') if n.get('text')=='主菜单 · 设备状态')
y=int(re.findall(r'\d+',target.get('bounds'))[1])
click(next(n for n in root.iter('node') if n.get('resource-id','').endswith('/checkbox') and int(re.findall(r'\d+',n.get('bounds'))[1])==y))
click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_copy')))
with ClipboardControl() as c:clip=c.get()
data=json.loads(clip.replace('##KUSTOMCLIP##',''))
(out/'status-live-before.clip.txt').write_text(clip,encoding='utf-8')
module=data['clip_modules'][0]
assert module['internal_title']=='主菜单 · 设备状态'
print(json.dumps({k:v for k,v in module.items() if k!='viewgroup_items'},ensure_ascii=True,indent=2))
print('CHILDREN',json.dumps([{k:v for k,v in n.items() if k in ['internal_title','config_opacity','paint_color','internal_animations','internal_formulas']} for n in module['viewgroup_items']],ensure_ascii=True))
run('shell','input','keyevent',4)
