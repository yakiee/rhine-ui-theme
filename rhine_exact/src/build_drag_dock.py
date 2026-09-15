"""Drive Dock folding directly with launcher wallpaper offsets, with no timer."""
from pathlib import Path
import copy,json,zipfile,math
BASE=Path(__file__).resolve().parents[1];SRC=BASE/'output/desktop-dock-fold-v0.13.47';OUT=BASE/'output/drag-dock-v0.13.50';OUT.mkdir(exist_ok=True)
def scroll(frames):
 return dict(type='SCROLL',action='ADVANCED',rule='CENTER',center='SCREEN2',speed=100,amount=100,anchor='MODULE_CENTER',ease='STRAIGHT',animator=frames,internal_toggles={'center':10},internal_formulas={'center':'$"SCREEN"+gv(homepg)$'})
def key(p,prop,v):return dict(position=p,property=prop,value=v,ease='STRAIGHT')
for suffix in ('','-off'):
 with zipfile.ZipFile(SRC/f'Rhine-UI-desktop-dock-fold{suffix}-v0.13.47.klwp') as src:
  p=json.loads(src.read('preset.json'));r=p['preset_root']['viewgroup_items']
  base_x=math.sin(math.radians(23.7))*139;base_y=633-math.cos(math.radians(23.7))*139
  plate=[];glow=[]
  for step in range(101):
   t=step/100;angle=23.7*(1-t);lower=145*t;sy=1+(80/130-1)*t;distance=114+25*sy
   plate.extend([key(step,'ROTATE',-23.7*t),key(step,'Y_OFFSET',lower)])
   for prop,value in dict(ROTATE=angle,X_OFFSET=math.sin(math.radians(angle))*distance-base_x,Y_OFFSET=633+lower-math.cos(math.radians(angle))*distance-base_y,SCALE_X=1+(768/1060-1)*t,SCALE_Y=sy).items():glow.append(key(step,prop,value))
  for index,frames in [(23,plate),(24,glow)]:
   animations=r[index]['internal_animations'];result=[]
   for a in animations:
    f=a.get('formula','')
    if f=='$(gv(page)=2 | gv(page)=-1)$':result.append(scroll(frames))
    elif f=='$gv(page)=1 | (gv(page)=2 | gv(page)=-1)$':
     b=copy.deepcopy(a);b['formula']='$gv(page)=1$';result.append(b)
    else:result.append(a)
   assert any(a['type']=='SCROLL' for a in result)
   r[index]['internal_animations']=result
  # Text uses the same transform but fades early as the finger leaves home.
  text_layer=copy.deepcopy(r[23]);text_layer['internal_title']='Dock 信息 · 跟随拖动淡出'
  for shape in text_layer['viewgroup_items'][:3]:
   shape['paint_color']='#00000000';shape.get('internal_formulas',{}).pop('paint_color',None);shape.get('internal_toggles',{}).pop('paint_color',None)
  text_layer['viewgroup_items'][3]['internal_formulas']['config_visible']='$if(gv(page)<=0,ALWAYS,REMOVE)$'
  text_layer['internal_animations'].append(scroll([key(0,'OPACITY',0),key(40,'OPACITY',100),key(100,'OPACITY',100)]))
  r[1]=copy.deepcopy(r[23]);r[1]['internal_title']='Dock 底板 · 桌面滚动同步';r[1]['viewgroup_items'][3]['viewgroup_items']=[];r[23]=text_layer
  p['preset_info'].update(title='Rhine UI · 跟手斜条 v0.13.50'+(' · 无重力视差' if suffix else ''),description='斜条转角、下移、光带缩放直接跟随桌面滚动偏移。拖动停住即停、回拉即恢复，电量日期随拖动淡出。终端入口与返回逻辑保持。')
  with zipfile.ZipFile(OUT/f'Rhine-UI-drag-dock{suffix}-v0.13.50.klwp','w',zipfile.ZIP_DEFLATED) as dst:
   for name in src.namelist():dst.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else src.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
 print(suffix or 'normal','built')
