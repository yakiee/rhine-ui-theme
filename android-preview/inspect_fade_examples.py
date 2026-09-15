import json
from pathlib import Path
root=json.loads(Path('rhine_exact/src/preset-revision-wip.json').read_text(encoding='utf-8'))
found=[]
def walk(node):
    if isinstance(node,dict):
        if node.get('action') in ('FADE_IN','FADE_OUT'):found.append(node)
        for child in node.values():walk(child)
    elif isinstance(node,list):
        for child in node:walk(child)
walk(root)
print(json.dumps(found[:3],ensure_ascii=True,indent=2))
