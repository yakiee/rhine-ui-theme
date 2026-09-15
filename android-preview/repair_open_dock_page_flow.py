import contextlib,io,json,time
from pathlib import Path
from toolbar_native import tree,click,run,ClipboardControl
OUT=Path('rhine_exact/output/open-dock-swipe-20260915')
raw=run('shell','dumpsys','activity','activities').decode(errors='replace')
assert any('topResumedActivity' in s and 'org.kustom.wallpaper.huawei/' in s for s in raw.splitlines())
run('shell','input','keyevent',3)
with contextlib.redirect_stdout(io.StringIO()):exec(Path('android-preview/open_current_editor.py').read_text(encoding='utf-8'))
run('shell','input','swipe',1100,2010,200,2010,350)
click(next(n for n in tree().iter('node') if n.get('text')=='流程'))
r=tree();checks=[n for n in r.iter('node') if n.get('resource-id','').endswith('/checkbox')]
assert len(checks)==2
click(checks[1]);click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_copy')))
with ClipboardControl() as c:before=c.get()
payload=json.loads(before.replace('##KUSTOMCLIP##',''));flow=list(payload['KUSTOM_FLOW'].values())[0]
assert flow['t'][0]['params']['formula']=='$si(screen)$'
(OUT/'page-flow-before.clip.txt').write_text(before,encoding='utf-8')
flow['t'][0]['params']['formula']='$if(gv(view)>0,si(screen)+":"+df(ss),"idle")$'
path=OUT/'page-flow-after.clip.txt';path.write_text('##KUSTOMCLIP##\n'+json.dumps(payload,ensure_ascii=False)+'\n##KUSTOMCLIP##',encoding='utf-8')
r=tree();delete=next((n for n in r.iter('node') if n.get('resource-id','').endswith('/action_delete')),None)
if delete is None:
    click([n for n in r.iter('node') if n.get('resource-id','').endswith('/checkbox')][1]);r=tree();delete=next(n for n in r.iter('node') if n.get('resource-id','').endswith('/action_delete'))
click(delete)
r=tree();confirm=next((n for n in r.iter('node') if n.get('resource-id')=='android:id/button1'),None)
if confirm is not None:click(confirm)
run('push',path.resolve(),'/data/local/tmp/rhine-editor-input.txt')
run('shell','CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard KUSTOM_FLOW /data/local/tmp/rhine-editor-input.txt')
click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_paste')))
click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_save')))
run('shell','input','keyevent',3);run('shell','am','force-stop','org.kustom.wallpaper.huawei')
run('shell','am','start','-W','-a','android.service.wallpaper.CHANGE_LIVE_WALLPAPER','--ecn','android.service.wallpaper.extra.LIVE_WALLPAPER_COMPONENT','org.kustom.wallpaper.huawei/org.kustom.wallpaper.WpGLService')
print('Saved page flow with active-Dock time dependency; fresh home preview ready')
