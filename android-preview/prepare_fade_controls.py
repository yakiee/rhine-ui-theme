from pathlib import Path
import json,copy
from rebuild_ui import run

out=Path('rhine_exact/output/dock-opacity-controls-20260914')
old=json.loads((out/'simple-controls.clip.txt').read_text(encoding='utf-8').replace('##KUSTOMCLIP##',''))['clip_modules']
modules=[]
for index,name in enumerate(('static','FADE','FADE_INVERTED','ADVANCED')):
    node=copy.deepcopy(old[0]);node['internal_title']='DIAGNOSTIC_OPACITY_'+name;node['position_offset_x']=-225+150*index
    if index:
        node['internal_formulas']['config_visible']='$if(1,ALWAYS,REMOVE)$'
        animation={'type':'FORMULA','formula':'$if(gv(page)=1,f,b)$','action':name,'duration':4.8,'delay':0,'anchor':'MODULE_CENTER','ease':'STRAIGHT','speed':100}
        if name=='ADVANCED':animation['animator']=copy.deepcopy(old[3]['internal_animations'][0]['animator'])
        node['internal_animations']=[animation]
    modules.append(node)
path=out/'fade-controls.clip.txt';path.write_text('##KUSTOMCLIP##\n'+json.dumps({'clip_version':1,'clip_modules':modules})+'\n##KUSTOMCLIP##',encoding='utf-8')
run('push',path.resolve(),'/data/local/tmp/rhine-editor-input.txt')
run('shell','CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard KUSTOM_MODULES /data/local/tmp/rhine-editor-input.txt')
print('Prepared native fade and explicit visibility controls.')
