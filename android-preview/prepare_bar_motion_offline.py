from pathlib import Path
import json
import re

out = Path('rhine_exact/output/unified-bar-motion-20260914')
out.mkdir(exist_ok=True)
source = Path('rhine_exact/output/live-bar-text-glow-before.clip.txt').read_text(encoding='utf-8')
decoder = json.JSONDecoder()
matches = list(re.finditer('"internal_animations"', source))
assert len(matches) == 2
for name, match in zip(('text', 'glow'), matches):
    start = source.index('[', match.end())
    animations, end = decoder.raw_decode(source, start)
    payload = {'clip_version': 1, 'KUSTOM_ANIMATION': {str(i): a for i, a in enumerate(animations)}}
    (out / (name + '-before.clip.txt')).write_text('##KUSTOMCLIP##\n' + json.dumps(payload) + '\n##KUSTOMCLIP##', encoding='utf-8')
    print(name, len(animations), 'complete live animation array recovered')
