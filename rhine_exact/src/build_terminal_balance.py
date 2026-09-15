"""Correct temperature semantics and lower the terminal content hierarchy."""
from pathlib import Path
import json,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/menu-parallax-v0.13.25';OUT=BASE/'output/terminal-balance-v0.13.26';OUT.mkdir(exist_ok=True)
S='mu(min,1,si(sheight)*720/si(swidth)/1600)'
def place(n,x,y):n.update(position_padding_left=max(0,2*x),position_padding_right=max(0,-2*x),position_padding_top=max(0,2*y),position_padding_bottom=max(0,-2*y))
def walk(n):
 yield n
 for c in n.get('viewgroup_items',[]):yield from walk(c)
for suffix in ['', '-off']:
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-menu-parallax{suffix}-v0.13.25.klwp') as src:
  p=json.loads(src.read('preset.json'));roots=p['preset_root']['viewgroup_items'];root=roots[5];t=root['viewgroup_items']
  old=root['internal_formulas']['position_offset_y'].strip('$');root['internal_formulas']['position_offset_y']=f'$({old})+6*{S}$'
  # Tighten card height around the lowered contents; preserve the lower-row gap.
  face=t[1]['viewgroup_items'][0]['viewgroup_items']
  for index in [0,1,2,3,5]:
   for n in walk(face[index]):
    if 'shape_height' in n:n['shape_height']-=8
  # Temperature is a readout, with no replenish/add affordance or resource emblem.
  t[5]['viewgroup_items']=[]
  for index in [3,12]:place(t[index],-179.12,-187)
  t[3]['viewgroup_items'][0]['viewgroup_items'][0]['shape_height']=80
  for n in walk(t[12]):
   if n.get('internal_type')=='TextModule':n['text_size']=86
  place(t[8],-5,-199);t[8]['viewgroup_items'][0]['viewgroup_items'][0]['text_size']=64
  for index in [6,7]:place(t[index],-46,-151)
  place(t[9],-5,-119)
  place(t[4],161,-166)
  parts=t[4]['viewgroup_items'][0]['viewgroup_items']
  parts[0]['viewgroup_items'][0]['shape_height']=133;parts[1]['shape_height']=129
  for index in [3,4]:place(parts[index],0,53)
  # Translate only the first-row touch proxies by the same unscaled screen offset.
  for n in roots[50]['viewgroup_items'][1:][78:96]:
   x=(n.get('position_padding_left',0)-n.get('position_padding_right',0))/2
   y=(n.get('position_padding_top',0)-n.get('position_padding_bottom',0))/2
   place(n,x,y+6)
  p['preset_info'].update(title='Rhine UI · 终端温度布局 v0.13.26'+(' · 无重力视差' if suffix else ''),description='首行和系统标签下移、温度数字缩小，去掉温度旁无意义的加号及资源装饰；保留右侧延伸与传感器视差。')
  target=OUT/f'Rhine-UI-terminal-balance{suffix}-v0.13.26.klwp'
  with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as dest:
   for name in src.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else src.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
  print(target)
