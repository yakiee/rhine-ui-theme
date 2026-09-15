"""Separate launcher desktops from the terminal overlay opened by the Dock."""
from pathlib import Path
import copy,json,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/interaction-cleanup-v0.13.43';OUT=BASE/'output/native-desktop-navigation-v0.13.46';OUT.mkdir(exist_ok=True)
def formula(n,key,value):
 n.setdefault('internal_toggles',{})[key]=10;n.setdefault('internal_formulas',{})[key]='$'+value.strip('$')+'$'
def switch(key,value):return dict(type='SINGLE_TAP',action='SWITCH_GLOBAL',switch=key,switch_text=value)
def walk(n):
 yield n
 for c in n.get('viewgroup_items',[]):yield from walk(c)
for suffix in ('','-off'):
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-interaction-cleanup{suffix}-v0.13.43.klwp') as source:
  p=json.loads(source.read('preset.json'));root=p['preset_root'];r=root['viewgroup_items'];g=root['globals_list']
  for key,title,value in [('homepg','斜条主页所在桌面页码','2'),('parent','功能页返回目标 0主页 1终端','0')]:
   g[key]=dict(index=max(v['index'] for v in g.values())+1,type='TEXT',title=title,value=value)
  g['view'].update(title='主题内部页面 0主页 1终端',value='0')
  g['origin']['value']='2';g['month']['value']='0'
  g['page'].update(title='计算：独立主题桌面与内部功能页',value='$if(si(screen)!=gv(homepg),-1,gv(origin)=si(screen) & gv(view)>0,gv(view),0)$')
  # Only the dedicated desktop owns theme controls; native app pages retain normal launcher input.
  for i,node in enumerate(r):
   if i==0 or i==1:continue
   old=node.get('internal_formulas',{}).get('config_visible',node.get('config_visible','ALWAYS')).strip('$')
   formula(node,'config_visible','if(si(screen)=gv(homepg),'+old+',REMOVE)')
  # The grid shortcut now opens the terminal, without moving the launcher page.
  for event in r[51]['viewgroup_items'][6]['viewgroup_items'][0]['internal_events']:
   if event.get('switch')=='view':event['switch_text']='1'
  r[3]['viewgroup_items'][13]['internal_title']='终端入口 · 四宫格'
  r[51]['viewgroup_items'][6]['internal_title']='终端 · 在当前桌面展开'
  # Keep one stable parent while navigating tabs inside a feature.
  for node in walk(root):
   events=node.get('internal_events',[])
   if any(e.get('switch')=='view' and e.get('switch_text') in ('3','4','5') for e in events):
    events.insert(0,switch('parent','$if(gv(page)<=1,gv(page),gv(parent))$'))
  back='$if(gv(parent)=1,1,0)$'
  for event in r[53]['viewgroup_items'][5]['viewgroup_items'][0]['internal_events']:
   if event.get('switch')=='view':event['switch_text']=back
  r[55]['viewgroup_items'][1]['viewgroup_items'][0]['internal_events']=[switch('view','$if(gv(detail)=1,3,gv(parent)=1,1,0)$'),switch('detail','0')]
  for node in walk(r[58]):
   for event in node.get('internal_events',[]):
    if event.get('switch')=='view' and event.get('switch_text')=='0':event['switch_text']=back
  # Reuse the existing header for an explicit terminal exit and editor shortcut.
  formula(r[52],'config_visible','if(si(screen)=gv(homepg) & gv(page)=1,ALWAYS,REMOVE)')
  r[52]['internal_title']='终端 · 返回主页与主题配置'
  formula(r[52]['viewgroup_items'][5],'config_visible','ALWAYS')
  r[52]['viewgroup_items'][5]['viewgroup_items'][0]['internal_events']=[switch('detail','0'),switch('view','0'),switch('parent','0')]
  root['internal_flows'][0]['name']='离开主题桌面时收起终端与功能页'
  root['internal_flows'][0]['a'][0]['params']['formula']='$if(si(screen)=gv(homepg) & gv(origin)=si(screen),gv(view),0)$'
  p['preset_info'].update(title='Rhine UI · 原生桌面交互 v0.13.46'+(' · 无重力视差' if suffix else ''),description='第2桌面为斜条主页，右划进入第1桌面的原生应用页；Dock 最下面四宫格点击展开终端；终端返回收起，功能页返回原入口。homepg 可修改主题桌面页码。')
  with zipfile.ZipFile(OUT/f'Rhine-UI-native-desktop-navigation{suffix}-v0.13.46.klwp','w',zipfile.ZIP_DEFLATED) as dest:
   for name in source.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else source.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
 print(suffix or 'normal','built')
