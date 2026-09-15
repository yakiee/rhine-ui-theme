"""Editable native paths give the reference home panels their missing depth."""
from copy import deepcopy
from static_helpers import formula, normalize_nested_positions, walk


def shape(width, height, color, path=None):
    node = {'internal_type': 'ShapeModule', 'position_anchor': 'CENTER',
            'shape_type': 'PATH' if path else 'RECT', 'shape_width': width,
            'shape_height': height, 'paint_color': color}
    if path:
        node.update(shape_path=path, shape_path_scale='FIT_XY')
    if color == 'accent':
        node['paint_color'] = '#FFFFC229'
        formula(node, 'paint_color', 'gv(accent)')
    return node


def at(node, x, y):
    node.update(position_offset_x=x, position_offset_y=y)
    return node


def label(value, width, size, color='#FFFFFFFF'):
    return {'internal_type': 'TextModule', 'position_anchor': 'CENTER',
            'text_expression': value, 'text_width': width, 'text_size': size,
            'text_size_type': 'FIXED_WIDTH', 'text_align': 'CENTER', 'text_lines': 1,
            'text_family': 'kfile://org.kustom.provider/fonts/Rajdhani-SemiBold.ttf',
            'paint_color': color}


def navigation(page):
    return [{'type': 'SINGLE_TAP', 'action': 'SWITCH_GLOBAL', 'switch': key,
             'switch_text': str(value)} for key, value in [('detail', 0), ('page', page)]]


def refine(preset):
    roots = preset['preset_root']['viewgroup_items']
    clock = roots[1]
    clock['internal_title'] = '01 透视时钟与斜切铭牌'
    bounds = shape(720, 1600, '#00000000')
    clock['viewgroup_items'] = [deepcopy(bounds)]
    items = clock['viewgroup_items']
    # The backplate and rules follow the reference's stepped, slanted silhouette.
    plate = at(shape(255, 88, '#B30C111B', 'M 0 23 L 100 0 L 92 80 L 0 100 Z'), -238, -580)
    plate['internal_events'] = navigation(1)
    items.append(plate)
    ellipse = 'M 50 0 C 78 0 100 22 100 50 C 100 78 78 100 50 100 C 22 100 0 78 0 50 C 0 22 22 0 50 0 Z'
    ring = shape(176, 193, '#62121921', ellipse)
    ring['internal_events'] = navigation(1)
    items.append(at(ring, -226, -622))
    outline = shape(176, 193, 'accent', ellipse)
    outline.update(paint_style='STROKE', paint_stroke=5)
    items.append(at(outline, -226, -622))
    items.append(at(label('11:43', 176, 55), -226, -622))
    items.append(at(label('AM', 120, 22), -226, -570))
    nameplate = at(shape(252, 49, '#A30C111B', 'M 0 0 L 100 0 L 92 100 L 0 100 Z'), -252, -485)
    nameplate['internal_events'] = navigation(1)
    items.append(nameplate)
    items.append(at(label('RHINE UI.KLWP', 224, 23), -251, -485))
    items.append(at(shape(232, 1.4, '#BFFFFFFF'), -258, -509))
    items.append(at(shape(216, 1.4, '#BFFFFFFF'), -266, -461))
    items.append(at(shape(18, 3, 'accent'), -171, -452))
    normalize_nested_positions(clock)

    sidebar = roots[9]
    sidebar['internal_title'] = '09 菱形层叠入口与侧面厚度'
    icons = [deepcopy(node) for node in walk(sidebar) if node.get('internal_type') == 'BitmapModule']
    sidebar['viewgroup_items'] = [deepcopy(bounds)]
    items = sidebar['viewgroup_items']
    # Top face, vertical body, and lower bevel remain separate editable paths.
    items.append(at(shape(122, 392, '#90000000', 'M 0 8 L 50 0 L 100 8 L 100 92 L 50 100 L 0 92 Z'), 254, 350))
    items.append(at(shape(116, 382, '#FF070B10', 'M 0 8 L 50 0 L 100 8 L 100 92 L 50 100 L 0 92 Z'), 251, 342))
    items.append(at(shape(108, 62, '#FF242932', 'M 50 0 L 100 50 L 50 100 L 0 50 Z'), 252, 186))
    items.append(at(shape(7, 316, 'accent'), 196, 358))
    items.append(at(shape(106, 40, 'accent', 'M 0 0 L 50 76 L 100 0 L 100 24 L 50 100 L 0 24 Z'), 252, 506))
    for index, (icon, page) in enumerate(zip(icons, [3, 4, 5, 2])):
        y = 266 + index * 64
        tile = shape(106, 60, '#FF1B2028' if index % 2 == 0 else '#FF262C35',
                     'M 50 0 L 100 50 L 50 100 L 0 50 Z')
        tile['internal_events'] = navigation(page)
        items.append(at(tile, 252, y))
        icon.update(bitmap_width=32, bitmap_height=32)
        icon['internal_events'] = navigation(page)
        items.append(at(icon, 252, y))
    normalize_nested_positions(sidebar)

    dock = roots[10]
    dock['internal_title'] = '10 斜向底栏与穿孔高亮边'
    old_items = dock['viewgroup_items']
    for node in walk(dock):
        if node.get('shape_type') == 'RECT' and node.get('paint_color') == '#F70B0F1A':
            node.update(shape_type='PATH', shape_path='M 3 0 L 100 0 L 100 86 L 96 100 L 0 100 L 0 14 Z', shape_path_scale='FIT_XY', paint_color='#F7090D14')
    # Replace the sparse dots with the reference's three-row perforated border.
    old_items[:] = [node for node in old_items if not any(
        part.get('shape_type') == 'CIRCLE' and part.get('shape_width') == 4
        for part in walk(node))]
    additions = [at(shape(720, 40, 'accent'), 0, -94)]
    for row in range(3):
        for column in range(60):
            dot = shape(3.6, 3.6, '#D9FFFFFF')
            dot['shape_type'] = 'CIRCLE'
            additions.append(at(dot, -353 + column * 12 + (row % 2) * 5, -107 + row * 12))
    additions.append(at(shape(720, 2, '#66000000'), 0, -73))
    additions_root = {'viewgroup_items': additions}
    normalize_nested_positions(additions_root)
    old_items[2:2] = additions_root['viewgroup_items']
