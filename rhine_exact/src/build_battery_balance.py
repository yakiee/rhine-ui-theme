"""Balance the operator-card battery typography and transparent circle interior."""
from pathlib import Path
import copy
import json
import zipfile

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / 'output/battery-type-v0.13.16'
OUT = BASE / 'output/battery-balance-v0.13.18'
OUT.mkdir(exist_ok=True)


def walk(node):
    yield node
    for child in node.get('viewgroup_items', []):
        yield from walk(child)


for suffix in ['', '-off']:
    with zipfile.ZipFile(SOURCE / f'Rhine-UI-battery-type{suffix}-v0.13.16.klwp') as source:
        preset = json.loads(source.read('preset.json'))
        dock = preset['preset_root']['viewgroup_items'][23]
        dock['viewgroup_items'][1]['paint_color'] = '#ED242526'
        reflection = dock['viewgroup_items'][2]
        reflection['internal_title'] = '深灰纸面上的轻微暖色反光'
        reflection['paint_color'] = '#30423C33'
        reflection['internal_formulas']['paint_color'] = '$if(gv(style)=0,#30423C33,ce(gv(accent),alpha,12))$'
        info = dock['viewgroup_items'][3]['viewgroup_items']
        info[0]['viewgroup_items'][0]['paint_color'] = '#00000000'
        info[1]['viewgroup_items'][0]['color_bgcolor'] = '#805D6062'
        label = info[2]['viewgroup_items'][0]
        label.update(text_size=16, text_width=70,
                     text_family='kfile://org.kustom.provider/fonts/Roboto-Regular.ttf', paint_color='#E5FFFFFF')
        # Keep the label close to the cap height, for both two- and three-digit values.
        info[2].setdefault('internal_toggles', {})['position_padding_bottom'] = 10
        info[2].setdefault('internal_formulas', {})['position_padding_bottom'] = '$if(bi(level)>=100,56,76)$'
        info[3].update(position_padding_right=500, position_padding_top=14)
        for node in walk(info[3]):
            if node.get('text_expression') == '$bi(level)$':
                node.update(text_family='kfile://org.kustom.provider/fonts/CenturyGothic-Regular.ttf',
                            text_size=96, text_width=139)
                node['internal_formulas']['text_size'] = '$if(bi(level)>=100,70,96)$'
                if node.get('internal_title') == '电量数字轻投影':
                    node['paint_color'] = '#40000000'
        outline = copy.deepcopy(info[3]['viewgroup_items'][-1])
        outline.update(internal_title='电量数字细描边', paint_style='STROKE', paint_stroke=1.2)
        info[3]['viewgroup_items'].insert(-1, outline)
        preset['preset_info'].update(title='Rhine UI · 电量留白与透明圆心 v0.13.18' + (' · 无重力视差' if suffix else ''),
                                     description='电量改常规字重，BAT 标签按数字位数收紧；圆心透明，底栏采用中性深灰及轻微反光。')
        target = OUT / f'Rhine-UI-battery-balance{suffix}-v0.13.18.klwp'
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as dest:
            for name in source.namelist():
                dest.writestr(name, json.dumps(preset, ensure_ascii=False) if name == 'preset.json' else source.read(name))
            dest.write(BASE / 'assets/fonts/CenturyGothic-Regular.ttf', 'fonts/CenturyGothic-Regular.ttf')
        if not suffix:
            (OUT / 'preset.json').write_text(json.dumps(preset, ensure_ascii=False, indent=2), encoding='utf8')
        print(target)
