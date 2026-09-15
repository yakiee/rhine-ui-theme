import time,re,json,xml.etree.ElementTree as ET
from rebuild_ui import run
from zhuang_ui import dump
for _ in range(10):
    run('shell','uiautomator','dump','/sdcard/rhine-widget-list.xml')
    root=ET.fromstring(run('shell','cat','/sdcard/rhine-widget-list.xml'))
    assert any(n.get('text')=='添加小部件' for n in root.iter('node'))
    titles=[n for n in root.iter('node') if n.get('resource-id','').endswith(':id/widget_line_title')]
    print(json.dumps([n.get('text') for n in titles],ensure_ascii=True),flush=True)
    match=next((n for n in root.iter('node') if 'transparent' in n.get('text','').lower() or 'transparent' in n.get('content-desc','').lower()),None)
    if match is not None:
        dump();break
    run('shell','input','swipe',650,2420,650,700,500)
    time.sleep(.7)
