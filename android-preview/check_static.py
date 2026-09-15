import subprocess,time,json,hashlib
from pathlib import Path
ADB=str(Path('android-preview/sdk/platform-tools/adb.exe').resolve());OUT=Path('rhine_exact/output/static-v0.1');REPORT=[]
def run(*a):
 r=subprocess.run([ADB,'-s','emulator-5580',*a],capture_output=True,timeout=20)
 if r.returncode:raise RuntimeError(r.stderr.decode(errors='replace'))
 return r.stdout
def tap(x,y):run('shell','input','tap',str(x),str(y));time.sleep(.65)
def save(name):
 time.sleep(.4);data=run('exec-out','screencap','-p');(OUT/'screens'/f'{name}.png').write_bytes(data);REPORT.append({'screen':name,'sha256':hashlib.sha256(data).hexdigest()});print(name,flush=True)
tap(480,96)
run('shell','am','start','-a','android.service.wallpaper.CHANGE_LIVE_WALLPAPER','--ecn','android.service.wallpaper.extra.LIVE_WALLPAPER_COMPONENT','org.kustom.wallpaper/.WpGLService');time.sleep(1)
tap(360,1438);tap(280,774);run('shell','input','keyevent','3');time.sleep(1)
save('01-home');tap(148,211);save('02-control');tap(530,735);save('08-appearance');tap(502,289);save('09-function');tap(210,289);tap(491,1167);save('10-loading');tap(360,1447);tap(609,1221);save('03-apps');tap(148,211);tap(609,1050);save('04-weather');tap(184,438);save('05-weather-detail');tap(618,274);tap(522,204);save('06-music');tap(605,204);save('07-calendar');tap(130,206)
(OUT/'runtime-check.json').write_text(json.dumps({'device':'emulator-5580','android':'11','klwp':'3.82aosp','screens':REPORT,'all_distinct':len({a['sha256'] for a in REPORT})==len(REPORT),'wallpaper_component':run('shell','dumpsys','wallpaper').decode(errors='replace')},indent=2),encoding='utf8')
