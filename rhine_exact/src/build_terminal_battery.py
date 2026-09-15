"""Bind the terminal headline to actual battery percentage, matching its battery icon."""
from pathlib import Path
import json
import zipfile

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / 'output/battery-cells-v0.13.21'
OUT = BASE / 'output/terminal-battery-v0.13.22'
OUT.mkdir(exist_ok=True)

def walk(node):
    yield node
    for child in node.get('viewgroup_items', []):
        yield from walk(child)

for suffix in ['', '-off']:
    with zipfile.ZipFile(SOURCE / f'Rhine-UI-battery-cells{suffix}-v0.13.21.klwp') as source:
        preset = json.loads(source.read('preset.json'))
        terminal = preset['preset_root']['viewgroup_items'][5]
        count = 0
        for node in walk(terminal):
            if node.get('text_expression') == '[i]$bi(tempc)$[/i]':
                node['text_expression'] = '[i]$bi(level)$[/i]'
                if node.get('internal_title') != '数字轻投影':
                    node['internal_title'] = '终端实时电量百分数'
                count += 1
            elif node.get('text_expression') == '电池 / °C':
                node.update(text_expression='电量 / %', internal_title='电量单位')
        assert count == 2
        preset['preset_info'].update(title='Rhine UI · 终端真实电量 v0.13.22' + (' · 无重力视差' if suffix else ''),
                                     description='终端大数字由电池温度改为实际电量百分比，与顶部四格电池及底部电量圆环使用同一数据源。')
        target = OUT / f'Rhine-UI-terminal-battery{suffix}-v0.13.22.klwp'
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as dest:
            for name in source.namelist():
                dest.writestr(name, json.dumps(preset, ensure_ascii=False) if name=='preset.json' else source.read(name))
        if not suffix:
            (OUT/'preset.json').write_text(json.dumps(preset,ensure_ascii=False,indent=2),encoding='utf8')
        print(target)
