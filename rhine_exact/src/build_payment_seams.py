"""Make the payment row read as continuous paper with fine tonal separators."""
from pathlib import Path
import copy,json,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/gallery-cover-v0.13.36';OUT=BASE/'output/payment-seams-v0.13.37';OUT.mkdir(exist_ok=True)
def pos(n,x,y):n.update(position_padding_left=max(0,x*2),position_padding_right=max(0,-x*2),position_padding_top=max(0,y*2),position_padding_bottom=max(0,-y*2))
def at(n,x,y):
 h=dict(internal_type='OverlapLayerModule',position_anchor='CENTER',viewgroup_items=[n]);pos(h,x,y);return h

def divider(x,height,direction):
 dark=dict(internal_type='ShapeModule',position_anchor='CENTER',shape_type='RECT',shape_width=.8,shape_height=height,paint_color='#48104455')
 light=dict(dark,shape_width=.7,paint_color='#40B9EEFA')
 h=dict(internal_type='OverlapLayerModule',position_anchor='CENTER',internal_title='纸面接缝 · 单像素明暗线',viewgroup_items=[dark,at(light,direction*.8,0)]);pos(h,x,0);return h
for suffix in ('','-off'):
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-gallery-cover{suffix}-v0.13.36.klwp') as source:
  p=json.loads(source.read('preset.json'));r=p['preset_root']['viewgroup_items']
  groups={i:r[i]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items'][0]['viewgroup_items'] for i in (6,8,14)}
  # These three soft layers now outline the whole row, behind all payment faces.
  for index,spread in enumerate((10,6,2)):
   holder=groups[6][index];pos(holder,8,-18.3783+2.5)
   holder['viewgroup_items'][0].update(shape_width=560+spread,shape_height=126+spread)
  for index in (8,14):
   for shadow in groups[index][:3]:shadow['viewgroup_items'][0]['paint_color']='#00000000'
  # Subpixel bleed closes rasterization cracks while preserving the original hit bounds.
  for index in (6,8,14):groups[index][3]['shape_width']+=.6
  groups[6][3]['paint_color']='#FF129FC9'
  groups[8][3]['paint_color']='#FF129FC9'
  groups[6][6]['viewgroup_items']=[]
  groups[14][6]=divider(87.6,126,-1)
  groups[8].append(divider(-95.6,89.25658,1))
  p['preset_info'].update(title='Rhine UI · 蓝色行连续接缝 v0.13.37'+(' · 无重力视差' if suffix else ''),description='蓝色三按钮保持连续底色，去掉内部独立投影，统一外围轻阴影；交界仅用细微明暗双线，点击区不变。')
  with zipfile.ZipFile(OUT/f'Rhine-UI-payment-seams{suffix}-v0.13.37.klwp','w',zipfile.ZIP_DEFLATED) as dest:
   for name in source.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else source.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
 print(suffix or 'normal','built')
