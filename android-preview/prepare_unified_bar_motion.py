"""Keep launcher geometry independent of terminal visibility."""
from pathlib import Path
import copy
import json
import sys
from rebuild_ui import run

source = Path(sys.argv[1])
name = sys.argv[2]
payload = json.loads(source.read_text(encoding='utf-8').replace('##KUSTOMCLIP##', ''))
if 'clip_modules' in payload:
    original = payload['clip_modules'][0]['internal_animations']
else:
    original = list(payload['KUSTOM_ANIMATION'].values())
motion = []
removed = []
for animation in original:
    if animation.get('type') == 'FORMULA' and animation.get('formula') == '$gv(page)=1$':
        removed.append(animation)
    else:
        motion.append(copy.deepcopy(animation))
assert len(removed) == 2, len(removed)
assert any(a['type'] == 'SCROLL' for a in motion)
motion.append({
    'type': 'FORMULA', 'formula': '$if(gv(page)=1,f,b)$',
    'action': 'FADE', 'duration': 3.2, 'delay': 0,
    'ease': 'STRAIGHT', 'speed': 100, 'amount': 100,
    'anchor': 'MODULE_CENTER',
})
assert [a for a in original if a['type'] == 'SCROLL'] == [a for a in motion if a['type'] == 'SCROLL']
out = Path('rhine_exact/output/unified-bar-motion-20260914')
out.mkdir(exist_ok=True)
path = out / (name + '-after.clip.txt')
path.write_text('##KUSTOMCLIP##\n' + json.dumps({'clip_version': 1, 'KUSTOM_ANIMATION': {str(i): a for i, a in enumerate(motion)}}) + '\n##KUSTOMCLIP##', encoding='utf-8')
run('push', path.resolve(), '/data/local/tmp/rhine-editor-input.txt')
run('shell', 'CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard KUSTOM_ANIMATION /data/local/tmp/rhine-editor-input.txt')
print(name, 'original', len(original), 'patched', len(motion), 'scroll keyframes preserved')
