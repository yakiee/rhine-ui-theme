import contextlib,io,json,re,time
from pathlib import Path
from toolbar_native import tree,click,run,ClipboardControl
OUT=Path('rhine_exact/output/open-dock-swipe-20260915')
raw=run('shell','dumpsys','activity','activities').decode(errors='replace')
assert any('topResumedActivity' in s and ('com.miui.home/' in s or 'org.kustom.wallpaper.huawei/' in s) for s in raw.splitlines())
run('shell','input','keyevent',3)
with contextlib.redirect_stdout(io.StringIO()):exec(Path('android-preview/open_current_editor.py').read_text(encoding='utf-8'))
for attempt in range(12):
    r=tree();target=next((n for n in r.iter('node') if n.get('text')=='SWIPE DIAGNOSTIC REMOVE'),None)
    if target is not None:break
    for _ in range(5):run('shell','input','swipe',650,2515,650,2080,60)
else:raise RuntimeError('Diagnostic not found')
y=sum(int(x) for x in re.findall(r'\d+',target.get('bounds'))[1::2])/2
check=min([n for n in r.iter('node') if n.get('resource-id','').endswith('/checkbox')],key=lambda n:abs(sum(int(x) for x in re.findall(r'\d+',n.get('bounds'))[1::2])/2-y))
click(check);click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_delete')))
r=tree();confirm=next((n for n in r.iter('node') if n.get('resource-id')=='android:id/button1'),None)
if confirm is not None:click(confirm)
module={'internal_type':'TextModule','internal_title':'桌面页码同步 · 无可视内容','text_expression':'$si(screen)$:$gv(view)$:$df(ss)$','text_size':1,'paint_color':'#00FFFFFF','position_anchor':'TOP','position_offset_y':105,'internal_events':[]}
path=OUT/'page-watcher.clip.txt';path.write_text('##KUSTOMCLIP##\n'+json.dumps({'clip_version':1,'clip_modules':[module]},ensure_ascii=False)+'\n##KUSTOMCLIP##',encoding='utf-8')
run('push',path.resolve(),'/data/local/tmp/rhine-editor-input.txt')
run('shell','CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard KUSTOM_MODULES /data/local/tmp/rhine-editor-input.txt')
click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_paste')))
click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_save')))
run('shell','input','keyevent',3);run('shell','am','force-stop','org.kustom.wallpaper.huawei')
run('shell','am','start','-W','-a','android.service.wallpaper.CHANGE_LIVE_WALLPAPER','--ecn','android.service.wallpaper.extra.LIVE_WALLPAPER_COMPONENT','org.kustom.wallpaper.huawei/org.kustom.wallpaper.WpGLService')
exec(compile(Path('android-preview/apply_saved_home_wallpaper.py').read_text(encoding='utf-8'),'apply-home','exec'))
source=Path('android-preview/stress_open_dock_swipe.py').read_text(encoding='utf-8').replace("OUT=Path('rhine_exact/output/open-dock-swipe-20260915')", "OUT=Path('rhine_exact/output/open-dock-swipe-20260915/watcher');OUT.mkdir(exist_ok=True)")
exec(compile(source,'stress-watcher','exec'))
