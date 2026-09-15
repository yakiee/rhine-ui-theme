import sys,json,math
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path('rhine_exact/tools').resolve()));import cv2
root=Path('rhine_exact/analysis/frames/f_000019')
last=cv2.imread(str(root/'065.png'));template=last[486:540,193:248]
track=[]
for f in range(51,78):
 im=cv2.imread(str(root/f'{f:03d}.png'));roi=im[390:682,:];best=(-1,None)
 # A bank of scaled templates measures actual icon movement, independently of guessed easing.
 for size in range(9,65):
  patch=cv2.resize(template,(size,size));res=cv2.matchTemplate(roi,patch,cv2.TM_CCOEFF_NORMED);_,score,_,pos=cv2.minMaxLoc(res)
  if score>best[0]:best=(score,(pos[0]+size/2,pos[1]+390+size/2,size))
 score,(x,y,size)=best
 hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV);mask=cv2.inRange(hsv,np.array([15,75,90]),np.array([43,255,255]));mask[:510]=0
 lines=cv2.HoughLinesP(mask,1,np.pi/180,60,minLineLength=155,maxLineGap=40);angles=[]
 if lines is not None:
  for seg in lines.reshape(-1,4):
   x1,y1,x2,y2=seg;angle=math.degrees(math.atan2(y2-y1,x2-x1))
   if -3<angle<28 and (y1+y2)/2>550:angles.append(angle)
 track.append({'frame':f,'t_ms':f*40,'icon_center':[round(x,2),round(y,2)],'icon_width':size,'template_ncc':round(score,4),'dock_angle_deg':round(float(np.median(angles)),2) if angles else None})
Path('rhine_exact/analysis/app-motion-measurements.json').write_text(json.dumps(track,indent=2),encoding='utf-8')
print(json.dumps(track,indent=2))
