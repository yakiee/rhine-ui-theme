"""Reference home geometry and an independently animated soft Dock highlight."""
from copy import deepcopy
import math
from static_helpers import formula,walk,normalize_nested_positions
from refine_homepage import shape,at
S='mu(min,1,si(sheight)*720/si(swidth)/1600)'

def refine_home(roots):
    for root in roots:
        title=root.get('internal_title','')
        if title.startswith('01 ') or title.startswith('交互区域 · 01 '):
            formula(root,'position_offset_x','-12*'+S);formula(root,'position_offset_y','36*'+S)
            for n in walk(root):
                if n.get('shape_type')=='PATH' and n.get('shape_width')==176:n['shape_width']=202
                if n.get('text_expression')=='11:43':n['text_size']=80;n['text_width']=202
                if n.get('text_expression')=='AM':n['text_size']=26
                if n.get('text_expression')=='RHINE UI.KLWP':n['text_size']=28
                for event in n.get('internal_events',[]):
                    if event.get('switch') in ['tapx','tapy']:
                        try:event['switch_text']=str(float(event['switch_text'])+(-12 if event['switch']=='tapx' else 36))
                        except ValueError:pass
        if title.startswith('09 ') or title.startswith('交互区域 · 09 '):
            formula(root,'position_offset_y','-40*'+S)
            for child in root['viewgroup_items']:
                if child.get('shape_width')==720 and child.get('shape_height')==1600:continue
                y=(child.get('position_padding_top',0)-child.get('position_padding_bottom',0))/2
                y=342+(y-342)*.92
                child.update(position_padding_top=max(0,2*y),position_padding_bottom=max(0,-2*y))
                for n in walk(child):
                    if n.get('internal_type')=='ShapeModule' and 'shape_height' in n:n['shape_height']*=.92
                    for event in n.get('internal_events',[]):
                        if event.get('switch')=='tapy':
                            try:event['switch_text']=str(342+(float(event['switch_text'])-342)*.92-40)
                            except ValueError:pass
    dock=roots[10];angle=23.7
    dock['config_rotate_offset']=angle
    formula(dock,'position_offset_y','(633-if(gv(avoid),90,0))*'+S)
    for frame in dock['internal_animations'][1]['animator']:
        if frame['property']=='ROTATE':frame['value']*=angle/22.02
        if frame['property']=='Y_OFFSET':frame['value']*=55/85
    # Remove the opaque narrow strip and old dot row; retain all body modes and text.
    kept=[]
    for child in dock['viewgroup_items']:
        leaves=[n for n in walk(child) if n.get('internal_type')!='OverlapLayerModule']
        if any((n.get('shape_width')==720 and n.get('shape_height') in [2,8,40]) or (n.get('shape_type')=='CIRCLE' and n.get('shape_width')==3.6) for n in leaves):continue
        for n in leaves:
            if n.get('shape_width')==720 and n.get('shape_height')==228 and n.get('paint_color')!='#00000000':
                formula(n,'shape_width','if(gv(page)=2,768,960)')
        kept.append(child)
    dock['viewgroup_items']=kept
    for root in roots:
        if root.get('internal_title','').startswith('交互区域 · 10 '):
            formula(root,'config_rotate_offset','if(gv(page)=2,0,23.7)')
            formula(root,'position_offset_y','(if(gv(page)=2,688,633)-if(gv(avoid),90,0))*'+S)
            for n in walk(root):
                if n.get('shape_width')==720:formula(n,'shape_width','if(gv(page)=2,768,960)')
    # One editable path contains the perforations, avoiding hundreds of separate rendering nodes.
    items=[]
    for row in range(26):
        strip=shape(1060,5.2,'accent');formula(strip,'paint_color',f'ce(gv(accent),alpha,{min(94,8+row*4)})')
        items.append(at(strip,0,-62.5+row*5))
    commands=[];rx=3.9/1060*50;ry=3.9/130*50
    for row in range(10):
        for column in range(87):
            x=(9+column*12+(row%2)*6)/1060*100;y=(7+row*12)/130*100
            commands.append(f'M {x-rx:.4f} {y:.4f} a {rx:.4f} {ry:.4f} 0 1 0 {rx*2:.4f} 0 a {rx:.4f} {ry:.4f} 0 1 0 {-rx*2:.4f} 0 Z')
    dots=shape(1060,130,'#DEFFFFFF',' '.join(commands));formula(dots,'paint_color','if(gv(dots),#DEFFFFFF,#00FFFFFF)');items.append(dots)
    initial_x=math.sin(math.radians(angle))*139;initial_y=633-math.cos(math.radians(angle))*139
    glow={'internal_type':'OverlapLayerModule','internal_title':'Dock 渐变点阵 · 独立缩展','position_anchor':'CENTER','config_visible':'ALWAYS','config_rotate_mode':'MANUAL','config_rotate_offset':0,'viewgroup_items':items,'internal_animations':[deepcopy(dock['internal_animations'][0])]}
    formula(glow,'config_scale_value','100*'+S);formula(glow,'position_offset_x',str(initial_x)+'*'+S);formula(glow,'position_offset_y','('+str(initial_y)+'-if(gv(avoid),90,0))*'+S)
    normalize_nested_positions(glow)
    tracks={'ROTATE':[(0,angle),(100,0)],'X_OFFSET':[(0,0),(100,-initial_x)],'Y_OFFSET':[(0,0),(100,536-initial_y)],'SCALE_X':[(0,1),(100,768/1060)],'SCALE_Y':[(0,1),(100,80/130)]}
    animator=[{'position':t,'property':prop,'value':value,'ease':'STRAIGHT'} for prop,values in tracks.items() for t,value in values]
    glow['internal_animations'].append({'type':'FORMULA','formula':'$gv(page)=2$','action':'ADVANCED','anchor':'MODULE_CENTER','duration':3.2,'delay':0,'ease':'STRAIGHT','animator':animator})
    return glow
