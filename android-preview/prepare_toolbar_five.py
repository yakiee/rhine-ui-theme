import copy, json
from pathlib import Path
from toolbar_native import OUT

def read(index):
    return json.loads((OUT/f'root-{index}-before.clip.txt').read_text(encoding='utf-8').replace('##KUSTOMCLIP##',''))['clip_modules'][0]

def shape(kind,w,h,color,**more):
    return dict(internal_type='ShapeModule',position_anchor='CENTER',shape_type=kind,shape_width=w,shape_height=h,paint_color=color,**more)

def place(x,y,items,title):
    return dict(internal_type='OverlapLayerModule',internal_title=title,position_anchor='CENTER',position_padding_left=x*2,position_padding_top=y*2,viewgroup_items=items)

def glyph(path,w=35,h=35):
    return shape('PATH',w,h,'#FFF4F7F5',shape_path=path,shape_path_scale='FIT_XY',paint_style='STROKE',paint_stroke=2.2)

names=['电话','信息','浏览器','相机','打开 Dock']
ys=[213,272,331,390,449]
paths=[
 'M 28 5 L 10 9 C -5 23 8 55 28 75 C 48 95 78 104 92 90 L 96 74 L 73 60 L 61 73 C 44 66 33 54 27 38 L 40 27 Z',
 'M 15 8 L 85 8 Q 97 8 97 20 L 97 66 Q 97 80 85 80 L 44 80 L 20 98 L 20 80 L 15 80 Q 3 80 3 66 L 3 20 Q 3 8 15 8 Z M 25 33 L 75 33 M 25 54 L 61 54',
 'M 50 5 A 45 45 0 1 1 49.9 5 Z M 5 50 L 95 50 M 50 5 C 18 30 18 70 50 95 C 82 70 82 30 50 5',
 'M 6 23 L 28 23 L 36 6 L 64 6 L 72 23 L 94 23 L 98 28 L 98 89 L 94 95 L 6 95 L 2 89 L 2 28 Z M 70 59 A 20 25 0 1 1 30 59 A 20 25 0 1 1 70 59 M 82 36 L 88 36',
 'M 7 7 L 40 7 L 40 40 L 7 40 Z M 60 7 L 93 7 L 93 40 L 60 40 Z M 7 60 L 40 60 L 40 93 L 7 93 Z M 60 60 L 93 60 L 93 93 L 60 93 Z',
]
visual=read(3)
old=visual['viewgroup_items']
visual['viewgroup_items']=[copy.deepcopy(old[i]) for i in (0,1,2,4,5)]
for index,(name,y,path) in enumerate(zip(names,ys,paths)):
    tile=shape('PATH',106,55.2,'#FF242B33' if index%2==0 else '#FF1C242C',shape_path='M 50 0 L 100 50 L 50 100 L 0 50 Z',shape_path_scale='FIT_XY')
    icon=glyph(path,37 if index==3 else 35,31 if index==3 else 35)
    visual['viewgroup_items'].append(place(252,y,[tile,icon],name+' · 原生矢量图标'))

frames=[]
for pos,opacity,scale in [(0,100,.96),(45,20,.985),(100,0,1)]:
    for prop,value in [('OPACITY',opacity),('SCALE_X',scale),('SCALE_Y',scale)]:
        frames.append(dict(position=pos,property=prop,value=value,ease='STRAIGHT'))
show=dict(type='FORMULA',formula='$gv(page)=0$',action='ADVANCED',anchor='MODULE_CENTER',duration=2.2,delay=0,ease='STRAIGHT',animator=frames,internal_toggles={'duration':10},internal_formulas={'duration':'$if(gv(page)=0,2.2,1.6)$'})
scroll=copy.deepcopy(next(a for a in visual['internal_animations'] if a['type']=='SCROLL'))
scroll['animator']=[dict(position=p,property='OPACITY',value=v,ease='STRAIGHT') for p,v in [(0,0),(15,10),(35,65),(60,100),(100,100)]]
visual['internal_animations']=[show,scroll]

touch=read(51)
old_events=next(c['viewgroup_items'][0]['internal_events'] for c in touch['viewgroup_items'] if '在当前桌面展开' in c.get('internal_title',''))
touch['internal_animations']=[]
touch['viewgroup_items']=[shape('RECT',720,1600,'#00000000')]
components=['com.android.contacts/com.android.contacts.activities.TwelveKeyDialer','com.android.mms/com.android.mms.ui.MmsTabActivity','com.android.browser/com.android.browser.launch.SplashActivity','com.android.camera/com.android.camera.Camera']
for i,(name,y) in enumerate(zip(names,ys)):
    if i<4:
        events=[dict(type='SINGLE_TAP',action='LAUNCH_APP',intent='intent:#Intent;action=android.intent.action.MAIN;category=android.intent.category.LAUNCHER;component='+components[i]+';launchFlags=0x10200000;end')]
    else:
        events=copy.deepcopy(old_events)
        for event in events:
            if event.get('switch')=='tapy':event['switch_text']=str(y-40)
    hit=shape('RECT',110,58,'#00000000',internal_events=events)
    touch['viewgroup_items'].append(place(252,y,[hit],name+' · 点击区'))

for index,module in [(3,visual),(51,touch)]:
    assert not any(x in json.dumps(module) for x in ['BitmapModule','kfile://','musicapp'])
    clip='##KUSTOMCLIP##\n'+json.dumps({'clip_version':1,'clip_modules':[module]},ensure_ascii=False)+'\n##KUSTOMCLIP##'
    (OUT/f'root-{index}-after.clip.txt').write_text(clip,encoding='utf-8')
print('Prepared 5 native icons and 5 matching hit regions; two synchronized visibility animations, no toolbar gyro')
