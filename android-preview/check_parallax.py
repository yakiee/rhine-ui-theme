from pathlib import Path
import subprocess,time,math,json
ADB=str(Path('android-preview/sdk/platform-tools/adb.exe').resolve());OUT=Path('rhine_exact/output/parallax-v0.8');SC=OUT/'screens'
def run(*args):return subprocess.check_output([ADB,'-s','emulator-5580',*args],timeout=20)
def tap(x,y):run('shell','input','tap',str(x),str(y));time.sleep(1.2)
def pose(x,y,z=8.96):run('emu','sensor','set','acceleration',f'{x}:{y}:{z}')
def shot(name):SC.joinpath(name+'.png').write_bytes(run('exec-out','screencap','-p'))
pose(0,0,9.81);time.sleep(2);tap(360,1390);shot('menu-neutral')
rec=subprocess.Popen([ADB,'-s','emulator-5580','shell','screenrecord','--bit-rate','5000000','--time-limit','24','/sdcard/Movies/rhine-parallax-v08.mp4'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
for name,x,y in [('menu-left',-4,0),('menu-right',4,0),('menu-forward',0,4),('menu-back',0,-4),('menu-return',0,0)]:
 pose(x,y,9.81 if x==y==0 else 8.96);time.sleep(2.6);shot(name)
tap(480,690);tap(520,294);shot('settings-gyro-on');tap(200,1180);shot('settings-gyro-off');tap(130,206)
pose(-4,0);time.sleep(2);shot('disabled-left');pose(4,0);time.sleep(2);shot('disabled-right')
pose(0,0,9.81);tap(360,1390);tap(480,690);tap(520,294);tap(490,1180);shot('settings-gyro-restored');tap(130,206);tap(360,1390);shot('final-menu')
rec.communicate(timeout=10);run('pull','/sdcard/Movies/rhine-parallax-v08.mp4',str(OUT/'parallax-demo.mp4'));print('Parallax verification captured')
