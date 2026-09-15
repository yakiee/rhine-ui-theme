from rebuild_ui import run
from pathlib import Path
import time
out=Path('rhine_exact/output/dock-opacity-controls-20260914')
run('shell','input','keyevent',3)
time.sleep(.6)
(out/'before-renderer-restart.png').write_bytes(run('exec-out','screencap','-p'))
run('shell','am','force-stop','org.kustom.wallpaper.huawei')
run('shell','am','start','-W','-a','android.service.wallpaper.CHANGE_LIVE_WALLPAPER','--ecn','android.service.wallpaper.extra.LIVE_WALLPAPER_COMPONENT','org.kustom.wallpaper.huawei/org.kustom.wallpaper.WpGLService')
print('Restarted KLWP and opened the system live wallpaper preview.')
