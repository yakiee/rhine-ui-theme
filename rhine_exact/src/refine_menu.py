"""Reconstruct the shared perspective plane of the Dock's expanded main menu."""
from static_helpers import formula

S = 'mu(min,1,si(sheight)*720/si(swidth)/1600)'


def refine_menu(preset):
    roots = preset['preset_root']['viewgroup_items']
    for index in range(3, 8):
        root = roots[index]
        root['internal_title'] += ' · 透视主菜单'
        # All menu rows share one vanishing point; text, plates and hit areas stay coplanar.
        root.update(config_rotate_mode='FLIP_Y', config_rotate_offset=-25)
        formula(root, 'position_offset_x', '110*'+S)
        formula(root, 'config_scale_value', '130*'+S)
        formula(root, 'position_offset_y', '-145*'+S)
        for child in root['viewgroup_items']:
            if (child.get('paint_color') == '#00000000'
                    and child.get('shape_width') == 720):
                continue
            x = (child.get('position_padding_left', 0)-child.get('position_padding_right', 0))/2-100
            y = (child.get('position_padding_top', 0)-child.get('position_padding_bottom', 0))/2+80
            child.update(position_padding_left=max(0, 2*x), position_padding_right=max(0, -2*x),
                         position_padding_top=max(0, 2*y), position_padding_bottom=max(0, -2*y))
