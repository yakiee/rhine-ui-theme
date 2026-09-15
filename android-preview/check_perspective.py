from pathlib import Path
import subprocess,time,json
ADB=str(Path('android-preview/sdk/platform-tools/adb.exe').resolve());OUT=Path('rhine_exact/output/perspective-v0.4');(OUT/'screens').mkdir(exist_ok=True)
def run(*args):
 r=subprocess.run([ADB,'-s','emulator-5580',*args],capture_output=True,timeout=20)
 if r.returncode:raise RuntimeError(r.stderr.decode(errors='replace'))
 return r.stdout
def tap(x,y,delay=1):run('shell','input','tap',str(x),str(y));time.sleep(delay)
def shot(name):(OUT/'screens'/f'{name}.png').write_bytes(run('exec-out','screencap','-p'))
shot('02-settings-center');tap(130,206)
rec=subprocess.Popen([ADB,'-s','emulator-5580','shell','screenrecord','--bit-rate','5000000','--time-limit','25','/sdcard/Movies/rhine-perspective-v04.mp4'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
start=time.monotonic();events=[];shot('00-home')
def action(name,x,y,delay=1.2):
 events.append({'name':name,'time_s':round(time.monotonic()-start,3),'x':x,'y':y});tap(x,y,delay);shot(name);print(name,flush=True)
action('01-dock-menu',360,1390)
action('03-settings-tilted-edge',447,645)
action('04-return-home',130,206)
action('05-dock-reopen',360,1390)
for index in range(4):
 events.append({'name':'rapid-dock-'+str(index),'time_s':round(time.monotonic()-start,3),'x':360,'y':1390});tap(360,1390,.06)
time.sleep(1.4);shot('06-rapid-final-menu')
(OUT/'interaction-events.json').write_text(json.dumps(events,indent=2),encoding='utf8')
rec.communicate(timeout=max(2,30-(time.monotonic()-start)))
run('pull','/sdcard/Movies/rhine-perspective-v04.mp4',str(OUT/'interaction-demo.mp4'));print('recorded',flush=True)
