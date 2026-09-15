from pathlib import Path
import json,time,xml.etree.ElementTree as ET
from rebuild_ui import run
out=Path('rhine_exact/assets/zhuangfangyi')
for local,remote in [('wallpaper-portrait.png','zhuang-wallpaper-portrait.png'),('terminal-cover.png','zhuang-terminal-cover.png')]:
    print(run('push',str((out/local).resolve()),'/sdcard/Download/Rhine-KLWP/bitmaps/'+remote).decode(errors='replace'))
run('shell','input','tap',1134,834)
run('shell','input','tap',1050,2010)
time.sleep(.5)
run('shell','uiautomator','dump','/sdcard/rhine-zhuang-ui.xml')
raw=run('shell','cat','/sdcard/rhine-zhuang-ui.xml')
(out/'current-ui.xml').write_bytes(raw)
print(json.dumps([{k:n.get(k) for k in ['text','content-desc','resource-id','bounds']} for n in ET.fromstring(raw).iter('node') if n.get('text') or n.get('content-desc')],ensure_ascii=True))
