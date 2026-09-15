from pathlib import Path
import subprocess,time,io
from PIL import Image,ImageDraw
base=Path.cwd();out=base/'rhine_exact/output/native-desktop-navigation-v0.13.45/verification';adb=str(base/'android-preview/sdk/platform-tools/adb.exe')
def run(*a):return subprocess.run([adb,'-s','emulator-5580',*a],capture_output=True,check=True).stdout
def tap(x,y):run('shell','input','tap',str(x),str(y));time.sleep(2)
def swipe(a,b):run('shell','input','swipe',str(a),'750',str(b),'750','450');time.sleep(2)
def shot(name):Image.open(io.BytesIO(run('exec-out','screencap','-p'))).convert('RGB').save(out/(name+'.jpg'))
tap(615,480)
activity=run('shell','dumpsys','activity','activities').decode(errors='replace');(out/'native-app-open.txt').write_text('\n'.join(s for s in activity.splitlines() if 'ResumedActivity' in s),encoding='utf-8')
run('shell','input','keyevent','3');time.sleep(3)
swipe(610,100);shot('01-home')
tap(595,1185);tap(520,665);shot('07-music-from-terminal')
tap(130,206);shot('08-music-back-terminal')
swipe(100,620);shot('09-swipe-closes-terminal')
swipe(610,100);shot('10-return-clean-home')
tap(595,1185);tap(578,212)
activity=run('shell','dumpsys','activity','activities').decode(errors='replace');(out/'config-entry.txt').write_text('\n'.join(s for s in activity.splitlines() if 'ResumedActivity' in s),encoding='utf-8')
run('shell','input','keyevent','3');time.sleep(3)
tap(130,206);shot('11-final-home')
canvas=Image.new('RGB',(1100,445),'#222222')
for i,name in enumerate(['01-home','02-terminal-from-dock','05-back-home','06-native-desktop','10-return-clean-home']):
 im=Image.open(out/(name+'.jpg'));im.thumbnail((220,420));canvas.paste(im,(i*220,25));ImageDraw.Draw(canvas).text((i*220+4,5),name,fill='white')
canvas.save(out/'navigation-final.jpg')
print((out/'native-app-open.txt').read_text());print((out/'config-entry.txt').read_text())
