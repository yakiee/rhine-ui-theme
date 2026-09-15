from pathlib import Path
import subprocess,time,json
ADB=str(Path('android-preview/sdk/platform-tools/adb.exe').resolve());OUT=Path('rhine_exact/output/matched-v0.5')
def run(*args):
 r=subprocess.run([ADB,'-s','emulator-5580',*args],capture_output=True,timeout=30)
 if r.returncode:raise RuntimeError(r.stderr.decode(errors='replace'))
 return r.stdout
def tap(x,y,delay=1):run('shell','input','tap',str(x),str(y));time.sleep(delay)
def shot(name):(OUT/'screens'/f'{name}.png').write_bytes(run('exec-out','screencap','-p'))
tap(360,1390);shot('15-normal-menu')
for _ in range(4):tap(360,1390,.06)
time.sleep(1.3);shot('16-rapid-menu')
tap(480,690);tap(350,510);tap(210,730);tap(130,206);shot('17-blue-no-dots')
tap(360,1390);tap(480,690);tap(164,510);tap(491,730);tap(130,206);shot('18-gold-dots-restored')
tap(596,1129,2);shot('19-calendar-final');tap(130,206);tap(360,1390);shot('20-final-menu')
print('Extra checks captured')
