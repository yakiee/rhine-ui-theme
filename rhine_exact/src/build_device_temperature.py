from pathlib import Path
import json,zipfile
BASE=Path('rhine_exact');source=BASE/'output/music-button-v0.13.30';out=BASE/'output/device-temperature-v0.13.31';out.mkdir(exist_ok=True)
def at(n,x,y):return dict(internal_type='OverlapLayerModule',position_anchor='CENTER',position_padding_left=max(0,2*x),position_padding_right=max(0,-2*x),position_padding_top=max(0,2*y),position_padding_bottom=max(0,-2*y),viewgroup_items=[n])
def shape(w,h,color,kind='RECT'):return dict(internal_type='ShapeModule',position_anchor='CENTER',shape_type=kind,shape_width=w,shape_height=h,paint_color=color)
for suffix in ['', '-off']:
 with zipfile.ZipFile(source/f'Rhine-UI-music-button{suffix}-v0.13.30.klwp') as src:
  p=json.loads(src.read('preset.json'));t=p['preset_root']['viewgroup_items'][5]['viewgroup_items']
  t[5]['internal_title']='机温 · 装饰加号'
  t[5]['viewgroup_items']=[at(shape(32,32,'#FF272B2E','CIRCLE'),-266,-187),at(shape(15,1.5,'#FFFFFFFF'),-266,-187),at(shape(1.5,15,'#FFFFFFFF'),-266,-187)]
  t[11]['viewgroup_items'][0]['viewgroup_items'][0]['text_expression']='机温 / °C'
  p['preset_info'].update(title='Rhine UI · 机温标识 v0.13.31'+(' · 无重力视差' if suffix else ''),description='恢复温度数值旁装饰加号，标签改为机温 / °C；实际读数仍为电池温度。')
  with zipfile.ZipFile(out/f'Rhine-UI-device-temperature{suffix}-v0.13.31.klwp','w',zipfile.ZIP_DEFLATED) as dest:
   for name in src.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else src.read(name))
  if not suffix:(out/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
print(out)
