import json,copy,time
from pathlib import Path

helper=Path('android-preview/toolbar_native.py')
s=helper.read_text(encoding='utf-8')
s=s.replace("    order={n['internal_title']:i for i,n in enumerate(SOURCE)}", "    layout=[i for i in range(len(SOURCE)) if not (OUT/f'root-{i}-applied.json').exists()]\n    layout += [i for i in (51,3) if (OUT/f'root-{i}-applied.json').exists()]\n    order={SOURCE[i]['internal_title']:p for p,i in enumerate(layout)}\n    target_position=order[title]")
s=s.replace('distance=index-min(positions)','distance=target_position-min(positions)')
helper.write_text(s,encoding='utf-8',newline='\n')
from toolbar_native import OUT,tree,click,find_root,run

p=OUT/'root-3-after.clip.txt'
data=json.loads(p.read_text(encoding='utf-8').replace('##KUSTOMCLIP##',''))
module=data['clip_modules'][0]
animation=copy.deepcopy(module['internal_animations'][0])
animation['formula']='$gv(page)=0 & si(screen)=gv(homepg)$'
module['internal_animations']=[animation]
(OUT/'root-3-final.clip.txt').write_text('##KUSTOMCLIP##\n'+json.dumps(data,ensure_ascii=False)+'\n##KUSTOMCLIP##',encoding='utf-8')
clip='##KUSTOMCLIP##\n'+json.dumps({'clip_version':1,'KUSTOM_ANIMATION':{'0':animation}})+'\n##KUSTOMCLIP##'
(OUT/'sidebar-stable-animation.clip.txt').write_text(clip,encoding='utf-8')
root,node=find_root(3)
click(node)
root=tree()
print(json.dumps([(n.get('text'),n.get('content-desc'),n.get('bounds'),n.get('resource-id')) for n in root.iter('node') if n.get('text') or n.get('content-desc')],ensure_ascii=True))
