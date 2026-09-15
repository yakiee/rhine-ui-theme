import re,time,json,xml.etree.ElementTree as ET
from pathlib import Path
from rebuild_ui import run
def ui():
    raw=run('shell','dumpsys','activity','activities').decode(errors='replace')
    assert any('topResumedActivity' in s and 'com.android.wallpaper.livepicker/' in s for s in raw.splitlines()),'Expected live wallpaper system preview'
    run('shell','uiautomator','dump','/sdcard/rhine-apply-home.xml')
    return ET.fromstring(run('shell','cat','/sdcard/rhine-apply-home.xml'))
def click(n):
    x1,y1,x2,y2=map(int,re.findall(r'\d+',n.get('bounds')));run('shell','input','tap',(x1+x2)//2,(y1+y2)//2);time.sleep(.5)
r=ui();click(next(n for n in r.iter('node') if n.get('resource-id','').endswith('/preview_attribution_pane_set_wallpaper_button')))
r=ui();click(next(n for n in r.iter('node') if n.get('text')=='主屏幕'))
run('shell','input','keyevent',3);time.sleep(.8)
raw=run('shell','dumpsys','wallpaper').decode(errors='replace')
summary=[s.strip() for s in raw.splitlines() if 'mWhich=' in s or 'mWallpaperComponent=' in s]
assert 'MoonSuperWallpaper' in raw and 'org.kustom.wallpaper.huawei' in raw
out=Path('rhine_exact/output/dock-toolbar-motion-20260915')
(out/'wallpaper-after-reload.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print('Saved theme reloaded on home screen; Moon lockscreen confirmed')
