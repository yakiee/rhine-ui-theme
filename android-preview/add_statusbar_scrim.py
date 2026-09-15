from pathlib import Path
import json,time,re,xml.etree.ElementTree as ET
from rebuild_ui import run
out=Path('rhine_exact/output/system-statusbar-contrast-20260915');out.mkdir(parents=True,exist_ok=True)
assert not (out/'applied.json').exists(), 'Already added: edit existing scrim instead of duplicating'
run('shell','uiautomator','dump','/sdcard/rhine-statusbar-ui.xml')
root=ET.fromstring(run('shell','cat','/sdcard/rhine-statusbar-ui.xml'))
assert any(n.get('text')=='根目录' for n in root.iter('node'))
assert any('64/' in n.get('text','') for n in root.iter('node'))
color='#99101922'
solid={'internal_type':'ShapeModule','internal_title':'系统状态栏 · 文字衬底','shape_type':'RECT','position_anchor':'TOP','shape_width':620,'shape_height':52,'paint_color':color,'internal_toggles':{'shape_width':10,'shape_height':10},'internal_formulas':{'shape_width':'$si(rwidth)+4$','shape_height':'$si(rheight)*0.037$'}}
fade={'internal_type':'ShapeModule','internal_title':'系统状态栏 · 向下柔和渐隐','shape_type':'RECT','position_anchor':'TOP','position_padding_top':52,'shape_width':620,'shape_height':74,'paint_color':color,'fx_gradient':'VERTICAL','fx_gradient_color':'#00101922','fx_gradient_width':100,'fx_gradient_offset':50,'internal_toggles':{'shape_width':10,'shape_height':10,'position_padding_top':10},'internal_formulas':{'shape_width':'$si(rwidth)+4$','shape_height':'$si(rheight)*0.053$','position_padding_top':'$si(rheight)*0.037$'}}
group={'internal_type':'OverlapLayerModule','internal_title':'系统状态栏 · 顶部可读性渐隐遮罩','position_anchor':'TOP','viewgroup_items':[solid,fade],'internal_events':[],'internal_animations':[]}
clip=out/'top-scrim.clip.txt';clip.write_text('##KUSTOMCLIP##\n'+json.dumps({'clip_version':1,'clip_modules':[group]},ensure_ascii=False)+'\n##KUSTOMCLIP##',encoding='utf8')
run('push',clip.resolve(),'/data/local/tmp/rhine-editor-input.txt')
run('shell','CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard KUSTOM_MODULES /data/local/tmp/rhine-editor-input.txt')
time.sleep(.4)
run('shell','uiautomator','dump','/sdcard/rhine-statusbar-ui.xml')
root=ET.fromstring(run('shell','cat','/sdcard/rhine-statusbar-ui.xml'))
node=next(n for n in root.iter('node') if n.get('resource-id','').endswith(':id/action_paste'))
b=list(map(int,re.findall(r'\d+',node.get('bounds'))));run('shell','input','tap',(b[0]+b[2])//2,(b[1]+b[3])//2);time.sleep(.6)
run('shell','uiautomator','dump','/sdcard/rhine-statusbar-ui.xml')
raw=run('shell','cat','/sdcard/rhine-statusbar-ui.xml');(out/'after-paste.xml').write_bytes(raw)
root=ET.fromstring(raw);assert any('65/' in n.get('text','') for n in root.iter('node'))
(out/'applied.json').write_text(json.dumps({'added':group['internal_title'],'saved':False}),encoding='utf8')
node=next(n for n in root.iter('node') if n.get('resource-id','').endswith(':id/action_save'))
b=list(map(int,re.findall(r'\d+',node.get('bounds'))));run('shell','input','tap',(b[0]+b[2])//2,(b[1]+b[3])//2);time.sleep(1.5)
(out/'applied.json').write_text(json.dumps({'added':group['internal_title'],'saved':True}),encoding='utf8')
run('shell','input','keyevent','KEYCODE_HOME')
print('Saved one top-only statusbar scrim; awaiting visual verification.')
