from rebuild_ui import run
from rebuild_clipboard import ClipboardControl
from pathlib import Path
import time
value='intent:#Intent;action=android.intent.action.MAIN;category=android.intent.category.LAUNCHER;component=com.tencent.mm/com.tencent.mm.ui.LauncherUI;launchFlags=0x10200000;end'
Path('rhine_exact/output/dock-phone-fix-20260914/wechat-direct-intent.txt').write_text(value,encoding='utf8')
run('shell','input','tap',450,658);run('shell','input','keycombination',113,29)
with ClipboardControl() as c:c.set(value,paste=True)
time.sleep(.4)
run('shell','input','tap',1128,216);time.sleep(.4)
print('Updated WeChat global text; root save pending.')
