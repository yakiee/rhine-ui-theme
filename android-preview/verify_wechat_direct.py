from rebuild_ui import run
from pathlib import Path
import time,json
run('shell','input','tap',1070,1520);time.sleep(1.5)
a=run('shell','dumpsys','activity','activities').decode(errors='replace');top='\n'.join(x.strip() for x in a.splitlines() if 'topResumedActivity' in x);print(top)
p=Path('rhine_exact/output/dock-phone-fix-20260914/wechat-fix.json');p.write_text(json.dumps({'before':'weixin://','after':Path('rhine_exact/output/dock-phone-fix-20260914/wechat-direct-intent.txt').read_text(),'saved_on_phone':True,'tap_test_top_activity':top},ensure_ascii=False,indent=2),encoding='utf8')
