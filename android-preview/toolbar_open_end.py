import time,json
from toolbar_native import tree,guard,run,click,SOURCE

for attempt in range(12):
    root=tree()
    node=next((n for n in root.iter('node') if n.get('resource-id','').endswith('/module_title') and n.get('text')==SOURCE[3]['internal_title']),None)
    if node is not None:
        click(node);break
    assert any(n.get('text')=='根目录' for n in root.iter('node'))
    guard();run('shell','input','swipe',650,2490,650,2070,70);time.sleep(.9)
else:raise RuntimeError('Toolbar not found')
run('shell','input','tap',755,2010);time.sleep(.3)
print(json.dumps([(n.get('text'),n.get('bounds'),n.get('resource-id')) for n in tree().iter('node') if n.get('text')],ensure_ascii=True))
