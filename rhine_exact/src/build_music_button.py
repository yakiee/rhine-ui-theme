"""Replace theme shortcut with configurable music destination."""
from pathlib import Path
import copy,json,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/status-seconds-v0.13.29';OUT=BASE/'output/music-button-v0.13.30';OUT.mkdir(exist_ok=True)
HEADPHONES='M 8 61 L 8 46 C 8 -4 92 -4 92 46 L 92 61 M 8 50 L 26 50 L 26 90 L 8 90 Z M 74 50 L 92 50 L 92 90 L 74 90 Z M 92 80 C 92 102 69 106 55 106 L 47 106'
for suffix in ['', '-off']:
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-status-seconds{suffix}-v0.13.29.klwp') as src:
  p=json.loads(src.read('preset.json'));r=p['preset_root']['viewgroup_items'];g=p['preset_root']['globals_list'];idx=max(v['index'] for v in g.values())+1
  for offset,(key,title,value,description) in enumerate([
   ('musicapp','音乐 · 自定义 App 包名','','留空打开主题音乐页；填写已安装播放器的应用包名，点击音乐即可打开。'),
   ('musicsub','音乐 · 按钮小字','播放与控制','显示在音乐标题下方，可改为常用播放器名称或说明。')]):
   g[key]=dict(index=idx+offset,type='TEXT',title=title,value=value,description=description,global_formula='')
  g['search'].update(title='系统 · 自定义 App 包名',value='com.android.settings',description='默认打开系统设置；可填写其他已安装 App 的应用包名。')
  r[11]['internal_title']='主菜单 · 音乐入口'
  r[11]['viewgroup_items'][2]['viewgroup_items'][0]['viewgroup_items'][0]['text_expression']='音乐'
  r[11]['viewgroup_items'][3]['viewgroup_items'][0]['viewgroup_items'][0]['text_expression']='$gv(musicsub)$'
  mark=r[11]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items'][4]
  mark['internal_title']='耳机 · 音乐背景水印'
  mark['viewgroup_items']=[dict(internal_type='ShapeModule',position_anchor='CENTER',shape_type='PATH',shape_path=HEADPHONES,shape_path_scale='FIT_XY',shape_width=94,shape_height=100,paint_color='#34616A6E',paint_style='STROKE',paint_stroke=4)]
  # Remove the old appearance-change badge; music has no such notification.
  r[11]['viewgroup_items'][4]['viewgroup_items']=[]
  hits=r[50]['viewgroup_items']
  for zone in range(9):
   # Central system configuration is shared by all nine pressure zones.
   sys=hits[1+zone]['viewgroup_items'][0];sys['internal_events']=sys['internal_events'][:1]+[dict(type='SINGLE_TAP',action='OPEN_LINK',url='$"android-app://"+gv(search)+"#Intent;action=android.intent.action.MAIN;category=android.intent.category.LAUNCHER;end"$')]
   holder=hits[10+zone];shape=holder['viewgroup_items'][0];pulse=copy.deepcopy(shape['internal_events'][0])
   holder['internal_formulas']['config_visible']='$if(gv(page)=1 & tc(len,gv(musicapp))=0,ALWAYS,REMOVE)$'
   shape['internal_events']=[pulse,dict(type='SINGLE_TAP',action='SWITCH_GLOBAL',switch='origin',switch_text='$si(screen)$'),dict(type='SINGLE_TAP',action='SWITCH_GLOBAL',switch='prev',switch_text='1'),dict(type='SINGLE_TAP',action='SWITCH_GLOBAL',switch='view',switch_text='4')]
   custom=copy.deepcopy(holder);custom['internal_title']=f'音乐自定义 App · 点击区 {zone+1}'
   custom['internal_formulas']['config_visible']='$if(gv(page)=1 & tc(len,gv(musicapp))>0,ALWAYS,REMOVE)$'
   custom['viewgroup_items'][0]['internal_events']=[copy.deepcopy(pulse),dict(type='SINGLE_TAP',action='OPEN_LINK',url='$"android-app://"+gv(musicapp)+"#Intent;action=android.intent.action.MAIN;category=android.intent.category.LAUNCHER;end"$')]
   hits.append(custom)
  p['preset_info'].update(title='Rhine UI · 音乐与自定义入口 v0.13.30'+(' · 无重力视差' if suffix else ''),description='主题按钮改为音乐及耳机水印；全局 musicapp 指定播放器，musicsub 设置小字，search 自定义系统启动链接。')
  target=OUT/f'Rhine-UI-music-button{suffix}-v0.13.30.klwp'
  with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as dest:
   for name in src.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else src.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
  print(target)
# A temporary verification edition targets installed Android Settings, requiring no new app.
with zipfile.ZipFile(OUT/'Rhine-UI-music-button-v0.13.30.klwp') as src:
 p=json.loads(src.read('preset.json'));p['preset_root']['globals_list']['musicapp']['value']='com.android.settings'
 with zipfile.ZipFile(OUT/'verify-custom-app-v3.klwp','w',zipfile.ZIP_DEFLATED) as dest:
  for name in src.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else src.read(name))
