"""Rebalance the terminal hero into a numeral, heading and wide banner."""
from pathlib import Path
import json, zipfile
BASE=Path(__file__).resolve().parents[1]
SOURCE=BASE/'output/button-watermarks-v0.13.23'
OUT=BASE/'output/terminal-proportions-v0.13.24'
OUT.mkdir(exist_ok=True)
def place(node,x,y):
    node.update(position_padding_left=max(0,2*x),position_padding_right=max(0,-2*x),position_padding_top=max(0,2*y),position_padding_bottom=max(0,-2*y))
def walk(node):
    yield node
    for child in node.get('viewgroup_items',[]): yield from walk(child)
for suffix in ['', '-off']:
    with zipfile.ZipFile(SOURCE/f'Rhine-UI-watermarks{suffix}-v0.13.23.klwp') as src:
        preset=json.loads(src.read('preset.json'))
        terminal=preset['preset_root']['viewgroup_items'][5]['viewgroup_items']
        # The outer card and hit geometry stay fixed; rebalance its three content columns.
        terminal[3]['viewgroup_items'][0]['viewgroup_items'][0]['shape_height']=90
        for n in walk(terminal[12]):
            if n.get('internal_type')=='TextModule': n['text_size']=100
        place(terminal[8],-5,-207)
        terminal[8]['viewgroup_items'][0]['viewgroup_items'][0].update(text_size=68,text_width=156)
        for index in [6,7]: place(terminal[index],-46,-163)
        terminal[7]['viewgroup_items'][0]['viewgroup_items'][0]['text_size']=19
        place(terminal[9],-5,-131)
        terminal[9]['viewgroup_items'][0]['viewgroup_items'][0].update(text_size=24,text_width=156)
        banner=terminal[4]
        place(banner,161,-168)
        parts=banner['viewgroup_items'][0]['viewgroup_items']
        parts[0]['viewgroup_items'][0]['shape_width']=190
        parts[1]['shape_width']=186
        parts[3]['viewgroup_items'][0]['shape_width']=186
        parts[4]['viewgroup_items'][0].update(text_width=178,text_size=14,text_expression='$tc(ell,si(model),20)$')
        preset['preset_info'].update(title='Rhine UI · 终端首行比例 v0.13.24'+(' · 无重力视差' if suffix else ''),description='放大真实温度数字与终端标题，收紧文字列并统一左边线，加宽壁纸横幅。保留原有纸面、点击和动画。')
        target=OUT/f'Rhine-UI-terminal-proportions{suffix}-v0.13.24.klwp'
        with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as dest:
            for name in src.namelist(): dest.writestr(name,json.dumps(preset,ensure_ascii=False) if name=='preset.json' else src.read(name))
        if not suffix: (OUT/'preset.json').write_text(json.dumps(preset,ensure_ascii=False,indent=2),encoding='utf8')
        print(target)
