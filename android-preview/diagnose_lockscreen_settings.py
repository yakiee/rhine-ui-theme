from pathlib import Path
import json
import re
from rebuild_ui import run

out = Path('rhine_exact/output/lockscreen-diagnosis-20260915')
out.mkdir(exist_ok=True)
report = {}
for namespace in ('secure', 'system', 'global'):
    raw = run('shell', 'settings', 'list', namespace).decode(errors='replace')
    selected = {}
    for line in raw.splitlines():
        key, separator, value = line.partition('=')
        if separator and re.search(r'lock.?screen|lock.?wallpaper|wallpaper.*(type|provider)|notification.*(lock|private|sensitive|hide)|face.*(notification|privacy)|zen_mode$', key, re.I):
            selected[key] = value
    report[namespace] = selected
wallpaper = run('shell', 'dumpsys', 'wallpaper').decode(errors='replace')
(out / 'wallpaper-state.txt').write_text(wallpaper, encoding='utf-8')
report['wallpaper_summary'] = [line.strip() for line in wallpaper.splitlines() if re.search(r'lock|which|component|wallpaperId|mId=|mName=|mWallpaperFile|mCropFile|mIsColorExtracted|mWallpaperDimAmount', line, re.I)]
power = run('shell', 'dumpsys', 'power').decode(errors='replace')
report['power'] = [line.strip() for line in power.splitlines() if 'mWakefulness=' in line or 'mDisplayReady=' in line]
(out / 'settings-before.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=True, indent=2))
