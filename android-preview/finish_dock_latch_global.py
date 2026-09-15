import json
from pathlib import Path
from toolbar_native import tree,click,ClipboardControl
with ClipboardControl() as c:c.set('$si(screen)!=gv(homepg) | gv(view)=0 | si(visible)=0$',paste=True)
click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/md_buttonDefaultPositive')))
print(json.dumps([(n.get('text'),n.get('resource-id'),n.get('bounds')) for n in tree().iter('node') if n.get('text') or n.get('resource-id','').endswith('/checkbox')],ensure_ascii=True))
