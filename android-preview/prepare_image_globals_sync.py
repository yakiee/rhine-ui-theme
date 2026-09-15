from pathlib import Path
import json
base=Path('rhine_exact/output/free-editor-rebuild')
p=json.loads((base/'phone-clips/globals.clip.txt').read_text(encoding='utf8').replace('##KUSTOMCLIP##',''))
p['KUSTOM_GLOBAL']={k:v for k,v in p['KUSTOM_GLOBAL'].items() if k in ['scene','termcover']}
(base/'phone-clips/image-globals.clip.txt').write_text('##KUSTOMCLIP##\n'+json.dumps(p,ensure_ascii=False)+'\n##KUSTOMCLIP##',encoding='utf8')
from rebuild_ui import run,snapshot
run('shell','input','tap',1050,2010)
snapshot()
