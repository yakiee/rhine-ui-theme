"""Let resource icons extend beyond the status strip, like the reference."""
from pathlib import Path
import json,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/menu-lift-v0.13.34';OUT=BASE/'output/status-icon-scale-v0.13.35';OUT.mkdir(exist_ok=True)
def shift_y(node,delta):
 y=(node.get('position_padding_top',0)-node.get('position_padding_bottom',0))/2+delta
 node.update(position_padding_top=max(0,2*y),position_padding_bottom=max(0,-2*y))
for suffix in ('','-off'):
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-menu-lift{suffix}-v0.13.34.klwp') as source:
  preset=json.loads(source.read('preset.json'));roots=preset['preset_root']['viewgroup_items'];status=roots[4]['viewgroup_items']
  status[6]['viewgroup_items'][0].update(shape_width=54,shape_height=46,paint_stroke=2.8)
  status[7]['viewgroup_items'][0].update(shape_width=46,shape_height=46,paint_stroke=3.4)
  status[8]['viewgroup_items'][0].update(shape_width=44,shape_height=46)
  # The thin strip remains 38 high; only the icons project beyond it.
  # Lift the small clock row slightly to preserve clear space above the larger icons.
  for index in (2,9,10,11):shift_y(status[index],-4)
  # Status content is scaled 130%, whereas flat touch proxies are scaled 100%.
  for hit_index in (72,73):shift_y(roots[50]['viewgroup_items'][hit_index+1],-4*1.3)
  preset['preset_info'].update(title='Rhine UI · 资源图标越出灰条 v0.13.35'+(' · 无重力视差' if suffix else ''),description='资源图标主体高度 46，灰条仍为 38；CPU/RAM/ROM 上下超出灰条，时间行微调留白，点击区同步。')
  with zipfile.ZipFile(OUT/f'Rhine-UI-status-icon-scale{suffix}-v0.13.35.klwp','w',zipfile.ZIP_DEFLATED) as destination:
   for name in source.namelist():destination.writestr(name,json.dumps(preset,ensure_ascii=False) if name=='preset.json' else source.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(preset,ensure_ascii=False,indent=2),encoding='utf8')
 print(suffix or 'normal','built')
