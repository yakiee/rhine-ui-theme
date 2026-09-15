from rebuild_ui import run
from rebuild_clipboard import ClipboardControl
from pathlib import Path
import time,json

run('shell','input','swipe',650,2470,650,2230,600)
time.sleep(.4)
run('shell','input','tap',1146,2500)
time.sleep(.4)
run('shell','input','tap',864,216)
time.sleep(.4)
with ClipboardControl() as clipboard:
    clip=clipboard.get()
modules=json.loads(clip.replace('##KUSTOMCLIP##',''))['clip_modules']
assert len(modules)==1 and modules[0]['internal_title']=='终端 · 设备及电池信息'
Path('rhine_exact/output/dock-page-lifecycle-20260914/live-first-row.clip.txt').write_text(clip,encoding='utf-8')
def walk(node,path='root'):
    fields={k:v for k,v in node.items() if (k.startswith('config_') or k in ['paint_color','internal_formulas'])}
    if fields: print(path,json.dumps(fields,ensure_ascii=True))
    for index,child in enumerate(node.get('viewgroup_items',[])):walk(child,path+'/'+str(index))
walk(modules[0])
