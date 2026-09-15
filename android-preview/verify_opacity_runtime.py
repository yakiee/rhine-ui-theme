import io,time,json
from pathlib import Path
from PIL import Image,ImageDraw
from rebuild_ui import run
out=Path('rhine_exact/output/opacity-repair-20260915')
shots=[]
def foreground():
    return next(s for s in run('shell','dumpsys','activity','activities').decode(errors='replace').splitlines() if 'topResumedActivity' in s)
def guard():
    assert 'com.miui.home/.launcher.Launcher' in foreground(),'Phone left launcher; stopped'
def touch(*args):
    guard();run('shell','input',*args);time.sleep(.5)
def capture(name):
    guard();raw=run('exec-out','screencap','-p');(out/(name+'.png')).write_bytes(raw)
    im=Image.open(io.BytesIO(raw)).convert('RGB');im.thumbnail((200,435))
    panel=Image.new('RGB',(200,460),'#222222');panel.paste(im,(0,25));ImageDraw.Draw(panel).text((6,6),name,fill='white');shots.append(panel)
touch('tap',140,1150);capture('01-toolbar-restored')
for i,duration in enumerate([250,700,1200],1):
    touch('tap',1010,1971);capture(f'cycle-{i}-dock')
    touch('swipe',1040,1150,160,1150,duration)
    touch('swipe',160,1150,1040,1150,duration)
    touch('tap',140,1150);capture(f'cycle-{i}-returned')
    print('Verified cycle',i,flush=True)
touch('tap',1010,1587)
top=foreground();assert 'com.android.contacts/' in top,'Unexpected application; stopping'
run('shell','input','keyevent',3);time.sleep(.6)
capture('08-app-return')
touch('tap',1010,1971);capture('09-final-dock')
touch('tap',140,1150)
sheet=Image.new('RGB',(200*5,460*2),'#222222')
for i,panel in enumerate(shots):sheet.paste(panel,((i%5)*200,(i//5)*460))
sheet.save(out/'runtime-verification.jpg',quality=75)
wall=run('shell','dumpsys','wallpaper').decode(errors='replace')
report={'cycles_ms':[250,700,1200],'phone_app_launch_verified':True,'returned_to_home':True,'moon_lockscreen_present':'MoonSuperWallpaper' in wall,'screenshots':[p.name for p in out.glob('cycle-*.png')],'editor_not_opened_during_verification':True}
(out/'runtime-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Three page cycles and app return captured; phone left on theme page')
