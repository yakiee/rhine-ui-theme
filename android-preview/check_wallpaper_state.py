from rebuild_ui import run
from pathlib import Path
for cmd in [('shell','settings','get','global','low_power'),('shell','settings','get','global','animator_duration_scale'),('shell','dumpsys','activity','services','org.kustom.wallpaper.huawei')]:
 s=run(*cmd).decode(errors='replace');print(' '.join(cmd),s[:9000]);
