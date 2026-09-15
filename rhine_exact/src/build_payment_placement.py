"""Match the filler tone and asymmetric payment watermark placement."""
from pathlib import Path
import json,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/terminal-balance-v0.13.26';OUT=BASE/'output/payment-placement-v0.13.27';OUT.mkdir(exist_ok=True)
SCAN_FRAME='M 24 4 L 4 4 L 4 24 M 76 4 L 96 4 L 96 24 M 4 76 L 4 96 L 24 96 M 76 96 L 96 96 L 96 76'
for suffix in ['', '-off']:
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-terminal-balance{suffix}-v0.13.26.klwp') as src:
  p=json.loads(src.read('preset.json'));r=p['preset_root']['viewgroup_items']
  filler=r[7]['viewgroup_items'];filler[2]['viewgroup_items'][0]['paint_color']='#80000000'
  r[7]['viewgroup_items']=filler[:3]
  for index in [6,8]:
   mark=r[index]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items'][0]['viewgroup_items'][4]
   mark.update(position_padding_left=0,position_padding_right=88,position_padding_top=0,position_padding_bottom=0)
   shape=mark['viewgroup_items'][0];shape['paint_color']='#38E4FBFF'
   if index==8:
    shape.update(shape_path=SCAN_FRAME,shape_width=77,shape_height=73,paint_stroke=4)
    mark['internal_title']='扫描框 · 左侧背景水印'
   else:mark['internal_title']='付款卡条码 · 左侧背景水印'
  p['preset_info'].update(title='Rhine UI · 支付水印位置 v0.13.27'+(' · 无重力视差' if suffix else ''),description='第二行末尾恢复中性半透明黑灰填充；蓝色右侧两入口水印左置，扫一扫只保留四角扫描框。')
  target=OUT/f'Rhine-UI-payment-placement{suffix}-v0.13.27.klwp'
  with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as dest:
   for name in src.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else src.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
  print(target)
