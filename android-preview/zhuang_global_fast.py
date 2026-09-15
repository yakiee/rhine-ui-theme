import json,re,time,xml.etree.ElementTree as ET
from pathlib import Path
from rebuild_ui import run
from zhuang_ui import dump
p=json.loads(Path('rhine_exact/output/free-editor-rebuild/phone-clips/globals.clip.txt').read_text(encoding='utf8').replace('##KUSTOMCLIP##',''))['KUSTOM_GLOBAL']
for attempt in range(12):
    run('shell','uiautomator','dump','/sdcard/rhine-zhuang-ui.xml')
    root=ET.fromstring(run('shell','cat','/sdcard/rhine-zhuang-ui.xml'))
    assert any(n.get('text')=='根目录' for n in root.iter('node'))
    nodes=[n for n in root.iter('node') if n.get('resource-id','').endswith(':id/title')]
    print('Visible',','.join(n.get('text','') for n in nodes),flush=True)
    match=next((n for n in nodes if n.get('text')=='termcover'),None)
    if match is not None:
        b=list(map(int,re.findall(r'\d+',match.get('bounds'))));run('shell','input','tap',650,(b[1]+b[3])//2);time.sleep(.7);dump();break
    indexes=[p[n.get('text')]['index'] for n in nodes if n.get('text') in p]
    assert indexes
    distance=220-min(indexes)
    if distance>18:run('shell','input','swipe',650,2490,650,2090,80)
    elif distance>=0:run('shell','input','swipe',650,2490,650,2100,450)
    else:run('shell','input','swipe',650,2140,650,2470,650)
    time.sleep(1.2)
