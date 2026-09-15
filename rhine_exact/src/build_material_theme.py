"""Arknights-derived card materials, settings surfaces and Dock lighting."""
from pathlib import Path
from copy import deepcopy
import json,zipfile,math
from static_helpers import walk,formula,normalize_nested_positions
from refine_homepage import shape,at,label
from refine_pages_matched import placed,rect,text
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/details-v0.6/Rhine-UI-details-v0.6.klwp';OUT=BASE/'output/material-v0.7';OUT.mkdir(exist_ok=True)
with zipfile.ZipFile(SOURCE)as z:p=json.loads(z.read('preset.json'))
roots=p['preset_root']['viewgroup_items']
def local(n,x,y):
 h={'viewgroup_items':[at(n,x,y)]};normalize_nested_positions(h);return h['viewgroup_items'][0]
def fixed_color(n,color):
 n['paint_color']=color;n.get('internal_formulas',{}).pop('paint_color',None);n.get('internal_toggles',{}).pop('paint_color',None)
def dots(w,h,color):
 commands=[]
 for row in range(12):
  for col in range(30):
   x=(col+.5)/30*100;y=(row+.5)/12*100;r=.15+.42*(col/29)*(row/11)
   commands.append(f'M {x-r:.3f} {y:.3f} a {r:.3f} {r*w/h:.3f} 0 1 0 {2*r:.3f} 0 a {r:.3f} {r*w/h:.3f} 0 1 0 {-2*r:.3f} 0 Z')
 return shape(w,h,color,' '.join(commands))
rook='M 12 0 L 32 0 L 32 16 L 43 16 L 43 0 L 63 0 L 63 16 L 75 16 L 75 0 L 95 0 L 90 32 L 77 41 L 77 72 L 90 87 L 90 100 L 10 100 L 10 87 L 23 72 L 23 41 L 8 30 Z M 37 40 L 63 40 L 63 73 L 37 73 Z'
hexagon='M 50 0 L 94 25 L 94 75 L 50 100 L 6 75 L 6 25 Z M 50 19 L 77 35 L 77 65 L 50 81 L 23 65 L 23 35 Z'
formation='M 8 12 L 35 12 L 35 38 L 8 38 Z M 46 12 L 93 12 L 93 22 L 46 22 Z M 46 30 L 93 30 L 93 38 L 46 38 Z M 8 55 L 35 55 L 35 83 L 8 83 Z M 46 55 L 93 55 L 93 65 L 46 65 Z M 46 75 L 93 75 L 93 83 L 46 83 Z'
# Each decoration stays in its original animated and projected card group.
for root in roots:
 title=root.get('internal_title','')
 if not title.startswith('主菜单 · ') or not ('底板'in title):continue
 for holder in root['viewgroup_items'][1:]:
  children=holder.get('viewgroup_items',[])
  if len(children)!=1:continue
  base=children[0];w=base.get('shape_width',0);h=base.get('shape_height',0)
  if base.get('shape_type')!='RECT' or w<200 or h<85:continue
  is_blue='支付'in title;dark=base.get('paint_color')=='#FF14171D'
  layers=[]
  for spread,alpha in [(9,8),(6,10),(3,16)]:
   shadow=shape(w+spread,h+spread,f'#{alpha:02X}050A10');layers.append(local(shadow,2,5))
  fixed_color(base,'#F208A9D4' if is_blue else '#EAF3F3F2' if not dark else '#ED171B20');layers.append(base)
  watermark=shape(min(w*.45,h*.88),h*.88,'#22616A6E' if not is_blue else '#33FFFFFF',hexagon if is_blue else rook if '设置'in title or '终端'in title else formation)
  layers.append(local(watermark,w*.26,0));layers.append(dots(w,h,'#23515A62' if not is_blue else '#2DFFFFFF'))
  # Faint paper lines and a hairline rim reveal overlapping surfaces.
  rim=shape(w,h,'#85FFFFFF');rim.update(paint_style='STROKE',paint_stroke=1);layers.append(rim)
  holder['viewgroup_items']=layers
# Section backgrounds and settings use the source screenshot's dark/blue controls.
for root in roots:
 title=root.get('internal_title','')
 if not title.startswith(('23 ','24 ')):continue
 items=root['viewgroup_items']
 # Local backdrop starts below navigation, keeping the existing return control visible.
 mask=shape(720,1380,'#FFFFFFFF');mask['fx_mask']='CLIP_NEXT'
 bitmap={'internal_type':'BitmapModule','position_anchor':'CENTER','bitmap_bitmap':'kfile://org.kustom.provider/bitmaps/wall-reconstructed.png','bitmap_width':720,'bitmap_height':1600,'bitmap_scale_mode':'CENTER_CROP','bitmap_blur':28}
 backdrop={'internal_type':'OverlapLayerModule','position_anchor':'CENTER','internal_title':'设置磨砂背景','viewgroup_items':[mask,local(bitmap,0,-110)]}
 frost=shape(720,1380,'#C4F2F3F3');formula(frost,'paint_color','if(gv(dark),#DC171B22,#C4F2F3F3)');backdrop['viewgroup_items'].append(frost)
 panel=shape(658,1270,'#66FFFFFF');formula(panel,'paint_color','if(gv(dark),#60242A33,#66FFFFFF)');backdrop['viewgroup_items'].append(panel)
 additions=[local(backdrop,0,110)]
 # Apply selected fills to the same conditional modules that previously drew only outlines.
 for i,holder in enumerate(items):
  for n in walk(holder):
   w=n.get('shape_width',0);h=n.get('shape_height',0)
   if n.get('shape_type')=='RECT' and 150<w<650 and 45<=h<=86 and n.get('paint_color')!='#00000000':
    fixed_color(n,'#E525292E')
   if n.get('internal_type')=='TextModule' and n.get('text_expression') in ['六星','赛博','取色','关闭','开启','主导','温和','活力','日期','图标','外观设置','功能设置']:
    fixed_color(n,'#FFF3F4F4')
  if any(n.get('shape_type')=='RECT' and 150<n.get('shape_width',0)<650 and 45<=n.get('shape_height',0)<=86 for n in walk(holder)):
   for following in items[i+1:i+3]:
    labels=[n for n in walk(following) if n.get('internal_type')=='TextModule']
    if labels:
     for n in labels:fixed_color(n,'#FFF3F4F4')
     break
  visible=holder.get('internal_formulas',{}).get('config_visible','')
  if visible.startswith('$if(') and visible.endswith(',ALWAYS,NEVER)$'):
   for n in walk(holder):
    if n.get('paint_style')=='STROKE':n['paint_style']='FILL';fixed_color(n,'#FF087EA5')
 # Thin button rims and restrained contact shadows sit underneath the existing selected overlays.
 for holder in items:
  children=holder.get('viewgroup_items',[])
  if len(children)==1:
   base=children[0];w=base.get('shape_width',0);h=base.get('shape_height',0)
   if base.get('shape_type')=='RECT' and 150<w<650 and 45<=h<=86:
    shadow=shape(w,h,'#33050B12');rim=shape(w,h,'#8CD6DADF');rim.update(paint_style='STROKE',paint_stroke=1)
    holder['viewgroup_items']=[local(shadow,1,4),base,rim]
 # Active settings tab stays light as in the game's left selected section.
 active_base=1 if title.startswith('23 ') else 3;active_text=active_base+1
 for n in walk(items[active_base]):
  if n.get('internal_type')=='ShapeModule':fixed_color(n,'#EDFFFFFF')
 for n in walk(items[active_text]):
  if n.get('internal_type')=='TextModule':fixed_color(n,'#FF191D22')
 # A compact black section band occupies the gap above the first existing setting.
 additions += [rect(180,157,288,19,'#EC1C2025'),text(180,157,270,12,'主页设置' if title.startswith('23 ') else '交互设置','#FFFFFFFF')]
 root['viewgroup_items']=[items[0]]+additions+items[1:]
 # Section headings and explanations get the larger contrast range visible in the reference.
 for n in walk(root):
  if n.get('text_expression') in ['主页光条风格','光条光点','壁纸取色模式','加载动画','主题风格','Dock 栏样式','避开 Dock 栏','全屏返回','重力视差']:
   n['text_size']=32
# A localized light bloom interrupts the previously uniform gold band.
glow=next(r for r in roots if r.get('internal_title','').startswith('Dock 渐变点阵'))
lights=[]
for i in range(18):
 size=1-i*.046;n=shape(270*size,87*size,f'#{(3+i//5):02X}FFF5CF');n.update(shape_type='PATH',shape_path='M 0 50 a 50 50 0 1 0 100 0 a 50 50 0 1 0 -100 0 Z',shape_path_scale='FIT_XY');lights.append(local(n,-190,7))
# Keep the original animation and insert the bloom beneath the perforations.
glow['viewgroup_items'][-1:-1]=lights
for n in walk(glow):
 if n.get('shape_type')=='PATH' and n.get('shape_width')==1060:formula(n,'paint_color','if(gv(dots),#BDFFFFFF,#00FFFFFF)')
p['preset_info'].update(title='Rhine UI · 材质校准 v0.7',description='按用户提供的明日方舟界面优化卡片暗纹、薄边与阴影、设置页磨砂面板和蓝色选中态、Dock 局部光晕。仍为可编辑交互预览。')
assert len(roots)==64
(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8',newline='\n')
with zipfile.ZipFile(SOURCE)as z,zipfile.ZipFile(OUT/'Rhine-UI-material-v0.7.klwp','w',zipfile.ZIP_DEFLATED)as target:
 for name in z.namelist():target.writestr(name,json.dumps(p,ensure_ascii=False)if name=='preset.json'else z.read(name))
print('Built v0.7 with',len(roots),'roots')
