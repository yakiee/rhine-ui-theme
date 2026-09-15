import json,re,time
from toolbar_native import OUT,SOURCE,tree,guard,run,click
data=json.loads((OUT/'root-3-after.clip.txt').read_text(encoding='utf-8').replace('##KUSTOMCLIP##',''))
module=data['clip_modules'][0]
module['internal_formulas']['config_visible']='$if(si(screen)=gv(homepg),if(gv(page)=0,ALWAYS,REMOVE),REMOVE)$'
module['internal_animations']=[dict(type='SCROLL',action='ADVANCED',center='SCREEN2',anchor='MODULE_CENTER',ease='STRAIGHT',speed=100,amount=100,internal_toggles={'center':10},internal_formulas={'center':'$"SCREEN"+gv(homepg)$'},animator=[dict(position=p,property=prop,value=value,ease='STRAIGHT') for p,value in [(0,1),(100,.98)] for prop in ['SCALE_X','SCALE_Y']])]
path=OUT/'root-3-final.clip.txt'
path.write_text('##KUSTOMCLIP##\n'+json.dumps(data,ensure_ascii=False)+'\n##KUSTOMCLIP##',encoding='utf-8')
for attempt in range(12):
    root=tree()
    node=next((n for n in root.iter('node') if n.get('resource-id','').endswith('/module_title') and n.get('text')==SOURCE[3]['internal_title']),None)
    if node is not None:break
    assert any(n.get('text')=='根目录' for n in root.iter('node'))
    guard();run('shell','input','swipe',650,2490,650,2070,70);time.sleep(.8)
else:raise RuntimeError('Toolbar not found')
y=int(re.findall(r'\d+',node.get('bounds'))[1])
click(next(n for n in root.iter('node') if n.get('resource-id','').endswith('/checkbox') and int(re.findall(r'\d+',n.get('bounds'))[1])==y))
click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_delete')))
root=tree()
confirm=next((n for n in root.iter('node') if n.get('resource-id')=='android:id/button1'),None)
if confirm is not None:click(confirm)
run('push',path.resolve(),'/data/local/tmp/rhine-editor-input.txt')
run('shell','CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard KUSTOM_MODULES /data/local/tmp/rhine-editor-input.txt')
click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_paste')))
click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_save')))
time.sleep(.7);run('shell','input','keyevent','KEYCODE_HOME')
print('Saved final toolbar: synchronized visibility, no opacity animation, 2% scroll scale')
