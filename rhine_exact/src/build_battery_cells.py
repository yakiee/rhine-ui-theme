"""Display exact battery capacity across the terminal's four battery segments."""
from pathlib import Path
import copy
import json
import zipfile

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / 'output/battery-balance-v0.13.18'
OUT = BASE / 'output/battery-cells-v0.13.21'
OUT.mkdir(exist_ok=True)

for suffix in ['', '-off']:
    with zipfile.ZipFile(SOURCE / f'Rhine-UI-battery-balance{suffix}-v0.13.18.klwp') as source:
        preset = json.loads(source.read('preset.json'))
        roots = preset['preset_root']['viewgroup_items']
        battery = roots[4]['viewgroup_items'][9]
        battery['internal_title'] = '终端电量 · 四格按真实百分比连续填充'
        cell_template = copy.deepcopy(battery['viewgroup_items'][2])
        battery['viewgroup_items'] = battery['viewgroup_items'][:2] + [copy.deepcopy(cell_template) for _ in range(4)]
        for index, holder in enumerate(battery['viewgroup_items'][2:]):
            track = holder['viewgroup_items'][0]
            center_x = -10.35 + index * 5.7
            holder.update(position_padding_left=max(0, 2*center_x),
                          position_padding_right=max(0, -2*center_x))
            track.update(shape_width=4.6, shape_height=9.8)
            track.pop('internal_toggles', None)
            track.pop('internal_formulas', None)
            track['paint_color'] = '#30FFFFFF'
            track['internal_title'] = f'电池格 {index+1} · 空槽'
            fraction = f'mu(max,0,mu(min,1,4*mu(max,0,mu(min,100,bi(level)))/100-{index}))'
            width = f'4.6*{fraction}'
            fill = copy.deepcopy(track)
            fill.update(internal_title=f'电池格 {index+1} · 实际填充', paint_color='#FFFFFFFF',
                        internal_toggles={'shape_width':10,'paint_color':10},
                        internal_formulas={'shape_width':f'$mu(max,0.001,{width})$',
                                           'paint_color':f'$if({fraction}>0,#FFFFFFFF,#00FFFFFF)$'})
            # Compensate width changes so each segment fills from its left edge.
            fill_holder = dict(internal_type='OverlapLayerModule', position_anchor='CENTER',
                               internal_toggles={'position_padding_right':10},
                               internal_formulas={'position_padding_right':f'$4.6-({width})$'},
                               viewgroup_items=[fill])
            holder['viewgroup_items'] = [track, fill_holder]
        preset['preset_info'].update(title='Rhine UI · 真实电量格 v0.13.21' + (' · 无重力视差' if suffix else ''),
                                     description='顶部四格电池按真实电量连续填充：50% 两格，100% 全满；保留原外框、位置及点击操作。')
        target = OUT / f'Rhine-UI-battery-cells{suffix}-v0.13.21.klwp'
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as dest:
            for name in source.namelist():
                dest.writestr(name, json.dumps(preset, ensure_ascii=False) if name=='preset.json' else source.read(name))
        if not suffix:
            (OUT/'preset.json').write_text(json.dumps(preset,ensure_ascii=False,indent=2),encoding='utf8')
        print(target)
