"""Keep the paired Dock materials across native pages and restore their folding animation."""
from pathlib import Path
import json,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/native-desktop-navigation-v0.13.46';OUT=BASE/'output/desktop-dock-fold-v0.13.47';OUT.mkdir(exist_ok=True)
def rewrite(value):
 if isinstance(value,str):return value.replace('gv(page)=2','(gv(page)=2 | gv(page)=-1)')
 if isinstance(value,list):return [rewrite(v) for v in value]
 if isinstance(value,dict):return {k:rewrite(v) for k,v in value.items()}
 return value
for suffix in ('','-off'):
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-native-desktop-navigation{suffix}-v0.13.46.klwp') as src:
  p=json.loads(src.read('preset.json'));r=p['preset_root']['viewgroup_items']
  for i in (23,24):
   r[i]['internal_formulas']['config_visible']='$ALWAYS$'
   r[i]['internal_animations']=rewrite(r[i]['internal_animations'])
  r[23]['viewgroup_items'][3]['internal_formulas']['config_visible']='$if(gv(page)=0,ALWAYS,REMOVE)$'
  p['preset_info'].update(title='Rhine UI · 跨桌面收平底条 v0.13.47'+(' · 无重力视差' if suffix else ''),description='斜条主页右划进入原生应用桌面，底条与光带同步下移转平、隐藏电量日期，作为无点击的 Dock 背景；回主页恢复斜条。终端仍由 Dock 四宫格打开。')
  with zipfile.ZipFile(OUT/f'Rhine-UI-desktop-dock-fold{suffix}-v0.13.47.klwp','w',zipfile.ZIP_DEFLATED) as dest:
   for name in src.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else src.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
 print(suffix or 'normal','built')
