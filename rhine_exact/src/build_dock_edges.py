"""Keep the Dock backing beyond the viewport throughout rotation."""
from pathlib import Path
import json,zipfile,math
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/dock-motion-v0.8.6';OUT=BASE/'output/dock-edges-v0.8.7';OUT.mkdir(exist_ok=True)
for suffix in ['', '-off']:
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-dock-motion{suffix}-v0.8.6.klwp') as source:
  p=json.loads(source.read('preset.json'));dock=p['preset_root']['viewgroup_items'][23]
  dock['internal_title']='Dock 底板 · 旋转全程覆盖屏幕边缘'
  for index in [0,1,2]:
   shape=dock['viewgroup_items'][index]
   shape['shape_width']=1060
   if index in [1,2]:
    shape['shape_type']='RECT'
    shape.pop('shape_path',None);shape.pop('shape_path_scale',None)
    shape.get('internal_formulas',{}).pop('shape_width',None)
    shape.get('internal_toggles',{}).pop('shape_width',None)
  p['preset_info']['title']='Rhine UI · Dock 边缘修复 v0.8.7'+(' · 静止版' if suffix else '')
  p['preset_info']['description']='黑色 Dock 与暖光反射底板采用固定宽度的完整矩形，避免切页瞬间收窄与切角露入屏幕；保留贴合动画和实时电量。'
  output=OUT/f'Rhine-UI-dock-edges{suffix}-v0.8.7.klwp'
  with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
   for name in source.namelist():z.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else source.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
  print(output.name)
# Account for the existing 720x1600 scene scaling on a 720x1504 wallpaper viewport.
minimum_margin=min((1060*math.cos(math.radians(angle))-228*math.sin(math.radians(angle)))*.94/2-360 for angle in [i*23.7/1000 for i in range(1001)])
assert minimum_margin>50
(OUT/'geometry-check.json').write_text(json.dumps({'minimum_side_margin_px_on_emulator':minimum_margin,'allows_gyro_px':22},indent=2),encoding='utf8')
print('Minimum side margin',minimum_margin)
