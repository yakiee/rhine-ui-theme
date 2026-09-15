import contextlib,io,json,re
from pathlib import Path
from toolbar_native import tree,click,run,ClipboardControl
raw=run('shell','dumpsys','activity','activities').decode(errors='replace')
assert any('topResumedActivity' in s and ('com.miui.home/' in s or 'org.kustom.wallpaper.huawei/' in s) for s in raw.splitlines())
run('shell','input','keyevent',3)
with contextlib.redirect_stdout(io.StringIO()):exec(Path('android-preview/open_current_editor.py').read_text(encoding='utf-8'))
run('shell','input','swipe',1100,2010,200,2010,350)
click(next(n for n in tree().iter('node') if n.get('text')=='全局变量'))
for attempt in range(18):
    r=tree();target=next((n for n in r.iter('node') if n.get('text')=='page'),None)
    if target is not None:break
    for _ in range(5):run('shell','input','swipe',650,2090,650,2520,60)
else:raise RuntimeError('page global not found')
y=sum(int(x) for x in re.findall(r'\d+',target.get('bounds'))[1::2])/2
check=min([n for n in r.iter('node') if n.get('resource-id','').endswith('/checkbox')],key=lambda n:abs(sum(int(x) for x in re.findall(r'\d+',n.get('bounds'))[1::2])/2-y))
click(check);click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_copy')))
with ClipboardControl() as c:s=c.get()
Path('rhine_exact/output/open-dock-swipe-20260915/live-page-global.clip.txt').write_text(s,encoding='utf-8');print(s)
