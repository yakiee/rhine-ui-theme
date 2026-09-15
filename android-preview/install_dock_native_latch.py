import json,re,copy,time,contextlib,io
from pathlib import Path
from toolbar_native import tree,click,run,ClipboardControl
from opacity_navigation import navigate
OUT=Path('rhine_exact/output/open-dock-swipe-20260915')
statepath=OUT/'latch-install-state.json';state=json.loads(statepath.read_text()) if statepath.exists() else {}
def done(key):state[key]=True;statepath.write_text(json.dumps(state),encoding='utf-8');print('SAVED',key,flush=True)
def action(suffix):click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/'+suffix)))
def checkbox(r,target):
    y=sum(int(x) for x in re.findall(r'\d+',target.get('bounds'))[1::2])/2
    return min([n for n in r.iter('node') if n.get('resource-id','').endswith('/checkbox')],key=lambda n:abs(sum(int(x) for x in re.findall(r'\d+',n.get('bounds'))[1::2])/2-y))
def delete_selected():
    action('action_delete');r=tree();confirm=next((n for n in r.iter('node') if n.get('resource-id')=='android:id/button1'),None)
    if confirm is not None:click(confirm)
def paste(payload,name,label):
    path=OUT/name;path.write_text('##KUSTOMCLIP##\n'+json.dumps(payload,ensure_ascii=False)+'\n##KUSTOMCLIP##',encoding='utf-8')
    run('push',path.resolve(),'/data/local/tmp/rhine-editor-input.txt')
    run('shell',f'CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard {label} /data/local/tmp/rhine-editor-input.txt');action('action_paste')
def open_root():
    run('shell','input','keyevent',3)
    with contextlib.redirect_stdout(io.StringIO()):exec(Path('android-preview/open_current_editor.py').read_text(encoding='utf-8'))
if 'page' not in state:
    r=tree();target=next(n for n in r.iter('node') if n.get('text')=='page');click(checkbox(r,target));delete_selected()
    payload=json.loads((OUT/'live-page-global.clip.txt').read_text(encoding='utf-8').replace('##KUSTOMCLIP##',''))
    payload['KUSTOM_GLOBAL']['page']['value']='$if(si(screen)!=gv(homepg),-1,gv(origin)=si(screen) & gv(view)>0,if(gv(view)=1,gv(docklive),gv(view)),0)$'
    paste(payload,'page-with-native-latch.clip.txt','KUSTOM_GLOBAL');action('action_save');done('page')
if 'toolbar' not in state:
    open_root();r,target=navigate(51);click(checkbox(r,target));action('action_copy')
    with ClipboardControl() as c:before=c.get()
    (OUT/'toolbar-touch-before-latch.clip.txt').write_text(before,encoding='utf-8');payload=json.loads(before.replace('##KUSTOMCLIP##',''))
    hits=[]
    def visit(node):
        events=node.get('internal_events',[])
        if any(e.get('switch')=='view' and e.get('switch_text')=='1' for e in events):
            assert not any(e.get('switch')=='docklive' for e in events)
            events.append({'type':'SINGLE','action':'SWITCH_GLOBAL','switch':'docklive'});hits.append(node.get('internal_title'))
        for child in node.get('viewgroup_items',[]):visit(child)
    visit(payload['clip_modules'][0]);assert len(hits)==1,hits
    r=tree()
    if not any(n.get('resource-id','').endswith('/action_delete') for n in r.iter('node')):
        r,target=navigate(51);click(checkbox(r,target))
    delete_selected();paste(payload,'toolbar-touch-with-latch.clip.txt','KUSTOM_MODULES');action('action_save');done('toolbar')
if 'remove_monitor' not in state:
    open_root();r,target=navigate(0);click(target);r=tree();target=next(n for n in r.iter('node') if n.get('text')=='页码刷新 · 被壁纸覆盖');click(checkbox(r,target));delete_selected();action('action_save');done('remove_monitor')
run('shell','input','keyevent',3);run('shell','am','force-stop','org.kustom.wallpaper.huawei')
run('shell','am','start','-W','-a','android.service.wallpaper.CHANGE_LIVE_WALLPAPER','--ecn','android.service.wallpaper.extra.LIVE_WALLPAPER_COMPONENT','org.kustom.wallpaper.huawei/org.kustom.wallpaper.WpGLService')
exec(compile(Path('android-preview/apply_saved_home_wallpaper.py').read_text(encoding='utf-8'),'apply-home','exec'))
source=Path('android-preview/stress_open_dock_swipe.py').read_text(encoding='utf-8').replace("OUT=Path('rhine_exact/output/open-dock-swipe-20260915')", "OUT=Path('rhine_exact/output/open-dock-swipe-20260915/native-latch');OUT.mkdir(exist_ok=True)")
exec(compile(source,'stress-native-latch','exec'))
