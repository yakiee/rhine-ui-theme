"""Attach the terminal accent to the paper edge, accounting for its inner scale."""
from pathlib import Path
import json
import zipfile
BASE=Path(__file__).resolve().parents[1]
SOURCE=BASE/'output/icon-balance-v0.13.32'
OUT=BASE/'output/terminal-edge-v0.13.33'
OUT.mkdir(exist_ok=True)
def center(node,axis):
    positive,negative=('top','bottom') if axis=='y' else ('left','right')
    return (node.get('position_padding_'+positive,0)-node.get('position_padding_'+negative,0))/2
for suffix in ('','-off'):
    with zipfile.ZipFile(SOURCE/f'Rhine-UI-icon-balance{suffix}-v0.13.32.klwp') as source:
        preset=json.loads(source.read('preset.json'))
        terminal=preset['preset_root']['viewgroup_items'][5]['viewgroup_items']
        paper_holder=terminal[1]
        paper_group=paper_holder['viewgroup_items'][0]
        paper=paper_group['viewgroup_items'][3]['viewgroup_items'][0]
        bottom=center(paper_holder,'y')+paper['shape_height']/2*paper_group['config_scale_value']/100
        accent=terminal[2]
        accent.update(internal_title='终端橙线 · 贴合纸面下边缘',position_padding_top=max(0,2*bottom),position_padding_bottom=max(0,-2*bottom))
        # Keep the established right-side accent length; straddle the physical paper edge.
        accent['viewgroup_items'][0]['shape_height']=6
        preset['preset_info'].update(title='Rhine UI · 终端贴边橙线 v0.13.33'+(' · 无重力视差' if suffix else ''),description='按首行纸面实际高度和内部缩放校准橙线，中心贴合下边缘；保留右侧短线长度和共同视差。')
        with zipfile.ZipFile(OUT/f'Rhine-UI-terminal-edge{suffix}-v0.13.33.klwp','w',zipfile.ZIP_DEFLATED) as dest:
            for name in source.namelist():dest.writestr(name,json.dumps(preset,ensure_ascii=False) if name=='preset.json' else source.read(name))
        if not suffix:(OUT/'preset.json').write_text(json.dumps(preset,ensure_ascii=False,indent=2),encoding='utf8')
        print('Paper bottom and accent center:',bottom,'length:',accent['viewgroup_items'][0]['shape_width'])
