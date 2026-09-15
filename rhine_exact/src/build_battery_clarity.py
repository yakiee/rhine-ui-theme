"""Give the four native battery cells clean, separated contours at small scale."""
from pathlib import Path
import json,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/payment-seams-v0.13.37';OUT=BASE/'output/battery-clarity-v0.13.38';OUT.mkdir(exist_ok=True)
def pos(n,x):n.update(position_padding_left=max(0,2*x),position_padding_right=max(0,-2*x))
for suffix in ('','-off'):
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-payment-seams{suffix}-v0.13.37.klwp') as source:
  p=json.loads(source.read('preset.json'));battery=p['preset_root']['viewgroup_items'][4]['viewgroup_items'][9];items=battery['viewgroup_items']
  battery['internal_title']='终端电量 · 清晰四格真实填充'
  pos(items[0],-1);items[0]['viewgroup_items'][0].update(shape_width=28,shape_height=16,paint_stroke=2)
  pos(items[1],14.5);items[1]['viewgroup_items'][0].update(shape_width=3,shape_height=6)
  for index,center in enumerate((-10,-4,2,8)):
   cell=items[index+2];pos(cell,center);cell['internal_title']=f'电量实心格 {index+1}'
   cell['viewgroup_items'][0].update(shape_width=4,shape_height=10,paint_color='#18FFFFFF')
   fill=cell['viewgroup_items'][1];fraction=f'mu(max,0,mu(min,1,4*mu(max,0,mu(min,100,bi(level)))/100-{index}))'
   fill['internal_formulas']['position_padding_right']=f'$4-(4*{fraction})$'
   shape=fill['viewgroup_items'][0];shape.update(shape_width=4,shape_height=10)
   shape['internal_formulas']['shape_width']=f'$mu(max,0.001,4*{fraction})$'
  p['preset_info'].update(title='Rhine UI · 电量内格清晰度 v0.13.38'+(' · 无重力视差' if suffix else ''),description='电量内格改为 4×10、间距 2，减少狭窄间隙经透视缩放后的粘连；空槽淡化，外框加清晰留白，仍按真实百分比连续填充。')
  with zipfile.ZipFile(OUT/f'Rhine-UI-battery-clarity{suffix}-v0.13.38.klwp','w',zipfile.ZIP_DEFLATED) as dest:
   for name in source.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else source.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
 print(suffix or 'normal','built')
