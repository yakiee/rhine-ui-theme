from rebuild_ui import run
from pathlib import Path
import json,time
p=Path('rhine_exact/output/dock-phone-fix-20260914');n=json.loads((p/'terminal-touches-fixed.json').read_text(encoding='utf8'));clip=p/'terminal-wechat-native.clip.txt';clip.write_text('##KUSTOMCLIP##\n'+json.dumps({'clip_version':1,'clip_modules':[n]},ensure_ascii=False)+'\n##KUSTOMCLIP##',encoding='utf8')
run('push',clip.resolve(),'/data/local/tmp/rhine-editor-input.txt');run('shell','CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard KUSTOM_MODULES /data/local/tmp/rhine-editor-input.txt')
run('shell','input','tap',1146,2354);time.sleep(.2);run('shell','input','tap',1140,216);time.sleep(.2)
