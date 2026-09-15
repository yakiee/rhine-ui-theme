"""Match terminal paper, blue and charcoal surfaces to the supplied game reference."""
from pathlib import Path
import json,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/battery-clarity-v0.13.38';OUT=BASE/'output/reference-palette-v0.13.39';OUT.mkdir(exist_ok=True)
PAPER='#F7FAFAFA';BLUE='#FF4EA4D2';CHARCOAL='#F7444444';HEADER='#FF373737'
for suffix in ('','-off'):
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-battery-clarity{suffix}-v0.13.38.klwp') as source:
  p=json.loads(source.read('preset.json'));r=p['preset_root']['viewgroup_items']
  r[5]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items'][3]['viewgroup_items'][0]['paint_color']=PAPER
  for index in (10,11,17,18):r[index]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items'][3]['paint_color']=PAPER
  for index in (6,8,14):r[index]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items'][0]['viewgroup_items'][3]['paint_color']=BLUE
  header=r[9]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items'][0]['viewgroup_items'];header[0]['paint_color']=BLUE;header[1]['paint_color']=HEADER
  r[19]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items'][3]['paint_color']=CHARCOAL
  r[7]['viewgroup_items'][2]['viewgroup_items'][0]['paint_color']='#88525252'
  terminal=r[5]['viewgroup_items']
  terminal[3]['viewgroup_items'][0]['viewgroup_items'][0]['paint_color']='#FFB8B8B8'
  terminal[6]['viewgroup_items'][0]['viewgroup_items'][0]['paint_color']=HEADER
  terminal[10]['viewgroup_items'][0]['viewgroup_items'][0]['paint_color']='#FF333333'
  terminal[4]['viewgroup_items'][0]['viewgroup_items'][3]['viewgroup_items'][0]['paint_color']='#DE292929'
  p['preset_info'].update(title='Rhine UI · 方舟参考底色 v0.13.39'+(' · 无重力视差' if suffix else ''),description='按用户方舟主页截图取色，白色纸面提亮、支付行改浅天蓝、标题栏与微信改中性炭灰；保留纸面透明感及连续细分界。')
  with zipfile.ZipFile(OUT/f'Rhine-UI-reference-palette{suffix}-v0.13.39.klwp','w',zipfile.ZIP_DEFLATED) as dest:
   for name in source.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else source.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
 print(suffix or 'normal','built')
