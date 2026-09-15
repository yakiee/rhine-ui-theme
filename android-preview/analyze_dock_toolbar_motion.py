import sys,json
from pathlib import Path
sys.path.insert(0,'rhine_exact/tools')
import cv2
from PIL import Image,ImageDraw
out=Path('rhine_exact/output/dock-toolbar-motion-20260915')
label=sys.argv[1];events=json.loads((out/(label+'-events.json')).read_text(encoding='utf-8'))
video=cv2.VideoCapture(str(out/(label+'.mp4')))
frames=[]
while True:
    ok,frame=video.read()
    if not ok:break
    frames.append((video.get(cv2.CAP_PROP_POS_MSEC)/1000,frame))
video.release()
samples=[-.12,.04,.12,.20,.32,.60]
selected=[e for e in events if e['name'] in ['open','close','reverse-close','open-after-swipe']]
sheet=Image.new('RGB',(180*len(samples),200*len(selected)),'#202020');draw=ImageDraw.Draw(sheet)
for row,event in enumerate(selected):
    for col,offset in enumerate(samples):
        target=max(0,event['start']+offset)
        timestamp,frame=min(frames,key=lambda f:abs(f[0]-target))
        crop=Image.fromarray(cv2.cvtColor(frame[800:1520,:],cv2.COLOR_BGR2RGB));crop.thumbnail((180,180))
        x,y=col*180,row*200;sheet.paste(crop,(x,y+20));draw.text((x+3,y+4),event['name']+' '+str(round(offset,2)),fill='white')
sheet.save(out/(label+'-motion-windows.jpg'),quality=75)
print('Extracted opening, closing, interrupted reversal and reopening windows; times relative to host input dispatch, not exact display timestamps')
