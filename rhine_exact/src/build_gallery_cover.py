"""Add gallery entry points and a separately configurable terminal cover."""
from pathlib import Path
import json,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/status-icon-scale-v0.13.35';OUT=BASE/'output/gallery-cover-v0.13.36';OUT.mkdir(exist_ok=True)
GALLERY=dict(type='SINGLE_TAP',action='LAUNCH_ACTIVITY',intent='intent:#Intent;action=android.intent.action.MAIN;category=android.intent.category.APP_GALLERY;end')
for suffix in ('','-off'):
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-status-icon-scale{suffix}-v0.13.35.klwp') as source:
  p=json.loads(source.read('preset.json'));r=p['preset_root']['viewgroup_items'];g=p['preset_root']['globals_list'];idx=max(x['index'] for x in g.values())+1
  g['termcover']=dict(index=idx,type='BITMAP',title='终端 · 相册封面',value=g['wall']['value'],description='独立选择第一行相册封面图片，按封面框居中裁切；不会更换桌面壁纸。',global_formula='')
  g['covertext']=dict(index=idx+1,type='TEXT',title='终端 · 封面文字',value='相册',description='第一行封面底部的小字，可自定义。',global_formula='')
  banner=r[5]['viewgroup_items'][4]['viewgroup_items'][0]['viewgroup_items']
  holder=banner[2];holder.update(position_padding_top=0,position_padding_bottom=0)
  bitmap=holder['viewgroup_items'][0];bitmap.update(bitmap_width=186,bitmap_height=129,bitmap_scale_mode='CENTER_CROP');bitmap['internal_formulas']['bitmap_bitmap']='$gv(termcover)$'
  banner[4]['viewgroup_items'][0]['text_expression']='$gv(covertext)$'
  hits=r[50]['viewgroup_items']
  # Keep the pressure pulse and spatial hit regions; replace only the destination.
  for index in range(78,87):
   shape=hits[index+1]['viewgroup_items'][0];shape['internal_events']=shape['internal_events'][:1]+[dict(GALLERY)]
  # Of the nine device/banner zones, the left column belongs to system information.
  for zone in range(9):
   if zone%3:
    shape=hits[88+zone]['viewgroup_items'][0];shape['internal_events']=shape['internal_events'][:1]+[dict(GALLERY)]
  p['preset_info'].update(title='Rhine UI · 相册与独立封面 v0.13.36'+(' · 无重力视差' if suffix else ''),description='第一行左侧区域与右侧封面打开系统相册；termcover 独立选封面图片，covertext 配置底部文字；中间保留设备信息。')
  with zipfile.ZipFile(OUT/f'Rhine-UI-gallery-cover{suffix}-v0.13.36.klwp','w',zipfile.ZIP_DEFLATED) as dest:
   for name in source.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else source.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
 print(suffix or 'normal','built')
