"""Editable detail pass based on reference posters and the music transition GIF."""
from pathlib import Path
from copy import deepcopy
import json,zipfile,math
from static_helpers import walk,formula,normalize_nested_positions
from refine_homepage import shape,at,label
from refine_pages_matched import placed,rect,text,shift
BASE=Path(__file__).resolve().parents[1];SOURCE=BASE/'output/matched-v0.5/Rhine-UI-matched-v0.5.klwp';OUT=BASE/'output/details-v0.6';OUT.mkdir(exist_ok=True)
with zipfile.ZipFile(SOURCE) as z:p=json.loads(z.read('preset.json'))
roots=p['preset_root']['viewgroup_items']
def find(prefix):return next(r for r in roots if r.get('internal_title','').startswith(prefix))
def native_text(x,y,w,size,value,color='#FF202329',lines=1,bold=False):
 n=label(('[b]'+value+'[/b]') if bold else value,w/.47,size*2,color);n.pop('text_family',None);n['text_lines']=lines;n['text_align']='LEFT';return placed(n,x,y)
def line(points,color='#FF303337',thickness=1):
 xs=[v[0] for v in points];ys=[v[1] for v in points];x0=min(xs);y0=min(ys);w=max(xs)-x0;h=max(ys)-y0
 if h==0:return rect(x0+w/2,y0,w,thickness,color)
 path='M '+' L '.join(f'{(x-x0)/max(w,.1)*100:.4f} {(y-y0)/max(h,.1)*100:.4f}' for x,y in points)
 n=shape(max(w,.1)/.47,max(h,.1)*2,color,path);n.update(paint_style='STROKE',paint_stroke=thickness*2);return placed(n,x0+w/2,y0+h/2)
def circle(x,y,size,color):
 n=shape(size/.47,size*2,color);n['shape_type']='CIRCLE';return placed(n,x,y)
# Rebuild the complete AQI graphic from the legible product poster, not placeholder copy.
aqi=find('14 ');bounds=deepcopy(aqi['viewgroup_items'][0]);leaf=deepcopy(aqi['viewgroup_items'][13]);items=[bounds]
items += [rect(180,374,82,16,'#FF202329'),native_text(180,374,74,10,'空气指数 26','#FFFFFFFF')]
for pts in [[(30,408),(132,408),(160,435)],[(232,420),(332,420)],[(201,438),(232,420)],[(30,503),(132,503),(157,489)],[(202,492),(234,520),(332,520)]]:items.append(line(pts,thickness=.85))
items += [circle(180,464,62,'#FF272A2D')]
# Keep the existing editable bitmap leaf; its normalized position was already measured.
items.append(leaf)
for x,y in [(158,435),(202,438),(157,491),(203,492)]:items.append(circle(x,y,4.3,'#FF25292B'))
copy=[('NO₂  13',30,400,'At short-term concentrations above 200 µg/m³, NO₂ is a toxic gas that causes severe inflammation of the respiratory tract.',416,5.05),('SO₂  8',232,412,'SO₂ affects respiratory and lung function and irritates the eyes. Inflammation of the respiratory tract leads to coughing, mucus secretion, worsening asthma and chronic bronchitis.',438,5.05),('PM₂.₅  5',30,495,'PM₂.₅ is easy to carry heavy metals, microorganisms and other harmful substances, which has a greater impact on human health.',518,5.05),('PM₁₀  13',232,512,'The main sources of PMs are construction activities and dust raised from the earth, containing oxide minerals and other components.',539,5.05)]
for value,x,y,paragraph,py,size in copy:
 items += [native_text(x+49,y,100,18,value,bold=True),native_text(x+73,y+3,27,8,'µg/m³'),native_text(x+50,py,100,size,paragraph,lines=5)]
aqi['viewgroup_items']=items
# Replace font-dependent square glyphs with five bordered native page markers and side rules.
forecast=find('13 ')
for n in walk(forecast):
 if '▣' in n.get('text_expression',''):n['text_expression']=''
forecast['viewgroup_items'] += [line([(29,333),(124,333)],'#FF616467',.65),line([(233,333),(333,333)],'#FF616467',.65)]
for i in range(5):
 n=shape(8/.47,8*2,'#FF25292B');n.update(paint_style='STROKE',paint_stroke=2.4);forecast['viewgroup_items'].append(placed(n,150+i*15,333))
# Restore the reference warning punctuation and temperature label.
weather=find('15 ')
weather['viewgroup_items'] += [rect(52,639,2.2,7,'#FF202329'),circle(52,645,2.2,'#FF202329')]
for n in walk(weather):
 if n.get('text_expression')=='[b]21[/b]':n.pop('text_family',None);n['text_expression']='[b][i]21[/i][/b]';n['text_size']=96;n['text_width']=190
 if n.get('text_expression')=='RHINE WEATHER':n['text_expression']='DEGREES CELSIUS'
# Preserve the tap-to-select calendar while matching the heavier reference type and weekday outlines.
calendar=find('20 ')
for n in walk(calendar):
 value=n.get('text_expression','')
 if value.isdigit() and 1<=int(value)<=31:
  n.pop('text_family',None);n['text_expression']='[b]'+value+'[/b]';n['text_size']=28
 if 'OCTOBER' in value:n.pop('text_family',None);n['text_size']=42
for day in [4,5,11,12]:
 # Each date uses four editable siblings: cell, date text, outline and event mark.
 for j,node in enumerate(calendar['viewgroup_items']):
  if any(n.get('text_expression')=='[b]'+str(day)+'[/b]' for n in walk(node)) and j+1<len(calendar['viewgroup_items']):
   border=calendar['viewgroup_items'][j+1];border['config_visible']='ALWAYS';border.get('internal_formulas',{}).pop('config_visible',None);border.get('internal_toggles',{}).pop('config_visible',None)
   for n in walk(border):
    if n.get('paint_style')=='STROKE':
     n['paint_color']='#FF25292B';n.get('internal_formulas',{}).pop('paint_color',None);n.get('internal_toggles',{}).pop('paint_color',None)
# Native shadow behind the year arrow, preserving every existing touch layer.
year=find('21 ');plate=deepcopy(year['viewgroup_items'][1]);shift(plate,12)
for n in walk(plate):
 if n.get('shape_type')=='PATH':n['paint_color']='#33606468';n.pop('internal_formulas',None);n.pop('internal_toggles',None)
year['viewgroup_items'].insert(1,plate)
# Rebuild the music subtitle/lyrics with readable type and the five visible reference rows.
music=find('17 ');lyrics=find('18 ');control=find('19 ')
# FIT_XY is not a supported KLWP bitmap mode. Keep the photo's aspect ratio and reveal its top edge.
for n in walk(music):
 if n.get('bitmap_bitmap')=='kfile://org.kustom.provider/bitmaps/reference-music.png':n['bitmap_scale_mode']='FIT_WIDTH'
 if n.get('position_padding_top')==746.0:n['position_padding_top']=826.0
original=deepcopy(music);music['viewgroup_items']=music['viewgroup_items'][:2]
heading=deepcopy(original);heading['internal_title']='17b 曲名与歌手 · 独立进入';heading['viewgroup_items']=[deepcopy(bounds),native_text(180,353,300,16,'青春コンプレックス',bold=True),native_text(180,377,300,11,'結束バンド')]
lyrics['viewgroup_items']=[deepcopy(bounds)]
for value,y,color in [('どうしようもなく愛を欲してた',448,'#44565A5D'),('雨に濡れるのが好きだった',473,'#55606468'),('曇った顔が似合うから',501,'#FF272A2D'),('嵐に怯えてるフリをして',527,'#55606468'),('空が割れるのを待っていた',552,'#44565A5D')]:lyrics['viewgroup_items'].append(native_text(180,y,300,12,value,color,bold=y==501))
# Thin waveform strokes are editable vectors. They represent the reference preview, not live audio.
wave=deepcopy(lyrics);wave['internal_title']='18b 音乐细线波形';wave['viewgroup_items']=[deepcopy(bounds)]
for phase in [0,1.2,2.7]:
 pts=[(36+i*2.8,412+math.sin(i*.21+phase)*5*math.exp(-i/50)) for i in range(102)];wave['viewgroup_items'].append(line(pts,'#5A373D41',.4))
wave['viewgroup_items'].append(circle(36,412,4,'#FF33383A'))
# The reference switches out the weather page, shows a hatch wipe, then expands the album.
def enter(root,delay,duration,kind):
 condition='gv(page)=4 & gv(loading)=0'
 frames=[{'position':0,'property':'OPACITY','value':100,'ease':'STRAIGHT'},{'position':100,'property':'OPACITY','value':0,'ease':'STRAIGHT'}]
 if kind=='cover':frames += [{'position':0,'property':'SCALE_Y','value':.015,'ease':'STRAIGHT'},{'position':100,'property':'SCALE_Y','value':1,'ease':'STRAIGHT'}]
 elif kind=='text':frames += [{'position':0,'property':'Y_OFFSET','value':10,'ease':'STRAIGHT'},{'position':100,'property':'Y_OFFSET','value':0,'ease':'STRAIGHT'}]
 a={'type':'FORMULA','formula':'$'+condition+'$','action':'ADVANCED','anchor':'MODULE_CENTER','duration':duration/100,'delay':delay/100,'animator':frames}
 formula(a,'duration',f'if({condition},{duration/100},1.6)');formula(a,'delay',f'if({condition},{delay/100},0)');root['internal_animations']=[a]
# Preserve the reference bitmap crop; offset compensates scaling about the full-canvas pivot.
music['viewgroup_items']=deepcopy(original['viewgroup_items'][:2])
enter(music,800,200,'cover');enter(heading,1120,220,'text');enter(lyrics,1180,280,'text');enter(wave,1020,180,'text');enter(control,1360,280,'text')
music['internal_animations'][0]['animator'] += [{'position':0,'property':'Y_OFFSET','value':-365.9275,'ease':'STRAIGHT'},{'position':100,'property':'Y_OFFSET','value':0,'ease':'STRAIGHT'}]
# Transient hatch and four corner registration marks, disappearing once the music page settles.
def transient(title,items,cx,cy,tracks,delay,duration):
 r={'internal_type':'OverlapLayerModule','internal_title':title,'position_anchor':'CENTER','viewgroup_items':items};formula(r,'config_scale_value','100*mu(min,1,si(sheight)*720/si(swidth)/1600)');formula(r,'position_offset_x',f'{cx}*mu(min,1,si(sheight)*720/si(swidth)/1600)');formula(r,'position_offset_y',f'{cy}*mu(min,1,si(sheight)*720/si(swidth)/1600)')
 frames=[{'position':t,'property':prop,'value':value,'ease':'STRAIGHT'}for prop,values in tracks.items()for t,value in values]
 a={'type':'FORMULA','formula':'$gv(page)=4$','action':'ADVANCED','anchor':'MODULE_CENTER','animator':frames};formula(a,'duration',f'if(gv(page)=4,{duration/100},.01)');formula(a,'delay',f'if(gv(page)=4,{delay/100},0)');r['internal_animations']=[a];return r
w=306/.47;h=38*2;commands=[]
for i in range(17):
 x=i*6;commands.append(f'M {x} 100 L {x+1.4} 100 L {x+4} 0 L {x+2.6} 0 Z')
hatches=[]
for quarter in range(4):
 commands=[]
 for i in range(4):
  x=i*25;commands.append(f'M {x} 100 L {x+6} 100 L {x+16} 0 L {x+10} 0 Z')
 duration=320+quarter*100
 hatches.append(transient('音乐入场 · 斜纹擦除 '+str(quarter+1),[shape(w/4,h,'#FF202329',' '.join(commands))],(-114.75+quarter*76.5)/.47,-73,{'OPACITY':[(0,100),(40/duration*100,0),((duration-70)/duration*100,0),(100,100)]},650,duration))
markeritems=[shape(306/.47,402,'#00000000')]
for x in [-153/.47,153/.47]:
 for y in [-201,201]:
  holder={'viewgroup_items':[at(shape(5/.47,10,'#FF202329'),x,y)]};normalize_nested_positions(holder);markeritems.extend(holder['viewgroup_items'])
marks=transient('音乐入场 · 四角定位',markeritems,0,-375,{'OPACITY':[(0,100),(10,0),(85,0),(100,100)],'SCALE_Y':[(0,.02),(40,.02),(85,1),(100,1)]},650,650)
idx=roots.index(music);roots[idx+1:idx+1]=[heading,wave,*hatches,marks]
for n in walk(p['preset_root']):
 if n.get('bitmap_bitmap')=='kfile://org.kustom.provider/bitmaps/reference-music.png':n['bitmap_bitmap']='kfile://org.kustom.provider/bitmaps/reference-music-v06.png'
p['preset_info'].update(title='Rhine UI · 细节校准 v0.6',description='空气质量图、天气页码、日历字体与边框、音乐分层入场及斜纹擦除；可编辑预览数据，素材及部分动效仍有差异。')
assert len(roots)<=64,len(roots)
(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8',newline='\n')
with zipfile.ZipFile(SOURCE)as z,zipfile.ZipFile(OUT/'Rhine-UI-details-v0.6.klwp','w',zipfile.ZIP_DEFLATED)as target:
 for name in z.namelist():target.writestr('bitmaps/reference-music-v06.png' if name=='bitmaps/reference-music.png' else name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else (BASE/'analysis/frames/f_00001c/070.png').read_bytes() if name=='bitmaps/reference-music.png' else z.read(name))
print('Built',len(roots),'roots')
