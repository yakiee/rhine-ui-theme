from rebuild_ui import run
from pathlib import Path
import time,xml.etree.ElementTree as ET
out=Path('rhine_exact/output/dock-phone-fix-20260914/second-page-only')
# Leave the terminal page; the existing page-change flow should close it.
run('shell','input','swipe',1040,1160,160,1160,650);time.sleep(1)
run('shell','input','swipe',160,1160,1040,1160,650);time.sleep(2)
(out/'terminal-leave-return.png').write_bytes(run('exec-out','screencap','-p'))
run('shell','am','start','-W','-a','android.settings.SETTINGS');time.sleep(.5)
run('shell','input','keyevent',3);time.sleep(2)
(out/'final-settings-return.png').write_bytes(run('exec-out','screencap','-p'))
run('shell','uiautomator','dump','/sdcard/Download/klwp-rebuild-ui.xml');raw=run('shell','cat','/sdcard/Download/klwp-rebuild-ui.xml');root=ET.fromstring(raw);print([n.get('content-desc') for n in root.iter('node') if '页' in n.get('content-desc','')]);(out/'final-settings-return.xml').write_bytes(raw)
print('Wallpaper process',run('shell','pidof','org.kustom.wallpaper').decode().strip())
