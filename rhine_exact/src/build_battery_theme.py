"""Rebuild the terminal battery as a thin frame and three solid cells."""
from pathlib import Path
import json,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/terminal-lines-v0.8.1';OUT=BASE/'output/battery-v0.8.2';OUT.mkdir(exist_ok=True)
def placed_rect(title,x,y,w,h,stroke=False):
 shape={'internal_type':'ShapeModule','internal_title':title,'position_anchor':'CENTER','shape_type':'RECT','shape_width':w,'shape_height':h,'paint_color':'#FFFFFFFF'}
 if stroke:shape.update(paint_style='STROKE',paint_stroke=1.5)
 return {'internal_type':'OverlapLayerModule','internal_title':title,'position_anchor':'CENTER','position_padding_left':max(0,2*x),'position_padding_right':max(0,-2*x),'position_padding_top':max(0,2*y),'position_padding_bottom':max(0,-2*y),'viewgroup_items':[shape]}
for suffix in ['', '-off']:
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-terminal-lines{suffix}-v0.8.1.klwp')as source:
  p=json.loads(source.read('preset.json'));battery=p['preset_root']['viewgroup_items'][4]['viewgroup_items'][8]
  battery['internal_title']='终端电量 · 三格电池'
  battery['viewgroup_items']=[placed_rect('电池细外框',-1.8,0,25.6,14,True),placed_rect('右侧实心电极',12.5,0,2.8,5.6)]+[placed_rect(f'电量实心格 {i+1}',x,0,3.8,8)for i,x in enumerate([-8.8,-2.8,3.2])]
  p['preset_info']['title']='Rhine UI · 电量图标校准 v0.8.2'+(' · 静止版'if suffix else '')
  p['preset_info']['description']='按清晰参考重建终端三格电池：薄外框、等距实心竖格、实心电极，保留状态栏透视与原有动画。电量数据仍延续预览状态。'
  with zipfile.ZipFile(OUT/f'Rhine-UI-battery{suffix}-v0.8.2.klwp','w',zipfile.ZIP_DEFLATED)as target:
   for name in source.namelist():target.writestr(name,json.dumps(p,ensure_ascii=False)if name=='preset.json'else source.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
print('Built both editions with five independent battery shapes')
