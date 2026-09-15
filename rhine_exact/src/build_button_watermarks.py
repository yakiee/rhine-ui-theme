"""Give the second and third menu rows function-specific native watermarks."""
from pathlib import Path
import json
import zipfile

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / 'output/battery-cells-v0.13.21'
OUT = BASE / 'output/button-watermarks-v0.13.23'
OUT.mkdir(exist_ok=True)


def vector(path, width, height, color, stroke=None):
    node = dict(internal_type='ShapeModule', position_anchor='CENTER', shape_type='PATH',
                shape_path=path, shape_path_scale='FIT_XY', shape_width=width,
                shape_height=height, paint_color=color)
    if stroke:
        node.update(paint_style='STROKE', paint_stroke=stroke)
    return node


CHIP = 'M 22 22 L 78 22 L 78 78 L 22 78 Z M 35 35 L 65 35 L 65 65 L 35 65 Z M 32 4 L 32 22 M 50 4 L 50 22 M 68 4 L 68 22 M 32 78 L 32 96 M 50 78 L 50 96 M 68 78 L 68 96 M 4 32 L 22 32 M 4 50 L 22 50 M 4 68 L 22 68 M 78 32 L 96 32 M 78 50 L 96 50 M 78 68 L 96 68'
PALETTE = 'M 49 5 C 22 5 5 23 5 50 C 5 78 24 95 49 95 C 61 95 66 86 58 80 C 51 74 55 65 65 65 L 77 65 C 102 65 100 39 85 22 C 75 10 62 5 49 5 Z M 27 27 m -5 0 a 5 5 0 1 0 10 0 a 5 5 0 1 0 -10 0 M 49 19 m -5 0 a 5 5 0 1 0 10 0 a 5 5 0 1 0 -10 0 M 72 29 m -5 0 a 5 5 0 1 0 10 0 a 5 5 0 1 0 -10 0 M 22 51 m -5 0 a 5 5 0 1 0 10 0 a 5 5 0 1 0 -10 0'
BARCODE = ' '.join(f'M {x} 12 L {x+w} 12 L {x+w} 88 L {x} 88 Z' for x,w in [(5,4),(12,2),(18,7),(28,3),(35,5),(43,2),(50,7),(60,3),(67,6),(77,2),(83,4),(91,4)])
SCAN = 'M 24 3 L 3 3 L 3 24 M 76 3 L 97 3 L 97 24 M 3 76 L 3 97 L 24 97 M 76 97 L 97 97 L 97 76 M 22 22 L 42 22 L 42 42 L 22 42 Z M 58 22 L 78 22 L 78 42 L 58 42 Z M 22 58 L 42 58 L 42 78 L 22 78 Z M 58 58 L 68 58 L 68 68 L 78 68 L 78 78 M 58 78 L 58 68 M 12 50 L 88 50'

for suffix in ['', '-off']:
    with zipfile.ZipFile(SOURCE / f'Rhine-UI-battery-cells{suffix}-v0.13.21.klwp') as source:
        preset = json.loads(source.read('preset.json'))
        roots = preset['preset_root']['viewgroup_items']
        for index, path, title in [(10, CHIP, '系统芯片'), (11, PALETTE, '主题调色盘')]:
            mark_holder = roots[index]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items'][4]
            mark_holder['internal_title'] = title + ' · 淡色背景水印'
            mark_holder['viewgroup_items'] = [vector(path, 101, 96, '#34616A6E', 4)]
        for index, path, title in [(6, BARCODE, '付款条形码'), (8, SCAN, '扫描框与二维码')]:
            mark_holder = roots[index]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items'][0]['viewgroup_items'][4]
            mark_holder['internal_title'] = title + ' · 淡色背景水印'
            mark_holder['viewgroup_items'] = [vector(path, 97 if index==6 else 69, 64, '#39E4FBFF', None if index==6 else 3)]
        alipay = roots[14]['viewgroup_items'][1]['viewgroup_items'][0]['viewgroup_items'][0]['viewgroup_items'][4]
        alipay['internal_title'] = '支付宝支字 · 淡色背景水印'
        alipay['viewgroup_items'] = [dict(internal_type='TextModule', position_anchor='CENTER',
                                         text_expression='支', text_size=91, text_width=113,
                                         text_size_type='FIXED_WIDTH', text_lines=1, text_align='CENTER',
                                         text_family='kfile://org.kustom.provider/fonts/SourceHanSerifSC-Heavy.otf',
                                         paint_color='#35E4FBFF')]
        preset['preset_info'].update(title='Rhine UI · 功能对应水印 v0.13.23' + (' · 无重力视差' if suffix else ''),
                                     description='第2行系统芯片/主题调色盘，第3行支付宝支字/付款条码/扫一扫扫描框；保留布局、纸片材质和原点击动作。')
        target = OUT / f'Rhine-UI-watermarks{suffix}-v0.13.23.klwp'
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as dest:
            for name in source.namelist():
                dest.writestr(name, json.dumps(preset,ensure_ascii=False) if name=='preset.json' else source.read(name))
        if not suffix:
            (OUT/'preset.json').write_text(json.dumps(preset,ensure_ascii=False,indent=2),encoding='utf8')
        print(target)
