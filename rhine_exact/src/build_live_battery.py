"""Bind the Dock battery gauge and terminal cells to Android's battery level."""
from pathlib import Path
from copy import deepcopy
import json
import zipfile
from static_helpers import formula
BASE=Path(__file__).resolve().parents[1]
SOURCE=BASE/'output/mudrock-light-v0.8.4'
OUT=BASE/'output/live-battery-v0.8.5'
OUT.mkdir(exist_ok=True)
for suffix in ['', '-off']:
    with zipfile.ZipFile(SOURCE/f'Rhine-UI-mudrock-light{suffix}-v0.8.4.klwp') as source:
        preset=json.loads(source.read('preset.json'))
        roots=preset['preset_root']['viewgroup_items']
        dock=roots[23]
        holder=dock['viewgroup_items'][4]
        ring=holder['viewgroup_items'][0]
        background=deepcopy(ring)
        background['internal_title']='100% 电量底环'
        background['paint_color']='#FF474A4D'
        background.pop('internal_formulas',None)
        background.pop('internal_toggles',None)
        arc={'internal_type':'ProgressModule','internal_title':'实时电量环 · 100% 满圈',
             'position_anchor':'CENTER','progress_progress':'BATTERY','progress_mode':'FLAT',
             'progress_min':0,'progress_max':100,'style_style':'CIRCLE','style_size':152,
             'style_height':4,'style_width':100,'color_color':'FLAT',
             'color_fgcolor':'#FFFFBB27','color_bgcolor':'#FF474A4D',
             'progress_rotate_mode':'MANUAL','progress_rotate_offset':0}
        formula(arc,'color_fgcolor','gv(accent)')
        holder['viewgroup_items']=[arc]
        number=dock['viewgroup_items'][6]['viewgroup_items'][0]
        number['internal_title']='实时电量百分数'
        number['text_expression']='$bi(level)$'
        formula(number,'text_size','if(bi(level)>=100,76,100)')
        # The three-cell symbol uses the same source as the larger Dock gauge.
        battery=roots[4]['viewgroup_items'][8]
        for index,cell in enumerate(battery['viewgroup_items'][2:]):
            shape=cell['viewgroup_items'][0]
            formula(shape,'paint_color',f'if(bi(level)>{index*100/3:.4f},#FFFFFFFF,#30FFFFFF)')
        preset['preset_info']['title']='Rhine UI · 实时电量 v0.8.5'+(' · 静止版' if suffix else '')
        preset['preset_info']['description']='Dock 圆环满圈对应 100% 电量；圆弧与数字读取实时 Android 电量，终端三格电池同步变化。保留泥岩光带与原有动画。'
        path=OUT/f'Rhine-UI-live-battery{suffix}-v0.8.5-release.klwp'
        with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as target:
            for name in source.namelist():
                target.writestr(name,json.dumps(preset,ensure_ascii=False) if name=='preset.json' else source.read(name))
        if not suffix:(OUT/'preset.json').write_text(json.dumps(preset,ensure_ascii=False,indent=2),encoding='utf8')
        print(path.name)
