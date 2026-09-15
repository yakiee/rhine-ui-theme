from rebuild_ui import run
from pathlib import Path
import time,xml.etree.ElementTree as ET
run('shell','input','tap',696,216);time.sleep(1.2);run('shell','input','keyevent',3);time.sleep(1)
run('shell','input','swipe',1040,1160,160,1160,650);time.sleep(2)
out=Path('rhine_exact/output/dock-phone-fix-20260914/second-page-only')
(out/'live-diagnostic.png').write_bytes(run('exec-out','screencap','-p'))
run('shell','uiautomator','dump','/sdcard/Download/klwp-rebuild-ui.xml')
root=ET.fromstring(run('shell','cat','/sdcard/Download/klwp-rebuild-ui.xml'))
print([n.get('content-desc') for n in root.iter('node') if '页' in n.get('content-desc','')])
