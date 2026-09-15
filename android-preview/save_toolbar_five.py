import json,time
from toolbar_native import OUT,tree,click,run

assert all((OUT/f'root-{i}-applied.json').exists() for i in (3,51))
root=tree()
click(next(n for n in root.iter('node') if n.get('resource-id','').endswith('/action_save')))
time.sleep(1.5)
for i in (3,51):
    p=OUT/f'root-{i}-applied.json'
    state=json.loads(p.read_text(encoding='utf-8'));state['saved']=True
    p.write_text(json.dumps(state),encoding='utf-8')
run('shell','input','keyevent','KEYCODE_HOME')
time.sleep(.8)
print('SAVED')
