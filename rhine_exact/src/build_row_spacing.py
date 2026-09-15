"""Tune row spacing against the supplied Arknights home screenshot."""
from pathlib import Path
import json,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/payment-placement-v0.13.27';OUT=BASE/'output/row-spacing-v0.13.28';OUT.mkdir(exist_ok=True)
S='mu(min,1,si(sheight)*720/si(swidth)/1600)'
SHIFTS={7:-4,10:-4,11:-4,6:-4,8:-4,9:-4,14:-4,17:-12,18:-12,19:-12}
def shift_holder(n,dy):
 y=(n.get('position_padding_top',0)-n.get('position_padding_bottom',0))/2+dy
 n.update(position_padding_top=max(0,2*y),position_padding_bottom=max(0,-2*y))
for suffix in ['', '-off']:
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-payment-placement{suffix}-v0.13.27.klwp') as src:
  p=json.loads(src.read('preset.json'));roots=p['preset_root']['viewgroup_items']
  for index,dy in SHIFTS.items():
   formulas=roots[index]['internal_formulas'];old=formulas['position_offset_y'].strip('$')
   formulas['position_offset_y']=f'$({old})+({dy})*{S}$'
  for index,n in enumerate(roots[50]['viewgroup_items'][1:]):
   dy=-4 if index<45 or index==77 else -12 if index<72 else 0
   if dy:shift_holder(n,dy)
  p['preset_info'].update(title='Rhine UI · 行间留白校准 v0.13.28'+(' · 无重力视差' if suffix else ''),description='依照用户方舟主页截图收紧首行下方与蓝色行下方留白，保留错位排布；点击区域随所在行同步。')
  target=OUT/f'Rhine-UI-row-spacing{suffix}-v0.13.28.klwp'
  with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as dest:
   for name in src.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else src.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
  print(target)
