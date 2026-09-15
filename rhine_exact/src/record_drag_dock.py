from pathlib import Path
import subprocess,time,sys
base=Path.cwd();out=base/'rhine_exact/output/drag-dock-v0.13.50/verification';out.mkdir(exist_ok=True);adb=str(base/'android-preview/sdk/platform-tools/adb.exe')
def run(*a):return subprocess.run([adb,'-s','emulator-5580',*a],capture_output=True,check=True).stdout
rec=subprocess.Popen([adb,'-s','emulator-5580','shell','screenrecord','--bit-rate','4000000','--time-limit','20','/sdcard/Movies/dock-drag-v50.mp4'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
time.sleep(1)
run('shell','input','swipe','80','1000','670','1000','3000');time.sleep(1)
run('shell','input','swipe','670','1000','80','1000','3000');time.sleep(1)
rec.communicate(timeout=15);run('pull','/sdcard/Movies/dock-drag-v50.mp4',str(out/'drag-demo.mp4'))
sys.path.insert(0,str(base/'rhine_exact/tools'));import cv2
from PIL import Image,ImageDraw
cap=cv2.VideoCapture(str(out/'drag-demo.mp4'));canvas=Image.new('RGB',(1800,425),'#222')
for i,t in enumerate([.5,1.5,2,2.5,3,4.5,7,9,13]):
 cap.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,frame=cap.read()
 if ok:
  im=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB));im.thumbnail((180,400));canvas.paste(im,(i*200,25));ImageDraw.Draw(canvas).text((i*200+4,4),str(t)+'s',fill='white')
cap.release();canvas.save(out/'video-drag-check.jpg');print('Recorded')
