import sys,io,base64
from pathlib import Path
sys.path.insert(0,'rhine_exact/tools')
import cv2
from PIL import Image,ImageDraw
out=Path('rhine_exact/output/open-dock-swipe-20260915');label=sys.argv[1]
cap=cv2.VideoCapture(str(out/(label+'.mp4')))
times=[.5,1,1.3,1.6,2.4,3.4,3.7,4,4.6,5.5]
sheet=Image.new('RGB',(1000,910),'#222222');d=ImageDraw.Draw(sheet)
for index,stamp in enumerate(times):
    cap.set(cv2.CAP_PROP_POS_MSEC,stamp*1000);ok,frame=cap.read()
    if not ok:continue
    im=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB));im.thumbnail((198,430))
    x=(index%5)*200;y=(index//5)*455;sheet.paste(im,(x,y+20));d.text((x,y),str(stamp),fill='white')
sheet.save(out/(label+'-contact.jpg'));sheet.thumbnail((850,775));buf=io.BytesIO();sheet.save(buf,format='JPEG',quality=24)
print('IMAGE:'+base64.b64encode(buf.getvalue()).decode())
