"""Back only the CPU, RAM and ROM row; leave the clock and battery row unbacked."""
from pathlib import Path
import json,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/paper-menu-v0.13.5';VERSION='0.13.8'
OUT=BASE/f'output/status-strip-v{VERSION}';OUT.mkdir(exist_ok=True)
for suffix in ['', '-off']:
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-paper{suffix}-v0.13.5.klwp') as source:
  p=json.loads(source.read('preset.json'));status=p['preset_root']['viewgroup_items'][4]
  backing={'internal_type':'OverlapLayerModule','internal_title':'CPU 行 · 半透明黑色背景','position_anchor':'CENTER','position_padding_bottom':626,'position_padding_right':36,'viewgroup_items':[{'internal_type':'ShapeModule','position_anchor':'CENTER','shape_type':'RECT','shape_width':620,'shape_height':38,'paint_color':'#33000000'}]}
  # The lower translucent band projects farther left than the time rule.
  items=status['viewgroup_items']
  items[3]['position_padding_left']=0;items[3]['position_padding_right']=24
  items[3]['viewgroup_items'][0]['text_width']=122
  items[6]['position_padding_left']=0;items[6]['position_padding_right']=182
  items[4]['position_padding_left']=320;items[4]['position_padding_right']=0
  items[4]['viewgroup_items'][0]['text_width']=104
  items[4]['viewgroup_items'][0]['text_size']=23
  items[7]['position_padding_left']=160;items[7]['position_padding_right']=0
  upper_right=next(n for n in items if n.get('internal_title')=='时间右侧细线')
  upper_right['position_padding_left']=372
  upper_right['viewgroup_items'][0]['shape_width']=92
  marker={'internal_type':'OverlapLayerModule','internal_title':'资源行 · 最右侧深色短横线','position_anchor':'CENTER','position_padding_left':522,'position_padding_bottom':626,'viewgroup_items':[{'internal_type':'ShapeModule','position_anchor':'CENTER','shape_type':'RECT','shape_width':62,'shape_height':3.2,'paint_color':'#78000000'}]}
  items.append(marker)
  # Keep RAM and ROM's existing actions aligned with their compacted information groups.
  hits=p['preset_root']['viewgroup_items'][50]['viewgroup_items'][1:]
  for index,x,y,w in [(75,418,420,145),(76,590,398,188)]:
   node=hits[index];local_x=(x-360)/.94;local_y=(y-800)/.94
   node.update(position_padding_left=max(0,local_x*2),position_padding_right=max(0,-local_x*2),position_padding_top=max(0,local_y*2),position_padding_bottom=max(0,-local_y*2))
   node['viewgroup_items'][0]['shape_width']=w/.94
  status['viewgroup_items'].insert(1,backing)
  p['preset_info'].update(title=f'Rhine UI · 半透明状态底条 v{VERSION}'+(' · 无重力视差' if suffix else ''),description='资源行底色减淡，上下横条端点错开；最右侧补深色短横线，时间行保持无底色。')
  target=OUT/f'Rhine-UI-status{suffix}-v{VERSION}.klwp'
  with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as dest:
   for name in source.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else source.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
  print(target)
