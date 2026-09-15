"""Keep the Dock glow edge attached through both directions of the page morph."""
from pathlib import Path
from copy import deepcopy
import json,zipfile,math
BASE=Path(__file__).resolve().parents[1]
SOURCE=BASE/'output/live-battery-v0.8.5'
OUT=BASE/'output/dock-motion-v0.8.6';OUT.mkdir(exist_ok=True)
def sample(keys,progress):
    for (left,first),(right,last) in zip(keys,keys[1:]):
        if progress<=right:return first+(last-first)*(progress-left)/(right-left)
    return keys[-1][1]
def keys_for(track,prop):
    return sorted((key['position'],key['value']) for key in track['animator'] if key['property']==prop)
for suffix in ['', '-off']:
    with zipfile.ZipFile(SOURCE/f'Rhine-UI-live-battery{suffix}-v0.8.5-release.klwp') as source:
        preset=json.loads(source.read('preset.json'))
        roots=preset['preset_root']['viewgroup_items'];dock=roots[23];glow=roots[24]
        dock_track=next(a for a in dock['internal_animations'] if a.get('formula')=='$gv(page)=2$')
        rotation=keys_for(dock_track,'ROTATE');translation=keys_for(dock_track,'Y_OFFSET')
        baseline_x=math.sin(math.radians(23.7))*139
        baseline_y=633-math.cos(math.radians(23.7))*139
        animator=[]
        for progress in range(101):
            ratio=progress/100
            angle=23.7+sample(rotation,progress)
            scale_y=1+(80/130-1)*ratio
            distance=114+25*scale_y
            # The glow's lower local edge is y=25; the card's top edge is y=-114.
            # Move its center along the orbit needed to keep those edges coincident.
            values={'ROTATE':angle,
                    'X_OFFSET':math.sin(math.radians(angle))*distance-baseline_x,
                    'Y_OFFSET':633+sample(translation,progress)-math.cos(math.radians(angle))*distance-baseline_y}
            for prop,value in values.items():
                animator.append({'position':progress,'property':prop,'value':value,'ease':'STRAIGHT'})
        for prop,start,end in [('SCALE_X',1,768/1060),('SCALE_Y',1,80/130)]:
            for progress,value in [(0,start),(100,end)]:animator.append({'position':progress,'property':prop,'value':value,'ease':'STRAIGHT'})
        track=deepcopy(dock_track)
        track['animator']=animator
        for index,existing in enumerate(glow['internal_animations']):
            if existing.get('formula')=='$gv(page)=2$':glow['internal_animations'][index]=track
        glow['internal_title']='Dock 光带 · 全程贴合卡片上沿'
        preset['preset_info']['title']='Rhine UI · Dock 动画贴合 v0.8.6'+(' · 静止版' if suffix else '')
        preset['preset_info']['description']='光带与 Dock 使用同一转动曲线和正反向时长，通过旋转中心补偿保持切页全过程贴边。保留光带缩展、实时电量和重力视差。'
        output=OUT/f'Rhine-UI-dock-motion{suffix}-v0.8.6.klwp'
        with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as target:
            for name in source.namelist():target.writestr(name,json.dumps(preset,ensure_ascii=False) if name=='preset.json' else source.read(name))
        if not suffix:(OUT/'preset.json').write_text(json.dumps(preset,ensure_ascii=False,indent=2),encoding='utf8')
        print(output.name)
# Measure interpolation error between generated keyframes, not just at keyframe endpoints.
curves={prop:keys_for(track,prop) for prop in ['ROTATE','X_OFFSET','Y_OFFSET','SCALE_Y']}
worst=0
for index in range(10001):
    progress=index/100
    angle=math.radians(23.7+sample(rotation,progress))
    light_angle=math.radians(sample(curves['ROTATE'],progress))
    light_x=baseline_x+sample(curves['X_OFFSET'],progress)
    light_y=baseline_y+sample(curves['Y_OFFSET'],progress)
    scale_y=sample(curves['SCALE_Y'],progress)
    for horizontal in [-530,0,530]:
        light_edge=(light_x+horizontal*math.cos(light_angle)-25*scale_y*math.sin(light_angle),light_y+horizontal*math.sin(light_angle)+25*scale_y*math.cos(light_angle))
        dock_edge=(horizontal*math.cos(angle)+114*math.sin(angle),633+sample(translation,progress)+horizontal*math.sin(angle)-114*math.cos(angle))
        worst=max(worst,math.dist(light_edge,dock_edge))
assert worst<.02,worst
(OUT/'validation.json').write_text(json.dumps({'samples':10001,'max_edge_error_native_units':worst,'forward_duration':track['internal_formulas']['duration'],'reverse_uses_same_clock':True},indent=2),encoding='utf8')
print('Maximum intermediate edge error:',worst)
