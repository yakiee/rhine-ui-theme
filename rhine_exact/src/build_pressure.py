"""Native direction-sensitive tap recoil; screen-aligned touch regions stay stationary."""
from pathlib import Path
import copy,json,zipfile
BASE=Path(__file__).resolve().parents[1]
SOURCE=BASE/'output/function-layout-v0.11.6'
OUT=BASE/'output/pressure-v0.12.0';OUT.mkdir(exist_ok=True)

def formula(node,key,value):
 node.setdefault('internal_toggles',{})[key]=10
 node.setdefault('internal_formulas',{})[key]='$'+value.strip('$')+'$'

def at(node,x,y):
 return {'internal_type':'OverlapLayerModule','position_anchor':'CENTER','position_padding_left':max(0,x*2),'position_padding_right':max(0,-x*2),'position_padding_top':max(0,y*2),'position_padding_bottom':max(0,-y*2),'viewgroup_items':[node]}

def rect(w,h,color='#00000000'):
 return {'internal_type':'ShapeModule','position_anchor':'CENTER','shape_type':'RECT','shape_width':w,'shape_height':h,'paint_color':color}

def zones(x,y,w,h,events,page,card,columns=None):
 result=[]
 for row in range(3):
  for col in range(3):
   zone=row*3+col if columns is None else row*3+columns
   key=f'p{card}{zone}'
   touch=rect(w/3,h/3)
   touch['internal_events']=[{'type':'SINGLE_TAP','action':'SWITCH_GLOBAL','switch':key,'switch_text':f'$1-gv({key})$'}]+copy.deepcopy(events)
   group=at(touch,x+(col-1)*w/3,y+(row-1)*h/3)
   formula(group,'config_visible',f'if(gv(page)={page},ALWAYS,REMOVE)')
   result.append(group)
 return result

def pressure(node,card,center,scale,globals_list):
 # A closed, symmetric pulse supports repeated taps without timers or delaying shortcuts.
 # Translation compensates scaling around the shared menu pivot.
 cx,cy=center
 for zone in range(9):
  key=f'p{card}{zone}'
  globals_list[key]={'index':len(globals_list),'type':'TEXT','title':f'按压 {card} · 方位 {zone+1}','value':'0'}
  dx=zone%3-1;dy=zone//3-1
  peak={'SCALE_XY':.967,'FLIP_Y':dx*1.8,'FLIP_X':-dy*1.4,'X_OFFSET':cx*scale*.033+dx*2.2,'Y_OFFSET':cy*scale*.033+dy*1.5,'OPACITY':4}
  animator=[]
  for position,amount in [(0,0),(22,.7),(40,1),(50,1),(60,1),(78,.7),(100,0)]:
   for prop,value in peak.items():
    neutral=1 if prop=='SCALE_XY' else 0
    animator.append({'position':position,'property':prop,'value':neutral+(value-neutral)*amount,'ease':'NORMAL'})
  node.setdefault('internal_animations',[]).append({'type':'FORMULA','formula':f'$gv({key})=1$','action':'ADVANCED','anchor':'MODULE_CENTER','duration':3.6,'delay':0,'ease':'STRAIGHT','animator':animator})

for suffix in ['', '-off']:
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-functions{suffix}-v0.11.6.klwp') as source:
  preset=json.loads(source.read('preset.json'));root=preset['preset_root'];items=root['viewgroup_items'];globals_list=root['globals_list']
  # Join plate, text and decoration before deformation so they cannot pull apart.
  for target,donors in [(10,[12]),(11,[13]),(14,[15,16]),(17,[20])]:
   for donor in donors:
    items[target]['viewgroup_items'].extend(copy.deepcopy(items[donor]['viewgroup_items'][1:]))
    items[donor]['viewgroup_items']=[]
  items[18]['viewgroup_items'].append(copy.deepcopy(items[21]['viewgroup_items'][1]))
  items[19]['viewgroup_items'].append(copy.deepcopy(items[21]['viewgroup_items'][2]))
  items[21]['viewgroup_items']=[]
  specs=[(10,'s',(-143,-15)),(11,'t',(143,-15)),(14,'b',(0,118)),(17,'p',(-182,255)),(18,'f',(26,255)),(19,'w',(208,255))]
  for index,card,center in specs:pressure(items[index],card,center,1.3*.94,globals_list)
  bounds=[(315,709,238,106,'s',None),(583,710,272,110,'t',None),(269,837,148,112,'b',0),(432,865,176,94,'b',1),(620,869,190,98,'b',2),(279,964,166,108,'p',None),(466,984,188,118,'f',None),(648,998,144,124,'w',None)]
  old=items[50]['viewgroup_items'][1:]
  items[50]['viewgroup_items']=items[50]['viewgroup_items'][:1]
  for (x,y,w,h,card,column),hit in zip(bounds,old):
   events=hit['viewgroup_items'][0]['internal_events']
   items[50]['viewgroup_items'].extend(zones((x-360)/.94,(y-800)/.94,w/.94,h/.94,events,1,card,column))
  # Reuse the emptied roots for application cards, keeping the native 64-root budget.
  app_template=copy.deepcopy(items[22]);app_tiles=app_template['viewgroup_items'][1:]
  items[22]['viewgroup_items']=[copy.deepcopy(app_template['viewgroup_items'][0])]
  for index,tile,slot in zip(range(8),app_tiles,[12,13,15,16,20,21,48,49]):
   card=f'a{index}';new=copy.deepcopy(app_template)
   new['internal_title']=tile['internal_title']+' · 方位按压'
   visual=copy.deepcopy(tile);events=visual['viewgroup_items'].pop()['viewgroup_items'][0]['internal_events']
   new['viewgroup_items']=[copy.deepcopy(app_template['viewgroup_items'][0]),visual]
   cx=(tile.get('position_padding_left',0)-tile.get('position_padding_right',0))/2
   cy=(tile.get('position_padding_top',0)-tile.get('position_padding_bottom',0))/2
   pressure(new,card,(cx,cy),.94,globals_list)
   items[slot]=new
   # Hits remain in the original page root, independent of each card's recoil.
   items[22]['viewgroup_items'].extend(zones(cx,cy,132,140,events,2,card))
  preset['preset_info'].update(title='Rhine UI · 方位按压 v0.12.0'+(' · 无重力视差' if suffix else ''),description='终端卡片和应用卡片按点击方位轻微内倾、缩小、复位；九宫格方向采样，保持原跳转。')
  target=OUT/f'Rhine-UI-pressure{suffix}-v0.12.0.klwp'
  with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as dest:
   for name in source.namelist():dest.writestr(name,json.dumps(preset,ensure_ascii=False) if name=='preset.json' else source.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(preset,ensure_ascii=False,indent=2),encoding='utf8')
  print(target)
