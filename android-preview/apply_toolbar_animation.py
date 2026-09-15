import json,time
from toolbar_native import OUT,tree,click,run

path=OUT/'sidebar-stable-animation.clip.txt'
data=json.loads(path.read_text(encoding='utf-8').replace('##KUSTOMCLIP##',''))
animation=data['KUSTOM_ANIMATION']['0']
animation['formula']='$if(gv(page)=0 & si(screen)=gv(homepg),f,b)$'
path.write_text('##KUSTOMCLIP##\n'+json.dumps(data)+'\n##KUSTOMCLIP##',encoding='utf-8')
root=tree()
assert sum(n.get('resource-id','').endswith('/checkbox') for n in root.iter('node'))==2
for check in [n for n in root.iter('node') if n.get('resource-id','').endswith('/checkbox')]:click(check)
root=tree()
click(next(n for n in root.iter('node') if n.get('resource-id','').endswith('/action_delete')))
root=tree()
positive=next((n for n in root.iter('node') if n.get('resource-id')=='android:id/button1'),None)
if positive:click(positive)
assert not any(n.get('resource-id','').endswith('/checkbox') for n in tree().iter('node'))
run('push',path.resolve(),'/data/local/tmp/rhine-editor-input.txt')
run('shell','CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard KUSTOM_ANIMATION /data/local/tmp/rhine-editor-input.txt')
root=tree();click(next(n for n in root.iter('node') if n.get('resource-id','').endswith('/action_paste')))
root=tree()
assert sum(n.get('resource-id','').endswith('/checkbox') for n in root.iter('node'))==1
click(next(n for n in root.iter('node') if n.get('resource-id','').endswith('/action_save')))
time.sleep(1)
run('shell','input','keyevent','KEYCODE_HOME');time.sleep(.8)
full=OUT/'root-3-final.clip.txt'
node=json.loads(full.read_text(encoding='utf-8').replace('##KUSTOMCLIP##',''))
node['clip_modules'][0]['internal_animations']=[animation]
full.write_text('##KUSTOMCLIP##\n'+json.dumps(node,ensure_ascii=False)+'\n##KUSTOMCLIP##',encoding='utf-8')
print('Single explicit forward/backward animation saved')
