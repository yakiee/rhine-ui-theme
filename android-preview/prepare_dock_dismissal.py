from pathlib import Path
import json
import copy
from rebuild_ui import run

out = Path('rhine_exact/output/dock-dismissal-20260914')
out.mkdir(exist_ok=True)
source = Path('rhine_exact/output/dock-exit-header-before.clip.txt').read_text(encoding='utf-8')
header = json.loads(source.replace('##KUSTOMCLIP##', ''))['clip_modules'][0]
assert header['internal_title'] == '终端 · 返回主页与主题配置'
assert len(header['viewgroup_items']) == 7
events = copy.deepcopy(header['viewgroup_items'][5]['viewgroup_items'][0]['internal_events'])
assert any(e.get('switch') == 'view' and e.get('switch_text') == '0' for e in events)
background = {
    'internal_type': 'ShapeModule', 'internal_title': '点击终端外空白收起',
    'position_anchor': 'CENTER', 'shape_type': 'RECT',
    'shape_width': 4000, 'shape_height': 8000, 'paint_color': '#00000000',
    'internal_events': events,
}
clip = '##KUSTOMCLIP##\n' + json.dumps({'clip_version': 1, 'clip_modules': [background]}, ensure_ascii=False) + '\n##KUSTOMCLIP##'
path = out / 'dismiss-background.clip.txt'
path.write_text(clip, encoding='utf-8')
flow = {
    'id': 'DockLeaveDesktop', 'name': '离开桌面时收起终端',
    't': [{'id': 'DockVisibleTrigger', 'type': 'T_FORMULA', 'params': {'formula': '$si(visible)$', 'trigger': 'ON_CHANGE'}}],
    'a': [
        {'id': 'DockVisibilityValue', 'type': 'A_FORMULA', 'params': {'formula': '0'}},
        {'id': 'DockVisibilityStore', 'type': 'A_GLOBAL', 'params': {'global': 'view', 'store_mode': 'TEXT'}},
    ],
}
(out / 'leave-desktop-flow.clip.txt').write_text('##KUSTOMCLIP##\n' + json.dumps({'clip_version': 1, 'KUSTOM_FLOW': {flow['id']: flow}}, ensure_ascii=False) + '\n##KUSTOMCLIP##', encoding='utf-8')
run('push', path.resolve(), '/data/local/tmp/rhine-editor-input.txt')
run('shell', 'CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard KUSTOM_MODULES /data/local/tmp/rhine-editor-input.txt')
print('Prepared background using original return actions; terminal hit regions remain above this group.')
