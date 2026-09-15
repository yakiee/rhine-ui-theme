from pathlib import Path
import sys,json,subprocess,bisect
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path('rhine_exact/tools').resolve()));import cv2
out=Path('rhine_exact/output/matched-v0.5');ff=Path('C:/Users/yakieewang/.codex/skills/video-batch-download/tools/ffmpeg-9.0.1-essentials_build/bin')
a=json.loads(subprocess.run([str(ff/'ffprobe.exe'),'-v','error','-select_streams','v:0','-show_entries','frame=best_effort_timestamp_time','-of','json',str(out/'interaction-demo.mp4')],capture_output=True,check=True).stdout);pts=[float(x['best_effort_timestamp_time']) for x in a['frames']]
(out/'frame-times.json').write_text(json.dumps(pts))
v=cv2.VideoCapture(str(out/'interaction-demo.mp4'));frames=[]
for t in pts:
 if t>4:break
 ok,b=v.read()
 if not ok:break
 frames.append(Image.fromarray(cv2.cvtColor(b,cv2.COLOR_BGR2RGB)).crop((0,48,720,1552)).resize((360,800)))
v.release()
# The terminal contains a large bright panel, absent from this ROI on the home image.
bright=[]
for a in frames:
 b=np.array(a)[245:302,160:340];bright.append(float(np.mean(np.all(b>180,axis=2))))
first=next(i for i,f in enumerate(bright) if f>.12);offset=pts[first]-.24
print('first panel',pts[first],'alignment offset',offset,'brightness samples',[(round(pts[i],3),round(b,2))for i,b in enumerate(bright) if .9<pts[i]<2.8])
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',16);im=Image.new('RGB',(1080,850),'#eee');d=ImageDraw.Draw(im)
for j,t in enumerate([.24,.32,.40,.56,.72,.96]):
 idx=max(0,bisect.bisect_right(pts,t+offset)-1);x=j%3*360;y=j//3*425
 ref=Image.open(f'rhine_exact/analysis/frames/f_000019/{round(t/.04):03d}.png').resize((180,400));cur=frames[min(idx,len(frames)-1)].resize((180,400));im.paste(ref,(x,y+25));im.paste(cur,(x+180,y+25));d.text((x+4,y+3),f'{t:.2f}s  原参考 / 当前',font=font,fill='#222')
im.save(out/'menu-motion-frames.jpg')
(out/'motion-alignment.json').write_text(json.dumps({'first_captured_panel_s':pts[first],'reference_first_panel_s':.24,'offset_s':offset,'method':'first terminal ROI fraction of RGB>180 exceeds 12%; manually review paired frames'},indent=2))
