from pathlib import Path
import subprocess,time,json
ADB=str(Path('android-preview/sdk/platform-tools/adb.exe').resolve());OUT=Path('rhine_exact/output/interactive-v0.2');(OUT/'screens').mkdir(exist_ok=True)
def run(*a):
 r=subprocess.run([ADB,'-s','emulator-5580',*a],capture_output=True,timeout=20)
 if r.returncode:raise RuntimeError(r.stderr.decode(errors='replace'))
 return r.stdout

def tap(x,y,delay=.8):run('shell','input','tap',str(x),str(y));time.sleep(delay)
def shot(name):(OUT/'screens'/f'{name}.png').write_bytes(run('exec-out','screencap','-p'))
run('shell','input','keyevent','3');time.sleep(1)
rec=subprocess.Popen([ADB,'-s','emulator-5580','shell','screenrecord','--bit-rate','6000000','--time-limit','60','/sdcard/Movies/rhine-motion-v02.mp4'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
start=time.monotonic();events=[]
def action(name,x,y,pause=1.5):
 events.append({'name':name,'time_s':round(time.monotonic()-start,3),'x':x,'y':y});tap(x,y,pause);shot(name);print(name,flush=True)
time.sleep(1);shot('00-home')
action('01-control',148,211);action('02-settings',530,735);action('03-blue-feedback',350,510,.6);action('04-functions',502,289);action('05-dark',350,470,.6);action('06-light',165,470,.6);action('07-home',130,206);action('08-apps',609,1221);action('09-control',148,211);action('10-weather',609,1050,2.2);action('11-detail',184,438);action('12-close-detail',618,274);action('13-music',522,204);action('14-pause',359,1365,.6);action('15-calendar',605,204);action('16-date-selection',331,482,.6)
# Stress rapid navigation, then allow every exit track to settle.
for name,x in [('17-rapid-weather',447),('18-rapid-music',522),('19-rapid-calendar',605)]:
 events.append({'name':name,'time_s':round(time.monotonic()-start,3),'x':x,'y':204});tap(x,204,.06)
time.sleep(1.8);shot('19-rapid-calendar');action('20-home',130,206)
(OUT/'interaction-events.json').write_text(json.dumps(events,indent=2),encoding='utf8')
remaining=max(1,65-(time.monotonic()-start));rec.communicate(timeout=remaining)
run('pull','/sdcard/Movies/rhine-motion-v02.mp4',str(OUT/'interaction-demo.mp4'))
print('recorded',flush=True)
