from pathlib import Path
p=Path('android-preview/record_dock_performance.py')
s=p.read_text(encoding='utf-8')
marker="label = sys.argv[1]"
guard="""def require_launcher():
    activity = run('shell','dumpsys','activity','activities').decode(errors='replace')
    if not any('topResumedActivity' in line and 'com.miui.home/.launcher.Launcher' in line for line in activity.splitlines()):
        raise RuntimeError('Foreground changed; stopped before next touch')

"""
if 'def require_launcher()' not in s:
    s=s.replace(marker,guard+marker)
    s=s.replace("run('shell', 'input',", "require_launcher()\nrun('shell', 'input',")
    p.write_text(s,encoding='utf-8')
out=Path('rhine_exact/output/animation-performance-20260915').resolve()
for name in ['zhuang-final.mp4','zhuang-final-contact.jpg','zhuang-final-video-analysis.json']:
    target=out/name
    assert target.parent==out
    if target.exists():target.unlink()
from rebuild_ui import run
run('shell','rm','-f','/sdcard/Download/rhine-performance-zhuang-final.mp4')
print('Added per-action foreground guard; removed interrupted private-app recording.')
