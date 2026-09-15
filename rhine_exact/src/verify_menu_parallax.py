from pathlib import Path
import subprocess,time,json
from PIL import Image
BASE=Path('rhine_exact');OUT=BASE/'output/menu-parallax-v0.13.25'; V=OUT/'verification';V.mkdir(exist_ok=True)
adb=str(Path('android-preview/sdk/platform-tools/adb.exe').resolve())
def run(*args):return subprocess.check_output([adb,'-s','emulator-5580',*args],timeout=20)
def pose(x):run('emu','sensor','set','acceleration',f'{x}:0:{(9.81**2-x*x)**.5:.3f}')
def shot(name):(V/(name+'.png')).write_bytes(run('exec-out','screencap','-p'))
rec=subprocess.Popen([adb,'-s','emulator-5580','shell','screenrecord','--bit-rate','3500000','--time-limit','15','/sdcard/Movies/rhine-menu-v1325.mp4'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
try:
 pose(0);time.sleep(1);shot('neutral')
 for x in [-1,-2,-3]:pose(x);time.sleep(.45)
 time.sleep(.8);shot('left')
 for x in [-2,-1,0,1,2,3]:pose(x);time.sleep(.45)
 time.sleep(.8);shot('right')
 for x in [2,1,0]:pose(x);time.sleep(.45)
 time.sleep(1);shot('returned')
finally:pose(0)
rec.communicate(timeout=20)
run('pull','/sdcard/Movies/rhine-menu-v1325.mp4',str(OUT/'parallax-demo.mp4'))
Image.open(V/'neutral.png').convert('RGB').crop((170,425,720,1030)).save(V/'menu-detail.jpg')
a=json.loads((BASE/'output/terminal-proportions-v0.13.24/preset.json').read_text(encoding='utf8')); b=json.loads((OUT/'preset.json').read_text(encoding='utf8'))
def events(n):
 if isinstance(n,dict):return [(k,v) for k,v in n.items() if k=='internal_events']+[e for v in n.values() for e in events(v)]
 if isinstance(n,list):return [e for v in n for e in events(v)]
 return []
assert events(a)==events(b)
for x,y in zip(a['preset_root']['viewgroup_items'],b['preset_root']['viewgroup_items']):
 assert [i for i in x.get('internal_animations',[]) if i.get('type')!='GYRO']==[i for i in y.get('internal_animations',[]) if i.get('type')!='GYRO']
print('Captured tilt demo; original actions and non-sensor animations verified; neutral pose restored.')
