"""Native sensor-driven parallax, retaining existing page animation tracks."""
from pathlib import Path
from copy import deepcopy
import json,zipfile
from static_helpers import formula,walk
BASE=Path(__file__).resolve().parents[1]
SOURCE=BASE/'output/material-v0.7/Rhine-UI-material-v0.7.klwp'
OUT=BASE/'output/parallax-v0.8';OUT.mkdir(exist_ok=True)
with zipfile.ZipFile(SOURCE)as archive:p=json.loads(archive.read('preset.json'))
roots=p['preset_root']['viewgroup_items'];globals=p['preset_root']['globals_list']
globals['gyro'].update(type='TEXT',value='1',description='手机倾斜时启用分层视差；设置页保持稳定')
# Fixed native sensor tracks avoid stale runtime parameter updates in KLWP 3.82.
def gyro(speed,limit,inverted=False):
 return {'type':'GYRO','action':'SCROLL_INVERTED' if inverted else 'SCROLL','axis':'XY','angle':0,'speed':speed,'limit':limit,'anchor':'MODULE_CENTER'}
assignments={}
def attach(index,speed,limit,inverted=False):
 roots[index].setdefault('internal_animations',[]).append(gyro(speed,limit,inverted))
 assignments[index]={'title':roots[index].get('internal_title'),'speed':speed,'limit':limit,'inverted':inverted}
# Extra wallpaper coverage prevents empty borders at maximum displacement.
formula(roots[0],'bitmap_width','si(rwidth)*1.08');formula(roots[0],'bitmap_height','si(rheight)*1.08')
wall=roots[0]
roots[0]={'internal_type':'OverlapLayerModule','internal_title':'00 背景视差容器','position_anchor':'CENTER','viewgroup_items':[wall]}
attach(0,4,20,True)
for index in [1,48]:attach(index,3,8)
for index in [3,51]:attach(index,8,18)
for index in list(range(4,22))+[50]:attach(index,6,14)
for index in [22]:attach(index,5,12)
for index in [23,24,52]:attach(index,9,22)
# Functional pages use subtle shared motion so borders, album and text stay aligned.
for index in list(range(27,44))+list(range(54,60)):attach(index,2,5)
# Offer explicit preset editions instead of exposing an unreliable live toggle.
settings=roots[45]
settings['viewgroup_items']=[holder for i,holder in enumerate(settings['viewgroup_items'])if i not in range(48,54)]
for node in walk(settings):
 if node.get('text_expression')=='重力视差':node['text_expression']='重力视差 · 已开启'
 if node.get('text_expression')=='静态预览中保持关闭':node['text_expression']='随手机倾斜移动；暂停可载入静止版'
p['preset_info'].update(title='Rhine UI · 重力视差 v0.8',description='原生传感器驱动分层视差：壁纸、菜单、Dock 与功能页不同幅度；保留切页动画。')
(OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
with zipfile.ZipFile(SOURCE)as source,zipfile.ZipFile(OUT/'Rhine-UI-parallax-v0.8.klwp','w',zipfile.ZIP_DEFLATED)as target:
 for name in source.namelist():target.writestr(name,json.dumps(p,ensure_ascii=False)if name=='preset.json'else source.read(name))
(OUT/'parallax-layers.json').write_text(json.dumps(assignments,ensure_ascii=False,indent=2),encoding='utf8')
still=deepcopy(p)
for root in still['preset_root']['viewgroup_items']:
 root['internal_animations']=[a for a in root.get('internal_animations',[])if a['type']!='GYRO']
 for node in walk(root):
  if node.get('text_expression')=='重力视差 · 已开启':node['text_expression']='重力视差 · 静止版'
  if node.get('text_expression')=='随手机倾斜移动；暂停可载入静止版':node['text_expression']='视差已暂停；切页动画仍然保留'
still['preset_root']['globals_list']['gyro']['value']='0'
still['preset_info']['title']='Rhine UI · 静止视差版 v0.8'
with zipfile.ZipFile(SOURCE)as source,zipfile.ZipFile(OUT/'Rhine-UI-parallax-off-v0.8.klwp','w',zipfile.ZIP_DEFLATED)as target:
 for name in source.namelist():target.writestr(name,json.dumps(still,ensure_ascii=False)if name=='preset.json'else source.read(name))
print('Built sensor and stationary editions, preserving all page animations')
