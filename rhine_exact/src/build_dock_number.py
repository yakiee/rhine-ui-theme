"""Refine only the terminal Dock numeral; preserve the lower battery ring."""
from pathlib import Path
import copy
import json
import zipfile

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / 'output/terminal-type-v0.13.10'
OUT = BASE / 'output/dock-number-v0.13.12'
OUT.mkdir(exist_ok=True)


def positioned(node, x, y):
    return {'internal_type': 'OverlapLayerModule', 'position_anchor': 'CENTER',
            'position_padding_left': max(0, 2*x), 'position_padding_right': max(0, -2*x),
            'position_padding_top': max(0, 2*y), 'position_padding_bottom': max(0, -2*y),
            'viewgroup_items': [node]}


for suffix in ['', '-off']:
    with zipfile.ZipFile(SOURCE / f'Rhine-UI-type{suffix}-v0.13.10.klwp') as source:
        preset = json.loads(source.read('preset.json'))
        roots = preset['preset_root']['viewgroup_items']
        lower_dock = copy.deepcopy(roots[23])
        plate = roots[5]['viewgroup_items'][3]['viewgroup_items'][0]['viewgroup_items'][0]
        plate['paint_color'] = '#FFB8BCC0'
        numeral_group = roots[5]['viewgroup_items'][12]['viewgroup_items'][0]
        numeral = numeral_group['viewgroup_items'][0]
        numeral.update(text_expression='[i]$bi(tempc)$[/i]',
                       text_family='kfile://org.kustom.provider/fonts/Roboto-MediumItalic.ttf')
        # All shadow copies share the original container, data and animation transform.
        shadows = []
        for x, y, color in [(0.8, 1.8, '#22000000'), (1.5, 2.6, '#28000000'), (2, 3.2, '#18000000')]:
            shadow = copy.deepcopy(numeral)
            shadow['internal_title'] = '终端数字轻投影'
            shadow['paint_color'] = color
            shadows.append(positioned(shadow, x, y))
        numeral_group['viewgroup_items'] = shadows + [numeral]
        assert roots[23] == lower_dock
        preset['preset_info'].update(title='Rhine UI · Dock 数字字重与投影 v0.13.12' + (' · 无重力视差' if suffix else ''),
                                     description='仅终端卡的大数字改用中等字重斜体、轻微投影与较深灰底；底部电量圆环完整保留。')
        target = OUT / f'Rhine-UI-dock-number{suffix}-v0.13.12.klwp'
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as dest:
            for name in source.namelist():
                dest.writestr(name, json.dumps(preset, ensure_ascii=False) if name == 'preset.json' else source.read(name))
            dest.write(BASE / 'assets/fonts/Roboto-MediumItalic.ttf', 'fonts/Roboto-MediumItalic.ttf')
        if not suffix:
            (OUT / 'preset.json').write_text(json.dumps(preset, ensure_ascii=False, indent=2), encoding='utf8')
        print(target)
