from pathlib import Path
import sys
import time
import json
import shlex
from rebuild_ui import run

out = Path('rhine_exact/output/animation-performance-20260915')
out.mkdir(parents=True, exist_ok=True)
label = sys.argv[1]
layers = run('shell', 'dumpsys', 'SurfaceFlinger', '--list').decode(errors='replace')
selected = [line for line in layers.splitlines() if 'org.kustom.wallpaper.WpGLService' in line]
result = {'label': label, 'layers': selected, 'latencies': {}}
for layer in selected:
    name = layer.split('RequestedLayerState{', 1)[-1].split(' parentId=', 1)[0]
    result['latencies'][name] = run('shell', 'dumpsys SurfaceFlinger --latency ' + shlex.quote(name)).decode(errors='replace')
for package in ('org.kustom.wallpaper.huawei', 'com.miui.home'):
    raw = run('shell', 'dumpsys', 'gfxinfo', package).decode(errors='replace')
    (out / (label + '-' + package + '-gfx.txt')).write_text(raw, encoding='utf-8')
    result[package] = [line.strip() for line in raw.splitlines() if any(k in line for k in ('Total frames', 'Janky frames', 'percentile', 'Number Missed'))]
(out / (label + '.json')).write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=True)[:11000])
