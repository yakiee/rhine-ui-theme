"""Build an editable native KLWP theme revision from the reviewed layout snapshot.
Timing ranges refer to observed frames; interpolation and unobserved exits remain estimates.
This generator does not overwrite its input or claim Android validation.
"""
from pathlib import Path
from copy import deepcopy
import json, math, re, zipfile
BASE=Path(__file__).resolve().parents[1]
WORK=BASE.parent
SOURCE=BASE/'src/preset-revision-wip.json'
# Relative dimensions depend on group scale and cause a circular zero scale in KLWP.
# Read device dimensions for fitting instead, including inherited layout formulas.
preset=json.loads(SOURCE.read_text(encoding='utf-8').replace('mu(min,si(rwidth)/720,si(rheight)/1600)', 'mu(min,1,si(sheight)*720/si(swidth)/1600)'))
source=deepcopy(preset['preset_root']['viewgroup_items'])
roots=[]
coverage=[]
S='mu(min,1,si(sheight)*720/si(swidth)/1600)'
G=preset['preset_root']['globals_list']
G['boot']={'index':max(v['index'] for v in G.values())+1,'type':'TEXT','title':'首页入口加载条件','value':'$gv(load)=1 & gv(prev)<=2 & gv(page)>=3 & gv(page)<=5$'}

def formula(item,field,value):
    item.setdefault('internal_toggles',{})[field]=10
    item.setdefault('internal_formulas',{})[field]=value if value.startswith('$') else '$'+value+'$'

def walk(item):
    yield item
    for child in item.get('viewgroup_items',[]):
        yield from walk(child)

def shift(item,dx,dy):
    if item.get('internal_title')=='显示条件':
        for child in item['viewgroup_items'][1:]:shift(child,dx,dy)
        return
    for field,delta in [('position_offset_x',dx),('position_offset_y',dy)]:
        if not delta:continue
        old=item.get('internal_formulas',{}).get(field)
        if old:formula(item,field,'('+old.strip('$')+')+'+str(delta))
        else:item[field]=item.get(field,0)+delta

def shape(x,y,w,h,color='#FF17191C'):
    item={'internal_type':'ShapeModule','shape_type':'RECT','shape_width':w,'shape_height':h,'paint_color':color,'position_anchor':'CENTER','position_offset_x':x-360+w/2,'position_offset_y':y-800+h/2}
    if color=='ink':formula(item,'paint_color','if(gv(dark),#FFF0F0F2,#FF17191C)')
    if color=='green':formula(item,'paint_color','if(gv(dark),#FFB4EF00,#FFAADE00)')
    return item

def transparent_copy(item):
    """Keep the native hit geometry while the visible copy animates independently of visibility."""
    result=deepcopy(item)
    if result.get('viewgroup_items') is not None:
        result['viewgroup_items']=[transparent_copy(n) for n in result['viewgroup_items']]
    for field in ['paint_color','bitmap_alpha']:
        result.get('internal_toggles',{}).pop(field,None)
        result.get('internal_formulas',{}).pop(field,None)
        result.get('internal_globals',{}).pop(field,None)
    result['paint_color']='#00000000'
    if result['internal_type']=='BitmapModule':result['bitmap_alpha']=0
    result.pop('internal_animations',None)
    return result

def key(position,prop,value):
    return {'position':round(position,4),'property':prop,'value':round(value,4),'ease':'STRAIGHT'}

def animation(condition,delay_ms,duration_ms,properties=None,exit_ms=200,loading_delay=False):
    tracks={'OPACITY':[(0,0),(min(100,4000/max(duration_ms,1)),100),(100,100)]}
    tracks.update(properties or {})
    frames=[key(t,prop,value) for prop,values in tracks.items() for t,value in values]
    anim={'type':'FORMULA','formula':'$'+condition+'$','action':'ADVANCED','duration':duration_ms/100,'delay':delay_ms/100,'ease':'STRAIGHT','anchor':'MODULE_CENTER','animator':sorted(frames,key=lambda n:(n['position'],n['property']))}
    delay=str(delay_ms/100)+('+if(gv(boot),20,0)' if loading_delay else '')
    formula(anim,'delay','if('+condition+','+delay+',0)')
    formula(anim,'duration','if('+condition+','+str(duration_ms/100)+','+str(exit_ms/100)+')')
    return anim

def layer(index,indices,name,condition,delay=0,duration=240,properties=None,pivot=(0,0),evidence='',confidence='observed_stages_estimated_interpolation',loading=False,exit_ms=200,extra=None):
    src=source[index]
    result=deepcopy(src)
    result['internal_title']=name
    result.pop('internal_animations',None)
    result.get('internal_toggles',{}).pop('config_visible',None)
    result.get('internal_formulas',{}).pop('config_visible',None)
    result['config_visible']='ALWAYS'
    original=src.get('viewgroup_items',[])
    chosen=range(1,len(original)) if indices is None else indices
    nodes=[deepcopy(original[n]) for n in chosen]
    nodes.extend(deepcopy(extra or []))
    for n in nodes:shift(n,-pivot[0],-pivot[1])
    bounds={'internal_type':'ShapeModule','shape_type':'RECT','shape_width':720,'shape_height':1600,'paint_color':'#00000000','position_anchor':'CENTER'}
    # Hit-only copies share the root transform, but are removed as soon as the page is inactive.
    hit_nodes=[]
    for n in nodes:
        if any(v.get('internal_events') for v in walk(n)):
            hit_nodes.append(transparent_copy(n))
        for child in walk(n):child.pop('internal_events',None)
    result['viewgroup_items']=[bounds]+nodes
    if hit_nodes:
        hits={'internal_type':'OverlapLayerModule','internal_title':'当前状态触摸区域','viewgroup_items':[deepcopy(bounds)]+hit_nodes}
        formula(hits,'config_visible','if('+condition+',ALWAYS,REMOVE)')
        result['viewgroup_items'].append(hits)
    for field,offset in [('position_offset_x',pivot[0]),('position_offset_y',pivot[1])]:
        old=result.get('internal_formulas',{}).get(field,'$'+str(result.get(field,0))+'$').strip('$')
        formula(result,field,'('+old+')+('+str(offset)+')*'+S)
    result['internal_animations']=[animation(condition,delay,duration,properties,exit_ms,loading)]
    roots.append(result)
    coverage.append({'source_group':index,'source_nodes':list(chosen),'pivot':list(pivot),'layer':name,'condition':condition,'source':evidence,'confidence':confidence,'start_ms':delay,'duration_ms':duration,'exit_ms':exit_ms,'exit_status':'measured envelope / estimated inverse trajectory' if evidence else 'unobserved estimate','loading_delay_ms':2000 if loading else 0,'properties':list(properties or {}),'implementation':'native KLWP advanced animation; runtime unverified'})
    return result

# Wallpaper stays a user-configurable bitmap; no synthetic replacement is bundled.
wall=deepcopy(source[0]);wall['bitmap_bitmap']='';roots.append(wall)
layer(1,None,'首页 · 时钟返回与退场','gv(page)<=2',0,200,{'SCALE_XY':[(0,94),(100,100)]},evidence='019 home/control; 01a wash-out',confidence='estimated; no independent unlock recording')
layer(2,None,'控制中心 · 背景压暗','gv(page)=1',0,200,evidence='019 f6–12 / f40–44')
layer(3,None,'控制中心 · 设备信息','gv(page)=1',40,200,{'X_OFFSET':[(0,24),(100,0)]},evidence='019 f8–16')
for index,label,start,span,pivot in [(4,'终端',40,320,(85,-227)),(5,'搜索设置',120,240,(69,-72)),(6,'支付栏',160,240,(92,55)),(7,'微信栏',200,280,(72,185))]:
    nodes=source[index]['viewgroup_items']
    bg=[n for n in range(1,len(nodes)) if nodes[n]['internal_type']!='TextModule']
    fg=[n for n in range(1,len(nodes)) if nodes[n]['internal_type']=='TextModule']
    layer(index,bg,'控制中心 · '+label+'卡面','gv(page)=1',start,span,{'SCALE_X':[(0,0),(60,96),(100,100)],'ROTATE':[(0,-2),(100,0)]},pivot,evidence='019 f8–24; per-card interpolation estimated',exit_ms=160)
    layer(index,fg,'控制中心 · '+label+'文字','gv(page)=1',start+160,200,{'X_OFFSET':[(0,14),(100,0)]},pivot,evidence='019 f12–24',exit_ms=120)
app=layer(8,None,'应用页 · 四列两行展开与回收','gv(page)=2',0,320,evidence='019 f53–61 / f75–77',exit_ms=160)
# Preserve the already measured application trajectory and the original local coordinate box.
app['viewgroup_items'][0]['shape_height']=400
for hit in app['viewgroup_items']:
    if hit.get('internal_title')=='当前状态触摸区域':hit['viewgroup_items'][0]['shape_height']=400
measured=json.loads((BASE/'src/native-motion-definitions.json').read_text(encoding='utf-8'))
app['internal_animations'][0]['animator']=measured['applications']['animator']
layer(9,None,'首页 · 功能侧栏展开与收起','gv(page)<=1',0,240,{'SCALE_Y':[(0,0),(100,100)],'Y_OFFSET':[(0,-28),(100,0)]},pivot=(268,370),evidence='019 f53–61 / f75–77')
dock=layer(10,None,'首页 · Dock角度与纵向联动','gv(page)<=2 & gv(dock)!=0',0,200,evidence='019 f53–61 / f75–77')
# Dock retains its 228-point local height; translation endpoint is measured, middle positions estimated.
dock['viewgroup_items'][0]['shape_height']=228
for hit in dock['viewgroup_items']:
    if hit.get('internal_title')=='当前状态触摸区域':hit['viewgroup_items'][0]['shape_height']=228
move=deepcopy(measured['dock'])
move['animator'] += [key(0,'Y_OFFSET',0),key(100,'Y_OFFSET',85)]
formula(move,'duration','if(gv(page)=2,3.2,1.6)')
dock['internal_animations'].append(move)
layer(11,None,'功能页 · 壁纸洗色底板','gv(page)>=3',0,240,evidence='018 f6–12; 01a f55–64')
layer(12,None,'功能页 · 返回线与导航标签','gv(page)>=3',160,200,{'SCALE_X':[(0,0),(100,100)]},evidence='01a f55–60',loading=True)
# Weather: the card opens sideways from a vertical slit, then the node graph arrives.
weather='gv(page)=3'
layer(13,[1,2,3],'天气 · 预报卡横向展开',weather,800,240,{'SCALE_X':[(0,0),(100,100)]},pivot=(0,-396.5),evidence='018 f26–32 relative to f6',loading=True,exit_ms=240)
layer(13,list(range(4,23)),'天气 · 温度节点与连接线',weather,1080,360,{'SCALE_X':[(0,0),(100,100)]},pivot=(0,-380),evidence='018 f33–42',loading=True,exit_ms=180)
layer(13,list(range(23,30)),'天气 · 翻页箭头与索引',weather,400,320,{'SCALE_X':[(0,0),(100,100)]},pivot=(0,-182),evidence='018 f16–24',loading=True,exit_ms=120)
layer(14,[1,2,11,12,13],'天气 · 空气指数中心',weather,560,400,{'SCALE_XY':[(0,0),(100,100)]},pivot=(0,110),evidence='018 f20–30',loading=True)
layer(14,list(range(3,11)),'天气 · 空气质量引线',weather,760,720,{'SCALE_X':[(0,0),(100,100)]},pivot=(0,135),evidence='018 f25–43',loading=True)
layer(14,list(range(14,22)),'天气 · 空气质量数值',weather,1080,920,{'OPACITY':[(0,0),(100,100)]},pivot=(0,135),evidence='018 f33–56',loading=True)
layer(15,None,'天气 · 当日温度与信息',weather,480,400,{'SCALE_Y':[(0,0),(100,100)]},pivot=(0,555),evidence='018 f18–28',loading=True)
layer(26,None,'天气 · 预警条绿色扫描',weather,1480,1240,{'SCALE_X':[(0,0),(10,100),(75,100),(100,0)],'OPACITY':[(0,0),(1,100),(99,100),(100,0)]},pivot=(0,442),evidence='018 f43–74',loading=True,exit_ms=80)
layer(16,[1],'天气 · 详情卡展开','gv(page)=3 & gv(detail)=1',0,240,{'SCALE_X':[(0,0),(100,100)]},pivot=(146.5,-396.5),evidence='01b f60–66',exit_ms=200)
layer(16,list(range(2,10)),'天气 · 详情文字分离','gv(page)=3 & gv(detail)=1',120,160,{'X_OFFSET':[(0,12),(100,0)]},pivot=(146.5,-396.5),evidence='01b f60–70',exit_ms=120)

# Music: temporary marks, cover, masked title, lyrics, transport and elapsed time are independent.
music='gv(page)=4'
guide=[]
for x,y in [(52,220),(658,220),(52,622),(658,622)]:guide.append(shape(x,y,8,8,'ink'))
for x in range(60,660,35):
    bar=shape(x,681,6,68,'ink');bar['shape_rotate_mode']='MANUAL';bar['shape_rotate_offset']=18;guide.append(bar)
layer(17,[],'音乐 · 定位点与斜纹遮罩',music,600,680,{'OPACITY':[(0,0),(6,100),(80,100),(100,0)],'SCALE_X':[(0,0),(30,100),(100,100)]},evidence='01c f21–38',loading=True,exit_ms=80,extra=guide)
layer(17,[1],'音乐 · 封面由横线展开',music,760,360,{'SCALE_Y':[(0,0),(100,100)]},pivot=(0,-391.5),evidence='01c f25–34',loading=True)
layer(17,[2,3,4,5],'音乐 · 曲名与歌手',music,920,360,{'X_OFFSET':[(0,16),(100,0)]},pivot=(0,-84),evidence='01c f29–38',loading=True,exit_ms=140)
# A native moving bar replaces a global fade for the text-reveal interval.
layer(17,[],'音乐 · 曲目信息扫掠遮罩',music,920,360,{'SCALE_X':[(0,1),(25,100),(65,100),(100,0)],'X_OFFSET':[(0,-306),(25,0),(65,0),(100,306)],'OPACITY':[(0,0),(1,100),(99,100),(100,0)]},pivot=(0,-84),evidence='01c f29–38; mask path estimated',loading=True,exit_ms=80,extra=[shape(54,653,612,123,'ink')])
layer(18,[1],'音乐 · 歌词区逐步出现',music,1160,800,{'OPACITY':[(0,0),(100,100)],'Y_OFFSET':[(0,18),(100,0)]},pivot=(0,204),evidence='01c f35–55; line sync remains external',loading=True)
layer(19,list(range(2,8)),'音乐 · 进度线与播放控制',music,1360,360,{'SCALE_X':[(0,0),(100,100)]},pivot=(0,530),evidence='01c f40–49',loading=True)
layer(19,[1],'音乐 · 播放时间显示',music,1880,280,evidence='01c f53–60',loading=True,exit_ms=100)
layer(19,[],'音乐 · 时间黑条扫掠',music,1760,600,{'SCALE_X':[(0,0),(35,100),(70,100),(100,0)],'X_OFFSET':[(0,-130),(35,0),(70,0),(100,130)],'OPACITY':[(0,0),(1,100),(99,100),(100,0)]},pivot=(163.5,450),evidence='01c f50–65',loading=True,exit_ms=80,extra=[shape(382,1223,283,54,'ink')])

# Calendar reveals by rows; year progress and the schedule card are not one moving bitmap.
cal='gv(page)=5'
layer(20,list(range(1,11)),'日历 · 月份与星期栏',cal,200,200,{'SCALE_X':[(0,0),(100,100)]},pivot=(0,-532),evidence='01a f55–60 after loader',loading=True)
for row in range(6):
    layer(20,list(range(11+28*row,11+28*(row+1))),'日历 · 第'+str(row+1)+'行日期',cal,240+row*80,240,{'SCALE_Y':[(0,0),(100,100)],'Y_OFFSET':[(0,-12),(100,0)]},pivot=(0,-460+row*69.5),evidence='01a f59–73; row boundaries estimated',loading=True,exit_ms=240)
layer(21,None,'日历 · 年进度卡横向展开',cal,720,400,{'SCALE_X':[(0,0),(100,100)]},pivot=(-150,210),evidence='01a f68–78',loading=True)
layer(22,[2,3,6,8,10],'日历 · 日程卡与边框',cal,760,360,{'SCALE_X':[(0,0),(100,100)]},pivot=(0,550),evidence='01a f69–78',loading=True)
layer(22,[1,4,5,7,9,11],'日历 · 日程文字与操作',cal,960,320,{'X_OFFSET':[(0,-16),(100,0)]},pivot=(0,550),evidence='01a f74–82',loading=True)

# Settings have static evidence only. Estimated row entry is clearly marked, not presented as measured.
layer(23,[1,2,3,4],'外观设置 · 页签','gv(page)=6',0,200,evidence='f_00000e static only',confidence='unobserved motion; provisional')
for section,indices in enumerate([range(5,17),range(17,26),range(26,38),range(38,49)]):
    layer(23,list(indices),'外观设置 · 选项组'+str(section+1),'gv(page)=6',80+section*60,200,{'SCALE_X':[(0,0),(100,100)]},evidence='f_00000e static only',confidence='unobserved motion; provisional')
layer(24,[1,2,3,4],'功能设置 · 页签','gv(page)=7',0,200,evidence='f_00000e static only',confidence='unobserved motion; provisional')
for section,indices in enumerate([range(5,16),range(16,27),range(27,35),range(35,43),range(43,53)]):
    layer(24,list(indices),'功能设置 · 选项组'+str(section+1),'gv(page)=7',80+section*60,200,{'SCALE_X':[(0,0),(100,100)]},evidence='f_00000e static only',confidence='unobserved motion; provisional')

# Loader uses a native one-shot keyframe envelope, not a visible page stuck behind a coarse timer.
boot='gv(boot)=1'
layer(25,[1],'入口加载 · 洗色背景',boot,0,2240,{'OPACITY':[(0,0),(15,100),(88,100),(100,0)]},evidence='01a f5–61',exit_ms=80)
layer(25,list(range(4,12)),'入口加载 · 扫描括号',boot,280,1720,{'OPACITY':[(0,0),(10,100),(20,100),(35,0),(100,0)],'SCALE_XY':[(0,55),(20,100),(100,100)]},evidence='01a f12–25',exit_ms=80)
layer(25,[12,13,14],'入口加载 · 标志',boot,560,1440,{'OPACITY':[(0,0),(10,100),(90,100),(100,0)]},evidence='01a f19–55; original mark asset missing',exit_ms=80)
layer(25,[2,3,18],'入口加载 · 终端文字',boot,760,1240,{'OPACITY':[(0,0),(20,100),(90,100),(100,0)],'SCALE_Y':[(0,0),(60,100),(100,100)]},evidence='01a f24–55; original terminal copy incomplete',exit_ms=80)
layer(25,[15,16,17,19],'入口加载 · 进度与跳过',boot,760,1240,{'OPACITY':[(0,0),(10,100),(90,100),(100,0)],'SCALE_X':[(0,0),(70,100),(100,100)]},pivot=(0,240),evidence='01a f24–55',exit_ms=80)
# Keep all navigation actions ordered and preserve the real source page for optional loading.
G['dest']={'index':max(v['index'] for v in G.values())+1,'type':'TEXT','title':'切换目标','value':'0'}
def switch(name,value):return {'type':'SINGLE_TAP','action':'SWITCH_GLOBAL','switch':name,'switch_text':value}
for root in roots:
    for node in walk(root):
        events=node.get('internal_events',[])
        navigation=[e for e in events if e.get('action')=='SWITCH_GLOBAL' and e.get('switch')=='page']
        if navigation:
            target=navigation[-1]['switch_text']
            rest=[e for e in events if not (e.get('action')=='SWITCH_GLOBAL' and e.get('switch') in ['page','prev','start','detail'])]
            node['internal_events']=[switch('dest',target),switch('prev','$if(gv(page)!=gv(dest),gv(page),gv(prev))$'),switch('start','$if(gv(page)!=gv(dest),df(S),gv(start))$'),switch('detail','0'),switch('page','$gv(dest)$')]+rest
        # Remove technical integration instructions from the theme's visible user interface.
        text=node.get('text_expression','')
        if '歌词尚未接入' in text:node['text_expression']='$gv(lyrics)$'
        if '暂无已接入的预警信息' in text:node['text_expression']='$gv(alert)$'
        if '天气、音乐、日历入场前显示扫描过渡' in text:node['text_expression']='从首页打开功能页时显示加载动画'
        if '可在全局变量中接入播放器' in text:node['text_expression']=''
        for field in ['bitmap_bitmap','background_bitmap']:
            if node.get(field,'').endswith(('/wallpaper.png','/weather-grid.png')):node[field]=''
        # Continuous state is bound to Android values; no recorded video replaces a live component.

# KLWP calls OPACITY 'Transparency': 100 is hidden. Scale uses a multiplier.
# Measurement tracks above stay in visible percentages; serialize once at the boundary.
for root in roots:
    for node in walk(root):
        for anim in node.get('internal_animations', []):
            for frame in anim.get('animator', []):
                if frame['property'] == 'OPACITY':
                    frame['value'] = round(100 - frame['value'], 4)
                elif frame['property'] in ['SCALE_X', 'SCALE_Y', 'SCALE_XY']:
                    frame['value'] = round(frame['value'] / 100, 6)

# Nested overlap items use padding, while root items use offsets.
# Centered padding displaces the visible item by half the padding difference.
def normalize_nested_positions(node):
    converted = []
    for child in node.get('viewgroup_items', []):
        child.setdefault('position_anchor', 'CENTER')
        placement = {'internal_type': 'OverlapLayerModule', 'internal_title': '定位容器',
                     'position_anchor': 'CENTER', 'viewgroup_items': [child]}
        shifted = False
        for axis, positive, negative in [('x', 'left', 'right'), ('y', 'top', 'bottom')]:
            field = 'position_offset_' + axis
            expression = child.get('internal_formulas', {}).pop(field, None)
            child.get('internal_toggles', {}).pop(field, None)
            value = child.pop(field, 0)
            if expression:
                shifted = True
                expression = expression.strip('$')
                formula(placement, 'position_padding_' + positive, 'mu(max,0,2*(' + expression + '))')
                formula(placement, 'position_padding_' + negative, 'mu(max,0,-2*(' + expression + '))')
            elif value:
                shifted = True
                placement['position_padding_' + positive] = max(0, 2 * value)
                placement['position_padding_' + negative] = max(0, -2 * value)
        normalize_nested_positions(child)
        converted.append(placement if shifted else child)
    if 'viewgroup_items' in node:
        node['viewgroup_items'] = converted

for root in roots:
    normalize_nested_positions(root)

# An empty bitmap resolves to KLWP's placeholder; hide it until the user binds an asset.
wall_child = deepcopy(roots[0])
wall_motion = wall_child.pop('internal_animations', [])
roots[0] = {'internal_type': 'OverlapLayerModule', 'internal_title': '原壁纸',
            'viewgroup_items': [wall_child], 'internal_animations': wall_motion}
formula(roots[0], 'config_visible', 'if(gv(wall)="",REMOVE,ALWAYS)')
preset['preset_root']['viewgroup_items']=roots
preset['preset_info']['title']='Rhine UI — native theme revision 0.3 (unfinished)'
preset['preset_info']['description']='安卓KLWP桌面主题返工版。全页面原生入退场分层；部分轨迹为推测。原壁纸及图标未绑定，原版字体未确认，页内翻页等仍待完成。尚未安卓运行验收，不是一比一完成版。'
preset['preset_info']['locked']=False
assert len(roots)<=64, len(roots)
out=BASE/'output/native-theme-v0.3'
out.mkdir(parents=True,exist_ok=True)
(out/'preset.json').write_text(json.dumps(preset,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
(BASE/'analysis/all-page-motion-coverage.json').write_text(json.dumps({'target':'Android KLWP live wallpaper / desktop theme','is_finished':False,'layers':coverage,'remaining':['原版壁纸、字体与图标资产','预报横移的连续插值和细节裁剪','逐行歌词同步与换曲动效','日历翻月与日期选中反馈','设置选项与深浅色切换的原版动效依据','原标志、动态虚化和逐字终端输出','原版持续循环及传感器响应参数','Android KLWP导入、数据与交互、快速往返切页、动画逐帧验收']},ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
text=json.dumps(preset,ensure_ascii=False)
paths=sorted(set(path.rstrip(chr(92)) for path in re.findall(r'kfile://org\.kustom\.provider/(bitmaps/[^"\s]+|fonts/[^"\s]+)',text)))
assets=WORK/'rhine_theme/assets'
missing=[]
with zipfile.ZipFile(out/'Rhine-UI-native-v0.3-unfinished.klwp','w',zipfile.ZIP_DEFLATED) as package:
    package.write(out/'preset.json','preset.json')
    for relative in paths:
        original=assets/Path(relative).name
        if original.is_file():package.write(original,relative)
        else:missing.append(relative)
    license_path=WORK/'rhine_theme/docs/Rajdhani-OFL.txt'
    if license_path.is_file():package.write(license_path,'licenses/OFL.txt')
print(json.dumps({'roots':len(roots),'animated_roots':len(coverage),'asset_files':len(paths),'missing_package_files':missing,'package':str(out/'Rhine-UI-native-v0.3-unfinished.klwp'),'runtime_validated':False},ensure_ascii=True))
