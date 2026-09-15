from pathlib import Path
import json,sys,time,contextlib,io
from rebuild_ui import run,snapshot
base=Path('rhine_exact/output/free-editor-rebuild'); plan=json.loads((base/'rebuild-plan.json').read_text(encoding='utf8'))
for idx in range(int(sys.argv[1]),int(sys.argv[2])):
 b=plan['root_batches'][idx];p=base/'phone-clips'/b['file']
 run('push',p.resolve(),'/data/local/tmp/rhine-editor-input.txt')
 run('shell','CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard KUSTOM_MODULES /data/local/tmp/rhine-editor-input.txt')
 time.sleep(.3);run('shell','input','tap',1128,216);time.sleep(1)
 with contextlib.redirect_stdout(io.StringIO()):root=snapshot()
 titles=[n.get('text') for n in root.iter('node') if n.get('resource-id','').endswith('/module_title')]
 assert b['titles'][-1] in titles,(idx,titles)
 print('Verified batch',idx,'last component',b['titles'][-1],flush=True)
 # Save separately after reviewing validation prompts.
 print('Batch ready for save',idx,flush=True)

