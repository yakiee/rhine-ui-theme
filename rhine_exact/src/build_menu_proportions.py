"""Match the reference's connected large/small cards, trailing filler and title proportions."""
from pathlib import Path
import copy,json,re,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/status-strip-v0.13.8';VERSION='0.13.9'
OUT=BASE/f'output/menu-proportions-v{VERSION}';OUT.mkdir(exist_ok=True)
def walk(n):
 yield n
 for c in n.get('viewgroup_items',[]):yield from walk(c)
def rect(w,h,c):return {'internal_type':'ShapeModule','position_anchor':'CENTER','shape_type':'RECT','shape_width':w,'shape_height':h,'paint_color':c}
def at(n,x,y):return {'internal_type':'OverlapLayerModule','position_anchor':'CENTER','position_padding_left':max(0,x*2),'position_padding_right':max(0,-x*2),'position_padding_top':max(0,y*2),'position_padding_bottom':max(0,-y*2),'viewgroup_items':[n]}
def shift(root,dx):
 for holder in root['viewgroup_items'][1:]:
  x=(holder.get('position_padding_left',0)-holder.get('position_padding_right',0))/2+dx
  holder['position_padding_left']=max(0,x*2);holder['position_padding_right']=max(0,-x*2)
 for a in root.get('internal_animations',[]):
  if not re.fullmatch(r'\$gv\((?:pt|pf|pw)\d\)=1\$',a.get('formula','')):continue
  for k in a['animator']:
   if k['property']=='X_OFFSET':k['value']+=dx*1.3*.94*.033*.42*{0:0,22:.7,40:1,50:1,60:1,78:.7,100:0}[k['position']]
def resize_face(root,delta,minimum):
 for n in walk(root['viewgroup_items'][1]):
  if n.get('internal_type')=='ShapeModule' and n.get('shape_width',0)>minimum and n.get('shape_height',0)>85:n['shape_width']+=delta

def recalibrate(root,control,x,y,w,h):
 for zone in range(9):
  old=root['viewgroup_items'][1+control*9+zone];events=copy.deepcopy(old['viewgroup_items'][0]['internal_events'])
  shape=rect(w/3/.94,h/3/.94,'#00000000');shape['internal_events']=events
  part=at(shape,(x+(zone%3-1)*w/3-360)/.94,(y+(zone//3-1)*h/3-800)/.94)
  part['internal_toggles']={'config_visible':10};part['internal_formulas']={'config_visible':'$if(gv(page)=1,ALWAYS,REMOVE)$'}
  root['viewgroup_items'][1+control*9+zone]=part

for suffix in ['', '-off']:
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-status{suffix}-v0.13.8.klwp') as source:
  p=json.loads(source.read('preset.json'));r=p['preset_root']['viewgroup_items']
  for n in walk(r[5]):
   if n.get('internal_type')=='TextModule':
    if n.get('text_expression')=='终端':n['text_size']=59;n['text_width']=224
    if n.get('text_expression')=='[i]$bi(tempc)$[/i]':n['text_size']=94;n['text_width']=184
    if n.get('text_expression')=='Android $si(aver)$':n['text_size']=22.5
   if n.get('shape_type')=='RECT' and n.get('paint_color') in ['#FF1D2029','#FF333940']:n['shape_corners']=6 if n['shape_height']>20 else 3
  # Keep the pair's outer edges fixed, with the second card larger and the third narrower.
  shift(r[18],21.28);resize_face(r[18],46.26087,150)
  shift(r[19],15.74);resize_face(r[19],-34.21739,130)
  for n in walk(r[18]):
   if n.get('text_expression')=='文件':n['text_width']=218
  for n in walk(r[19]):
   if n.get('text_expression')=='微信':n['text_width']=96;n['text_size']=33
  # Shorten the second white card to reveal the non-interactive trailing square.
  shift(r[11],-14);resize_face(r[11],-28/.97,250)
  for n in walk(r[11]):
   if n.get('internal_type')=='TextModule':n['text_width']=210
  filler=copy.deepcopy(r[11]);filler['internal_title']='第二行 · 灰色装饰方块（无点击）'
  filler['internal_animations']=[a for a in filler.get('internal_animations',[]) if a.get('type')=='GYRO' or 'gv(page)' in a.get('formula','')]
  filler['viewgroup_items']=[rect(720,1600,'#00000000'),at(rect(112,112.64,'#08000000'),273.6,-12),at(rect(108,108.64,'#70757C82'),272.6,-15)]
  for yy in [-39,-16,7]:filler['viewgroup_items'].append(at(rect(55,10,'#20656B70'),270,yy))
  r[7]=filler
  recalibrate(r[50],1,532,678,234,96)
  recalibrate(r[50],6,480,953,210,102)
  recalibrate(r[50],7,647,970,98,106)
  p['preset_info'].update(title=f'Rhine UI · 卡片比例与圆角标签 v{VERSION}'+(' · 无重力视差' if suffix else ''),description='底排文件/微信改为相接的一大一小；第二行加入无点击灰色填充方块；加大终端标题和数字，黑色信息标签使用圆角。')
  target=OUT/f'Rhine-UI-proportions{suffix}-v{VERSION}.klwp'
  with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as dest:
   for name in source.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else source.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
  print(target)
