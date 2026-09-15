from rebuild_ui import run
from pathlib import Path
import time,xml.etree.ElementTree as ET
out=Path('rhine_exact/output/dock-phone-fix-20260914/second-page-only')
run('shell','input','tap',190,280);time.sleep(1.5)
def cap(label):
 run('shell','uiautomator','dump','/sdcard/Download/klwp-rebuild-ui.xml')
 raw=run('shell','cat','/sdcard/Download/klwp-rebuild-ui.xml');root=ET.fromstring(raw)
 print(label,[n.get('content-desc') for n in root.iter('node') if '页' in n.get('content-desc','')],flush=True)
 (out/(label+'.xml')).write_bytes(raw);(out/(label+'.png')).write_bytes(run('exec-out','screencap','-p'))
cap('closed-page2')
for label,start,end in [('closed-page1',160,1040),('returned-page2',1040,160),('closed-page3',1040,160),('closed-page4',1040,160),('back-page3',160,1040),('back-page2',160,1040)]:
 run('shell','input','swipe',start,1160,end,1160,650);time.sleep(1.5);cap(label)
