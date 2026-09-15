"""Balance top rules around the actual seconds clock and battery icon."""
from pathlib import Path
import json,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/row-spacing-v0.13.28';OUT=BASE/'output/status-seconds-v0.13.29';OUT.mkdir(exist_ok=True)
for suffix in ['', '-off']:
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-row-spacing{suffix}-v0.13.28.klwp') as src:
  p=json.loads(src.read('preset.json'));status=p['preset_root']['viewgroup_items'][4]['viewgroup_items']
  status[2].update(position_padding_left=0,position_padding_right=4)
  status[2]['viewgroup_items'][0].update(text_expression='$df(yyyy/MM/dd HH:mm:ss)$',text_width=218,text_align='LEFT')
  status[10].update(position_padding_left=0,position_padding_right=444)
  status[10]['viewgroup_items'][0]['shape_width']=84
  status[11].update(position_padding_left=356,position_padding_right=0)
  status[11]['viewgroup_items'][0]['shape_width']=128
  p['preset_info'].update(title='Rhine UI · 秒钟与顶部横线 v0.13.29'+(' · 无重力视差' if suffix else ''),description='真实时间显示到秒；收短左横线、拉近右横线，协调电池图标及时间文字间距。')
  target=OUT/f'Rhine-UI-status-seconds{suffix}-v0.13.29.klwp'
  with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as dest:
   for name in src.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else src.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
  print(target)
