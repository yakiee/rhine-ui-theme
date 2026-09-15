from pathlib import Path
import json,copy
from rebuild_ui import run

out=Path('rhine_exact/output/dock-opacity-controls-20260914');out.mkdir(parents=True,exist_ok=True)
source=Path('rhine_exact/output/dock-page-lifecycle-20260914/live-first-row.clip.txt')
live=json.loads(source.read_text(encoding='utf-8').replace('##KUSTOMCLIP##',''))['clip_modules'][0]
modules=[]
for index,name in enumerate(('static','formula','fixed','gyro')):
    node={'internal_type':'OverlapLayerModule','internal_title':'DIAGNOSTIC_OPACITY_'+name,
          'position_anchor':'CENTER','position_offset_x':-225+150*index,'position_offset_y':-530,
          'viewgroup_items':[{'internal_type':'ShapeModule','position_anchor':'CENTER','shape_type':'RECT','shape_width':100,'shape_height':46,'paint_color':'#FFFFFFFF'}]}
    if name=='static':
        node['internal_toggles']={'config_visible':10}
        node['internal_formulas']={'config_visible':'$if(gv(page)=1,ALWAYS,REMOVE)$'}
    else:
        node['internal_animations']=[copy.deepcopy(live['internal_animations'][0])]
        if name=='fixed':
            node['internal_animations'][0].pop('internal_toggles',None)
            node['internal_animations'][0].pop('internal_formulas',None)
        if name=='gyro':
            node['internal_animations'].append(copy.deepcopy(live['internal_animations'][1]))
    modules.append(node)
clip='##KUSTOMCLIP##\n'+json.dumps({'clip_version':1,'clip_modules':modules})+'\n##KUSTOMCLIP##'
path=out/'controls.clip.txt';path.write_text(clip,encoding='utf-8')
run('push',path.resolve(),'/data/local/tmp/rhine-editor-input.txt')
run('shell','CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard KUSTOM_MODULES /data/local/tmp/rhine-editor-input.txt')
print('Prepared four temporary opacity controls; no touch actions.')
