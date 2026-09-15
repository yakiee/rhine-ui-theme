from rebuild_ui import run,snapshot
from rebuild_clipboard import ClipboardControl
from pathlib import Path
import json
run('shell','input','tap',1146,2119);run('shell','input','tap',840,216)
with ClipboardControl() as c:clip=c.get()
Path('rhine_exact/output/free-editor-rebuild/phone-flow-roundtrip.txt').write_text(clip,encoding='utf8')
f=list(json.loads(clip.replace('##KUSTOMCLIP##',''))['KUSTOM_FLOW'].values())[0]
assert f['t'][0]['params']['formula']=='$si(screen)$'
assert f['a'][0]['params']['formula']=='$if(si(screen)=gv(homepg) & gv(origin)=si(screen),gv(view),0)$'
assert f['a'][1]['params']['global']=='view'
print('Phone flow parameters verified',json.dumps(f,ensure_ascii=False))
run('shell','input','tap',696,216)
snapshot()
