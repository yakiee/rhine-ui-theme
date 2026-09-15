from rebuild_ui import run
from pathlib import Path
import json,time
run('shell','input','tap',1146,2327);run('shell','input','tap',1008,216)
base=Path('rhine_exact/output/free-editor-rebuild/phone-clips')
p=json.loads((base/'image-globals.clip.txt').read_text(encoding='utf8').replace('##KUSTOMCLIP##',''));p['KUSTOM_GLOBAL'].pop('termcover')
(base/'scene.clip.txt').write_text('##KUSTOMCLIP##\n'+json.dumps(p,ensure_ascii=False)+'\n##KUSTOMCLIP##',encoding='utf8')
