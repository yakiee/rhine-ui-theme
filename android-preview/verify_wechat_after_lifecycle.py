from rebuild_ui import run
from pathlib import Path
import time,json

run('shell','input','tap',1020,1967)
time.sleep(1)
run('shell','input','tap',1070,1520)
time.sleep(1)
activity=run('shell','dumpsys','activity','activities').decode(errors='replace')
top=[line.strip() for line in activity.splitlines() if 'topResumedActivity' in line]
result={'wechat_launcher_verified':any('com.tencent.mm/.ui.LauncherUI' in line for line in top),'top_activity':top}
print(json.dumps(result,ensure_ascii=True),flush=True)
run('shell','input','keyevent',3)
time.sleep(.8)
run('shell','input','tap',190,280)
Path('rhine_exact/output/dock-page-lifecycle-20260914/wechat-verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
