"""Independent sculpted terminal buttons and complete semantic hit coverage."""
from pathlib import Path
import copy,json,zipfile
from build_calendar_weather import formula,rect,path,label,group,at,hit,switch,S
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/calendar-weather-v0.13.0'
VERSION='0.13.3';OUT=BASE/f'output/calendar-weather-v{VERSION}';OUT.mkdir(exist_ok=True)
SERIF='kfile://org.kustom.provider/fonts/SourceHanSerifSC-Heavy.otf'

def native(action):return [{'type':'SINGLE_TAP','action':'LAUNCH_ACTIVITY','intent':'intent:#Intent;action='+action+';end'}]

def plane(template,title,children):
 n=copy.deepcopy(template);n['internal_title']=title;n['viewgroup_items']=[rect(720,1600,'#00000000'),*children];n['internal_animations']=[a for a in n['internal_animations'] if a.get('type')=='GYRO' or 'gv(page)' in a.get('formula','')];return n

def press(n,key,center,g,reference):
 for zone,source in enumerate([a for a in reference['internal_animations'] if a.get('formula','').startswith('$gv(ps')]):
  name=f'{key}{zone}';g[name]={'index':len(g),'type':'TEXT','title':f'独立按压 {key} {zone}','value':'0'}
  a=copy.deepcopy(source);a['formula']=f'$gv({name})=1$';cx,cy=center;dx=zone%3-1;dy=zone//3-1
  for frame in a['animator']:
   amount={0:0,22:.7,40:1,50:1,60:1,78:.7,100:0}[frame['position']]
   if frame['property']=='X_OFFSET':frame['value']=(cx*1.3*.94*.033+dx*2.2)*amount
   if frame['property']=='Y_OFFSET':frame['value']=(cy*1.3*.94*.033+dy*1.5)*amount
  n['internal_animations'].append(a)

def tile(template,name,w,h,x,y,fill,icon):
 children=[at(rect(w+3,h+3,'#75000F19'),2,4),rect(w,h,fill),at(path(w*.66,h*.72,icon,'#283CE0F0',0),w*.18,-h*.03),at(rect(w-2,1.2,'#8668E2F5'),0,-h/2+1),at(rect(1.1,h-2,'#6744D6ED'),-w/2+1,0),at(rect(2,h,'#AF0B597B'),w/2-1,0),at(rect(w,2,'#BB065F82'),0,h/2-1)]
 # Both lower buttons share a text baseline; the tall left tile aligns to them.
 baseline=22 if h>100 else 1
 children.append(at(label(name,34,w-18,'#FFF5FBFD','LEFT',SERIF),2,baseline))
 return plane(template,'蓝色独立按钮 · '+name,[at(group(children),x,y)])

for suffix in ['', '-off']:
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-calendar-weather{suffix}-v0.13.0.klwp') as source:
  p=json.loads(source.read('preset.json'));r=p['preset_root']['viewgroup_items'];g=p['preset_root']['globals_list'];template=copy.deepcopy(r[14]);reference=copy.deepcopy(r[10])
  for index in [6,7,8,9]:r[5]['viewgroup_items'].extend(copy.deepcopy(r[index]['viewgroup_items'][1:]));r[index]['viewgroup_items']=[]
  main=copy.deepcopy(r[5]);main['internal_title']='终端 · 设备及电池信息';press(main,'pm',(0,-130),g,reference);r[5]=main
  icons=['M 5 8 L 95 8 L 95 92 L 5 92 Z M 15 30 L 85 30 L 85 70 L 15 70 Z','M 4 3 L 32 3 L 32 32 L 4 32 Z M 68 3 L 96 3 L 96 32 L 68 32 Z M 4 68 L 32 68 L 32 97 L 4 97 Z M 47 40 L 67 40 L 67 60 L 47 60 Z M 76 70 L 96 70 L 96 97 L 76 97 Z','M 0 0 L 34 0 L 34 8 L 8 8 L 8 34 L 0 34 Z M 66 0 L 100 0 L 100 34 L 92 34 L 92 8 L 66 8 Z M 0 66 L 8 66 L 8 92 L 34 92 L 34 100 L 0 100 Z M 92 66 L 100 66 L 100 100 L 66 100 L 66 92 L 92 92 Z M 12 46 L 88 46 L 88 54 L 12 54 Z']
  for slot,key,name,w,h,x,y,color,icon in [(14,'bl','支付宝',166,124,-197,118,'#FF129FC9',icons[0]),(6,'bc','付款码',180,82,-10,139,'#FF129DC9',icons[1]),(8,'br','扫一扫',186,82,187,139,'#FF1498C4',icons[2])]:
   n=tile(template,name,w,h,x,y,color,icon);press(n,key,(x,y),g,reference);r[slot]=n
  header=group([at(rect(380,30,'#5A000A12'),2,4),rect(380,30,'#FF30373B'),at(rect(378,1,'#556FC8D4'),0,-14),at(label('快捷支付',20,331,'#FFE5ECED','LEFT'),11,0)])
  r[9]=plane(template,'快捷支付 · 深色标题栏',[at(header,90,73)])
  # Match the reference's restrained sizing, aligned baselines and complete glyph bounds.
  def walk(n):
   yield n
   for c in n.get('viewgroup_items',[]):yield from walk(c)
  for index in [10,11]:
   for n in walk(r[index]):
    if n.get('text_expression') in ['系统','主题']:n['text_size']=45;n['text_width']=240
  for index in [17,18,19]:
   for n in walk(r[index]):
    if n.get('text_expression') in ['电话','文件','微信']:n['text_size']=35;n['text_width']=max(n.get('text_width',128),128)
  for n in walk(r[4]):
   if n.get('text_expression')=='$df(yyyy/MM/dd hh:mm)$':n['text_expression']='$df(yyyy/MM/dd HH:mm)$'
  # Preserve each card's own texture and shadow while exposing wallpaper between faces.
  for index in [10,11,17,18,19]:
   holder=r[index]['viewgroup_items'][1]
   content=group(holder['viewgroup_items']);content['config_scale_value']=96
   holder['viewgroup_items']=[content]
  # Recalibrate independent hit rectangles so the new gutters do not join the buttons.
  # Existing nine-zone boundaries remain fixed; only their pressure targets change.
  holders=r[50]['viewgroup_items'][1:]
  for control,key in [(2,'bl'),(3,'bc'),(4,'br')]:
   for zone,n in enumerate(holders[control*9:(control+1)*9]):
    event=n['viewgroup_items'][0]['internal_events'][0];event.update(switch=f'{key}{zone}',switch_text=f'$1-gv({key}{zone})$')
  calibrated=[(315,709,228,96),(583,710,262,100),(264,837,136,104),(431,869,160,74),(628,879,178,78),(279,964,152,98),(466,984,174,108),(648,998,132,112)]
  rebuilt=[r[50]['viewgroup_items'][0]]
  for control,(x,y,w,h) in enumerate(calibrated):
   for zone in range(9):
    events=holders[control*9+zone]['viewgroup_items'][0]['internal_events']
    touch=rect(w/3/.94,h/3/.94,'#00000000');touch['internal_events']=copy.deepcopy(events)
    part=at(touch,(x+(zone%3-1)*w/3-360)/.94,(y+(zone//3-1)*h/3-800)/.94)
    formula(part,'config_visible','if(gv(page)=1,ALWAYS,REMOVE)');rebuilt.append(part)
  r[50]['viewgroup_items']=rebuilt
  # Cover meaningful header and device areas, keeping margins non-interactive.
  def screen_hit(x,y,w,h,events):hit(r[50],(x-360)/.94,(y-800)/.94,w/.94,h/.94,events,'gv(page)=1')
  calendar=[switch('origin','$si(screen)$'),switch('detail',0),switch('view',5)]
  for x,y,w,h,events in [(470,382,236,44,calendar),(307,402,48,34,native('android.intent.action.POWER_USAGE_SUMMARY')),(244,444,148,42,native('android.settings.DEVICE_INFO_SETTINGS')),(435,419,167,44,native('android.settings.APPLICATION_SETTINGS')),(636,394,168,44,native('android.settings.INTERNAL_STORAGE_SETTINGS')),(533,801,374,30,[{'type':'SINGLE_TAP','action':'OPEN_LINK','url':'$gv(alipay)$'}])]:screen_hit(x,y,w,h,events)
  for x,y,w,h,events in [(290,570,192,160,native('android.intent.action.POWER_USAGE_SUMMARY')),(554,563,330,174,native('android.settings.DEVICE_INFO_SETTINGS'))]:
   for row in range(3):
    for col in range(3):
     zone=row*3+col;screen_hit(x+(col-1)*w/3,y+(row-1)*h/3,w/3,h/3,[switch(f'pm{zone}',f'$1-gv(pm{zone})$'),*events])
  for key in list(g):
   if key.startswith('pb') and key[2:].isdigit():g.pop(key)
  for i,(key,value) in enumerate(g.items()):value['index']=i
  p['preset_info'].update(title=f'Rhine UI · 独立悬浮卡片与月历天气 v{VERSION}'+(' · 无重力视差' if suffix else ''),description='主菜单卡片之间保留真实露底间隙，蓝色三块及标题栏各自独立；收紧点击区域，保留按压、月历与天气节点。')
  target=OUT/f'Rhine-UI-refined{suffix}-v{VERSION}.klwp'
  with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as dest:
   for name in source.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else source.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
  print(target)
