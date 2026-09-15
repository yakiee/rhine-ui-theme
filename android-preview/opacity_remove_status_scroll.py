import json,time
from pathlib import Path
from toolbar_native import tree,click,run
out=Path('rhine_exact/output/opacity-repair-20260915')
r=tree();click(next(n for n in r.iter('node') if n.get('text')=='主菜单 · 设备状态'))
run('shell','input','tap',755,2010)
r=tree()
print(json.dumps([(n.get('text'),n.get('bounds')) for n in r.iter('node') if n.get('text')],ensure_ascii=True),flush=True)
checks=[n for n in r.iter('node') if n.get('resource-id','').endswith('/checkbox')]
assert len(checks)==3
click(checks[-1]);click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_delete')))
click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_save')))
time.sleep(.6);run('shell','input','keyevent',3);time.sleep(.6)
raw=run('shell','dumpsys','activity','activities').decode(errors='replace')
assert any('topResumedActivity' in s and 'com.miui.home/' in s for s in raw.splitlines())
run('shell','input','tap',1010,1971);time.sleep(.8)
(out/'status-scroll-removed.png').write_bytes(run('exec-out','screencap','-p'))
print('Only the status row extra scroll-opacity animation removed for direct comparison')
