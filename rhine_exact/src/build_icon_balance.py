"""Optically balance terminal watermarks without changing button hit areas."""
from pathlib import Path
import json
import zipfile

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / 'output/device-temperature-v0.13.31'
OUT = BASE / 'output/icon-balance-v0.13.32'
OUT.mkdir(exist_ok=True)

def position(node, x, y):
    node.update(position_padding_left=max(0, 2*x), position_padding_right=max(0, -2*x),
                position_padding_top=max(0, 2*y), position_padding_bottom=max(0, -2*y))

def watermark(roots, index):
    group = roots[index]['viewgroup_items'][1]['viewgroup_items'][0]
    if index in (6, 8, 14):
        group = group['viewgroup_items'][0]
    return group['viewgroup_items'][4]

for suffix in ('', '-off'):
    with zipfile.ZipFile(SOURCE / f'Rhine-UI-device-temperature{suffix}-v0.13.31.klwp') as source:
        preset = json.loads(source.read('preset.json'))
        roots = preset['preset_root']['viewgroup_items']
        # Shared optical height within each row; filled silhouettes need less area.
        settings = [
            (10, 90, 86, 71, 0, '#34616A6E', 3.5),
            (11, 82, 88, 69, 0, '#34616A6E', 3.5),
            (17, 84, 90, 40, 4, '#2E616A6E', None),
            (18, 108, 91, 47, 4, '#34616A6E', 3.5),
            (19, 68, 68, 7, 23, '#428F9799', 3.5),
            (6, 80, 64, -44, 0, '#38E4FBFF', 3.2),
            (8, 68, 64, -44, 0, '#38E4FBFF', 3.2),
        ]
        for index, width, height, x, y, color, stroke in settings:
            holder = watermark(roots, index)
            position(holder, x, y)
            icon = holder['viewgroup_items'][0]
            icon.update(shape_width=width, shape_height=height, paint_color=color)
            if stroke is not None:
                icon['paint_stroke'] = stroke
        alipay = watermark(roots, 14)
        position(alipay, 28, -8)
        alipay['viewgroup_items'][0].update(text_size=92, paint_color='#38E4FBFF')
        status = roots[4]['viewgroup_items']
        status[6]['viewgroup_items'][0].update(shape_width=28.8, shape_height=24, paint_stroke=2.2)
        status[7]['viewgroup_items'][0].update(shape_width=28.8, shape_height=24, paint_stroke=2.6)
        status[8]['viewgroup_items'][0].update(shape_width=23.4, shape_height=23)
        preset['preset_info'].update(
            title='Rhine UI · 图标比例协调 v0.13.32' + (' · 无重力视差' if suffix else ''),
            description='统一终端各行图标的视觉分量、线宽与留白，缩小偏大的背景水印，平衡 CPU/RAM/ROM 状态图标；功能、数据与动效保持原样。')
        target = OUT / f'Rhine-UI-icon-balance{suffix}-v0.13.32.klwp'
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as destination:
            for name in source.namelist():
                destination.writestr(name, json.dumps(preset, ensure_ascii=False) if name == 'preset.json' else source.read(name))
        if not suffix:
            (OUT / 'preset.json').write_text(json.dumps(preset, ensure_ascii=False, indent=2), encoding='utf-8')
        print(target)
