import sys,time,re,xml.etree.ElementTree as ET,json
from rebuild_ui import run
from zhuang_ui import dump
target=sys.argv[1]
for attempt in range(12):
    run('shell','uiautomator','dump','/sdcard/rhine-zhuang-ui.xml')
    root=ET.fromstring(run('shell','cat','/sdcard/rhine-zhuang-ui.xml'))
    assert any(n.get('text')=='根目录' for n in root.iter('node'))
    nodes=[n for n in root.iter('node') if n.get('resource-id','').endswith(':id/title')]
    print('Visible',','.join(n.get('text','') for n in nodes),flush=True)
    match=next((n for n in nodes if n.get('text')==target),None)
    if match is not None:
        b=list(map(int,re.findall(r'\d+',match.get('bounds'))))
        run('shell','input','tap',650,(b[1]+b[3])//2)
        time.sleep(.7);dump();break
    run('shell','input','swipe',650,2490,650,2100,450)
    time.sleep(.7)
