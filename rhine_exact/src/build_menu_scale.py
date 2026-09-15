"""Enlarge the edge-aligned terminal menu while preserving its layout."""
from pathlib import Path
import json,zipfile,copy
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/menu-edge-v0.9.4';OUT=BASE/'output/menu-scale-v0.9.5';OUT.mkdir(exist_ok=True)
S='mu(min,1,si(sheight)*720/si(swidth)/1600)'
for suffix in ['', '-off']:
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-menu-edge{suffix}-v0.9.4.klwp') as source:
  p=json.loads(source.read('preset.json'));r=p['preset_root']['viewgroup_items'];old=copy.deepcopy(r)
  for index in list(range(4,22))+[50]:
   for field,value in [('config_scale_value','115*'+S),('position_offset_x','120*'+S)]:
    r[index].setdefault('internal_toggles',{})[field]=10
    r[index].setdefault('internal_formulas',{})[field]='$'+value+'$'
  assert [n.get('internal_animations') for n in r]==[n.get('internal_animations') for n in old]
  for index in set(range(64))-set(range(4,22))-{50}:assert r[index]==old[index]
  p['preset_info']['title']='Rhine UI · 终端放大 v0.9.5'+(' · 无重力视差' if suffix else '')
  p['preset_info']['description']='终端菜单整体放大15%，同步调整右侧贴边位置与设置点击区域，保留排列、实时数据和动画。'
  target=OUT/f'Rhine-UI-menu-scale{suffix}-v0.9.5.klwp'
  with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as dest:
   for name in source.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else source.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
  print(target)
