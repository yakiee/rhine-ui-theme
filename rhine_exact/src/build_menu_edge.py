"""Place the aligned terminal menu against the right screen edge."""
from pathlib import Path
import json,zipfile,copy
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/menu-alignment-v0.9.3';OUT=BASE/'output/menu-edge-v0.9.4';OUT.mkdir(exist_ok=True)
S='mu(min,1,si(sheight)*720/si(swidth)/1600)'
for suffix in ['', '-off']:
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-menu-alignment{suffix}-v0.9.3.klwp') as source:
  p=json.loads(source.read('preset.json'));r=p['preset_root']['viewgroup_items'];old=copy.deepcopy(r)
  for index in list(range(4,22))+[50]:
   r[index].setdefault('internal_toggles',{})['position_offset_x']=10
   r[index].setdefault('internal_formulas',{})['position_offset_x']='$156*'+S+'$'
  assert [n.get('internal_animations') for n in r]==[n.get('internal_animations') for n in old]
  for index in set(range(64))-set(range(4,22))-{50}:assert r[index]==old[index]
  p['preset_info']['title']='Rhine UI · 终端右侧贴边 v0.9.4'+(' · 无重力视差' if suffix else '')
  p['preset_info']['description']='已对齐的终端菜单整体靠右贴边，并留出少量屏外底板余量覆盖重力视差。排列、实时数据与动画保持不变。'
  target=OUT/f'Rhine-UI-menu-edge{suffix}-v0.9.4.klwp'
  with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as dest:
   for name in source.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else source.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
  print(target)
