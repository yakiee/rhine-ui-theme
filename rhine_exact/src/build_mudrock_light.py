"""Rebuild the Dock light using editable gradients and fading halftone rows."""
from pathlib import Path
import json
import math
import zipfile
from static_helpers import formula

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / 'output/dock-light-v0.8.3'
OUT = BASE / 'output/mudrock-light-v0.8.4'
OUT.mkdir(exist_ok=True)

def rect(width, height, color, title):
    return {'internal_type': 'ShapeModule', 'internal_title': title,
            'position_anchor': 'CENTER', 'shape_type': 'RECT',
            'shape_width': width, 'shape_height': height, 'paint_color': color}

def placed(item, x, y):
    return {'internal_type': 'OverlapLayerModule', 'position_anchor': 'CENTER',
            'position_padding_left': max(0, 2*x), 'position_padding_right': max(0, -2*x),
            'position_padding_top': max(0, 2*y), 'position_padding_bottom': max(0, -2*y),
            'viewgroup_items': [item]}

def tinted(item, rgb, opacity, dots=False):
    color = '#' + f'{round(255*opacity):02X}' + ''.join(f'{round(c):02X}' for c in rgb)
    item['paint_color'] = color
    expression = f'if(gv(style)=0,{color},ce(gv(accent),alpha,{opacity*100:.2f}))'
    if dots:
        expression = f'if(gv(dots),{expression},#00FFFFFF)'
    formula(item, 'paint_color', expression)
    return item

def make_light():
    layers = [rect(1060, 210, '#00000000', '光带动画尺寸基准')]
    # Overlapping low-alpha rectangles avoid seams while combining horizontal
    # orange/lime color with a nonlinear fade into the portrait above the edge.
    previous = 0
    for index in range(100):
        vertical = (index+1)/100
        target = .90*vertical**1.8
        opacity = (target-previous)/(1-previous)
        previous = target
        height = 130*(1-index/100)
        shape = rect(1060,height,'#00000000','橙黄至黄绿渐变')
        tinted(shape,(244,130,6),opacity)
        shape.update(fx_gradient='HORIZONTAL',fx_gradient_width=100,fx_gradient_offset=50)
        end_color = f'#{round(opacity*255):02X}ADCA05'
        formula(shape,'fx_gradient_color',f'if(gv(style)=0,{end_color},ce(gv(accent),alpha,{opacity*100:.2f}))')
        layers.append(placed(shape,0,25-height/2))
    for index in range(28):
        scale=1-index*.030
        shape=rect(690*scale,88*scale,'#00000000','中部饱和金黄光池')
        shape.update(shape_type='PATH',shape_path='M 0 50 a 50 50 0 1 0 100 0 a 50 50 0 1 0 -100 0 Z',shape_path_scale='FIT_XY')
        tinted(shape,(255,225,0),.035)
        layers.append(placed(shape,-45,-19))
    dots=[rect(1060,210,'#00000000','圆点定位范围')]
    pitch=14.2
    for row in range(12):
        vertical=(row+1)/12
        radius=1.48+1.16*vertical
        y=-95+row*10.6
        centers=[-524+column*pitch+(row%2)*pitch/2 for column in range(74)]
        centers=[center for center in centers if center+radius < 530]
        for start in range(0,len(centers),10):
            chunk=centers[start:start+10]
            horizontal=((chunk[0]+chunk[-1])/2+530)/1060
            pool=.80+.20*math.exp(-((horizontal-.53)/.33)**2)
            strength=min(.96,vertical**1.05*.96*pool)
            # Small concentric rims soften each point without whitening the gold underneath.
            for size,alpha in [(1.85,.09),(1.40,.18),(1.0,1)]:
                dot_radius=radius*size
                width=chunk[-1]-chunk[0]+2*dot_radius
                commands=[]
                for center in chunk:
                    x=(center-chunk[0]+dot_radius)/width*100
                    rx=dot_radius/width*100
                    commands.append(f'M {x-rx:.4f} 50 a {rx:.4f} 50 0 1 0 {2*rx:.4f} 0 a {rx:.4f} 50 0 1 0 {-2*rx:.4f} 0 Z')
                shape=rect(width,2*dot_radius,'#FFFFFFFF','柔边圆形网点')
                shape.update(shape_type='PATH',shape_path=' '.join(commands),shape_path_scale='FIT_XY')
                tinted(shape,(255,249,159),strength*alpha,True)
                dots.append(placed(shape,(chunk[0]+chunk[-1])/2,y))
    layers.append({'internal_type':'OverlapLayerModule','position_anchor':'CENTER',
                   'internal_title':'泥岩卡片 · 清晰柔边圆点','viewgroup_items':dots})
    return layers

for suffix in ['', '-off']:
    with zipfile.ZipFile(SOURCE/f'Rhine-UI-dock-light{suffix}-v0.8.3-release.klwp') as source:
        preset = json.loads(source.read('preset.json'))
        roots = preset['preset_root']['viewgroup_items']
        roots[24]['internal_title'] = 'Dock 泥岩卡片 · 橙黄绿光与柔边圆点'
        roots[24]['viewgroup_items'] = make_light()
        # Warm light reflects on the upper black face of the card, as in the reference.
        card = roots[23]
        card['viewgroup_items'][1]['paint_color'] = '#F51C1D1F'
        reflection = rect(720,228,'#91643B2C','黑色斜面上的棕红反光')
        reflection.update(shape_type='PATH',shape_path='M 3 0 L 100 0 L 100 86 L 96 100 L 0 100 L 0 14 Z',shape_path_scale='FIT_XY',fx_gradient='VERTICAL',fx_gradient_width=75,fx_gradient_offset=32,fx_gradient_color='#001C1D1F')
        formula(reflection,'shape_width','if(gv(page)=2,768,960)')
        formula(reflection,'paint_color','if(gv(style)=0,#91643B2C,ce(gv(accent),alpha,22))')
        card['viewgroup_items'].insert(2,reflection)
        preset['preset_info']['title'] = 'Rhine UI · 泥岩光带 v0.8.4'+(' · 静止版' if suffix else '')
        preset['preset_info']['description'] = '以用户提供的泥岩卡片为准：橙黄至黄绿色高饱和光带、清晰柔边圆点和黑色卡面暖色反光，保留原有交互。'
        output = OUT/f'Rhine-UI-mudrock-light{suffix}-v0.8.4.klwp'
        with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as target:
            for name in source.namelist():
                target.writestr(name, json.dumps(preset,ensure_ascii=False) if name=='preset.json' else source.read(name))
        if not suffix:
            (OUT/'preset.json').write_text(json.dumps(preset,ensure_ascii=False,indent=2),encoding='utf8')
        assert len(roots)==64
        assert [r for i,r in enumerate(roots) if i not in (23,24)] == [r for i,r in enumerate(json.loads(source.read('preset.json'))['preset_root']['viewgroup_items']) if i not in (23,24)]
        print(output.name, output.stat().st_size)
