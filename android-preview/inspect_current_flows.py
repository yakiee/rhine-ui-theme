import contextlib,io,json,time
from pathlib import Path
from toolbar_native import run,tree,click
raw=run('shell','dumpsys','activity','activities').decode(errors='replace')
assert any('topResumedActivity' in s and ('com.miui.home/' in s or 'org.kustom.wallpaper.huawei/' in s) for s in raw.splitlines())
run('shell','input','keyevent',3)
with contextlib.redirect_stdout(io.StringIO()):exec(Path('android-preview/open_current_editor.py').read_text(encoding='utf-8'))
run('shell','input','swipe',1100,2010,200,2010,350);time.sleep(.4)
r=tree()
print(json.dumps([(n.get('text'),n.get('resource-id'),n.get('bounds'),n.get('content-desc')) for n in r.iter('node') if n.get('text') or n.get('content-desc')],ensure_ascii=True))
