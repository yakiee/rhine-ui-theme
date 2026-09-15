"""Improve terminal captions and use rounded numerals for battery readouts."""
from pathlib import Path
import json
import zipfile

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / 'output/menu-proportions-v0.13.9'
OUT = BASE / 'output/terminal-type-v0.13.10'
OUT.mkdir(exist_ok=True)


def walk(node):
    yield node
    for child in node.get('viewgroup_items', []):
        yield from walk(child)


def move(holder, x, y):
    holder.update(position_padding_left=max(0, 2*x), position_padding_right=max(0, -2*x),
                  position_padding_top=max(0, 2*y), position_padding_bottom=max(0, -2*y))


for suffix in ['', '-off']:
    with zipfile.ZipFile(SOURCE / f'Rhine-UI-proportions{suffix}-v0.13.9.klwp') as source:
        preset = json.loads(source.read('preset.json'))
        roots = preset['preset_root']['viewgroup_items']
        # Keep the small badge's left edge aligned with the terminal title.
        for index in [6, 7]:
            move(roots[5]['viewgroup_items'][index], -22, -162)
        move(roots[5]['viewgroup_items'][9], 51.28, -130)
        for node in walk(roots[5]):
            text = node.get('text_expression')
            if text == '系统':
                node.update(text_size=17.5, text_width=60)
            elif text == 'Android $si(aver)$':
                node.update(text_size=27, text_width=224,
                            text_family='kfile://org.kustom.provider/fonts/Roboto-Regular.ttf')
            elif text == '电池 / °C':
                node.update(text_size=24, text_width=168)
            elif text == '[i]$bi(tempc)$[/i]':
                node.update(text_size=85, text_width=184,
                            text_family='kfile://org.kustom.provider/fonts/Roboto-Regular.ttf')
            if node.get('paint_color') == '#FF333940' and node.get('shape_type') == 'RECT':
                node.update(shape_width=66, shape_height=25, shape_corners=4)
            if node.get('paint_color') == '#FF1D2029' and node.get('shape_type') == 'RECT':
                node.update(shape_height=34)
        for node in walk(roots[23]):
            if node.get('text_expression') == '$bi(level)$':
                node['text_family'] = 'kfile://org.kustom.provider/fonts/Roboto-LightItalic.ttf'
                node['text_size'] = 92
                node['internal_formulas']['text_size'] = '$if(bi(level)>=100,72,92)$'
        preset['preset_info'].update(title='Rhine UI · 终端文字与电量字形 v0.13.10' + (' · 无重力视差' if suffix else ''),
                                     description='放大系统标签、系统版本和电池说明；电量圆环采用圆润倾斜数字，终端数值同步调整字形。')
        target = OUT / f'Rhine-UI-type{suffix}-v0.13.10.klwp'
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as dest:
            for name in source.namelist():
                dest.writestr(name, json.dumps(preset, ensure_ascii=False) if name == 'preset.json' else source.read(name))
            for name in ['Roboto-LightItalic.ttf', 'Roboto-Regular.ttf']:
                dest.write(BASE / 'assets/fonts' / name, 'fonts/' + name)
        if not suffix:
            (OUT / 'preset.json').write_text(json.dumps(preset, ensure_ascii=False, indent=2), encoding='utf8')
        print(target)
