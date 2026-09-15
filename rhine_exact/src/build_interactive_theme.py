"""Add native KLWP motion to the validated static theme without modifying it."""
from pathlib import Path
from copy import deepcopy
import json,zipfile,re,argparse
from static_helpers import formula,walk
BASE=Path(__file__).resolve().parents[1]
SOURCE=BASE/'output/static-v0.1/Rhine-UI-static-v0.1.klwp'
parser=argparse.ArgumentParser()
parser.add_argument('--diagonal',action='store_true')
parser.add_argument('--perspective',action='store_true')
options=parser.parse_args()
edition='perspective-v0.4' if options.perspective else ('diagonal-v0.3' if options.diagonal else 'interactive-v0.2')
OUT=BASE/'output'/edition;OUT.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(SOURCE) as archive:p=json.loads(archive.read('preset.json'))
if options.diagonal or options.perspective:
 from refine_homepage import refine
 refine(p)
if options.perspective:
 from refine_menu import refine_menu
 refine_menu(p)
original=p['preset_root']['viewgroup_items'];g=p['preset_root']['globals_list']
S='mu(min,1,si(sheight)*720/si(swidth)/1600)'
def switch(name,value):return {'type':'SINGLE_TAP','action':'SWITCH_GLOBAL','switch':name,'switch_text':str(value)}
def global_text(name,value,title):g[name]={'index':len(g),'type':'TEXT','title':title,'value':str(value)}
for name,value,title in [('pulse',0,'点击反馈'),('tapx',0,'反馈横坐标'),('tapy',0,'反馈纵坐标'),('playing',1,'播放按钮演示状态'),('pick',5,'选中日期'),('prev',0,'前一页面')]:global_text(name,value,title)
g['page']['value']='0';g['load']['value']='1';g['loading']['value']='0'
g['mode']['value']='0';g['detail']['value']='0'
# Change only the interaction controls relevant to motion.
for root in original:
 for n in walk(root):
  text=n.get('text_expression','')
  if text=='静态预览中保持关闭' and root is original[23]:n['text_expression']='打开功能页时显示加载过渡；点击标题预览'
  if text=='静态预览':n['text_expression']='开启';n['internal_events']=[switch('load',1)]
  if text=='加载动画':n['internal_events']=[switch('page',8)]
  if text=='点击返回' and root is original[25]:n['text_expression']='点击返回'
# Restore the off control to its reference location (wrapped static nodes keep their geometry).
for n in walk(original[23]['viewgroup_items'][42]):
 if n.get('internal_type')=='TextModule':n['internal_events']=[switch('load',0)]
# Play/pause is a visual state interaction; no audio is claimed or started.
for n in walk(original[19]):
 if n.get('bitmap_bitmap','').endswith('/icon-pause.png'):
  formula(n,'bitmap_bitmap','if(gv(playing),"kfile://org.kustom.provider/bitmaps/icon-pause.png","kfile://org.kustom.provider/bitmaps/icon-play.png")')
  n['internal_events']=[switch('playing','$1-gv(playing)$')]
# Give each date a persistent native selection state as well as a click pulse.
cal=original[20]['viewgroup_items']
for index in range(42):
 day=index-1
 if not 1<=day<=31:continue
 for component in cal[11+index*4:13+index*4]:
  for n in walk(component):
   if n.get('internal_type') in ['TextModule','ShapeModule']:n['internal_events']=[switch('pick',day)]
 outline=cal[13+index*4];formula(outline,'config_visible','if(gv(pick)='+str(day)+',ALWAYS,REMOVE)')
 for n in walk(outline):
  if n.get('internal_type')=='ShapeModule' and n.get('paint_style')=='STROKE':formula(n,'paint_color','gv(accent)');n['internal_events']=[switch('pick',day)]
# Each touch receives its own center for feedback, with root-local padding converted to coordinates.
def wire_touches(n,root_index,x=0,y=0):
 x+=(n.get('position_padding_left',0)-n.get('position_padding_right',0))/2
 y+=(n.get('position_padding_top',0)-n.get('position_padding_bottom',0))/2
 events=n.get('internal_events',[])
 if events:
  navigation=[e for e in events if e.get('switch')=='page']
  if navigation:events=[switch('prev','$gv(page)$')]+[e for e in events if e.get('switch')!='prev']
  # Full-page backdrops and the loading page do not get an artificial center flash.
  if n.get('internal_type') in ['TextModule','BitmapModule','ShapeModule'] and (abs(x)+abs(y)>0 or root_index==8):
   yoff={8:318,10:603,21:-120,22:-96}.get(root_index,0)
   if root_index!=10 and not (options.perspective and 3<=root_index<=7):events += [switch('tapx',round(x,2)),switch('tapy',round(y+yoff,2)),switch('pulse','$1-gv(pulse)$')]
  n['internal_events']=events
 for child in n.get('viewgroup_items',[]):wire_touches(child,root_index,x,y)
for index,root in enumerate(original):wire_touches(root,index)

def frame(position,prop,value):return {'position':position,'property':prop,'value':value,'ease':'STRAIGHT'}
def motion(condition,duration=360,delay=0,properties=None,reverse=180,loading=False):
 tracks={'OPACITY':[(0,100),(35,0),(100,0)]};tracks.update(properties or {})
 frames=[frame(t,prop,v) for prop,values in tracks.items() for t,v in values]
 a={'type':'FORMULA','formula':'$'+condition+'$','action':'ADVANCED','anchor':'MODULE_CENTER','duration':duration/100,'delay':delay/100,'ease':'STRAIGHT','animator':sorted(frames,key=lambda f:(f['position'],f['property']))}
 formula(a,'duration','if('+condition+','+str(duration/100)+','+str(reverse/100)+')')
 extra='+if(gv(load)=1 & gv(prev)<=2,8,0)' if loading else ''
 formula(a,'delay','if('+condition+','+str(delay/100)+extra+',0)')
 return a

def clear(n,field):
 for key in ['internal_formulas','internal_toggles','internal_globals']:n.get(key,{}).pop(field,None)
def hide_paint(n):
 for field in ['paint_color','bitmap_alpha','fx_gradient','fx_shadow','fx_overlay','fx_mask']:
  clear(n,field)
 n['paint_color']='#00000000';n['bitmap_alpha']=0;n['fx_shadow']='NONE';n['fx_gradient']='NONE';n['fx_overlay']='NONE';n['fx_mask']='NONE'
 n.pop('internal_animations',None)
 for child in n.get('viewgroup_items',[]):hide_paint(child)
def touch_geometry(root):
 hit=deepcopy(root);hit.pop('internal_events',None);hit.pop('internal_animations',None);hit['viewgroup_items']=[]
 def collect(node,x=0,y=0,inherited=()):
  x+=(node.get('position_padding_left',0)-node.get('position_padding_right',0))/2
  y+=(node.get('position_padding_top',0)-node.get('position_padding_bottom',0))/2
  visible=node.get('internal_formulas',{}).get('config_visible')
  conditions=list(inherited)
  if visible:
   match=re.match(r'\$if\((.*),ALWAYS,REMOVE\)\$',visible)
   if match:conditions.append(match.group(1))
  elif node.get('config_visible')=='REMOVE':return
  events=node.get('internal_events')
  if events:
   width=node.get('shape_width',node.get('bitmap_width',node.get('text_width',720)))
   height=node.get('shape_height',node.get('bitmap_height',max(48,node.get('text_size',28)*1.6)))
   if node.get('internal_type')=='OverlapLayerModule':height=1600
   target={'internal_type':'ShapeModule','shape_type':'RECT','shape_width':max(width,44),'shape_height':max(height,44),'paint_color':'#00000000','position_anchor':'CENTER','internal_events':deepcopy(events)}
   wrapper={'internal_type':'OverlapLayerModule','position_anchor':'CENTER','position_padding_left':max(0,2*x),'position_padding_right':max(0,-2*x),'position_padding_top':max(0,2*y),'position_padding_bottom':max(0,-2*y),'viewgroup_items':[target]}
   if conditions:formula(wrapper,'config_visible','if('+ ' & '.join('('+c+')' for c in conditions)+',ALWAYS,REMOVE)')
   hit['viewgroup_items'].append(wrapper)
  for child in node.get('viewgroup_items',[]):collect(child,x,y,conditions)
 for child in root.get('viewgroup_items',[]):collect(child)
 if root.get('internal_events'):
  target={'internal_type':'ShapeModule','shape_type':'RECT','shape_width':720,'shape_height':1600,'paint_color':'#00000000','position_anchor':'CENTER','internal_events':deepcopy(root['internal_events'])};hit['viewgroup_items'].append(target)
 return hit

# Readable endpoints come from the static edition; intermediate timings are reconstruction estimates.
plans={
 1:(260,0,{'SCALE_XY':[(0,.96),(70,1.01),(100,1)]}),
 2:(220,0,{}),3:(300,20,{'X_OFFSET':[(0,24),(70,1),(100,0)]}),
 4:(420,30,{'SCALE_X':[(0,.03),(65,1.025),(100,1)]}),
 5:(380,90,{'X_OFFSET':[(0,45),(70,-2),(100,0)]}),
 6:(380,140,{'X_OFFSET':[(0,50),(70,-2),(100,0)]}),
 7:(380,190,{'X_OFFSET':[(0,50),(70,-2),(100,0)]}),
 8:(320,0,{}),9:(300,0,{'SCALE_Y':[(0,.1),(75,1.02),(100,1)]}),10:(220,0,{}),
 11:(220,0,{}),12:(280,40,{'X_OFFSET':[(0,-15),(100,0)]}),
 13:(440,80,{'SCALE_X':[(0,.04),(70,1.015),(100,1)]}),
 14:(450,210,{'SCALE_XY':[(0,.84),(70,1.025),(100,1)]}),
 15:(340,300,{'Y_OFFSET':[(0,30),(75,-1),(100,0)]}),
 16:(320,0,{'X_OFFSET':[(0,145),(75,-3),(100,0)]}),
 17:(440,80,{'SCALE_Y':[(0,.02),(70,1.01),(100,1)]}),
 18:(380,240,{'Y_OFFSET':[(0,24),(100,0)]}),
 19:(360,330,{'SCALE_X':[(0,.65),(80,1.01),(100,1)]}),
 20:(440,40,{'Y_OFFSET':[(0,-28),(75,1),(100,0)]}),
 21:(440,180,{'SCALE_X':[(0,.05),(75,1.02),(100,1)]}),
 22:(400,300,{'Y_OFFSET':[(0,32),(75,-1),(100,0)]}),
 23:(340,30,{'X_OFFSET':[(0,-32),(75,1),(100,0)]}),
 24:(340,30,{'X_OFFSET':[(0,32),(75,-1),(100,0)]}),
 25:(320,0,{'SCALE_XY':[(0,.96),(100,1)]})}
roots=[];hits=[];coverage=[]
for index,root in enumerate(original):
 if index==0:roots.append(deepcopy(root));continue
 condition=root.get('internal_formulas',{}).get('config_visible','')
 match=re.match(r'\$if\((.*),ALWAYS,REMOVE\)\$',condition)
 assert match,(index,condition)
 active=match.group(1)
 visual=deepcopy(root);clear(visual,'config_visible');visual['config_visible']='ALWAYS'
 for n in walk(visual):
  n.pop('internal_events',None)
  # Keep nested measurement boxes allocated while hidden; REMOVE can retain a zero-size
  # cached origin when a state is revealed during a parent animation.
  if n is not visual:
   if n.get('config_visible')=='REMOVE':n['config_visible']='NEVER'
   value=n.get('internal_formulas',{}).get('config_visible')
   if value:n['internal_formulas']['config_visible']=value.replace(',REMOVE)',',NEVER)')
 duration,delay,properties=plans[index]
 anim=motion(active,duration,delay,properties,loading=12<=index<=15 or 17<=index<=22)
 if index==8:
  measured=json.loads((BASE/'src/native-motion-definitions.json').read_text())['applications']['animator']
  anim['animator']=deepcopy(measured)
  for f in anim['animator']:
   if f['property']=='OPACITY':f['value']=100-f['value']
   if f['property'].startswith('SCALE'):f['value']/=100
 visual['internal_animations']=[anim]
 if index==10:
  clear(visual,'config_rotate_offset');visual['config_rotate_offset']=22.02
  formula(visual,'position_offset_y','(603-if(gv(avoid),90,0))*'+S)
  visual['internal_animations'].append(motion('gv(page)=2',320,0,{'OPACITY':[(0,0),(100,0)],'ROTATE':[(0,0),(30,-9.9),(60,-20),(100,-22.02)],'Y_OFFSET':[(0,0),(35,35),(70,79),(100,85)]}))
 roots.append(visual)
 if any(n.get('internal_events') for n in walk(root)):
  hit=touch_geometry(root);hit['internal_title']='交互区域 · '+root.get('internal_title','')
  # Incoming touch regions become active when the loader has cleared; hidden pages never intercept touches.
  hits.append(hit)
 coverage.append({'group':index,'title':root['internal_title'],'condition':active,'duration_ms':duration,'delay_ms':delay,'exit_ms':180,'status':'reconstructed timing; not original preset parameters'})
# Automatic loader uses a one-shot envelope whose two endpoints are transparent.
boot='gv(load)=1 & gv(prev)<=2 & gv(page)>=3 & gv(page)<=5'
auto=deepcopy(original[25]);clear(auto,'config_visible');auto['config_visible']='ALWAYS';auto['internal_title']='功能入口加载过渡'
for n in walk(auto):
 n.pop('internal_events',None)
 if n.get('text_expression')=='点击返回':n['text_expression']=''
auto['internal_animations']=[motion(boot,800,0,{'OPACITY':[(0,100),(15,0),(72,0),(100,100)],'SCALE_XY':[(0,.97),(70,1),(100,1.015)]},reverse=1)]
roots.append(auto);roots.extend(hits)
# A ring expands at the activated control. Both toggle directions end transparent.
ring={'internal_type':'ShapeModule','internal_title':'点击反馈光环','shape_type':'CIRCLE','shape_width':68,'paint_style':'STROKE','paint_stroke':3,'position_anchor':'CENTER','paint_color':'#FFB4EF00'}
formula(ring,'paint_color','gv(accent)');formula(ring,'position_offset_x','gv(tapx)*'+S);formula(ring,'position_offset_y','gv(tapy)*'+S)
ring['internal_animations']=[motion('gv(pulse)=1',300,0,{'OPACITY':[(0,100),(25,0),(75,0),(100,100)],'SCALE_XY':[(0,.72),(50,1),(100,1.4)]},reverse=300)]
roots.append(ring)
p['preset_root']['viewgroup_items']=roots
p['preset_info'].update(title='Rhine UI · 交互动画 v0.2',description='基于可编辑静态首版增加原生切页、卡片展开、Dock联动、详情开合、加载过渡和点击反馈。动画时序为参考重建，非原预设参数。天气音乐日历仍为演示数据。',version=17,locked=False)
if options.diagonal:
 p['preset_info'].update(title='Rhine UI · 斜面首页 v0.3',description='依据首页浏览图修正菱形入口、斜向底栏与时钟框线，参考明日方舟的工业界面设计。原生可编辑 KLWP，保留页面交互动画。素材和动画为参考重建，非原版预设。')
if options.perspective:
 p['preset_info'].update(title='Rhine UI · 透视主菜单 v0.4',description='点击 Dock 展开的终端、搜索、设置与支付快捷栏采用统一三维透视，文字与点击区域随面板同步变换，保留所有页面交互动画。参考重建，非原版预设。')
assert len(roots)<=64,len(roots)
(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8',newline='\n')
with zipfile.ZipFile(SOURCE) as source,zipfile.ZipFile(OUT/('Rhine-UI-'+edition+'.klwp'),'w',zipfile.ZIP_DEFLATED) as target:
 target.writestr('preset.json',json.dumps(p,ensure_ascii=False))
 for name in source.namelist():
  if name!='preset.json':target.writestr(name,source.read(name))
 if 'bitmaps/icon-play.png' not in source.namelist():target.write(BASE.parent/'rhine_theme/assets/icon-play.png','bitmaps/icon-play.png')
(OUT/'motion-coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'package':str(OUT/('Rhine-UI-'+edition+'.klwp')),'roots':len(roots),'animated_roots':sum(bool(n.get('internal_animations')) for n in roots),'hit_layers':len(hits)},ensure_ascii=True))
