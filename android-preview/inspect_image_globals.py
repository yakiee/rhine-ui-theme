import json
from pathlib import Path
v=json.loads(Path('rhine_exact/output/free-editor-rebuild/globals.clip.txt').read_text(encoding='utf8').replace('##KUSTOMCLIP##',''))['KUSTOM_GLOBAL']
print([(i,k,a.get('value')) for i,(k,a) in enumerate(v.items()) if a.get('type')=='BITMAP'])
