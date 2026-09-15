import contextlib,io,json,time
from pathlib import Path
from toolbar_native import tree,click,run
from opacity_navigation import navigate
out=Path('rhine_exact/output/opacity-repair-20260915')
for index,expected in [(2,1),(4,2)]:
    run('shell','input','keyevent',3)
    with contextlib.redirect_stdout(io.StringIO()):
        exec(Path('android-preview/open_current_editor.py').read_text(encoding='utf-8'))
    r,n=navigate(index);click(n);run('shell','input','tap',755,2010)
    r=tree();checks=[n for n in r.iter('node') if n.get('resource-id','').endswith('/checkbox')]
    assert len(checks)==expected,(index,len(checks))
    path=Path(f'rhine_exact/output/animation-performance-20260915/root-{index}-follow-scroll.clip.txt')
    assert path.exists()
    run('push',path.resolve(),'/data/local/tmp/rhine-editor-input.txt')
    run('shell','CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard KUSTOM_ANIMATION /data/local/tmp/rhine-editor-input.txt')
    click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_paste')))
    r=tree();assert sum(n.get('resource-id','').endswith('/checkbox') for n in r.iter('node'))==expected+1
    click(next(n for n in r.iter('node') if n.get('resource-id','').endswith('/action_save')))
    print('RESTORED AND SAVED',index,flush=True)
(out/'comparison-restored.json').write_text(json.dumps({'restored':[2,4],'other_modules_changed':False}),encoding='utf-8')
run('shell','input','keyevent',3)
time.sleep(.6)
(out/'before-runtime-restart.png').write_bytes(run('exec-out','screencap','-p'))
run('shell','am','force-stop','org.kustom.wallpaper.huawei')
run('shell','am','start','-W','-a','android.service.wallpaper.CHANGE_LIVE_WALLPAPER','--ecn','android.service.wallpaper.extra.LIVE_WALLPAPER_COMPONENT','org.kustom.wallpaper.huawei/org.kustom.wallpaper.WpGLService')
print('Fresh home wallpaper preview opened; waiting for home-only selection',flush=True)
