"""Function-specific paper watermarks, edge bleed and coherent native parallax."""
from pathlib import Path
import json,zipfile
BASE=Path(__file__).resolve().parents[1]
SOURCE=BASE/'output/terminal-proportions-v0.13.24'
OUT=BASE/'output/menu-parallax-v0.13.25';OUT.mkdir(exist_ok=True)
def at(n,x,y):
 return dict(internal_type='OverlapLayerModule',position_anchor='CENTER',position_padding_left=max(0,2*x),position_padding_right=max(0,-2*x),position_padding_top=max(0,2*y),position_padding_bottom=max(0,-2*y),viewgroup_items=[n])
def position(n,x,y):
 n.update(position_padding_left=max(0,2*x),position_padding_right=max(0,-2*x),position_padding_top=max(0,2*y),position_padding_bottom=max(0,-2*y))
def vector(path,w,h,color,stroke=None):
 n=dict(internal_type='ShapeModule',position_anchor='CENTER',shape_type='PATH',shape_path=path,shape_path_scale='FIT_XY',shape_width=w,shape_height=h,paint_color=color)
 if stroke:n.update(paint_style='STROKE',paint_stroke=stroke)
 return n
PHONE='M 21 5 C 14 4 6 10 5 21 C 3 44 25 74 47 89 C 62 99 78 101 88 93 L 97 82 Q 99 78 95 74 L 76 62 Q 71 59 67 63 L 60 71 Q 48 66 38 55 Q 29 44 27 35 L 36 28 Q 40 25 37 20 L 28 7 Q 26 4 21 5 Z'
FOLDER='M 5 22 L 38 22 L 48 34 L 95 34 L 95 87 L 5 87 Z M 5 43 L 95 43 M 20 12 L 47 12 L 56 24 L 86 24'
CHAT='M 58 54 C 76 54 95 61 95 76 C 95 85 90 91 84 95 L 88 102 L 72 98 C 53 101 36 91 36 77 C 36 64 44 57 58 54 Z M 37 5 C 58 5 76 18 76 34 C 76 48 62 59 45 61 C 41 66 34 70 24 71 L 26 61 C 10 56 2 47 2 34 C 2 18 18 5 37 5 Z M 23 29 L 29 29 M 48 29 L 54 29 M 53 75 L 58 75 M 75 75 L 80 75'
PAYCARD='M 4 8 L 96 8 L 96 92 L 4 92 Z M 4 28 L 96 28 M 18 45 L 18 78 M 27 45 L 27 78 M 36 45 L 36 78 M 50 45 L 50 78 M 60 45 L 60 78 M 71 45 L 71 78 M 82 45 L 82 78'
SCAN='M 24 4 L 4 4 L 4 24 M 76 4 L 96 4 L 96 24 M 4 76 L 4 96 L 24 96 M 76 96 L 96 96 L 96 76 M 22 22 L 42 22 L 42 42 L 22 42 Z M 58 22 L 78 22 L 78 42 L 58 42 Z M 22 58 L 42 58 L 42 78 L 22 78 Z M 58 58 L 68 58 L 68 68 L 78 68 L 78 78 M 58 78 L 58 68 M 13 50 L 87 50'
for suffix in ['', '-off']:
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-terminal-proportions{suffix}-v0.13.24.klwp') as src:
  p=json.loads(src.read('preset.json'));r=p['preset_root']['viewgroup_items']
  for i,path,w,h,x,y in [(17,PHONE,100,107,43,4),(18,FOLDER,128,108,47,4)]:
   mark=r[i]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items'][4]
   position(mark,x,y);mark['viewgroup_items']=[vector(path,w,h,'#37616A6E',None if i==17 else 4)]
   mark['internal_title']='电话听筒水印' if i==17 else '文件夹水印'
  wechat=r[19]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items']
  wechat[3]['paint_color']='#EF45484A'
  wechat.append(at(vector(CHAT,79,79,'#428F9799',4),7,22))
  for i,path in [(6,PAYCARD),(8,SCAN)]:
   mark=r[i]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items'][0]['viewgroup_items'][4]
   position(mark,44,-2);mark['viewgroup_items']=[vector(path,91 if i==6 else 83,73,'#48E4FBFF',3)]
  mark=r[14]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items'][0]['viewgroup_items'][4]
  position(mark,29,-10);mark['viewgroup_items'][0].update(text_size=103,paint_color='#40E4FBFF')
  # Extend only paper and texture to the right. All original left edges stay fixed.
  face=r[5]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items']
  for index in [0,1,2]:
   face[index]['viewgroup_items'][0]['shape_width']+=110
   position(face[index],55,2.5)
  face[3]['shape_width']+=110;face[3]=at(face[3],55,0)
  face[5]['shape_width']+=110;face[5]=at(face[5],55,0)
  # Keep the menu, dividers, decorative filler and touch proxies in one sensor cohort.
  if not suffix:
   for index in [4,5,6,7,8,9,10,11,14,17,18,19,50]:
    for a in r[index].get('internal_animations',[]):
     if a.get('type')=='GYRO':a.update(speed=8,limit=18)
  p['preset_info'].update(title='Rhine UI · 水印与视差 v0.13.25'+(' · 无重力视差' if suffix else ''),description='补全电话/文件/微信图案，强化支付图案，微信改为炭灰纸面；首行向右出血，菜单与点击区同步轻微视差。')
  target=OUT/f'Rhine-UI-menu-parallax{suffix}-v0.13.25.klwp'
  with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as dest:
   for name in src.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else src.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
  print(target)
