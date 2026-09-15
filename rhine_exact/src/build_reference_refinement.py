"""Refine Arknights-inspired hierarchy while preserving native theme actions."""
from pathlib import Path
import copy
import json
import zipfile

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / 'output/dock-number-v0.13.12'
OUT = BASE / 'output/reference-refinement-v0.13.15'
OUT.mkdir(exist_ok=True)
S = 'mu(min,1,si(sheight)*720/si(swidth)/1600)'


def walk(node):
    yield node
    for child in node.get('viewgroup_items', []):
        yield from walk(child)


def rect(w, h, color):
    return dict(internal_type='ShapeModule', position_anchor='CENTER', shape_type='RECT',
                shape_width=w, shape_height=h, paint_color=color)


def at(node, x, y):
    return dict(internal_type='OverlapLayerModule', position_anchor='CENTER',
                position_padding_left=max(0, 2*x), position_padding_right=max(0, -2*x),
                position_padding_top=max(0, 2*y), position_padding_bottom=max(0, -2*y),
                viewgroup_items=[node])


def group(children):
    return dict(internal_type='OverlapLayerModule', position_anchor='CENTER', viewgroup_items=children)


def vector(path, w, h, color, stroke=None):
    node = dict(internal_type='ShapeModule', position_anchor='CENTER', shape_type='PATH',
                shape_path=path, shape_path_scale='FIT_XY', shape_width=w, shape_height=h,
                paint_color=color)
    if stroke:
        node.update(paint_style='STROKE', paint_stroke=stroke)
    return node


for suffix in ['', '-off']:
    with zipfile.ZipFile(SOURCE / f'Rhine-UI-dock-number{suffix}-v0.13.12.klwp') as source:
        preset = json.loads(source.read('preset.json'))
        roots = preset['preset_root']['viewgroup_items']
        original_dock = copy.deepcopy(roots[23])
        terminal = roots[5]['viewgroup_items']
        # Offset accents belong to their cards and follow each card's pressure animation.
        terminal[2] = at(rect(286, 5.5, '#FFFF762E'), 95, -86)
        roots[17]['viewgroup_items'].append(at(rect(140, 5.5, '#FFFF762E'), -185, 199))
        # Reduce the numeral's multiple ghosted edges to one restrained cast shadow.
        numeral_group = terminal[12]['viewgroup_items'][0]
        numeral = numeral_group['viewgroup_items'][-1]
        shadow = copy.deepcopy(numeral)
        shadow.update(paint_color='#32000000', internal_title='数字轻投影')
        numeral_group['viewgroup_items'] = [at(shadow, 1, 1.2), numeral]
        wire = vector('M 42 0 L 77 11 L 100 39 L 83 67 L 51 81 L 25 100 L 29 66 L 0 41 L 13 14 Z M 42 0 L 29 66 L 77 11 L 83 67 L 13 14 L 51 81 L 0 41 L 100 39 L 25 100 M 13 14 L 100 39 M 0 41 L 83 67', 91, 113, '#BFFFFFFF', 1)
        plus = rect(35, 35, '#FF272B2E')
        plus['shape_type'] = 'CIRCLE'
        # Insert below the real-time numeral, after the grey backing.
        terminal[5] = group([at(wire, -218, -179), at(plus, -274, -192),
                             at(rect(17, 1.5, '#FFFFFFFF'), -274, -192),
                             at(rect(1.5, 17, '#FFFFFFFF'), -274, -192)])
        # Native clipping displays the user's current wallpaper without baking UI into an image.
        mask = rect(142, 137, '#FFFFFFFF')
        mask['fx_mask'] = 'CLIP_NEXT'
        bitmap = dict(internal_type='BitmapModule', position_anchor='CENTER', bitmap_width=288,
                      bitmap_height=640, bitmap_scale_mode='FIT_XY',
                      internal_toggles={'bitmap_bitmap': 10},
                      internal_formulas={'bitmap_bitmap': '$gv(wall)$'})
        label = dict(internal_type='TextModule', position_anchor='CENTER', text_expression='$tc(ell,si(model),16)$',
                     text_size=12, text_width=134, text_size_type='FIXED_WIDTH', text_lines=1, text_align='CENTER',
                     text_family='kfile://org.kustom.provider/fonts/Roboto-Regular.ttf', paint_color='#FFFFFFFF')
        terminal[4] = at(group([at(rect(146, 141, '#18000000'), 0, 2), mask, at(bitmap, 0, 120),
                                at(rect(142, 23, '#DE171B20'), 0, 57), at(label, 0, 57)]), 182, -168)
        sizes = {'系统': 56, '主题': 56, '电话': 49, '文件': 49, '微信': 40,
                 '支付宝': 39, '付款码': 39, '扫一扫': 39, '外观与交互': 22, '快捷支付': 22}
        for index in [5, 6, 8, 9, 10, 11, 14, 17, 18, 19]:
            for node in walk(roots[index]):
                if index != 5 and node.get('text_expression') in sizes:
                    node['text_size'] = sizes[node['text_expression']]
                if node.get('shape_type') == 'PATH':
                    if len(node.get('shape_path', '')) > 2000:
                        node['paint_color'] = '#10515A62'
                    elif node.get('paint_color') == '#22616A6E':
                        node['paint_color'] = '#1C616A6E'
                        node['shape_width'] *= 1.13
                        node['shape_height'] *= 1.05
        # Move the theme subtitle down slightly to retain separation from its larger heading.
        roots[11]['viewgroup_items'][3]['position_padding_top'] += 8
        # A cyan rim surrounds the inset shared black header, without changing its hit action.
        header = roots[9]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items'][0]
        header['viewgroup_items'][0].update(shape_width=372, shape_height=30, paint_color='#FF303336')
        header['viewgroup_items'].insert(0, rect(384, 36.74342, '#FF159FC6'))
        for index in [6, 14]:
            for node in list(walk(roots[index])):
                children = node.get('viewgroup_items', [])
                if any(c.get('paint_color') == '#65335D6B' for c in children):
                    edge = next(c for c in children if c.get('paint_color') == '#65335D6B')
                    edge['paint_color'] = '#58375E69'
                    children.append(at(rect(.7, edge['shape_height'], '#55DAF9FF'), -1, 0))
        # Tighten rows as units, retaining the large/small pair and the continuous payment strip.
        for index in [6, 8, 9, 14, 17, 18, 19]:
            old = roots[index]['internal_formulas']['position_offset_y'].strip('$')
            roots[index]['internal_formulas']['position_offset_y'] = f'$({old})-8*{S}$'
        hits = roots[50]['viewgroup_items'][1:]
        for index in list(range(18, 72)) + [77]:
            holder = hits[index]
            y = (holder.get('position_padding_top', 0)-holder.get('position_padding_bottom', 0))/2-8
            holder.update(position_padding_top=max(0, 2*y), position_padding_bottom=max(0, -2*y))
        assert roots[23] == original_dock
        assert len(roots) == 64
        preset['preset_info'].update(title='Rhine UI · 参考图层次校准 v0.13.15' + (' · 无重力视差' if suffix else ''),
                                     description='补充数字线框与壁纸面板，放大按钮标题，错位橙色短线，收紧行距与蓝色标题内边距，淡化均匀底纹。')
        target = OUT / f'Rhine-UI-refined{suffix}-v0.13.15.klwp'
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as dest:
            for name in source.namelist():
                dest.writestr(name, json.dumps(preset, ensure_ascii=False) if name == 'preset.json' else source.read(name))
        if not suffix:
            (OUT / 'preset.json').write_text(json.dumps(preset, ensure_ascii=False, indent=2), encoding='utf8')
        print(target)
