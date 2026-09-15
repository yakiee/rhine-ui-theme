from pathlib import Path
import subprocess,time,json
ADB=str(Path('android-preview/sdk/platform-tools/adb.exe').resolve());OUT=Path('rhine_exact/output/material-v0.7');(OUT/'screens').mkdir(exist_ok=True)
def run(*args):
 r=subprocess.run([ADB,'-s','emulator-5580',*args],capture_output=True,timeout=30)
 if r.returncode:raise RuntimeError(r.stderr.decode(errors='replace'))
 return r.stdout
def tap(x,y,delay=1):run('shell','input','tap',str(x),str(y));time.sleep(delay)
def shot(name):(OUT/'screens'/(name+'.png')).write_bytes(run('exec-out','screencap','-p'))
rec=subprocess.Popen([ADB,'-s','emulator-5580','shell','screenrecord','--bit-rate','5000000','--time-limit','45','/sdcard/Movies/rhine-material-v07.mp4'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
start=time.monotonic();events=[];time.sleep(.8);shot('00-home')
def action(name,x,y,delay=1):
 events.append({'name':name,'time_s':round(time.monotonic()-start,3),'x':x,'y':y});tap(x,y,delay);shot(name);print(name,flush=True)
action('01-menu',360,1390)
action('02-appearance',480,690)
action('03-function',520,294)
action('04-appearance-return',200,294)
action('05-blue-selected',350,510)
action('06-dots-off',210,730)
action('07-blue-home',130,206)
action('08-blue-menu',360,1390)
action('09-settings-edge',450,675)
tap(164,510);tap(491,730)
action('10-gold-home',130,206)
action('11-apps',596,1184)
action('12-apps-to-menu',360,1390)
action('13-home-return',360,1390)
(OUT/'interaction-events.json').write_text(json.dumps(events,indent=2),encoding='utf8')
rec.communicate(timeout=max(5,50-(time.monotonic()-start)));run('pull','/sdcard/Movies/rhine-material-v07.mp4',str(OUT/'interaction-demo.mp4'));print('Recorded')
