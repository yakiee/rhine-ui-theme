from pathlib import Path
import json
p=Path('rhine_exact/output/free-editor-rebuild/phone-clips')
for f in p.glob('*.txt'):
 try:d=json.loads(f.read_text(encoding='utf8').replace('##KUSTOMCLIP##',''))
 except:continue
 for n in d.get('clip_modules',[]):
  if n.get('internal_title') in ['主菜单 · 设备状态','终端 · 设备及电池信息']:
   print(f.name,n['internal_title'],len(json.dumps(n).encode()))
