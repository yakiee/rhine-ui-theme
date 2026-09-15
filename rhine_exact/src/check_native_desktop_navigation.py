from pathlib import Path
import subprocess,time,io
from PIL import Image,ImageOps,ImageDraw
base=Path.cwd();out=base/'rhine_exact/output/native-desktop-navigation-v0.13.46/verification';out.mkdir(exist_ok=True)
adb=str(base/'android-preview/sdk/platform-tools/adb.exe')
def run(*args):return subprocess.run([adb,'-s','emulator-5580',*args],capture_output=True,check=True).stdout
def tap(x,y):run('shell','input','tap',str(x),str(y));time.sleep(2)
def shot(name):Image.open(io.BytesIO(run('exec-out','screencap','-p'))).convert('RGB').save(out/(name+'.jpg'))
time.sleep(2);shot('01-home')
tap(595,1185);shot('02-terminal-from-dock')
tap(448,376);shot('03-calendar-from-terminal')
tap(645,189);shot('04-back-to-terminal')
tap(130,206);shot('05-back-home')
run('shell','input','swipe','100','750','620','750','450');time.sleep(2);shot('06-native-desktop')
run('shell','input','swipe','610','750','100','750','450');time.sleep(2);shot('07-return-home-no-ghost')
tap(595,1185)
run('shell','input','swipe','100','750','620','750','450');time.sleep(2)
run('shell','input','swipe','610','750','100','750','450');time.sleep(2);shot('08-swipe-dismiss-terminal')
canvas=Image.new('RGB',(1440,430),'#222222')
for i,path in enumerate(sorted(out.glob('*.jpg'))):
 im=Image.open(path);im.thumbnail((180,400));canvas.paste(im,(i*180,25));ImageDraw.Draw(canvas).text((i*180+5,5),path.stem,fill='white')
canvas.save(out/'check.jpg')
print('saved',out/'check.jpg')
