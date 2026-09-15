import json,subprocess,time,sys
from pathlib import Path
from rebuild_ui import run,ADB,SERIAL
out=Path('rhine_exact/output/dock-toolbar-motion-20260915');out.mkdir(exist_ok=True)
label=sys.argv[1]
events=[]
def guard():
    raw=run('shell','dumpsys','activity','activities').decode(errors='replace')
    assert any('topResumedActivity' in s and 'com.miui.home/.launcher.Launcher' in s for s in raw.splitlines()),'Phone left launcher; stopping gestures'
def gesture(name,*args):
    guard();start=time.monotonic()-began;run('shell','input',*args);events.append({'name':name,'start':start,'end':time.monotonic()-began})
guard();run('shell','input','tap',140,1150);time.sleep(.6)
remote='/sdcard/Download/rhine-dock-toolbar-'+label+'.mp4'
began=time.monotonic()
record=subprocess.Popen([ADB,'-s',SERIAL,'shell','screenrecord','--size','720x1564','--bit-rate','4500000','--time-limit','12',remote],stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
try:
    time.sleep(.7)
    gesture('open','tap',1010,1971);time.sleep(.7)
    gesture('close','tap',140,1150);time.sleep(.7)
    gesture('open-again','tap',1010,1971);time.sleep(.14)
    gesture('reverse-close','tap',140,1150);time.sleep(.6)
    gesture('swipe-away','swipe',1040,1150,160,1150,900);time.sleep(.3)
    gesture('swipe-return','swipe',160,1150,1040,1150,900);time.sleep(.65)
    gesture('open-after-swipe','tap',1010,1971);time.sleep(.7)
    gesture('final-close','tap',140,1150)
finally:
    stdout,stderr=record.communicate(timeout=16)
    (out/(label+'-events.json')).write_text(json.dumps(events,indent=2),encoding='utf-8')
if record.returncode:raise RuntimeError(stderr.decode(errors='replace'))
run('pull',remote,(out/(label+'.mp4')).resolve())
guard();(out/(label+'-final.png')).write_bytes(run('exec-out','screencap','-p'))
print('Recorded complete open/close, rapid reversal and page return:',label)
