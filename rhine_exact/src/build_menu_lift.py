"""Tighten the gap below status without disturbing row spacing or touch alignment."""
from pathlib import Path
import json,zipfile
BASE=Path(__file__).resolve().parents[1]
SOURCE=BASE/'output/terminal-edge-v0.13.33'
OUT=BASE/'output/menu-lift-v0.13.34';OUT.mkdir(exist_ok=True)
S='mu(min,1,si(sheight)*720/si(swidth)/1600)'
MENU=(5,6,7,8,9,10,11,14,17,18,19)
SHIFT=-10
for suffix in ('','-off'):
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-terminal-edge{suffix}-v0.13.33.klwp') as source:
  p=json.loads(source.read('preset.json'));roots=p['preset_root']['viewgroup_items']
  for index in MENU:
   formulas=roots[index]['internal_formulas'];old=formulas['position_offset_y'].strip('$')
   formulas['position_offset_y']=f'$({old})+({SHIFT})*{S}$'
  for index,holder in enumerate(roots[50]['viewgroup_items'][1:]):
   if 72 <= index <= 76:continue
   y=(holder.get('position_padding_top',0)-holder.get('position_padding_bottom',0))/2+SHIFT
   holder.update(position_padding_top=max(0,2*y),position_padding_bottom=max(0,-2*y))
  p['preset_info'].update(title='Rhine UI · 状态条间距 v0.13.34'+(' · 无重力视差' if suffix else ''),description='按钮组整体上移 10 个自适应单位，收紧状态条下方间距；各行间距、贴边橙线与点击区域同步保持。')
  with zipfile.ZipFile(OUT/f'Rhine-UI-menu-lift{suffix}-v0.13.34.klwp','w',zipfile.ZIP_DEFLATED) as dest:
   for name in source.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else source.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
 print(suffix or 'normal','built')
