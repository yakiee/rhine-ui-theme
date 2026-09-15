import contextlib,io,json,re,time
from pathlib import Path
from toolbar_native import tree,click,run,ClipboardControl
from opacity_navigation import navigate
OUT=Path('rhine_exact/output/open-dock-swipe-20260915')
# Reuse only the guarded root entry and deletion of the failed transparent watcher.
source=Path('android-preview/replace_swipe_diagnostic_with_watcher.py').read_text(encoding='utf-8').split("module={'internal_type'")[0]
source=source.replace('SWIPE DIAGNOSTIC REMOVE','桌面页码同步 · 无可视内容')
exec(compile(source,'remove-transparent-watcher','exec'))
r,target=navigate(0);click(target)
r=tree();checks=[n for n in r.iter('node') if n.get('resource-id','').endswith('/checkbox')]
assert len(checks)==1,'Expected one background bitmap child'
click(checks[0]);click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_copy')))
with ClipboardControl() as c:before=c.get()
payload=json.loads(before.replace('##KUSTOMCLIP##',''))
assert len(payload['clip_modules'])==1 and payload['clip_modules'][0]['internal_type'] in ['BitmapModule','ImageModule']
(OUT/'background-child-before.clip.txt').write_text(before,encoding='utf-8')
watcher={'internal_type':'TextModule','internal_title':'页码刷新 · 被壁纸覆盖','text_expression':'$si(screen)$:$gv(view)$:$df(ss)$','text_size':20,'paint_color':'#FF101010','position_anchor':'CENTER','internal_events':[]}
payload['clip_modules'].insert(0,watcher)
path=OUT/'background-children-after.clip.txt';path.write_text('##KUSTOMCLIP##\n'+json.dumps(payload,ensure_ascii=False)+'\n##KUSTOMCLIP##',encoding='utf-8')
r=tree();delete=next((n for n in r.iter('node') if n.get('resource-id','').endswith('/action_delete')),None)
if delete is None:
    click(next(n for n in r.iter('node') if n.get('resource-id','').endswith('/checkbox')));delete=next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_delete'))
click(delete)
r=tree();confirm=next((n for n in r.iter('node') if n.get('resource-id')=='android:id/button1'),None)
if confirm is not None:click(confirm)
run('push',path.resolve(),'/data/local/tmp/rhine-editor-input.txt')
run('shell','CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard KUSTOM_MODULES /data/local/tmp/rhine-editor-input.txt')
click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_paste')))
click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_save')))
run('shell','input','keyevent',3);run('shell','am','force-stop','org.kustom.wallpaper.huawei')
run('shell','am','start','-W','-a','android.service.wallpaper.CHANGE_LIVE_WALLPAPER','--ecn','android.service.wallpaper.extra.LIVE_WALLPAPER_COMPONENT','org.kustom.wallpaper.huawei/org.kustom.wallpaper.WpGLService')
exec(compile(Path('android-preview/apply_saved_home_wallpaper.py').read_text(encoding='utf-8'),'apply-home','exec'))
source=Path('android-preview/stress_open_dock_swipe.py').read_text(encoding='utf-8').replace("OUT=Path('rhine_exact/output/open-dock-swipe-20260915')", "OUT=Path('rhine_exact/output/open-dock-swipe-20260915/occluded');OUT.mkdir(exist_ok=True)")
exec(compile(source,'stress-occluded','exec'))
