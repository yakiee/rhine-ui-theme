"""Append one reversible native scroll animation to selected live root groups."""
from pathlib import Path
import sys
import json
import re
import time
import zipfile
import xml.etree.ElementTree as ET
from rebuild_ui import run

out = Path('rhine_exact/output/animation-performance-20260915')
out.mkdir(parents=True, exist_ok=True)
state_path = out / 'scroll-patches.json'
state = json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {}
with zipfile.ZipFile('rhine_exact/output/hyperos-klwp-v0.13.51/Rhine-UI-HyperOS-v0.13.51.klwp') as archive:
    source = json.loads(archive.read('preset.json'))['preset_root']['viewgroup_items']

def tree():
    run('shell', 'uiautomator', 'dump', '/sdcard/rhine-animation-editor.xml')
    raw = run('shell', 'cat', '/sdcard/rhine-animation-editor.xml')
    return ET.fromstring(raw), raw

def click(node):
    x1,y1,x2,y2 = map(int,re.findall(r'\d+',node.get('bounds')))
    run('shell','input','tap',(x1+x2)//2,(y1+y2)//2)
    time.sleep(1.2)

def open_root():
    root,raw = tree()
    current = next(n.get('text') for n in root.iter('node') if n.get('resource-id','').endswith(':id/text'))
    if current != '根目录':
        run('shell','input','keyevent','KEYCODE_BACK')
        time.sleep(1.0)
    root,raw = tree()
    assert any(n.get('text')=='根目录' for n in root.iter('node'))
    return root

def find_module(title):
    root = open_root()
    ordering = {node['internal_title']: index for index,node in enumerate(source)}
    target_index = ordering[title]
    for attempt in range(40):
        nodes = [n for n in root.iter('node') if n.get('resource-id','').endswith(':id/module_title')]
        match = next((n for n in nodes if n.get('text')==title and int(re.findall(r'\d+',n.get('bounds'))[3])-int(re.findall(r'\d+',n.get('bounds'))[1])>30),None)
        if match is not None:
            click(match)
            return
        visible_indices = [ordering[n.get('text')] for n in nodes if n.get('text') in ordering]
        assert visible_indices, 'No known root modules in current list'
        first = min(visible_indices)
        distance = target_index-first
        step = 300 if abs(distance)>6 else 115
        if distance<0:
            run('shell','input','swipe','650','2190','650',str(2190+step),'850')
        else:
            run('shell','input','swipe','650','2470','650',str(2470-step),'850')
        time.sleep(1)
        root,raw = tree()
    raise RuntimeError('Target root group not found: '+title)

for index in map(int,sys.argv[1:]):
    title = source[index]['internal_title']
    if title in state:
        print('Already patched:',index,flush=True)
        continue
    find_module(title)
    run('shell','input','tap','755','2010')
    time.sleep(.4)
    root,raw = tree()
    assert any(n.get('resource-id','').endswith(':id/text') and n.get('text')==title for n in root.iter('node'))
    (out / f'root-{index}-animation-before.xml').write_bytes(raw)
    keyframes = []
    for position, opacity in ((0,0),(12,20),(30,75),(45,100),(100,100)):
        keyframes.append({'position':position,'property':'OPACITY','value':opacity,'ease':'STRAIGHT'})
    animation = {'type':'SCROLL','action':'ADVANCED','rule':'CENTER','center':'SCREEN2','speed':100,'amount':100,'anchor':'MODULE_CENTER','ease':'STRAIGHT','animator':keyframes,'internal_toggles':{'center':10},'internal_formulas':{'center':'$"SCREEN"+gv(homepg)$'}}
    payload='##KUSTOMCLIP##\n'+json.dumps({'clip_version':1,'KUSTOM_ANIMATION':{'0':animation}})+'\n##KUSTOMCLIP##'
    clip_path = out / f'root-{index}-follow-scroll.clip.txt'
    clip_path.write_text(payload,encoding='utf-8')
    run('push',clip_path.resolve(),'/data/local/tmp/rhine-editor-input.txt')
    run('shell','CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard KUSTOM_ANIMATION /data/local/tmp/rhine-editor-input.txt')
    time.sleep(.3)
    root,raw = tree()
    paste = next(n for n in root.iter('node') if n.get('resource-id','').endswith(':id/action_paste'))
    click(paste)
    root,raw = tree()
    (out / f'root-{index}-animation-after.xml').write_bytes(raw)
    state[title]={'source_index':index,'action':'appended one SCROLL animation; original animations untouched','clip':str(clip_path)}
    state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Patched root',index,flush=True)
print('Batch finished; pending save and phone verification',flush=True)
