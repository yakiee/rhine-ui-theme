from rebuild_ui import run
from rebuild_clipboard import ClipboardControl
from pathlib import Path
import json,time,copy

out=Path('rhine_exact/output/dock-page-lifecycle-20260914')
run('shell','input','tap',1146,2143)
time.sleep(.3)
run('shell','input','tap',864,216)
time.sleep(.3)
with ClipboardControl() as clipboard:
    raw=clipboard.get()
modules=json.loads(raw.replace('##KUSTOMCLIP##',''))['clip_modules']
assert len(modules)==1 and modules[0]['internal_title']=='终端唯一入口与点击区域'
(out/'current-touches-before.clip.txt').write_text(raw,encoding='utf-8')
fixed=copy.deepcopy(modules[0])
count=0
def walk(value):
    global count
    if isinstance(value,dict):
        if value.get('action')=='OPEN_LINK' and value.get('url')=='$gv(wechat)$':
            value['action']='LAUNCH_APP'
            value.pop('url')
            value['intent']='intent:#Intent;action=android.intent.action.MAIN;category=android.intent.category.LAUNCHER;component=com.tencent.mm/com.tencent.mm.ui.LauncherUI;launchFlags=0x10200000;end'
            count+=1
        for child in value.values():walk(child)
    elif isinstance(value,list):
        for child in value:walk(child)
walk(fixed)
assert count==9,count
clip='##KUSTOMCLIP##\n'+json.dumps({'clip_version':1,'clip_modules':[fixed]},ensure_ascii=False)+'\n##KUSTOMCLIP##'
path=out/'wechat-restored.clip.txt';path.write_text(clip,encoding='utf-8')
print('Backed up current touch group; patched exactly',count,'WeChat touch actions.')
run('push',path.resolve(),'/data/local/tmp/rhine-editor-input.txt')
run('shell','CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard KUSTOM_MODULES /data/local/tmp/rhine-editor-input.txt')
