"""Use launcher pages for home/terminal; make the terminal Dock decorative."""
from pathlib import Path
import copy,json,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/menu-scale-v0.9.5';OUT=BASE/'output/swipe-pages-v0.10.7';OUT.mkdir(exist_ok=True)
S='mu(min,1,si(sheight)*720/si(swidth)/1600)'
def formula(n,k,v):n.setdefault('internal_toggles',{})[k]=10;n.setdefault('internal_formulas',{})[k]='$'+v.strip('$')+'$'
def walk(n):
 yield n
 for c in n.get('viewgroup_items',[]):yield from walk(c)
for suffix in ['', '-off']:
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-menu-scale{suffix}-v0.9.5.klwp') as source:
  p=json.loads(source.read('preset.json'));r=p['preset_root']['viewgroup_items'];g=p['preset_root']['globals_list']
  g['view']={'index':max(x['index'] for x in g.values())+1,'type':'TEXT','title':'功能子页 0跟随桌面','value':'0'}
  g['origin']={'index':g['view']['index']+1,'type':'TEXT','title':'子页所在桌面','value':'1'}
  g['page']['title']='计算：桌面分页与功能子页'
  g['page']['value']='$if(gv(view)>=2 & gv(origin)=si(screen),gv(view),mu(max,0,mu(min,1,si(screen)-1)))$'
  g['blank']['value']='0'
  for n in walk(p['preset_root']):
   for event in n.get('internal_events',[]):
    if event.get('switch')=='page':
     event['switch']='view'
     if event.get('switch_text')=='1' or 'if(gv(page)=1,0,1)' in event.get('switch_text',''):event['switch_text']='0'
  p['preset_root']['internal_flows']=[{'id':'PageSync','name':'桌面切页时退出子页','t':[{'id':'PageTrig','type':'T_FORMULA','params':{'formula':'$si(screen)$','trigger':'ON_CHANGE'}}],'a':[{'id':'ZeroView','type':'A_FORMULA','params':{'formula':'0'}},{'id':'ViewSync','type':'A_GLOBAL','params':{'global':'view','store_mode':'TEXT'}}]}]
  for n in walk(p['preset_root']):
   events=n.get('internal_events',[])
   if any(e.get('switch')=='view' and e.get('switch_text') not in ['0','1'] for e in events):
    events.insert(0,{'type':'SINGLE_TAP','action':'SWITCH_GLOBAL','switch':'origin','switch_text':'$si(screen)$'})
  # A page cannot be dismissed by tapping its empty background or decorative Dock.
  for index in [48,49]:
   r[index]['viewgroup_items']=[]
   formula(r[index],'config_visible','REMOVE')
  formula(r[52],'config_visible','if(gv(page)=0 & gv(dock)=2,ALWAYS,REMOVE)')
  r[52]['viewgroup_items']=r[52]['viewgroup_items'][1:]
  formula(r[51],'config_visible','if(gv(page)=0,ALWAYS,REMOVE)')
  # Home-only foreground moves out when the second desktop page is selected.
  for index,old in [(1,'gv(page)<=2'),(3,'gv(page)<=1')]:
   for n in walk(r[index]):
    for field,value in n.get('internal_formulas',{}).items():
     if isinstance(value,str):n['internal_formulas'][field]=value.replace(old,'gv(page)=0')
   for a in r[index].get('internal_animations',[]):
    if a.get('type')=='FORMULA':
     a['formula']=a.get('formula','').replace(old,'gv(page)=0')
     for field,value in a.get('internal_formulas',{}).items():a['internal_formulas'][field]=value.replace(old,'gv(page)=0')
  # Both terminal and horizontal app Dock use only the background material.
  foreground={'internal_type':'OverlapLayerModule','position_anchor':'CENTER','internal_title':'Dock 信息 · 首页显示','viewgroup_items':r[23]['viewgroup_items'][3:]}
  formula(foreground,'config_visible','if(gv(page)=1 | gv(page)=2,REMOVE,ALWAYS)')
  r[23]['viewgroup_items']=r[23]['viewgroup_items'][:3]+[foreground]
  lower={'type':'FORMULA','formula':'$gv(page)=1 | gv(page)=2$','action':'ADVANCED','anchor':'MODULE_CENTER','duration':3.2,'delay':0,'animator':[{'position':0,'property':'Y_OFFSET','value':0,'ease':'NORMAL'},{'position':100,'property':'Y_OFFSET','value':90,'ease':'NORMAL'}]}
  for index in [23,24]:r[index]['internal_animations'].append(copy.deepcopy(lower))
  # Fade the two Dock materials together while they settle below the screen.
  terminal_exit=copy.deepcopy(lower)
  terminal_exit['formula']='$gv(page)=1$'
  terminal_exit['duration']=4.8
  terminal_exit['internal_toggles']={'duration':10}
  terminal_exit['internal_formulas']={'duration':'$if(gv(page)=1,4.8,3.6)$'}
  terminal_exit['animator']=[]
  for position,offset,opacity in [(0,0,0),(18,80,18),(40,290,58),(65,555,94),(82,690,100),(100,720,100)]:
   for prop,value in [('Y_OFFSET',offset),('OPACITY',opacity)]:
    terminal_exit['animator'].append({'position':position,'property':prop,'value':value,'ease':'NORMAL'})
  for index in [23,24]:r[index]['internal_animations'].append(copy.deepcopy(terminal_exit))
  # Enlarge around the same right edge, including the settings touch target.
  for index in list(range(4,22))+[50]:
   formula(r[index],'config_scale_value','130*'+S)
   formula(r[index],'position_offset_x','84*'+S)
  # All menu planes share the same pivot and curve, so labels stay attached to cards.
  menu_motion=[]
  for position,scale,x,y,opacity in [(0,0.86,52,24,100),(18,0.91,30,16,60),(40,0.974,10,5,18),(65,1.018,-4,-2,0),(82,1.008,-1,-0.5,0),(100,1,0,0,0)]:
   for prop,value in [('SCALE_XY',scale),('X_OFFSET',x),('Y_OFFSET',y),('OPACITY',opacity)]:
    menu_motion.append({'position':position,'property':prop,'value':value,'ease':'NORMAL'})
  for index in range(4,22):
   a=r[index]['internal_animations'][0]
   a['animator']=copy.deepcopy(menu_motion)
   a['duration']=4.8;a['delay']=0
   a['internal_formulas']={'duration':'$if(gv(page)=1,4.8,3.2)$'}
   a['internal_toggles']={'duration':10}
  # Arknights uses a full-height left divider and a shorter divider below the header.
  blue_panel=r[14]['viewgroup_items'][1]
  for name,x,y,height in [('左入口分隔',-104,0,126.0131592689295),('右入口分隔',88,18.3782898172324,89.2565796344648)]:
   for title,offset,width,color in [('阴影',0,4,'#26003A53'),('细线',0,1.8,'#BD146B85'),('亮边',1.2,0.65,'#7009D7EF')]:
    line={'internal_type':'ShapeModule','internal_title':name+title,'position_anchor':'CENTER','shape_type':'RECT','shape_width':width,'shape_height':height,'paint_color':color}
    positioned={'internal_type':'OverlapLayerModule','internal_title':name+title,'position_anchor':'CENTER','viewgroup_items':[line],'position_padding_left':max(0,2*(x+offset)),'position_padding_right':max(0,-2*(x+offset)),'position_padding_top':max(0,2*y),'position_padding_bottom':max(0,-2*y)}
    blue_panel['viewgroup_items'].append(positioned)
  p['preset_info'].update(title='Rhine UI · 左右分页 v0.10.7'+(' · 无重力视差' if suffix else ''),description='首页和终端分别对应桌面第1、2页。左右滑动切换，点击空白不再收起；终端页底条及光带整体滑出屏幕，右侧菜单缩放回弹渐显、缩小渐隐；应用页保留无文字的底部Dock。桌面需保留2页并启用壁纸滚动。',width=360,height=752,xscreens=1,yscreens=0)
  target=OUT/f'Rhine-UI-swipe-pages{suffix}-v0.10.7.klwp'
  with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
   for name in source.namelist():z.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else source.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
  print(target)
