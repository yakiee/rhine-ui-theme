from pathlib import Path
import subprocess,time,io
from PIL import Image,ImageDraw
base=Path.cwd();out=base/'rhine_exact/output/drag-dock-v0.13.49/verification';out.mkdir(exist_ok=True);adb=str(base/'android-preview/sdk/platform-tools/adb.exe')
def run(*a):return subprocess.run([adb,'-s','emulator-5580',*a],capture_output=True,check=True).stdout
def shot(n):Image.open(io.BytesIO(run('exec-out','screencap','-p'))).convert('RGB').save(out/(n+'.jpg'))
def motion(kind,x):run('shell','input','motionevent',kind,str(x),'750')
run('shell','input','swipe','610','750','100','750','450');time.sleep(2);shot('01-home')
try:
 motion('DOWN',80);motion('MOVE',120);motion('MOVE',250);time.sleep(.25);shot('02-quarter-held')
 time.sleep(1.4);shot('03-quarter-still-held')
 motion('MOVE',430);time.sleep(.3);shot('04-half-held')
 motion('MOVE',250);time.sleep(.3);shot('05-pull-back-quarter')
 motion('MOVE',100);motion('UP',100)
finally:motion('UP',100)
time.sleep(2);shot('06-cancelled-home')
run('shell','input','swipe','100','750','620','750','450');time.sleep(2);shot('07-native-flat')
run('shell','input','swipe','610','750','100','750','450');time.sleep(2);shot('08-final-home')
canvas=Image.new('RGB',(1600,465),'#222')
for i,path in enumerate(sorted(out.glob('0*.jpg'))):
 im=Image.open(path);im.thumbnail((200,440));canvas.paste(im,(i*200,25));ImageDraw.Draw(canvas).text((i*200+3,5),path.stem,fill='white')
canvas.save(out/'drag-check.jpg');print('Saved drag verification')
