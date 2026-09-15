"""Connected button faces with independent interaction and staggered row extents."""
from pathlib import Path
import copy,json,zipfile,re
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/calendar-weather-v0.13.2'
VERSION='0.13.4';OUT=BASE/f'output/calendar-weather-v{VERSION}';OUT.mkdir(exist_ok=True)

def group(children):return {'internal_type':'OverlapLayerModule','position_anchor':'CENTER','viewgroup_items':children}
def formula(n,k,v):n.setdefault('internal_toggles',{})[k]=10;n.setdefault('internal_formulas',{})[k]='$'+v.strip('$')+'$'
def place(n,x,y):
 n.update(position_padding_left=max(0,x*2),position_padding_right=max(0,-x*2),position_padding_top=max(0,y*2),position_padding_bottom=max(0,-y*2))

ROWS={
 'device':{'roots':[5],'scale':.96,'shift':-14,'cy':-166,'screen_y':558},
 'system':{'roots':[10,11],'scale':.97,'shift':-34,'cy':-15,'screen_y':710},
 'payment':{'roots':[6,8,9,14],'scale':.88,'shift':16,'cy':118,'screen_y':859},
 'tools':{'roots':[17,18,19],'scale':.92,'shift':-8,'cy':255,'screen_y':984},
}
CENTERS={5:(0,-130),10:(-143,-15),11:(143,-15),6:(-8,136.3783),8:(184,136.3783),14:(-192,118),17:(-182,255),18:(26,255),19:(208,255)}

def transform_row(root,index,row):
 scale=row['scale'];shift=row['shift'];cy=row['cy']
 for holder in root['viewgroup_items'][1:]:
  x=(holder.get('position_padding_left',0)-holder.get('position_padding_right',0))/2
  y=(holder.get('position_padding_top',0)-holder.get('position_padding_bottom',0))/2
  content=group(holder['viewgroup_items']);content['config_scale_value']=100*scale
  holder['viewgroup_items']=[content];place(holder,x*scale+shift,cy+(y-cy)*scale)
 if index in CENTERS:
  x,y=CENTERS[index];delta_x=x*(scale-1)+shift;delta_y=(y-cy)*(scale-1)
  for animation in root.get('internal_animations',[]):
   if not re.fullmatch(r'\$gv\((?:pm|ps|pt|pp|pf|pw|bl|bc|br)\d\)=1\$',animation.get('formula','')):continue
   for key in animation.get('animator',[]):
    amount={0:0,22:.7,40:1,50:1,60:1,78:.7,100:0}[key['position']]
    if key['property']=='X_OFFSET':key['value']+=delta_x*1.3*.94*.033*amount
    if key['property']=='Y_OFFSET':key['value']+=delta_y*1.3*.94*.033*amount

# Screen-aligned touch proxies follow each row without inheriting its perspective transform.
def transform_hit(holder,row):
 scale=row['scale'];x=(holder.get('position_padding_left',0)-holder.get('position_padding_right',0))/2*.94+360
 y=(holder.get('position_padding_top',0)-holder.get('position_padding_bottom',0))/2*.94+800
 x=439+(x-439)*scale+row['shift']*1.02
 y=row['screen_y']+(y-row['screen_y'])*scale
 place(holder,(x-360)/.94,(y-800)/.94)
 shape=holder['viewgroup_items'][0];shape['shape_width']*=scale;shape['shape_height']*=scale

for suffix in ['', '-off']:
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-refined{suffix}-v0.13.2.klwp') as source:
  p=json.loads(source.read('preset.json'));r=p['preset_root']['viewgroup_items']
  for row in ROWS.values():
   for index in row['roots']:transform_row(r[index],index,row)
  holders=r[50]['viewgroup_items'][1:]
  for control,rowname in enumerate(['system','system','payment','payment','payment','tools','tools','tools']):
   for h in holders[control*9:(control+1)*9]:transform_hit(h,ROWS[rowname])
  transform_hit(holders[77],ROWS['payment'])
  for h in holders[78:]:transform_hit(h,ROWS['device'])
  p['preset_info'].update(title=f'Rhine UI · 连续按钮与错落排布 v{VERSION}'+(' · 无重力视差' if suffix else ''),description='恢复蓝色区连贯表面与明暗分隔，三个按钮独立点击；终端、白色功能行、支付行及底排采用不同起止位置。')
  target=OUT/f'Rhine-UI-staggered{suffix}-v{VERSION}.klwp'
  with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as dest:
   for name in source.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else source.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
  print(target)
