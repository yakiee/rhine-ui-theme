"""Lay out terminal content from one paper frame, instead of accumulating offsets."""
from pathlib import Path
import json,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/translucent-patterns-v0.13.40';OUT=BASE/'output/terminal-content-grid-v0.13.41';OUT.mkdir(exist_ok=True)
LAYOUT=dict(number_size=76,title_size=60,number_inset_top=18,label_inset_bottom=13,title_inset_top=19,system_gap=6.5,description_inset_bottom=13,cover_height=124,cover_inset_bottom=9)
def set_y(node,y):node.update(position_padding_top=max(0,2*y),position_padding_bottom=max(0,-2*y))
for suffix in ('','-off'):
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-translucent-patterns{suffix}-v0.13.40.klwp') as source:
  p=json.loads(source.read('preset.json'));t=p['preset_root']['viewgroup_items'][5]['viewgroup_items']
  paper_group=t[1]['viewgroup_items'][0];scale=paper_group['config_scale_value']/100
  paper_center=(t[1].get('position_padding_top',0)-t[1].get('position_padding_bottom',0))/2
  height=paper_group['viewgroup_items'][3]['viewgroup_items'][0]['shape_height']*scale
  top,bottom=paper_center-height/2,paper_center+height/2
  number_y=top+LAYOUT['number_inset_top']+80*scale/2
  label_y=bottom-LAYOUT['label_inset_bottom']-34*scale/2
  title_y=top+LAYOUT['title_inset_top']+LAYOUT['title_size']*scale/2
  system_y=title_y+LAYOUT['title_size']*scale/2+LAYOUT['system_gap']+25*scale/2
  description_y=bottom-LAYOUT['description_inset_bottom']-24*scale/2
  for index in (3,12):set_y(t[index],number_y)
  for plus_part in t[5]['viewgroup_items']:set_y(plus_part,number_y)
  for index in (10,11):set_y(t[index],label_y)
  set_y(t[8],title_y)
  for index in (6,7):set_y(t[index],system_y)
  set_y(t[9],description_y)
  t[8]['viewgroup_items'][0]['viewgroup_items'][0]['text_size']=LAYOUT['title_size']
  number_nodes=t[12]['viewgroup_items'][0]['viewgroup_items']
  number_nodes[0]['viewgroup_items'][0]['text_size']=LAYOUT['number_size'];number_nodes[1]['text_size']=LAYOUT['number_size']
  cover_h=LAYOUT['cover_height'];cover_y=bottom-LAYOUT['cover_inset_bottom']-cover_h/2
  set_y(t[4],cover_y);banner=t[4]['viewgroup_items'][0]['viewgroup_items']
  banner[0]['viewgroup_items'][0]['shape_height']=cover_h+4
  banner[1]['shape_height']=cover_h
  banner[2]['viewgroup_items'][0]['bitmap_height']=cover_h
  for index in (3,4):set_y(banner[index],cover_h/2-23/2)
  metrics=dict(paper_top=top,paper_bottom=bottom,number_center=number_y,label_center=label_y,title_center=title_y,system_center=system_y,description_center=description_y,cover_top=cover_y-cover_h/2,cover_bottom=cover_y+cover_h/2,**LAYOUT)
  p['preset_info'].update(title='Rhine UI · 首行统一比例 v0.13.41'+(' · 无重力视差' if suffix else ''),description='首行内容按纸面边框统一计算留白：数字缩至76、标题60，灰底/小标签/描述/封面共同校准；外部状态条及按钮组间距保持。')
  with zipfile.ZipFile(OUT/f'Rhine-UI-terminal-content-grid{suffix}-v0.13.41.klwp','w',zipfile.ZIP_DEFLATED) as dest:
   for name in source.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else source.read(name))
  if not suffix:
   (OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8');(OUT/'layout-metrics.json').write_text(json.dumps(metrics,indent=2),encoding='utf8')
 print(suffix or 'normal','built')
