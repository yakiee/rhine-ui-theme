"""Align the terminal menu on one perspective plane and one shared grid."""
from pathlib import Path
import copy,json,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/live-data-v0.9.2';OUT=BASE/'output/menu-alignment-v0.9.3';OUT.mkdir(exist_ok=True)
S='mu(min,1,si(sheight)*720/si(swidth)/1600)'
def formula(n,k,v):n.setdefault('internal_toggles',{})[k]=10;n.setdefault('internal_formulas',{})[k]='$'+v+'$'
def put(n,x,y):
 for key,value in [('left',max(0,2*x)),('right',max(0,-2*x)),('top',max(0,2*y)),('bottom',max(0,-2*y))]:
  field='position_padding_'+key;n[field]=value;n.get('internal_formulas',{}).pop(field,None);n.get('internal_toggles',{}).pop(field,None)
def scale_contents(n,sx,sy):
 for field in ['position_padding_left','position_padding_right','shape_width','bitmap_width','text_width']:
  if isinstance(n.get(field),(int,float)):n[field]*=sx
 for field in ['position_padding_top','position_padding_bottom','shape_height','bitmap_height']:
  if isinstance(n.get(field),(int,float)):n[field]*=sy
 for c in n.get('viewgroup_items',[]):scale_contents(c,sx,sy)
def rect_hit(x,y,w,h,events):
 n={'internal_type':'OverlapLayerModule','position_anchor':'CENTER','viewgroup_items':[{'internal_type':'ShapeModule','position_anchor':'CENTER','shape_type':'RECT','shape_width':w,'shape_height':h,'paint_color':'#00000000','internal_events':events}]};put(n,x,y);return n
for suffix in ['', '-off']:
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-live-data{suffix}-v0.9.2.klwp') as z:
  p=json.loads(z.read('preset.json'));r=p['preset_root']['viewgroup_items'];before=copy.deepcopy(r)
  def item(root,child):return r[root]['viewgroup_items'][child]
  def place(root,child,x,y,width=None):
   holder=item(root,child);put(holder,x,y)
   if width is not None:
    leaf=holder['viewgroup_items'][0]
    if leaf.get('internal_type')=='TextModule':leaf['text_width']=width
    elif 'shape_width' in leaf:leaf['shape_width']=width
  def plate(root,child,x,y,w,h,ow,oh):
   holder=item(root,child)
   for c in holder['viewgroup_items']:scale_contents(c,w/ow,h/oh)
   put(holder,x,y)
  for index in list(range(4,22))+[50]:
   root=r[index];formula(root,'config_scale_value','100*'+S);formula(root,'position_offset_x','0');formula(root,'position_offset_y','-80*'+S)
   root.update(config_rotate_mode='FLIP_Y',config_rotate_offset=-15)
  # The full-width rows share -280 / +280 edges, with 12-unit internal gutters.
  plate(5,1,0,-166,560,162,529.2,151.3)
  place(5,2,0,-86.5,560)
  place(5,3,-172,-194,176)
  place(6,1,230,-166)
  place(6,2,-252,-194)
  place(6,3,-24,-168)
  place(6,4,-24,-168)
  item(6,4)['viewgroup_items'][0]['text_expression']='系统'
  place(7,1,64,-205,216)
  place(7,2,68,-139,224)
  place(8,1,-172,-126,176);place(8,2,-172,-126,176)
  place(9,1,-172,-194,176)
  plate(10,1,-143,-15,274,112,235.5,110.4)
  plate(11,1,143,-15,274,112,247.968,105.55776)
  place(12,1,-143,-28,240)
  place(13,1,143,-28,240);place(13,2,143,17,240);place(13,3,193,-33)
  plate(14,1,0,118,560,126,487.9,114.9)
  place(15,1,88,78,384);place(15,2,88,78,384);place(15,3,98,78,340)
  place(16,1,-192,134,160);place(16,2,-12,134,168);place(16,3,180,134,176)
  plate(17,1,-182,255,196,120,210.2,113.1)
  plate(18,1,26,255,196,120,213.8,108.2)
  plate(19,1,208,255,144,120,148.8,116.9)
  place(20,1,-182,238,176)
  place(21,1,26,238,176);place(21,2,208,238,128);place(21,3,-27,283,66)
  # Status text and flanking rules stay within the same two outer edges.
  place(4,1,0,-347,252)
  place(4,2,-191,-313,132);place(4,3,-2,-313,132);place(4,4,187,-313,132)
  place(4,5,-270,-313);place(4,6,-81,-313);place(4,7,108,-313)
  place(4,8,-145,-347)
  place(4,9,-223,-347,106);place(4,10,213,-347,126)
  # Touch geometry receives exactly the same projected transform as the plates.
  settings_events=copy.deepcopy(item(50,0)['viewgroup_items'][0]['internal_events'])
  settings_events=[e for e in settings_events if e.get('switch') not in ['tapx','tapy','pulse']]
  r[50]['viewgroup_items']=[rect_hit(143,-15,274,112,settings_events)]
  # Keep this layout revision scoped to existing visual layers and the settings hit area.
  assert len(r)==len(before)==64
  for index in range(64):
   assert r[index].get('internal_animations')==before[index].get('internal_animations'),index
   if index not in list(range(4,22))+[50]:assert r[index]==before[index],index
  p['preset_info']['title']='Rhine UI · 终端排列对齐 v0.9.3'+(' · 无重力视差' if suffix else '')
  p['preset_info']['description']='终端页统一为同一透视平面、560 宽网格和12间距；收回超出屏幕的状态与入口，保留设备实时数据与原有动画。'
  target=OUT/f'Rhine-UI-menu-alignment{suffix}-v0.9.3.klwp'
  with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as dest:
   for name in z.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else z.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
  print(target)
