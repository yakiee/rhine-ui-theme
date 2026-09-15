from pathlib import Path
import subprocess,time,json
ADB=str(Path('android-preview/sdk/platform-tools/adb.exe').resolve())
OUT=Path('rhine_exact/output/diagonal-v0.3');(OUT/'screens').mkdir(exist_ok=True)
def run(*a):
 r=subprocess.run([ADB,'-s','emulator-5580',*a],capture_output=True,timeout=20)
 if r.returncode:raise RuntimeError(r.stderr.decode(errors='replace'))
 return r.stdout
def shot(name):(OUT/'screens'/f'{name}.png').write_bytes(run('exec-out','screencap','-p'))
rec=subprocess.Popen([ADB,'-s','emulator-5580','shell','screenrecord','--bit-rate','6000000','--time-limit','45','/sdcard/Movies/rhine-diagonal-v03.mp4'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
start=time.monotonic();events=[]
shot('00-home')
def action(name,x,y,pause=1.5):
 events.append({'name':name,'time_s':round(time.monotonic()-start,3),'x':x,'y':y})
 run('shell','input','tap',str(x),str(y));time.sleep(pause);shot(name);print(name,flush=True)
action('01-control',148,215)
action('02-applications',596,1230)
action('03-control-return',148,215)
action('04-home-return',360,1390)
action('05-weather',596,1050,2)
action('06-home',130,206)
action('07-music',596,1112,2)
action('08-home',130,206)
action('09-calendar',596,1172,2)
action('10-home',130,206)
(OUT/'interaction-events.json').write_text(json.dumps(events,indent=2),encoding='utf8')
rec.communicate(timeout=max(2,50-(time.monotonic()-start)))
run('pull','/sdcard/Movies/rhine-diagonal-v03.mp4',str(OUT/'interaction-demo.mp4'))
print('recorded',time.monotonic()-start,flush=True)
