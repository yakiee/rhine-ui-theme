"""Clean home composition and make navigation/configuration entry points consistent."""
from pathlib import Path
import copy,json,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/status-optical-balance-v0.13.42';OUT=BASE/'output/interaction-cleanup-v0.13.43';OUT.mkdir(exist_ok=True)
def switch(key,value):return dict(type='SINGLE_TAP',action='SWITCH_GLOBAL',switch=key,switch_text=value)
MUSIC_URL='$"android-app://"+gv(musicapp)+"#Intent;action=android.intent.action.MAIN;category=android.intent.category.LAUNCHER;end"$'
for suffix in ('','-off'):
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-status-optical-balance{suffix}-v0.13.42.klwp') as source:
  p=json.loads(source.read('preset.json'));r=p['preset_root']['viewgroup_items']
  r[1]['viewgroup_items']=[];r[1]['config_visible']='REMOVE';r[1]['internal_title']='主页留白 · 已移除时钟与机型铭牌'
  dock=r[51]['viewgroup_items']
  for index in (1,3,5,7):dock[index]['viewgroup_items']=[]
  music=dock[2];custom=copy.deepcopy(music)
  music.setdefault('internal_toggles',{})['config_visible']=10
  music.setdefault('internal_formulas',{})['config_visible']='$if(tc(len,gv(musicapp))=0,ALWAYS,REMOVE)$'
  custom.setdefault('internal_toggles',{})['config_visible']=10
  custom.setdefault('internal_formulas',{})['config_visible']='$if(tc(len,gv(musicapp))>0,ALWAYS,REMOVE)$'
  custom['internal_title']='音乐 · 与终端共用自定义播放器'
  custom['viewgroup_items'][0]['internal_events']=[dict(type='SINGLE_TAP',action='OPEN_LINK',url=MUSIC_URL)]
  dock.append(custom)
  header=r[52]['viewgroup_items'];header[4]['viewgroup_items'][0].update(text_expression='主题配置',text_size=24)
  config=copy.deepcopy(header[3]);config['internal_title']='主题配置 · 打开 KLWP 编辑器'
  config['viewgroup_items'][0].update(paint_color='#00000000',internal_events=[dict(type='SINGLE_TAP',action='KUSTOM_ACTION',kustom_action='ADVANCED_EDITOR')]);header.append(config)
  # Exit nested weather details before leaving the weather page.
  r[55]['viewgroup_items'][1]['viewgroup_items'][0]['internal_events']=[switch('view','$if(gv(detail)=1,3,0)$'),switch('detail','0')]
  # Every plain subpage exit clears transient detail state as well.
  header[5]['viewgroup_items'][0]['internal_events']=[switch('detail','0'),switch('view','0')]
  back=r[53]['viewgroup_items'][5]['viewgroup_items'][0]['internal_events']
  back.insert(0,switch('detail','0'))
  p['preset_info'].update(title='Rhine UI · 清爽主页与交互整理 v0.13.43'+(' · 无重力视差' if suffix else ''),description='移除主页左上角时钟与机型；主页 Dock 每格仅保留一处点击，音乐自定义播放器两处入口一致；应用页新增主题配置；天气返回先收起详情。')
  with zipfile.ZipFile(OUT/f'Rhine-UI-interaction-cleanup{suffix}-v0.13.43.klwp','w',zipfile.ZIP_DEFLATED) as dest:
   for name in source.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else source.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
 print(suffix or 'normal','built')
