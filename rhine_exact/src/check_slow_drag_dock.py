from pathlib import Path
import subprocess,time,io
from PIL import Image,ImageDraw
base=Path.cwd();out=base/'rhine_exact/output/drag-dock-v0.13.49/verification';adb=str(base/'android-preview/sdk/platform-tools/adb.exe')
def run(*a):return subprocess.run([adb,'-s','emulator-5580',*a],capture_output=True,check=True).stdout
def shot(n):Image.open(io.BytesIO(run('exec-out','screencap','-p'))).convert('RGB').save(out/(n+'.jpg'))
run('shell','input','keyevent','4');time.sleep(1)
shot('slow-00-home')
for direction,a,b in [('forward',80,670),('back',670,80)]:
 proc=subprocess.Popen([adb,'-s','emulator-5580','shell','input','swipe',str(a),'750',str(b),'750','4200'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 for i in range(5):
  time.sleep(.65);shot(f'slow-{direction}-{i}')
 proc.communicate(timeout=10);time.sleep(1);shot('slow-'+direction+'-end')
canvas=Image.new('RGB',(1600,450),'#222')
for i,n in enumerate(['slow-00-home','slow-forward-0','slow-forward-1','slow-forward-2','slow-forward-3','slow-forward-end','slow-back-2','slow-back-end']):
 im=Image.open(out/(n+'.jpg'));im.thumbnail((200,420));canvas.paste(im,(i*200,25));ImageDraw.Draw(canvas).text((i*200+3,5),n,fill='white')
canvas.save(out/'slow-drag-check.jpg');print('Saved slow drag')
