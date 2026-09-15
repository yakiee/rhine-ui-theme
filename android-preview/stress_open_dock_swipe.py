import json,time
from pathlib import Path
from rebuild_ui import run
OUT=Path('rhine_exact/output/open-dock-swipe-20260915')
def guard():
    raw=run('shell','dumpsys','activity','activities').decode(errors='replace')
    assert any('topResumedActivity' in s and 'com.miui.home/.launcher.Launcher' in s for s in raw.splitlines()),'Phone left launcher'
def command(*args):guard();run('shell','input',*args)
def shot(name):guard();(OUT/(name+'.png')).write_bytes(run('exec-out','screencap','-p'))
raw=run('shell','dumpsys','activity','activities').decode(errors='replace')
assert any('topResumedActivity' in s and ('com.miui.home/' in s or 'org.kustom.wallpaper.huawei/' in s) for s in raw.splitlines())
run('shell','input','keyevent',3);time.sleep(.8)
for label,direction,duration,pause in [('left-normal','left',650,.8),('right-normal','right',650,.8),('left-fast','left',300,.06),('right-fast','right',300,.06)]:
    command('tap',140,1150);time.sleep(.35);command('tap',1010,1971);time.sleep(.6);shot(label+'-opened')
    start,end=(1040,160) if direction=='left' else (160,1040)
    command('swipe',start,1150,end,1150,duration);time.sleep(pause)
    command('swipe',end,1150,start,1150,duration);time.sleep(1.1);shot(label+'-returned')
    print('CAPTURED',label,flush=True)
command('tap',140,1150);time.sleep(.4);command('tap',1010,1971);time.sleep(.5)
command('swipe',600,1150,645,1150,500);time.sleep(.7);shot('partial-cancelled')
command('tap',140,1150);time.sleep(.6);shot('final-closed')
print('Captured both directions, quick reversals, small cancelled drag, and final close')
