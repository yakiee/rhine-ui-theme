from pathlib import Path
import subprocess,time,io
from PIL import Image,ImageDraw
base=Path.cwd();out=base/'rhine_exact/output/desktop-dock-fold-v0.13.47/verification';adb=str(base/'android-preview/sdk/platform-tools/adb.exe')
def run(*a):return subprocess.run([adb,'-s','emulator-5580',*a],capture_output=True,check=True).stdout
def shot(name):Image.open(io.BytesIO(run('exec-out','screencap','-p'))).convert('RGB').save(out/(name+'.jpg'))
def swipe(x,y):run('shell','input','swipe',str(x),'750',str(y),'750','450');time.sleep(2)
shot('01-native-flat')
swipe(610,100);shot('02-home-diagonal')
swipe(100,620);shot('03-native-flat-again')
swipe(610,100)
run('shell','input','tap','595','1185');time.sleep(2);shot('04-terminal-hidden-dock')
swipe(100,620);shot('05-terminal-to-native-flat')
swipe(610,100);shot('06-final-home')
canvas=Image.new('RGB',(1200,465),'#222')
for i,path in enumerate(sorted(out.glob('0*.jpg'))):
 im=Image.open(path);im.thumbnail((200,440));canvas.paste(im,(i*200,25));ImageDraw.Draw(canvas).text((i*200+4,5),path.stem,fill='white')
canvas.save(out/'dock-fold-check.jpg')
print('Saved screenshots')
