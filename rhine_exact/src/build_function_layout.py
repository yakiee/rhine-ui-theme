"""Organize unique theme destinations and bind native Android entry points."""
from pathlib import Path
import copy,json,zipfile
BASE=Path(__file__).resolve().parents[1]
SOURCE=BASE/'output/swipe-pages-v0.10.7'
OUT=BASE/'output/function-layout-v0.11.6';OUT.mkdir(exist_ok=True)
def formula(n,k,v):n.setdefault('internal_toggles',{})[k]=10;n.setdefault('internal_formulas',{})[k]='$'+v.strip('$')+'$'
def walk(n):
 yield n
 for c in n.get('viewgroup_items',[]):yield from walk(c)
def text(n,value):
 for c in walk(n):
  if c.get('internal_type')=='TextModule':c['text_expression']=value;break
def at(node,x,y):
 return {'internal_type':'OverlapLayerModule','position_anchor':'CENTER','position_padding_left':max(0,x*2),'position_padding_right':max(0,-x*2),'position_padding_top':max(0,y*2),'position_padding_bottom':max(0,-y*2),'viewgroup_items':[node]}
def rect(w,h,color):return {'internal_type':'ShapeModule','position_anchor':'CENTER','shape_type':'RECT','shape_width':w,'shape_height':h,'paint_color':color}
def label(value,size,width,color):return {'internal_type':'TextModule','position_anchor':'CENTER','text_expression':value,'text_size':size,'text_width':width,'text_size_type':'FIXED_WIDTH','text_lines':1,'text_align':'CENTER','paint_color':color}
def intent(action,category=None):return 'intent:#Intent;action='+action+(';'+'category='+category if category else '')+';end'
def native(uri):return [{'type':'SINGLE_TAP','action':'LAUNCH_ACTIVITY','intent':uri}]
def url(value):return [{'type':'SINGLE_TAP','action':'OPEN_LINK','url':value}]
def hit(x,y,w,h,events,page):
 n=rect(w,h,'#00000000');n['internal_events']=events;group=at(n,x,y);formula(group,'config_visible',f'if(gv(page)={page},ALWAYS,REMOVE)');return group
apps=[
 ('浏览器',intent('android.intent.action.MAIN','android.intent.category.APP_BROWSER'),'M 50 5 A 45 45 0 1 1 49.9 5 Z M 5 50 L 95 50 M 50 5 C 18 30 18 70 50 95 C 82 70 82 30 50 5'),
 ('相册',intent('android.intent.action.MAIN','android.intent.category.APP_GALLERY'),'M 5 10 L 95 10 L 95 90 L 5 90 Z M 5 80 L 37 42 L 59 66 L 74 48 L 95 80 M 70 24 A 7 7 0 1 1 69.9 24 Z'),
 ('时钟',intent('android.intent.action.SHOW_ALARMS'),'M 50 5 A 45 45 0 1 1 49.9 5 Z M 50 20 L 50 52 L 72 64'),
 ('地图',intent('android.intent.action.MAIN','android.intent.category.APP_MAPS'),'M 50 95 C 5 48 7 5 50 5 C 93 5 95 48 50 95 Z M 50 25 A 14 14 0 1 1 49.9 25 Z'),
 ('邮件',intent('android.intent.action.MAIN','android.intent.category.APP_EMAIL'),'M 5 18 L 95 18 L 95 82 L 5 82 Z M 5 18 L 50 55 L 95 18'),
 ('短信',intent('android.intent.action.MAIN','android.intent.category.APP_MESSAGING'),'M 5 10 L 95 10 L 95 73 L 38 73 L 15 93 L 15 73 L 5 73 Z M 22 32 L 78 32 M 22 49 L 64 49'),
 ('联系人',intent('android.intent.action.MAIN','android.intent.category.APP_CONTACTS'),'M 50 5 A 19 19 0 1 1 49.9 5 Z M 12 92 C 12 38 88 38 88 92 Z'),
 ('云盘','intent:#Intent;action=android.intent.action.MAIN;category=android.intent.category.LAUNCHER;component=com.google.android.apps.docs/.app.NewMainProxyActivity;end','M 22 80 C -10 80 0 38 26 40 C 23 0 80 0 78 39 C 107 40 108 80 78 80 Z M 50 70 L 50 32 M 36 47 L 50 32 L 64 47')]
for suffix in ['', '-off']:
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-swipe-pages{suffix}-v0.10.7.klwp') as z:
  p=json.loads(z.read('preset.json'));r=p['preset_root']['viewgroup_items'];g=p['preset_root']['globals_list']
  text(r[12],'系统');text(r[13]['viewgroup_items'][1],'主题');text(r[13]['viewgroup_items'][2],'外观与交互')
  text(r[15],'支付宝快捷');text(r[20],'电话');text(r[21]['viewgroup_items'][1],'文件')
  r[21]['viewgroup_items']=r[21]['viewgroup_items'][:3]
  for key in ['wxpay','wxscan']:g.pop(key,None)
  g['search']['title']='系统设置入口';g['search']['value']=intent('android.settings.SETTINGS')
  # One hit area per visible control, with the same full-canvas pivot as the menu.
  controls=copy.deepcopy(r[5]);controls['internal_title']='终端唯一入口与点击区域';controls['internal_animations']=[a for a in controls.get('internal_animations',[]) if a.get('type')=='GYRO']
  formula(controls,'config_visible','if(gv(page)=1,ALWAYS,REMOVE)')
  controls['viewgroup_items']=[copy.deepcopy(r[5]['viewgroup_items'][0])]
  theme=[{'type':'SINGLE_TAP','action':'SWITCH_GLOBAL','switch':'origin','switch_text':'$si(screen)$'},{'type':'SINGLE_TAP','action':'SWITCH_GLOBAL','switch':'prev','switch_text':'1'},{'type':'SINGLE_TAP','action':'SWITCH_GLOBAL','switch':'view','switch_text':'6'}]
  for x,y,w,h,events in [(-143,-15,274,112,native(intent('android.settings.SETTINGS'))),(143,-15,274,112,theme),(-192,118,176,126,url('$gv(alipay)$')),(-8,136.4,192,89,url('$gv(apay)$')),(184,136.4,192,89,url('$gv(ascan)$')),(-182,255,196,120,native('intent:#Intent;action=android.intent.action.MAIN;category=android.intent.category.LAUNCHER;component=com.android.dialer/.main.impl.MainActivity;end')),(26,255,196,120,native('intent:#Intent;action=android.intent.action.MAIN;category=android.intent.category.LAUNCHER;component=com.google.android.documentsui/com.android.documentsui.LauncherActivity;end')),(208,255,144,120,url('$gv(wechat)$'))]:controls['viewgroup_items'].append(hit(x,y,w,h,events,1))
  # Screen-aligned hit areas avoid the runtime's unreliable inverse mapping of 3D planes.
  controls['config_rotate_mode']='NONE';controls['config_rotate_offset']=0
  formula(controls,'config_scale_value','100*mu(min,1,si(sheight)*720/si(swidth)/1600)')
  formula(controls,'position_offset_x','0');formula(controls,'position_offset_y','0')
  bounds=[(315,709,238,106),(583,710,272,110),(269,837,148,112),(432,865,176,94),(620,869,190,98),(279,964,166,108),(466,984,188,118),(648,998,144,124)]
  events=[n['viewgroup_items'][0]['internal_events'] for n in controls['viewgroup_items'][1:]]
  controls['viewgroup_items']=controls['viewgroup_items'][:1]
  for (x,y,w,h),event in zip(bounds,events):controls['viewgroup_items'].append(hit((x-360)/0.94,(y-800)/0.94,w/0.94,h/0.94,event,1))
  r[50]=controls
  # The application page contains labeled shortcuts distinct from terminal and information pages.
  for i,(name,uri,path) in enumerate(apps):
   g[f'app{i}']['title']=name+' · 可在触摸动作中更换应用';g[f'app{i}']['value']=uri
   tile=r[22]['viewgroup_items'][i+1]
   icon={'internal_type':'ShapeModule','position_anchor':'CENTER','shape_type':'PATH','shape_width':40,'shape_height':40,'shape_path':path,'shape_path_scale':'FIT_XY','paint_color':'#FF18252C','paint_style':'STROKE','paint_stroke':2}
   tile['viewgroup_items']=[rect(126,132,'#ECF1F3F3'),at(rect(126,3,'#FF098AA6'),0,-64),at(icon,0,-21),at(label(name,25,118,'#FF172029'),0,37),hit(0,0,132,140,native(uri),2)]
   tile['internal_title']=name+' · 应用入口'
  # Do not clear a subpage opened after the new desktop page has already arrived.
  p['preset_root']['internal_flows'][0]['a'][0]['params']['formula']='$if(gv(origin)=si(screen),gv(view),0)$'
  # Dock choices now control information density, not a second navigation menu.
  for n in r[23]['viewgroup_items'][3]['viewgroup_items'][6:]:formula(n,'config_visible','REMOVE')
  r[52]['viewgroup_items']=[];formula(r[52],'config_visible','REMOVE')
  # Give the application page a readable return affordance over the wallpaper.
  header={'internal_type':'OverlapLayerModule','internal_title':'应用页返回与标题','position_anchor':'CENTER','viewgroup_items':[rect(720,1600,'#00000000')]}
  formula(header,'config_scale_value','100*mu(min,1,si(sheight)*720/si(swidth)/1600)')
  formula(header,'config_visible','if(gv(page)=2,ALWAYS,REMOVE)')
  header['viewgroup_items'] += [at(rect(180,66,'#C4172029'),-246,-625),at(label('‹ 返回',28,166,'#FFFFFFFF'),-246,-625),at(rect(150,66,'#C4172029'),232,-625),at(label('应用',28,140,'#FFFFFFFF'),232,-625),hit(-246,-625,180,80,[{'type':'SINGLE_TAP','action':'SWITCH_GLOBAL','switch':'view','switch_text':'0'}],2)]
  r[52]=header
  text(r[45]['viewgroup_items'][20],'日期模式显示时间信息，电量模式仅显示电量')
  text(r[45]['viewgroup_items'][29],'电量')
  text(r[45]['viewgroup_items'][38],'页面导航')
  text(r[45]['viewgroup_items'][39],'左右滑动切换桌面；子页点左上角返回')
  for i in range(40,46):formula(r[45]['viewgroup_items'][i],'config_visible','REMOVE')
  for n in walk(r[61]):n['internal_events']=[e for e in n.get('internal_events',[]) if e.get('switch')!='blank']
  # These two footer buttons both open the editor, scoped to their settings tab.
  for ri,page in [(60,6),(61,7)]:r[ri]['viewgroup_items'].append(hit(-0.5,598,609,86,[{'type':'SINGLE_TAP','action':'KUSTOM_ACTION','kustom_action':'ADVANCED_EDITOR'}],page))
  p['preset_info'].update(title='Rhine UI · 功能整理 v0.11.6'+(' · 无重力视差' if suffix else ''),description='首页集中信息页，终端区分系统和主题；支付宝快捷集中，底排电话、文件、微信；应用页带名称和独立启动动作，Dock仅显示信息。')
  target=OUT/f'Rhine-UI-functions{suffix}-v0.11.6.klwp'
  with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as dest:
   for name in z.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else z.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
  print(target)
