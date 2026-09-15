"""Patch only the Dock exit track on the three bar layers and the toolbar."""
import contextlib,io,json,re,time
from pathlib import Path
from toolbar_native import tree,click,run,ClipboardControl,SOURCE
from opacity_navigation import navigate

OUT=Path('rhine_exact/output/dock-toolbar-motion-20260915');OUT.mkdir(exist_ok=True)
STATE=OUT/'applied.json'
state=json.loads(STATE.read_text(encoding='utf-8')) if STATE.exists() else {}

def open_root():
    raw=run('shell','dumpsys','activity','activities').decode(errors='replace')
    assert any('topResumedActivity' in s and ('com.miui.home/' in s or 'org.kustom.wallpaper.huawei/' in s) for s in raw.splitlines()),'Phone left desktop/theme editor'
    run('shell','input','keyevent',3)
    with contextlib.redirect_stdout(io.StringIO()):
        exec(Path('android-preview/open_current_editor.py').read_text(encoding='utf-8'))

def clipboard(path,label,payload):
    path.write_text('##KUSTOMCLIP##\n'+json.dumps(payload,ensure_ascii=False)+'\n##KUSTOMCLIP##',encoding='utf-8')
    run('push',path.resolve(),'/data/local/tmp/rhine-editor-input.txt')
    run('shell',f'CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard {label} /data/local/tmp/rhine-editor-input.txt')

def animation(toolbar=False):
    # Kustom duration units are 100 ms. Both directions share one continuous track.
    keyframes=[]
    for position,factor in [(0,0),(22,.14),(55,.64),(82,.94),(100,1)]:
        values={'OPACITY':100*factor,'Y_OFFSET':(12 if toolbar else 48)*factor}
        if toolbar:values.update(SCALE_X=1-.08*factor,SCALE_Y=1-.08*factor)
        for prop,value in values.items():keyframes.append(dict(position=position,property=prop,value=value,ease='STRAIGHT'))
    return dict(type='FORMULA',formula='$if(gv(page)!=0 | si(screen)!=gv(homepg),f,b)$' if toolbar else '$if(gv(page)=1,f,b)$',action='ADVANCED',anchor='MODULE_CENTER',duration=3.2,delay=0,ease='STRAIGHT',amount=100,speed=100,animator=keyframes)

def checkbox_for(r,node):
    y=sum(int(x) for x in re.findall(r'\d+',node.get('bounds'))[1::2])/2
    return min([n for n in r.iter('node') if n.get('resource-id','').endswith('/checkbox')],key=lambda n:abs(sum(int(x) for x in re.findall(r'\d+',n.get('bounds'))[1::2])/2-y))

for index in [1,23,24]:
    if str(index) in state:continue
    open_root();r,n=navigate(index);click(n);run('shell','input','tap',755,2010)
    for attempt in range(8):
        r=tree();fade=next((n for n in r.iter('node') if n.get('resource-id','').endswith('/value') and n.get('text')=='淡出'),None)
        if fade is not None:break
        run('shell','input','swipe',650,2480,650,2090,200);time.sleep(.4)
    else:raise RuntimeError('Unique fade-out track not found')
    click(checkbox_for(r,fade));click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_copy')))
    with ClipboardControl() as c:before=c.get()
    data=json.loads(before.replace('##KUSTOMCLIP##',''))
    tracks=list(data['KUSTOM_ANIMATION'].values())
    assert len(tracks)==1 and tracks[0]['action']=='FADE' and 'gv(page)=1' in tracks[0]['formula']
    (OUT/f'root-{index}-dock-before.clip.txt').write_text(before,encoding='utf-8')
    r=tree();delete=next((n for n in r.iter('node') if n.get('resource-id','').endswith('/action_delete')),None)
    if delete is None:
        fade=next(n for n in r.iter('node') if n.get('resource-id','').endswith('/value') and n.get('text')=='淡出')
        click(checkbox_for(r,fade));r=tree();delete=next(n for n in r.iter('node') if n.get('resource-id','').endswith('/action_delete'))
    click(delete)
    clipboard(OUT/f'root-{index}-dock-after.clip.txt','KUSTOM_ANIMATION',{'clip_version':1,'KUSTOM_ANIMATION':{'0':animation()}})
    click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_paste')))
    click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_save')))
    state[str(index)]={'title':SOURCE[index]['internal_title'],'saved':True}
    STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
    print('SAVED BAR TRACK',index,flush=True)

if '3' not in state:
    open_root();r,n=navigate(3);click(checkbox_for(r,n))
    click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_copy')))
    with ClipboardControl() as c:before=c.get()
    data=json.loads(before.replace('##KUSTOMCLIP##',''));module=data['clip_modules'][0]
    assert module['internal_title']==SOURCE[3]['internal_title'] and len(module['viewgroup_items'])==10
    (OUT/'root-3-before.clip.txt').write_text(before,encoding='utf-8')
    module['internal_formulas']['config_visible']='$if(1,ALWAYS,REMOVE)$'
    module['internal_animations']=[animation(True)]
    r=tree();delete=next((n for n in r.iter('node') if n.get('resource-id','').endswith('/action_delete')),None)
    if delete is None:
        r,n=navigate(3);click(checkbox_for(r,n));delete=next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_delete'))
    click(delete)
    r=tree();confirm=next((n for n in r.iter('node') if n.get('resource-id')=='android:id/button1'),None)
    if confirm is not None:click(confirm)
    clipboard(OUT/'root-3-after.clip.txt','KUSTOM_MODULES',data)
    click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_paste')))
    click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_save')))
    state['3']={'title':SOURCE[3]['internal_title'],'saved':True}
    STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
    print('SAVED TOOLBAR ANIMATION',flush=True)
run('shell','input','keyevent',3)
run('shell','am','force-stop','org.kustom.wallpaper.huawei')
run('shell','am','start','-W','-a','android.service.wallpaper.CHANGE_LIVE_WALLPAPER','--ecn','android.service.wallpaper.extra.LIVE_WALLPAPER_COMPONENT','org.kustom.wallpaper.huawei/org.kustom.wallpaper.WpGLService')
print('Final save complete; fresh wallpaper preview ready for HOME ONLY selection',flush=True)
