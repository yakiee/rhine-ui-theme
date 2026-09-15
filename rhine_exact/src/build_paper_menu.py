"""Thin paper surfaces with soft cast shadows and a tighter status-to-menu gap."""
from pathlib import Path
import copy,json,re,zipfile
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/calendar-weather-v0.13.4';VERSION='0.13.5'
OUT=BASE/f'output/paper-menu-v{VERSION}';OUT.mkdir(exist_ok=True)
S='mu(min,1,si(sheight)*720/si(swidth)/1600)'
MENU=[5,6,8,9,10,11,14,17,18,19]

def group(children):return {'internal_type':'OverlapLayerModule','position_anchor':'CENTER','viewgroup_items':children}
def rect(w,h,color):return {'internal_type':'ShapeModule','position_anchor':'CENTER','shape_type':'RECT','shape_width':w,'shape_height':h,'paint_color':color}
def at(n,x,y):
 g=group([n]);g.update(position_padding_left=max(0,x*2),position_padding_right=max(0,-x*2),position_padding_top=max(0,y*2),position_padding_bottom=max(0,-y*2));return g

def walk(n):
 yield n
 for c in n.get('viewgroup_items',[]):yield from walk(c)

def formula(n,k,v):n.setdefault('internal_toggles',{})[k]=10;n.setdefault('internal_formulas',{})[k]='$'+v.strip('$')+'$'

def shadows(w,h):
 return [at(rect(w+spread,h+spread,f'#{alpha:02X}080D12'),0,2.5) for spread,alpha in [(10,4),(6,7),(2,13)]]

for suffix in ['', '-off']:
 with zipfile.ZipFile(SOURCE/f'Rhine-UI-staggered{suffix}-v0.13.4.klwp') as source:
  p=json.loads(source.read('preset.json'));r=p['preset_root']['viewgroup_items'];counts={'blue_faces':0,'white_faces':0,'dark_faces':0}
  for idx in [6,8,14]:
   for n in list(walk(r[idx])):
    children=n.get('viewgroup_items',[])
    if len(children)==8 and children[1].get('paint_color') in ['#FF129FC9','#FF129DC9','#FF1498C4']:
     face=children[1];w=face['shape_width'];h=face['shape_height']
     # Keep printed face, watermark and text; remove bevel highlights and side walls.
     n['viewgroup_items']=[*shadows(w,h),face,children[2],children[7]]
     if idx in [14,6]:n['viewgroup_items'].append(at(rect(.8,h,'#65335D6B'),w/2-.4,0))
     counts['blue_faces']+=1
  for idx in [5,10,11,17,18]:
   for n in list(walk(r[idx])):
    children=n.get('viewgroup_items',[])
    if len(children)==7 and children[3].get('paint_color')=='#EAF3F3F2':
     face=children[3];w=face['shape_width'];h=face['shape_height']
     n['viewgroup_items']=[*shadows(w,h),face,children[4],children[5]]
     counts['white_faces']+=1
  for n in list(walk(r[19])):
   children=n.get('viewgroup_items',[])
   if len(children)==1 and children[0].get('paint_color')=='#FF14171D':
    face=children[0];n['viewgroup_items']=[*shadows(face['shape_width'],face['shape_height']),face];counts['dark_faces']+=1
  assert counts=={'blue_faces':3,'white_faces':5,'dark_faces':1},counts
  for idx in MENU:
   old=r[idx]['internal_formulas']['position_offset_y'].strip('$');formula(r[idx],'position_offset_y',f'({old})-34*{S}')
   # A small paper deflection replaces the deeper key-like recoil.
   for a in r[idx].get('internal_animations',[]):
    if not re.fullmatch(r'\$gv\((?:pm|ps|pt|pp|pf|pw|bl|bc|br)\d\)=1\$',a.get('formula','')):continue
    for k in a['animator']:
     if k['property']=='SCALE_XY':k['value']=1+(k['value']-1)*.42
     elif k['property'] in ['X_OFFSET','Y_OFFSET','FLIP_X','FLIP_Y','OPACITY']:k['value']*=.42
  holders=r[50]['viewgroup_items'][1:]
  for index,h in enumerate(holders):
   if index<72 or index>=77:
    y=(h.get('position_padding_top',0)-h.get('position_padding_bottom',0))/2-34
    h.update(position_padding_top=max(0,y*2),position_padding_bottom=max(0,-y*2))
  p['preset_info'].update(title=f'Rhine UI · 纸片阴影 v{VERSION}'+(' · 无重力视差' if suffix else ''),description='去除按钮凸起亮边和厚侧面，保留薄纸片投影；菜单上移靠近时间与设备状态条，保留错落排布和独立点击。')
  target=OUT/f'Rhine-UI-paper{suffix}-v{VERSION}.klwp'
  with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as dest:
   for name in source.namelist():dest.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else source.read(name))
  if not suffix:(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
  print(target,counts)
