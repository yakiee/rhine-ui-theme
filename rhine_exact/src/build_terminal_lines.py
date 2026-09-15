"""Restore the paired time-row rules visible in the original Rhine preview."""
from pathlib import Path
import json,zipfile
BASE=Path(__file__).resolve().parents[1]
SOURCE=BASE/'output/parallax-v0.8';OUT=BASE/'output/terminal-lines-v0.8.1';OUT.mkdir(exist_ok=True)
def placed_rule(title,x,y,width):
 return {'internal_type':'OverlapLayerModule','internal_title':title,'position_anchor':'CENTER','position_padding_left':max(0,x*2),'position_padding_right':max(0,-x*2),'position_padding_top':max(0,y*2),'position_padding_bottom':max(0,-y*2),'viewgroup_items':[{'internal_type':'ShapeModule','internal_title':title,'position_anchor':'CENTER','shape_type':'RECT','shape_width':width,'shape_height':2.2,'paint_color':'#E6FFFFFF'}]}
for suffix in ['', '-off']:
 filename=f'Rhine-UI-parallax{suffix}-v0.8.klwp'
 with zipfile.ZipFile(SOURCE/filename)as archive:
  preset=json.loads(archive.read('preset.json'));status=preset['preset_root']['viewgroup_items'][4]
  assert status['internal_title']=='主菜单 · 设备状态'
  # The battery sits between the left rule and timestamp; align its gap to the reference.
  battery=status['viewgroup_items'][8]
  assert battery['viewgroup_items'][0]['shape_width']==30
  battery['position_padding_right']=184
  status['viewgroup_items'] += [placed_rule('时间左侧细线',-182.5,-315,125),placed_rule('时间右侧细线',238,-315,208)]
  preset['preset_info']['title']='Rhine UI · 终端细节 v0.8.1'+(' · 静止版' if suffix else '')
  preset['preset_info']['description']='补齐日期时间两侧白色细线，与状态栏共享透视及入场动画；随动版同时保留重力视差。'
  targetname=f'Rhine-UI-terminal-lines{suffix}-v0.8.1.klwp'
  with zipfile.ZipFile(OUT/targetname,'w',zipfile.ZIP_DEFLATED)as target:
   for name in archive.namelist():target.writestr(name,json.dumps(preset,ensure_ascii=False)if name=='preset.json'else archive.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(preset,ensure_ascii=False,indent=2),encoding='utf8')
print('Built both editions with paired editable time rules')
