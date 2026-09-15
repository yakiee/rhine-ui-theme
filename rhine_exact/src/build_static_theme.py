"""Editable static KLWP review edition; all data are reference fixtures."""
from pathlib import Path
from copy import deepcopy
import json,re,zipfile
from static_helpers import formula,walk,normalize_nested_positions
BASE=Path(__file__).resolve().parents[1]; WORK=BASE.parent
S='mu(min,1,si(sheight)*720/si(swidth)/1600)'
p=json.loads((BASE/'src/preset-revision-wip.json').read_text(encoding='utf8').replace('mu(min,si(rwidth)/720,si(rheight)/1600)',S))
r=p['preset_root']['viewgroup_items'];g=p['preset_root']['globals_list']
out=BASE/'output/static-v0.1';out.mkdir(parents=True,exist_ok=True)
assets={}
def asset(name,path):
 assets['bitmaps/'+name]=Path(path)
 return 'kfile://org.kustom.provider/bitmaps/'+name
def clear(n,k):
 for field in ['internal_formulas','internal_toggles','internal_globals']:n.get(field,{}).pop(k,None)
def text(group,index,value):
 n=r[group]['viewgroup_items'][index];clear(n,'text_expression');n['text_expression']=value

def switch(key,value):return {'type':'SINGLE_TAP','action':'SWITCH_GLOBAL','switch':key,'switch_text':str(value)}
def rect(w,h,color):return {'internal_type':'ShapeModule','position_anchor':'CENTER','shape_type':'RECT','shape_width':w,'shape_height':h,'paint_color':color}
def crop_reference(old,path,box,name):
 # Native KLWP clip mask crops only an image asset; all UI outside this component remains native.
 uri=asset(name,path);x,y,w,h=box
 mask=rect(w,h,'#FFFFFFFF');mask['fx_mask']='CLIP_NEXT'
 bitmap={'internal_type':'BitmapModule','position_anchor':'CENTER','bitmap_bitmap':uri,'bitmap_width':720,'bitmap_height':1600,'bitmap_scale_mode':'FIT_XY','position_offset_x':360-x-w/2,'position_offset_y':800-y-h/2}
 return {'internal_type':'OverlapLayerModule','internal_title':old.get('internal_title',name),'position_anchor':'CENTER','position_offset_x':old.get('position_offset_x',0),'position_offset_y':old.get('position_offset_y',0),'viewgroup_items':[mask,bitmap],'internal_events':old.get('internal_events',[])}
for n in walk(p['preset_root']):
 n.pop('internal_animations',None)
 # Format 17 is essential; older version flags migrate away these events and modern paint fields.
 events=n.get('internal_events',[])
 nav=[e for e in events if e.get('switch')=='page']
 if nav:n['internal_events']=[switch('detail',0),nav[-1]]
 else:n['internal_events']=[e for e in events if e.get('switch') not in ['start','prev','gyro','load'] and e.get('action')=='SWITCH_GLOBAL']
 n.pop('fx_shadow_distance',None)
 if n.get('internal_type')=='TextModule':
  n['text_size_type']='FIXED_WIDTH';n.setdefault('paint_color','#FF17191C')
for key,val in [('page','0'),('style','0'),('load','0'),('loading','0'),('gyro','0'),('dark','$if(gv(mode)=1,1,0)$'),('base','$dp(2024y10M1d0h0m0s)$'),('daydate','$dp(2024y10M5d)$')]:g[key]['value']=val
wall=asset('wall-reconstructed.png',BASE/'assets/static/wall-reconstructed.png')
g['wall'].update(value=wall,description='临时AI清理重建底图，非原版文件，可替换')
r[0]['bitmap_bitmap']=wall
formula(r[0],'bitmap_width','si(rwidth)');formula(r[0],'bitmap_height','si(rheight)')
r[0]['bitmap_scale_mode']='CENTER_CROP'
text(1,3,'11:43');text(1,4,'AM');text(1,5,'RHINE UI.KLWP')
text(3,1,'2024/10/05 11:43');text(3,2,'CPU 12%     RAM 36%     SD 51%')
text(4,2,'28');text(4,6,'Android 14');text(7,7,'')
# Static fixtures avoid requiring weather, calendar, media permissions for review.
text(10,42,'78')
for n in walk(r[10]):
 t=n.get('text_expression','')
 if 'EEEE' in t:n['text_expression']='SATURDAY'
 elif 'yyyy' in t:n['text_expression']='2024.10.5'
 n.get('internal_formulas',{}).update({k:v.replace('bi(level)','78') for k,v in n.get('internal_formulas',{}).items()})
r[10]['config_rotate_mode']='MANUAL';formula(r[10],'config_rotate_offset','if(gv(page)=2,0,22.02)')
formula(r[10],'position_offset_y','(if(gv(page)=2,688,603)-if(gv(avoid),90,0))*'+S)
# Exact reference icon imagery is clipped within individual editable bitmap components.
appref=BASE/'analysis/frames/f_000019/065.png'
for index in range(8):
 old=r[8]['viewgroup_items'][index+1];x=58+(index%4)*166;y=968+(index//4)*194
 r[8]['viewgroup_items'][index+1]=crop_reference(old,appref,(x,y,110,110),'reference-apps.png')
# Set functional page wash to retain a faint impression of the background.
r[11]['viewgroup_items'][1].update(shape_width=900,shape_height=1800)
formula(r[11]['viewgroup_items'][1],'paint_color','if(gv(dark),#F014161B,#EDF4F3F6)')
r[11]['viewgroup_items']=r[11]['viewgroup_items'][:3]
# Forecast uses editable labels, node geometry and connection lines, with a replaceable scene.
text(13,3,'2024/10/05')
for j,value in [(6,'23/19°'),(7,'10/06'),(10,'22/17°'),(11,'10/07'),(14,'23/16°'),(15,'10/08'),(18,'24/18°'),(19,'10/09'),(21,'24/21°'),(22,'10/10'),(30,'')]:text(13,j,value)
# Preserve source node positions rather than live weather-dependent vertical movement.
for n in walk(r[13]):
 for key,value in list(n.get('internal_formulas',{}).items()):
  if any(token in value for token in ['wf(','wi(']):
   clear(n,key)
# Rebuild the reference three-node forecast card from native components.
import math
scene=asset('scene-reconstructed.png',BASE/'assets/static/scene-reconstructed.png')
g['scene'].update(value=scene,description='参考画面AI清理重建的临时城市图片，可替换')
def at(n,x,y):n.update(position_offset_x=x-360,position_offset_y=y-800);return n
def label(value,x,y,w,size,color='#FF17191C'):
 return at({'internal_type':'TextModule','text_expression':value,'text_width':w,'text_size':size,'text_size_type':'FIXED_WIDTH','text_align':'CENTER','text_lines':1,'paint_color':color,'position_anchor':'CENTER'},x,y)
def line(x1,y1,x2,y2):
 n=rect(math.hypot(x2-x1,y2-y1),3,'#FFFFFFFF');n.update(shape_rotate_mode='MANUAL',shape_rotate_offset=math.degrees(math.atan2(y2-y1,x2-x1)));return at(n,(x1+x2)/2,(y1+y2)/2)
card=r[13];card['viewgroup_items']=[rect(720,1600,'#00000000')]
card['viewgroup_items'].append(at({'internal_type':'BitmapModule','bitmap_bitmap':scene,'bitmap_width':612,'bitmap_height':403,'bitmap_scale_mode':'CENTER_CROP','position_anchor':'CENTER'},360,403.5))
positions=[(91,414),(294,535),(499,535)]
for first,second in zip(positions,positions[1:]):card['viewgroup_items'].append(line(*first,*second))
for index,((x,y),value) in enumerate(zip(positions,['23/19°','22/17°','23/16°'])):
 box=at(rect(148,37,'#FFF8F8F8'),x+72,y);box['internal_events']=[switch('selected',index),switch('detail',1)]
 dot=at({'internal_type':'ShapeModule','shape_type':'CIRCLE','shape_width':43,'paint_color':'#FF31BBEF','position_anchor':'CENTER'},x,y)
 card['viewgroup_items'] += [box,dot,label('◇',x,y,40,31,'#FFFFFFFF'),label(value,x+77,y,124,27),label('2024/10/0'+str(index+6),x+63,y-27,133,13,'#FFFFFFFF')]
for x,value in [(50,'‹'),(670,'›')]:card['viewgroup_items'].append(label(value,x,421,38,45,'#FFFFFFFF'))
card['viewgroup_items'].append(label('▣ ▣ ▣ ▣ ▣',360,645,190,25))

# Music artwork remains an individual image crop from the supplied reference, not a screenshot page.
r[17]['viewgroup_items'][1]=crop_reference(r[17]['viewgroup_items'][1],BASE/'analysis/frames/f_00001c/070.png',(56,228,608,398),'reference-music.png')
text(17,2,'青春コンプレックス');text(17,3,'結束バンド')
text(18,1,'憂った風が似合うから');text(18,2,'')
text(19,1,'00:31 / 03:25')
for n in walk(r[19]):
 for key,value in list(n.get('internal_formulas',{}).items()):
  if 'mi(' in value:clear(n,key)
for j,value in [(2,'空气指数 26'),(15,'13'),(17,'8'),(19,'5'),(21,'13'),(22,'μg/m³')]:text(14,j,value)
for j,value in [(3,''),(4,'21'),(5,'°C'),(6,'24 / 21°C'),(7,'气压 1016.3   体感 22°C'),(8,'湿度 80%'),(10,'')]:text(15,j,value)
for j,value in [(2,'10/06 SUN'),(4,'多云'),(5,'23° / 19°'),(6,'降水概率 10%'),(7,'风速 7 km/h'),(8,'东北风'),(9,'点击收起')]:text(16,j,value)
# Calendar is the same October review state as the initial reference.
text(20,1,'OCTOBER')
for index in range(42):
 nodes=r[20]['viewgroup_items'];date=index-1;valid=1<=date<=31
 for off in range(4):
  n=nodes[11+4*index+off]
  if n['internal_type']=='TextModule':n['text_expression']=str(date) if valid else ''
  for key in list(n.get('internal_formulas',{})):
   if key=='paint_color':
    clear(n,key);n[key]='#FF17191C' if n['internal_type']=='TextModule' else '#1F777777'
   elif key=='config_visible':
    clear(n,key);n[key]='ALWAYS' if valid and date in [4,5,11,12] else 'REMOVE'
  n['internal_events']=[]
text(21,3,'10/5');text(21,4,'2024年已经过76%');text(21,7,'87天')
for n in walk(r[21]):
 for key,value in list(n.get('internal_formulas',{}).items()):
  if 'df(' in value:clear(n,key)
text(22,4,'暂无日程安排');text(22,5,'')
text(23,39,'静态预览中保持关闭');text(24,44,'静态预览中保持关闭')
# Include loading as a selectable static review page, never an automatic transition.
formula(r[25],'config_visible','if(gv(page)=8,ALWAYS,REMOVE)');text(25,17,'100 %');text(25,19,'点击返回')
for n in walk(r[25]):
 if n.get('internal_events'):n['internal_events']=[switch('page',0)]
r.pop(26)
# Static review entry and consistent state-specific fixture details.
r[2]['viewgroup_items'][1].update(shape_width=900,shape_height=1800)
text(23,45,'静态预览')
r[23]['viewgroup_items'][45]['internal_events']=[switch('page',8)]
text(16,2,'$if(gv(selected)=0,"10/06 SUN",gv(selected)=1,"10/07 MON","10/08 TUE")$')
text(16,5,'$if(gv(selected)=0,"23° / 19°",gv(selected)=1,"22° / 17°","23° / 16°")$')
for n in walk(r[19]):
 if n.get('bitmap_bitmap','').endswith('/icon-play.png'):
  n['bitmap_bitmap']=n['bitmap_bitmap'].replace('icon-play.png','icon-pause.png')

# Preserve the visible loading emblem as a small reference image component.
loader=r[25];loader['internal_title']='25 加载静态预览'
loader['viewgroup_items']=[rect(720,1600,'#00000000'),{'internal_type':'BitmapModule','bitmap_bitmap':wall,'bitmap_width':900,'bitmap_height':2000,'bitmap_scale_mode':'CENTER_CROP','bitmap_blur':40,'position_anchor':'CENTER'},rect(900,2000,'#80737748')]
logo_old={'internal_title':'参考加载标志','position_offset_x':0,'position_offset_y':40}
loader['viewgroup_items'].append(crop_reference(logo_old,BASE/'analysis/frames/f_00001a/035.png',(290,775,150,145),'reference-loading.png'))
loader['viewgroup_items'] += [label('SYSTEM INITIALIZATION',487,357,260,14,'#CCFFFFFF'),label('RHINE LAB / TERMINAL',480,385,260,14,'#CCFFFFFF'),label('START PROCESSING',360,982,390,20,'#CCFFFFFF'),label('LOADING INTERFACE',199,1160,290,16,'#CCFFFFFF'),label('点击返回',360,1450,240,24,'#FFFFFFFF')]
loader['internal_events']=[switch('page',0)]

# Generous invisible click targets improve the thin reference back line's usability.
back=rect(150,90,'#00000000');back.update(internal_title='返回首页',position_offset_x=-234,position_offset_y=-625,internal_events=[switch('page',0)])
r[12]['viewgroup_items'].append(back)
for root in r:normalize_nested_positions(root)
p['preset_info'].update(title='Rhine UI · 静态主题 v0.1',description='可编辑静态布局复刻，参考固定演示数据。8个主页面与天气详情、加载静态页。无动画。人物底图为AI清理重建，封面和应用图标为参考素材裁切，字体与细节尚非一比一。',version=17,release=382621115,locked=False,width=720,height=1600,xscreens=1,yscreens=1,features='')
# All asset URIs in globals and modules are bundled.
serialized=json.dumps(p,ensure_ascii=False)
for name in set(re.findall(r'kfile://org\.kustom\.provider/(bitmaps/[^"\s]+|fonts/[^"\s]+)',serialized)):
 if name not in assets:
  path=WORK/'rhine_theme/assets'/Path(name).name
  if path.is_file():assets[name]=path
# Obsolete bitmap fallback is not used as the wallpaper but must not bundle the old generated wallpaper.
for n in walk(p['preset_root']):
 if n.get('bitmap_bitmap','').endswith('/wallpaper.png'):n['bitmap_bitmap']=wall
assets.pop('bitmaps/wallpaper.png',None)
(out/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
with zipfile.ZipFile(out/'Rhine-UI-static-v0.1.klwp','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('preset.json',json.dumps(p,ensure_ascii=False))
 for name,path in assets.items():z.write(path,name)
 z.write(WORK/'rhine_theme/docs/Rajdhani-OFL.txt','licenses/OFL.txt')
print(json.dumps({'package':str(out/'Rhine-UI-static-v0.1.klwp'),'roots':len(r),'animated_nodes':sum(bool(n.get('internal_animations')) for n in walk(p['preset_root'])),'asset_count':len(assets)},ensure_ascii=True))
