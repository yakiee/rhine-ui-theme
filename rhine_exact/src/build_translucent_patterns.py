"""Add translucent paper and native micro-patterns visible at handset scale."""
from pathlib import Path
import json,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/reference-palette-v0.13.39';OUT=BASE/'output/translucent-patterns-v0.13.40';OUT.mkdir(exist_ok=True)

def path_shape(path,w,h,color):
 return dict(internal_type='ShapeModule',position_anchor='CENTER',shape_type='PATH',shape_path=path,shape_path_scale='FIT_XY',shape_width=w,shape_height=h,paint_color=color)

def pattern(w,h,light=False):
 # Tiny non-visible path segments establish stable bounds without a raster texture.
 bounds=f'M 0 0 L .001 .001 M {w} {h} l -.001 -.001 '
 dots=[];tiles=[];rules=[]
 step=6
 for row,y in enumerate(range(4,int(h)-3,step)):
  for col,x in enumerate(range(4,int(w)-3,step)):
   # Dense in the lower-right corner; clear around the main title on the left.
   if x<w*.54 or y<h*.43 or (x<w*.7 and y<h*.7):continue
   radius=.95 if x>w*.76 and y>h*.7 else .62
   dots.append(f'M {x-radius:.3f} {y} a {radius} {radius} 0 1 0 {2*radius} 0 a {radius} {radius} 0 1 0 {-2*radius} 0 Z')
 for fx,fy,size in ((.61,.16,6),(.78,.25,4),(.92,.11,5),(.48,.79,3),(.88,.58,3),(.72,.65,4)):
  x,y=fx*w,fy*h;tiles.append(f'M {x} {y} h {size} v {size} h {-size} Z')
 for j in range(5):
  x=w*.09+j*5;y=h*.78+(j%3)*3
  rules.append(f'M {x} {y} h .8 v {h*.16-(j%3)*3} h -.8 Z')
 shapes=[path_shape(bounds+' '.join(dots),w,h,'#22D9F5FF' if light else '#245E6467'),path_shape(bounds+' '.join(tiles),w,h,'#13E6F8FF' if light else '#12555C60'),path_shape(bounds+' '.join(rules),w,h,'#18E6F8FF' if light else '#145D656A')]
 return dict(internal_type='OverlapLayerModule',position_anchor='CENTER',internal_title='纸面微纹理 · 边角点阵与淡色几何块',viewgroup_items=shapes)

for suffix in ('','-off'):
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-reference-palette{suffix}-v0.13.39.klwp') as source:
  p=json.loads(source.read('preset.json'));r=p['preset_root']['viewgroup_items']
  first=r[5]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items'];face=first[3]['viewgroup_items'][0];face['paint_color']='#DEFFFFFF'
  first[5]['viewgroup_items'][0]=pattern(face['shape_width'],face['shape_height'])
  for index in (10,11,17,18):
   group=r[index]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items'];face=group[3];face['paint_color']='#DEFFFFFF';group[5]=pattern(face['shape_width'],face['shape_height'])
  for index in (6,8,14):
   group=r[index]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items'][0]['viewgroup_items'];face=group[3];face['paint_color']='#DB58B4E6'
   watermark=group[4];group[4]=dict(internal_type='OverlapLayerModule',position_anchor='CENTER',internal_title='蓝色半透明纸面 · 纹理与功能水印',viewgroup_items=[pattern(face['shape_width'],face['shape_height'],True),watermark])
  header=r[9]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items'][0]['viewgroup_items'];header[0]['paint_color']='#DB58B4E6';header[1]['paint_color']='#E6373737'
  group=r[19]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items'];face=group[3];face['paint_color']='#D9444444';group.append(pattern(face['shape_width'],face['shape_height'],True))
  p['preset_info'].update(title='Rhine UI · 半透明纹理纸面 v0.13.40'+(' · 无重力视差' if suffix else ''),description='按钮底层透出壁纸；保留不透明文字。补充边角细点阵、淡色几何块与短线，蓝色底补偿透明混色，保持方舟参考色调。')
  with zipfile.ZipFile(OUT/f'Rhine-UI-translucent-patterns{suffix}-v0.13.40.klwp','w',zipfile.ZIP_DEFLATED) as dest:
   for name in source.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else source.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
 print(suffix or 'normal','built')
