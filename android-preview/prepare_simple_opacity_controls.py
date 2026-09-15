from pathlib import Path
import json,copy
from rebuild_ui import run

out=Path('rhine_exact/output/dock-opacity-controls-20260914')
old=json.loads((out/'controls.clip.txt').read_text(encoding='utf-8').replace('##KUSTOMCLIP##',''))['clip_modules'][0]
modules=[]
for index,name in enumerate(('static','flip_only','zero_to_hundred','hundred_to_zero')):
    node=copy.deepcopy(old)
    node['internal_title']='DIAGNOSTIC_OPACITY_'+name
    node['position_offset_x']=-225+150*index
    if name=='flip_only':
        node['config_rotate_mode']='FLIP_Y';node['config_rotate_offset']=-15
    if index>=2:
        node.pop('internal_toggles',None);node.pop('internal_formulas',None)
        start,end=(0,100) if index==2 else (100,0)
        node['internal_animations']=[{'type':'FORMULA','formula':'$gv(page)=1$','action':'ADVANCED','duration':4.8,'delay':0,'anchor':'MODULE_CENTER','ease':'STRAIGHT',
            'animator':[{'position':0,'property':'OPACITY','value':start,'ease':'STRAIGHT'},{'position':100,'property':'OPACITY','value':end,'ease':'STRAIGHT'}]}]
    modules.append(node)
path=out/'simple-controls.clip.txt';path.write_text('##KUSTOMCLIP##\n'+json.dumps({'clip_version':1,'clip_modules':modules})+'\n##KUSTOMCLIP##',encoding='utf-8')
run('push',path.resolve(),'/data/local/tmp/rhine-editor-input.txt')
run('shell','CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard KUSTOM_MODULES /data/local/tmp/rhine-editor-input.txt')
print('Prepared static, 3D-only, and both opacity directions.')
