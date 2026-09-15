from rebuild_ui import run
import time
from pathlib import Path
run('shell','input','tap',1014,1967);time.sleep(3)
p=Path('rhine_exact/output/dock-phone-fix-20260914/second-page-only/terminal-after-service-restart.png');p.write_bytes(run('exec-out','screencap','-p'))
print(run('shell','pidof','org.kustom.wallpaper').decode())
