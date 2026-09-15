from pathlib import Path
import sys,subprocess,json,bisect
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path('rhine_exact/tools').resolve()));import cv2
out=Path('rhine_exact/output/details-v0.6');ff='C:/Users/yakieewang/.codex/skills/video-batch-download/tools/ffmpeg-9.0.1-essentials_build/bin/ffprobe.exe'
a=json.loads(subprocess.run([ff,'-v','error','-select_streams','v:0','-show_entries','frame=best_effort_timestamp_time','-of','json',str(out/'interaction-demo.mp4')],capture_output=True,check=True).stdout);pts=[float(x['best_effort_timestamp_time']) for x in a['frames']];events=json.loads((out/'interaction-events.json').read_text());start=next(e['time_s']for e in events if e['name']=='12-music');print('music tap',start)
v=cv2.VideoCapture(str(out/'interaction-demo.mp4'));frames=[];times=[]
for t in pts:
 ok,a=v.read()
 if not ok or t>start+3:break
 if t>=start-.2:frames.append(Image.fromarray(cv2.cvtColor(a,cv2.COLOR_BGR2RGB)).crop((0,48,720,1552)).resize((360,800)));times.append(t)
v.release();(out/'music-frame-times.json').write_text(json.dumps(times));font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',14)
canvas=Image.new('RGB',(1080,850),'#EEE');d=ImageDraw.Draw(canvas)
for j,dt in enumerate([.2,.55,.8,1,1.2,1.5]):
 idx=max(0,bisect.bisect_right(times,start+dt)-1);rf=round((.24+dt)/.04);ref=Image.open(f'rhine_exact/analysis/frames/f_00001c/{rf:03d}.png');x=j%3*360;y=j//3*425;canvas.paste(ref.resize((180,400)),(x,y+25));canvas.paste(frames[idx].resize((180,400)),(x+180,y+25));d.text((x+2,y+3),f'点击后 {dt:.2f}s  原参考 / 当前',font=font,fill='#222')
canvas.save(out/'music-motion-review.jpg',quality=90)
