"""Measured menu geometry and independently timed native KLWP components."""
from pathlib import Path
from copy import deepcopy
import json,zipfile
from static_helpers import formula,walk,normalize_nested_positions
from refine_homepage import shape,at,label
BASE=Path(__file__).resolve().parents[1]
SOURCE=BASE/'output/perspective-v0.4/Rhine-UI-perspective-v0.4.klwp'
OUT=BASE/'output/matched-v0.5';OUT.mkdir(exist_ok=True)
with zipfile.ZipFile(SOURCE) as z:p=json.loads(z.read('preset.json'))
old=p['preset_root']['viewgroup_items']
from refine_home_matched import refine_home
glow=refine_home(old)
from refine_pages_matched import refine_pages
refine_pages(old)
for n in walk(old[10]):
    if n.get('text_expression')=='78':n['text_size']=100
    if n.get('text_expression')=='SATURDAY':n['text_size']=82
    if n.get('text_expression')=='2024.10.5':n['text_size']=42
# Reference dimming continues while the first panels appear.
shade=old[2]['internal_animations'][0]
shade['animator']=[{'position':0,'property':'OPACITY','value':100,'ease':'STRAIGHT'},{'position':100,'property':'OPACITY','value':0,'ease':'STRAIGHT'}]
formula(shade,'duration','if(gv(page)=1,3.6,1.8)')

S='mu(min,1,si(sheight)*720/si(swidth)/1600)'
SX=1.20
SHIFTS={3:48,4:30,5:30,6:58,7:88}

def placed(node,x,y):
    wrapper={'viewgroup_items':[at(node,x-100,y+80)]}
    normalize_nested_positions(wrapper)
    return wrapper['viewgroup_items'][0]

def calibrate(root,index):
    root['config_rotate_offset']=-15
    formula(root,'position_offset_x','135*'+S)
    formula(root,'position_offset_y',str(-145+SHIFTS[index])+'*'+S)
    def visit(node,is_root=False):
        if not is_root and node.get('shape_width')==720 and node.get('shape_height')==1600 and node.get('paint_color')=='#00000000':return
        for key in ['position_padding_left','position_padding_right','shape_width','bitmap_width','text_width']:
            if key in node:node[key]*=SX
        if index>=5 and node.get('internal_type')=='ShapeModule' and node.get('shape_height',0)>60:node['shape_height']*=1.12
        for child in node.get('viewgroup_items',[]):visit(child)
    visit(root,True)
    return root

# Correct fixture typography and add independently editable details before splitting the rows.
menu={i:deepcopy(old[i]) for i in range(3,8)}
for index,root in menu.items():
    for node in walk(root):
        text=node.get('text_expression')
        if text=='28':node['text_expression']='[i]37[/i]'
        if text=='电池 / °C':node['text_expression']='机温 / °C'
        if text=='CPU 12%     RAM 36%     SD 51%':node['text_expression']='CPU 57%     RAM 77%     SD 51%'
        if text=='2024/10/05 11:43':node['text_expression']='2024/10/5 11:43'
        if text in ['终端','搜索','设置','支付宝','付款码','扫一扫','微信']:
            node['text_expression']=text
            node['text_family']='kfile://org.kustom.provider/fonts/SourceHanSerifSC-Heavy.otf'
            node['text_size']*=1.05
            if index>=5:node['text_align']='LEFT'
            if index==6:node['text_size']*=1.18
phone=shape(75,111,'#FFC8CED0','M 9 0 L 91 0 Q 100 0 100 9 L 100 91 Q 100 100 91 100 L 9 100 Q 0 100 0 91 L 0 9 Q 0 0 9 0 Z M 10 9 L 90 9 L 90 84 L 10 84 Z M 45 93 L 55 93')
phone.update(paint_style='STROKE',paint_stroke=3)
menu[4]['viewgroup_items'].append(placed(phone,269,-239)) # 8
menu[4]['viewgroup_items'].append(placed(shape(145,90,'#FFD8DADC'),-42.5,-250)) # 9
chip=shape(29,30,'#FF686D70','M 23 23 L 77 23 L 77 77 L 23 77 Z M 38 38 L 62 38 L 62 62 L 38 62 Z M 0 30 L 20 30 M 0 50 L 20 50 M 0 70 L 20 70 M 80 30 L 100 30 M 80 50 L 100 50 M 80 70 L 100 70 M 30 0 L 30 20 M 50 0 L 50 20 M 70 0 L 70 20 M 30 80 L 30 100 M 50 80 L 50 100 M 70 80 L 70 100')
chip.update(paint_style='STROKE',paint_stroke=2)
menu[4]['viewgroup_items'].append(placed(chip,-111,-250)) # 10
menu[4]['viewgroup_items'].append(placed(shape(31,16,'#FF333940'),90,-219)) # 11
small=label('型号',29,10);menu[4]['viewgroup_items'].append(placed(small,90,-219)) # 12
point=shape(8,10,'#FFFFA928','M 50 0 L 100 50 L 50 100 L 0 50 Z');menu[5]['viewgroup_items'].append(placed(point,198,-94)) # 6
menu[6]['viewgroup_items'].append(placed(shape(282,30,'#FF172029'),151,18.5)) # 6
border=shape(282,30,'#FF06B9E7');border.update(paint_style='STROKE',paint_stroke=2)
menu[6]['viewgroup_items'].append(placed(border,151,18.5)) # 7
for node in walk(menu[6]['viewgroup_items'][2]):
    if node.get('internal_type')=='TextModule':node['text_size']=22;node['text_width']=235;node['text_align']='LEFT'
beta=label('BETA',55,12,'#FFFFA526');menu[7]['viewgroup_items'].append(placed(beta,42,213)) # 8
# Colored hardware glyphs supplement the text-only status row.
for x,color in [(-91,'#FF10C4DE'),(33,'#FFFF694C'),(181,'#FFFFCD32')]:
    glyph=deepcopy(chip);glyph.update(shape_width=17,shape_height=17,paint_color=color)
    menu[3]['viewgroup_items'].append(placed(glyph,x,-341))

def adjust(root,indices,cx,cy,sx,sy,dx,dy):
    cx-=100;cy+=80
    def resize(node):
        for k in ['shape_width','bitmap_width','text_width']:
            if k in node:node[k]*=sx
        for k in ['shape_height','bitmap_height','text_size']:
            if k in node:node[k]*=sy
        for c in node.get('viewgroup_items',[]):resize(c)
    for index in indices:
        node=root['viewgroup_items'][index]
        x=(node.get('position_padding_left',0)-node.get('position_padding_right',0))/2
        y=(node.get('position_padding_top',0)-node.get('position_padding_bottom',0))/2
        x=cx+(x-cx)*sx+dx;y=cy+(y-cy)*sy+dy
        node.update(position_padding_left=max(0,x*2),position_padding_right=max(0,-x*2),position_padding_top=max(0,y*2),position_padding_bottom=max(0,-y*2))
        resize(node)
# Correct each measured panel, including its independently animated contents.
adjust(menu[4],[8],269,-239,.7,.8,-20,0)
adjust(menu[4],list(range(1,13)),85.5,-226,1,.89,21,22)
adjust(menu[5],[1,2],-61,-72,.917,.966,-3,6)
adjust(menu[5],[3,4,5,6],183,-72,.84,.924,-26,5)
adjust(menu[7],[1,2],-86.5,185.5,1.16,.91,38,-57)
adjust(menu[7],[3,4,8],84.5,185.5,1.08,.87,60,-44)
adjust(menu[7],[5,6],244,185.5,1,.94,63,-40)
# The payment card's target strip sits above the final shortcut row.
adjust(menu[6],list(range(1,8)),92,55,.95,.95,14,-25)
# Bring the status date back inside the viewport and restore its reference reading size.
adjust(menu[3],[1],110,-379,1.05,1.15,-80,25)
for node in walk(menu[3]['viewgroup_items'][2]):
    if node.get('internal_type')=='TextModule':node['text_size']*=1.25


# Use separate status glyphs and labels so spacing does not depend on a long text string.
menu[3]['viewgroup_items']=menu[3]['viewgroup_items'][:1]
for text,x,y,w,size in [('2024/10/5 11:43',129,-395,210,25),('CPU 57%',-30,-366,110,25),('RAM 77%',156,-366,120,25),('SD 51%',310,-366,110,25)]:
    menu[3]['viewgroup_items'].append(placed(label(text,w,size),x,y))
cpu=deepcopy(chip);cpu.update(shape_width=20,shape_height=20,paint_color='#FF00B8E4')
menu[3]['viewgroup_items'].append(placed(cpu,-113,-366))
ram=shape(21,21,'#FFFF4564');ram.update(shape_type='CIRCLE',paint_style='STROKE',paint_stroke=3)
menu[3]['viewgroup_items'].append(placed(ram,73,-366))
sd=shape(21,25,'#FFFFCD32','M 20 0 L 100 0 L 100 100 L 0 100 L 0 20 Z')
menu[3]['viewgroup_items'].append(placed(sd,236,-366))
battery=shape(25,14,'#FFFFFFFF','M 0 0 L 84 0 L 84 100 L 0 100 Z M 84 30 L 100 30 L 100 70 L 84 70 M 18 18 L 45 18 L 45 82 L 18 82 Z')
battery.update(paint_style='STROKE',paint_stroke=2)
menu[3]['viewgroup_items'].append(placed(battery,0,-395))
for node in walk(menu[5]['viewgroup_items'][5]):
    if node.get('internal_type')=='TextModule':node['text_align']='LEFT';node['text_width']=193


# Text ink bounds in the reference are larger and sit above the panel midpoint.
for group,indices,scale,dy in [(5,[2,4],1.35,-14),(7,[2,4,6],1.5,-16),(6,[3,4,5],1.25,0)]:
    for idx in indices:
        node=menu[group]['viewgroup_items'][idx]
        y=(node.get('position_padding_top',0)-node.get('position_padding_bottom',0))/2+dy
        node.update(position_padding_top=max(0,2*y),position_padding_bottom=max(0,-2*y))
        for leaf in walk(node):
            if leaf.get('internal_type')=='TextModule':leaf['text_size']*=scale
for node in walk(menu[5]['viewgroup_items'][5]):
    if node.get('internal_type')=='TextModule':node['text_size']*=1.3

for i in menu:calibrate(menu[i],i)

def motion(duration,delay,kind):
    tracks={'OPACITY':[(0,100),(80,0),(100,0)]}
    if kind=='panel':tracks['X_OFFSET']=[(0,28),(65,3),(100,0)]
    elif kind=='text':tracks['Y_OFFSET']=[(0,7),(100,0)]
    elif kind=='number':tracks['SCALE_XY']=[(0,.88),(100,1)]
    elif kind=='button':tracks['X_OFFSET']=[(0,20),(100,0)]
    frames=[{'position':t,'property':prop,'value':value,'ease':'STRAIGHT'} for prop,values in tracks.items() for t,value in values]
    a={'type':'FORMULA','formula':'$gv(page)=1$','action':'ADVANCED','anchor':'MODULE_CENTER','duration':duration/100,'delay':delay/100,'ease':'STRAIGHT','animator':sorted(frames,key=lambda v:v['position'])}
    formula(a,'duration',f'if(gv(page)=1,{duration/100},1.6)')
    formula(a,'delay',f'if(gv(page)=1,{delay/100},0)')
    return a

# Delays are relative to the first dimming response; reference frames are spaced 40 ms.
specs=[
 (3,[1,2,3,4,5,6,7,8],'设备状态',220,0,'text'),
 (4,[1,7,9],'终端底板',240,40,'panel'),
 (4,[8,10,11,12],'设备线稿与小标',180,120,'text'),
 (4,[5,6],'终端标题',200,240,'text'),
 (4,[3,4],'温度标签',160,360,'text'),
 (4,[2],'温度数字',160,520,'number'),
 (5,[1],'搜索底板',220,120,'panel'),
 (5,[3],'设置底板',220,160,'panel'),
 (5,[2],'搜索文字',180,360,'text'),
 (5,[4,5,6],'设置文字与提示',180,400,'text'),
 (6,[1],'支付底板',220,160,'panel'),
 (6,[6,7,2],'支付标题条',180,240,'text'),
 (6,[3,4,5],'支付入口文字',180,280,'text'),
 (7,[1],'付款码底板',200,240,'button'),
 (7,[3],'扫一扫底板',200,400,'button'),
 (7,[5],'微信底板',200,520,'button'),
 (7,[2],'付款码文字',160,400,'text'),
 (7,[4,6,8],'扫一扫及微信文字',160,560,'text')]
parts=[]
for index,indices,title,duration,delay,kind in specs:
    root=deepcopy(menu[index]);root['internal_title']='主菜单 · '+title
    root['viewgroup_items']=[deepcopy(menu[index]['viewgroup_items'][0])]+[deepcopy(menu[index]['viewgroup_items'][j]) for j in indices]
    root['internal_animations']=[motion(duration,delay,kind)];parts.append(root)
# Static touch surfaces undergo exactly the same layout transform as their visual group.
for root in old[27:]:
    if root.get('internal_title','').startswith('交互区域 · 05 搜索'):
        
        # Existing geometry targets are all settings targets; transform around the settings center.
        adjust(root,list(range(len(root['viewgroup_items']))),183,-72,.84,.924,-26,5)
        calibrate(root,5)
roots=old[:3]+[old[9]]+parts+[old[8]]+[old[10],glow]+old[11:]
p['preset_root']['viewgroup_items']=roots
p['preset_info'].update(title='Rhine UI · 视频校准 v0.5',description='主菜单按清晰原动图校准尺寸与位置，拆分18组底板、文字、数字与图标动画。设备轮廓及标题条原生可编辑。继续参考重建，仍未达到逐像素一致。')
assert len(roots)<=64,len(roots)
(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8',newline='\n')
with zipfile.ZipFile(SOURCE) as source,zipfile.ZipFile(OUT/'Rhine-UI-matched-v0.5.klwp','w',zipfile.ZIP_DEFLATED) as target:
    target.writestr('preset.json',json.dumps(p,ensure_ascii=False))
    for name in source.namelist():
        if name!='preset.json':target.writestr(name,source.read(name))
    target.write(BASE/'assets/fonts/SourceHanSerifSC-Heavy.otf','fonts/SourceHanSerifSC-Heavy.otf')
    target.write(BASE/'assets/fonts/SourceHanSerif-LICENSE.txt','licenses/SourceHanSerif-LICENSE.txt')
(OUT/'menu-layer-timing.json').write_text(json.dumps([dict(group=s[0],components=s[1],title=s[2],duration_ms=s[3],delay_ms=s[4],kind=s[5]) for s in specs],ensure_ascii=False,indent=2),encoding='utf8')
print('Built',len(roots),'roots /',len(parts),'menu motion groups')
