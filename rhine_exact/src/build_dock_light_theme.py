"""Rebuild the Dock light using editable gradients and fading halftone rows."""
from pathlib import Path
import json
import math
import zipfile
from static_helpers import formula

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / 'output/battery-v0.8.2'
OUT = BASE / 'output/dock-light-v0.8.3'
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
    # Keep the previous 1060 x 130 extent so the rotation and page morph keep their pivots.
    extent = rect(1060, 130, '#00000000', '光带动画尺寸基准')
    layers = [extent]
    # One native shader removes all joints between the previous gradient tiles.
    base = rect(1060, 90, '#00F1CD58', '连续透明至浅金渐变')
    base.update(fx_gradient='VERTICAL', fx_gradient_width=100,
                fx_gradient_offset=50, fx_gradient_color='#C8EEE777')
    formula(base, 'fx_gradient_color', 'if(gv(style)=0,#C8EEE777,ce(gv(accent),alpha,78))')
    layers.append(placed(base, 0, -20))
    # Low-opacity nested ellipses form local light pools without rectangular seams.
    for title, center, width, height, rgb in [
        ('左侧琥珀暖光', (-335, -9), 390, 66, (255, 148, 43)),
        ('中段浅金亮区', (70, 5), 590, 38, (255, 252, 180))]:
        for index in range(24):
            scale = 1-index*.035
            shape = rect(width*scale, height*scale, '#00000000', title)
            shape.update(shape_type='PATH', shape_path='M 0 50 a 50 50 0 1 0 100 0 a 50 50 0 1 0 -100 0 Z', shape_path_scale='FIT_XY')
            tinted(shape, rgb, .030 if index < 14 else .040)
            layers.append(placed(shape, *center))
    # Printed halftone: smaller, dimmer dots toward the transparent edge.
    dot_layers = []
    pitch = 9.5
    for row in range(9):
        vertical = (row+1)/9
        radius = .46+1.23*vertical
        y = -53+row*8.6
        centers = [-525+column*pitch+(row%2)*pitch/2 for column in range(111)]
        centers = [center for center in centers if center+radius < 530]
        for start in range(0,len(centers),12):
            chunk = centers[start:start+12]
            width = chunk[-1]-chunk[0]+2*radius
            height = 2*radius
            commands = []
            for center in chunk:
                x = (center-chunk[0]+radius)/width*100
                rx = radius/width*100
                commands.append(f'M {x-rx:.4f} 50 a {rx:.4f} 50 0 1 0 {2*rx:.4f} 0 a {rx:.4f} 50 0 1 0 {-2*rx:.4f} 0 Z')
            shape = rect(width,height,'#FFFFFFFF','渐隐半调网点')
            shape.update(shape_type='PATH',shape_path=' '.join(commands),shape_path_scale='FIT_XY')
            horizontal = ((chunk[0]+chunk[-1])/2+530)/1060
            pool = .60+.40*math.exp(-((horizontal-.58)/.30)**2)
            tinted(shape, (255,249,190), vertical**1.45*.76*pool, True)
            dot_layers.append(placed(shape,(chunk[0]+chunk[-1])/2,y))
    layers.append({'internal_type':'OverlapLayerModule','position_anchor':'CENTER',
                   'internal_title':'随光衰减的细网点', 'viewgroup_items':[rect(1060,130,'#00000000','网点定位范围')]+dot_layers})
    return layers

for suffix in ['', '-off']:
    with zipfile.ZipFile(SOURCE/f'Rhine-UI-battery{suffix}-v0.8.2.klwp') as source:
        preset = json.loads(source.read('preset.json'))
        roots = preset['preset_root']['viewgroup_items']
        roots[24]['internal_title'] = 'Dock 柔金光带 · 明日方舟半调材质'
        roots[24]['viewgroup_items'] = make_light()
        # The narrower band must land on the card edge after its horizontal morph.
        for track in roots[24]['internal_animations']:
            if track.get('formula') == '$gv(page)=2$':
                for key in track['animator']:
                    if key['property']=='Y_OFFSET' and key['position']==100:
                        key['value'] += 574-(536+25*80/130)

        preset['preset_info']['title'] = 'Rhine UI · 柔金光带 v0.8.3'+(' · 静止版' if suffix else '')
        preset['preset_info']['description'] = '参照明日方舟干员卡底部的橙金至浅黄柔光与渐隐网点；保留原生编辑、Dock 斜向切换、终端横线及三格电池。'
        output = OUT/f'Rhine-UI-dock-light{suffix}-v0.8.3-release.klwp'
        with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as target:
            for name in source.namelist():
                target.writestr(name, json.dumps(preset,ensure_ascii=False) if name=='preset.json' else source.read(name))
        if not suffix:
            (OUT/'preset.json').write_text(json.dumps(preset,ensure_ascii=False,indent=2),encoding='utf8')
        assert len(roots)==64
        assert [r for i,r in enumerate(roots) if i!=24] == [r for i,r in enumerate(json.loads(source.read('preset.json'))['preset_root']['viewgroup_items']) if i!=24]
        print(output.name, output.stat().st_size)
