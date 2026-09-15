import json, re, time, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
from rebuild_ui import run
from rebuild_clipboard import ClipboardControl

OUT = Path('rhine_exact/output/toolbar-five-apps-20260915')
OUT.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile('rhine_exact/output/hyperos-klwp-v0.13.51/Rhine-UI-HyperOS-v0.13.51.klwp') as z:
    SOURCE = json.loads(z.read('preset.json'))['preset_root']['viewgroup_items']

def guard():
    raw = run('shell','dumpsys','activity','activities').decode(errors='replace')
    assert any('topResumedActivity=' in line and 'org.kustom.wallpaper.huawei/' in line for line in raw.splitlines()), 'Phone left KLWP; stopping'

def tree():
    guard()
    run('shell','uiautomator','dump','/sdcard/rhine-toolbar-ui.xml')
    raw=run('shell','cat','/sdcard/rhine-toolbar-ui.xml')
    (OUT/'current-ui.xml').write_bytes(raw)
    return ET.fromstring(raw)

def click(node):
    guard()
    x1,y1,x2,y2=map(int,re.findall(r'\d+',node.get('bounds')))
    run('shell','input','tap',(x1+x2)//2,(y1+y2)//2)
    time.sleep(.45)

def find_root(index):
    title=SOURCE[index]['internal_title']
    layout=[i for i in range(len(SOURCE)) if not (OUT/f'root-{i}-applied.json').exists()]
    layout += [i for i in (51,3) if (OUT/f'root-{i}-applied.json').exists()]
    order={SOURCE[i]['internal_title']:p for p,i in enumerate(layout)}
    target_position=order[title]
    for _ in range(50):
        root=tree()
        assert any(n.get('text')=='根目录' for n in root.iter('node'))
        nodes=[n for n in root.iter('node') if n.get('resource-id','').endswith('/module_title')]
        for node in nodes:
            xy=list(map(int,re.findall(r'\d+',node.get('bounds'))))
            if node.get('text')==title and xy[3]-xy[1]>35 and xy[3]<2490:
                return root,node
        positions=[order[n.get('text')] for n in nodes if n.get('text') in order]
        assert positions
        distance=target_position-min(positions)
        delta=320 if abs(distance)>5 else 119
        guard()
        if distance<0:run('shell','input','swipe',650,2170,650,2170+delta,650)
        else:run('shell','input','swipe',650,2480,650,2480-delta,650)
        time.sleep(.35)
    raise RuntimeError('root target not found')

def select_root(index):
    root,title=find_root(index)
    y=int(re.findall(r'\d+',title.get('bounds'))[1])
    checks=[n for n in root.iter('node') if n.get('resource-id','').endswith('/checkbox') and int(re.findall(r'\d+',n.get('bounds'))[1])==y]
    assert len(checks)==1
    click(checks[0])

def copy_root(index):
    select_root(index)
    root=tree()
    print(json.dumps([(n.get('content-desc'),n.get('resource-id')) for n in root.iter('node') if 'action_' in n.get('resource-id','')]),flush=True)
    copy=next(n for n in root.iter('node') if n.get('resource-id','').endswith('/action_copy'))
    click(copy)
    with ClipboardControl() as c:clip=c.get()
    payload=json.loads(clip.replace('##KUSTOMCLIP##',''))
    assert payload['clip_modules'][0]['internal_title']==SOURCE[index]['internal_title']
    (OUT/f'root-{index}-before.clip.txt').write_text(clip,encoding='utf-8')
    root=tree()
    if any(n.get('resource-id','').endswith('/action_copy') for n in root.iter('node')):
        run('shell','input','keyevent','KEYCODE_BACK');time.sleep(.3)
    print('BACKED UP',index,flush=True)

if __name__=='__main__':
    import sys
    for index in map(int,sys.argv[1:]):copy_root(index)
