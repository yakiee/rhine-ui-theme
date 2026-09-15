"""Reduce status icon visual weight while retaining slight strip overhang."""
from pathlib import Path
import json,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/terminal-content-grid-v0.13.41';OUT=BASE/'output/status-optical-balance-v0.13.42';OUT.mkdir(exist_ok=True)
for suffix in ('','-off'):
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-terminal-content-grid{suffix}-v0.13.41.klwp') as source:
  p=json.loads(source.read('preset.json'));s=p['preset_root']['viewgroup_items'][4]['viewgroup_items']
  s[6]['viewgroup_items'][0].update(shape_width=48,shape_height=40,paint_stroke=2.4)
  s[7]['viewgroup_items'][0].update(shape_width=40,shape_height=40,paint_stroke=2.8)
  # The solid storage symbol needs less width than outline icons to feel balanced.
  s[8]['viewgroup_items'][0].update(shape_width=34,shape_height=40)
  p['preset_info'].update(title='Rhine UI · 状态图标视觉平衡 v0.13.42'+(' · 无重力视差' if suffix else ''),description='资源图标高度收至40，灰条仍38；描边同步收细，实心存储图标额外收窄以平衡视觉重量。其余排版不变。')
  with zipfile.ZipFile(OUT/f'Rhine-UI-status-optical-balance{suffix}-v0.13.42.klwp','w',zipfile.ZIP_DEFLATED) as dest:
   for name in source.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else source.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
 print(suffix or 'normal','built')
