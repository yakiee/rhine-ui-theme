"""Match operator-card rounded battery numerals without changing the terminal menu."""
from pathlib import Path
import copy
import json
import zipfile

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / 'output/reference-refinement-v0.13.15'
OUT = BASE / 'output/battery-type-v0.13.16'
OUT.mkdir(exist_ok=True)

for suffix in ['', '-off']:
    with zipfile.ZipFile(SOURCE / f'Rhine-UI-refined{suffix}-v0.13.15.klwp') as source:
        preset = json.loads(source.read('preset.json'))
        roots = preset['preset_root']['viewgroup_items']
        terminal = copy.deepcopy(roots[5])
        holder = roots[23]['viewgroup_items'][3]['viewgroup_items'][3]
        numeral = holder['viewgroup_items'][0]
        numeral.update(text_family='kfile://org.kustom.provider/fonts/CenturyGothic-Bold.ttf',
                       text_size=90, text_width=139)
        numeral['internal_formulas']['text_size'] = '$if(bi(level)>=100,67,90)$'
        shadow = copy.deepcopy(numeral)
        shadow.update(internal_title='电量数字轻投影', paint_color='#65000000')
        shadow_holder = dict(internal_type='OverlapLayerModule', position_anchor='CENTER',
                             position_padding_left=1.6, position_padding_top=2.4,
                             viewgroup_items=[shadow])
        holder['viewgroup_items'] = [shadow_holder, numeral]
        assert roots[5] == terminal
        preset['preset_info'].update(title='Rhine UI · 干员卡电量字形 v0.13.16' + (' · 无重力视差' if suffix else ''),
                                     description='底部电量采用宽圆的几何粗体，保留数字正体与底栏整体旋转；三位数缩小适配圆环，真实电量绑定不变。')
        target = OUT / f'Rhine-UI-battery-type{suffix}-v0.13.16.klwp'
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as dest:
            for name in source.namelist():
                dest.writestr(name, json.dumps(preset, ensure_ascii=False) if name == 'preset.json' else source.read(name))
            dest.write(BASE / 'assets/fonts/CenturyGothic-Bold.ttf', 'fonts/CenturyGothic-Bold.ttf')
        if not suffix:
            (OUT / 'preset.json').write_text(json.dumps(preset, ensure_ascii=False, indent=2), encoding='utf8')
        print(target)
