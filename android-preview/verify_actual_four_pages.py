from rebuild_ui import run
from pathlib import Path
import time,xml.etree.ElementTree as ET
out=Path('rhine_exact/output/dock-phone-fix-20260914/second-page-only')
for page in range(1,5):
 if page>1:
  run('shell','input','swipe',1040,1160,160,1160,650);time.sleep(1.5)
 run('shell','uiautomator','dump','/sdcard/Download/klwp-rebuild-ui.xml')
 raw=run('shell','cat','/sdcard/Download/klwp-rebuild-ui.xml');root=ET.fromstring(raw)
 labels=[n.attrib.get('content-desc','') for n in root.iter('node') if '页' in n.attrib.get('content-desc','')]
 print(page,labels,flush=True)
 (out/f'verified-page{page}.xml').write_bytes(raw)
 (out/f'verified-page{page}.png').write_bytes(run('exec-out','screencap','-p'))
