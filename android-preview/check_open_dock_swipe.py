import json,subprocess,time,sys
from pathlib import Path
from rebuild_ui import run,ADB,SERIAL
out=Path('rhine_exact/output/open-dock-swipe-20260915');out.mkdir(exist_ok=True)
label=sys.argv[1]; events=[]
def guard():
    raw=run('shell','dumpsys','activity','activities').decode(errors='replace')
    assert any('topResumedActivity' in s and 'com.miui.home/.launcher.Launcher' in s for s in raw.splitlines()),'Phone left launcher'
def gesture(name,*args):
    guard();start=time.monotonic()-began;run('shell','input',*args);events.append(dict(name=name,start=start,end=time.monotonic()-began))
guard()
remote='/sdcard/Download/rhine-open-swipe-'+label+'.mp4'
began=time.monotonic()
record=subprocess.Popen([ADB,'-s',SERIAL,'shell','screenrecord','--size','720x1564','--bit-rate','3500000','--time-limit','9',remote],stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
time.sleep(.8)
gesture('opened-away','swipe',1040,1150,160,1150,1100);time.sleep(1)
gesture('return','swipe',160,1150,1040,1150,1100);time.sleep(1)
guard();(out/(label+'-returned.png')).write_bytes(run('exec-out','screencap','-p'))
stdout,stderr=record.communicate(timeout=12)
assert record.returncode==0,stderr
run('pull',remote,(out/(label+'.mp4')).resolve())
(out/(label+'-events.json')).write_text(json.dumps(events,indent=2),encoding='utf-8')
print(label,events)
