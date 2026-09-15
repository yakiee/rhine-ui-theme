import json,time
from toolbar_native import OUT,tree,click,run
animation=dict(type='FORMULA',formula='$if(gv(page)!=0 | si(screen)!=gv(homepg),1,0)$',action='FADE',anchor='MODULE_CENTER',duration=2.2,delay=0,ease='STRAIGHT',speed=100,limit=100)
path=OUT/'sidebar-rest-opaque-animation.clip.txt'
path.write_text('##KUSTOMCLIP##\n'+json.dumps({'clip_version':1,'KUSTOM_ANIMATION':{'0':animation}})+'\n##KUSTOMCLIP##',encoding='utf-8')
root=tree()
assert not any(n.get('resource-id','').endswith('/checkbox') for n in root.iter('node'))
run('push',path.resolve(),'/data/local/tmp/rhine-editor-input.txt')
run('shell','CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard KUSTOM_ANIMATION /data/local/tmp/rhine-editor-input.txt')
click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_paste')))
root=tree()
assert sum(n.get('resource-id','').endswith('/checkbox') for n in root.iter('node'))==1
click(next(n for n in root.iter('node') if n.get('resource-id','').endswith('/action_save')))
time.sleep(.8)
run('shell','input','keyevent','KEYCODE_HOME')
print('Saved native fade-out with explicit 100% range; visible state uses untransformed layer')
