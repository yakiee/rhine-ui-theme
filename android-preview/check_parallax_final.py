from pathlib import Path
import subprocess,time
ADB=str(Path('android-preview/sdk/platform-tools/adb.exe').resolve());OUT=Path('rhine_exact/output/parallax-v0.8');SC=OUT/'screens'
def run(*args):return subprocess.check_output([ADB,'-s','emulator-5580',*args],timeout=20)
def tap(x,y):run('shell','input','tap',str(x),str(y));time.sleep(1.2)
def pose(x,y,z=8.96):run('emu','sensor','set','acceleration',f'{x}:{y}:{z}')
def shot(name):SC.joinpath(name+'.png').write_bytes(run('exec-out','screencap','-p'))
pose(0,0,9.81);time.sleep(2);tap(360,1390);shot('menu-neutral')
rec=subprocess.Popen([ADB,'-s','emulator-5580','shell','screenrecord','--bit-rate','5000000','--time-limit','18','/sdcard/Movies/rhine-parallax-final.mp4'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
for name,x,y in [('menu-left',-4,0),('menu-right',4,0),('menu-forward',0,4),('menu-back',0,-4),('menu-return',0,0)]:
 pose(x,y,9.81 if x==y==0 else 8.96);time.sleep(2.5);shot(name)
tap(480,690);tap(520,294);shot('settings-final');tap(130,206);tap(360,1390);shot('final-menu')
rec.communicate(timeout=20);run('pull','/sdcard/Movies/rhine-parallax-final.mp4',str(OUT/'parallax-demo.mp4'));print('Final recording captured')
