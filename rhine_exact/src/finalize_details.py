from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,zipfile,hashlib,sys,subprocess,bisect
sys.path.insert(0,str(Path('rhine_exact/tools').resolve()));import cv2
OUT=Path('rhine_exact/output/details-v0.6');PREV=Path('rhine_exact/output/matched-v0.5');FF=Path('C:/Users/yakieewang/.codex/skills/video-batch-download/tools/ffmpeg-9.0.1-essentials_build/bin')
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',20);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',14)
def shot(name,folder=OUT):return Image.open(folder/'screens'/(name+'.png')).convert('RGB').crop((0,48,720,1552)).resize((360,800))
def ref(folder,idx):return Image.open(f'rhine_exact/analysis/frames/{folder}/{idx:03d}.png').convert('RGB')
sections=[('空气质量','f_00001b',5,'09-weather',(20,357,340,560)),('音乐排版','f_00001c',70,'12-music',(20,305,340,570)),('日历与卡片','f_000018',0,'13-calendar',(20,105,340,711))]
height=sum(c[4][3]-c[4][1]+38 for c in sections)+40;im=Image.new('RGB',(984,height),'#EDF0F2');d=ImageDraw.Draw(im)
for x,title in [(8,'原参考'),(336,'上一版 v0.5'),(664,'本轮 v0.6')]:d.text((x,6),title,font=font,fill='#17191C')
y=40
for title,f,i,name,box in sections:
 d.text((8,y),title,font=small,fill='#444');y+=28
 for j,a in enumerate([ref(f,i),shot(name,PREV),shot(name)]):im.paste(a.crop(box),(8+j*328,y))
 y+=box[3]-box[1]+10
im.save(OUT/'details-before-after.jpg',quality=92)
# Full page pairs retain the same 360x800 visible-content scale.
im=Image.new('RGB',(1440,858),'#EDF0F2');d=ImageDraw.Draw(im)
for j,(title,f,i,name)in enumerate([('天气','f_00001b',5,'09-weather'),('音乐','f_00001c',70,'12-music')]):
 x=j*720;d.text((x+8,12),title+'：原参考 / 当前',font=font,fill='#17191C');im.paste(ref(f,i),(x,48));im.paste(shot(name),(x+360,48))
im.save(OUT/'weather-music-comparison.jpg',quality=92)
def mae(a,b,folder=OUT):return float(np.abs(np.array(shot(a),dtype=float)-np.array(shot(b,folder),dtype=float)).mean())
checks={'settings_center_vs_edge_mae':mae('02-settings-center','05-settings-edge'),'home_return_mae':mae('00-home','14-home'),'home_vs_v05_mae':mae('00-home','00-home',PREV),'weather_detail_return_mae':mae('09-weather','11-detail-close'),'music_resume_vs_playing_mae':mae('15-music-playing','17-music-resumed'),'pause_changes_render':mae('15-music-playing','16-music-paused')>0,'calendar_selection_changes_render':mae('13-calendar','18-calendar-selected')>0}
with zipfile.ZipFile(OUT/'Rhine-UI-details-v0.6.klwp')as z:
 assert z.testzip()is None;p=json.loads(z.read('preset.json'));names=set(z.namelist())
 def walk(n):
  yield n
  for c in n.get('viewgroup_items',[]):yield from walk(c)
 nodes=list(walk(p['preset_root']));refs={v.removeprefix('kfile://org.kustom.provider/')for n in nodes for v in n.values()if isinstance(v,str)and v.startswith('kfile://org.kustom.provider/')};assert not refs-names,refs-names
 roots=p['preset_root']['viewgroup_items'];assert len(roots)<=64 and p['preset_info']['version']==17
 package={'valid_archive':True,'embedded_assets_complete':True,'editable_nodes':len(nodes),'root_count':len(roots),'animated_roots':sum(bool(n.get('internal_animations'))for n in roots),'format':17,'sha256':hashlib.sha256((OUT/'Rhine-UI-details-v0.6.klwp').read_bytes()).hexdigest()}
(OUT/'runtime-check.json').write_text(json.dumps(checks,indent=2),encoding='utf8');(OUT/'package-check.json').write_text(json.dumps(package,indent=2),encoding='utf8')
# Side-by-side recording uses the logged tap time; alignment is approximate, with no interpolated frames.
a=json.loads(subprocess.run([str(FF/'ffprobe.exe'),'-v','error','-select_streams','v:0','-show_entries','frame=best_effort_timestamp_time','-of','json',str(OUT/'interaction-demo.mp4')],capture_output=True,check=True).stdout);pts=[float(x['best_effort_timestamp_time'])for x in a['frames']];start=next(e['time_s']for e in json.loads((OUT/'interaction-events.json').read_text())if e['name']=='12-music');v=cv2.VideoCapture(str(OUT/'interaction-demo.mp4'));frames=[];times=[]
for t in pts:
 ok,a=v.read()
 if not ok or t>start+2.5:break
 if t>=start-.2:frames.append(Image.fromarray(cv2.cvtColor(a,cv2.COLOR_BGR2RGB)).crop((0,48,720,1552)).resize((360,800)));times.append(t)
v.release()
proc=subprocess.Popen([str(FF/'ffmpeg.exe'),'-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','744x900','-r','25','-i','-','-c:v','libx264','-crf','20','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'music-transition-comparison.mp4')],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
refs=[ref('f_00001c',i)for i in range(78)]
for title,speed,length in [('原速',1,2.3),('半速',.5,4.2)]:
 for i in range(round(length*25)):
  t=min(i/25*speed,2.1);idx=max(0,bisect.bisect_right(times,start+t)-1);im=Image.new('RGB',(744,900),'#EDF0F2');d=ImageDraw.Draw(im);d.text((12,12),'原主题参考',font=font,fill='#17191C');d.text((386,12),'当前 v0.6',font=font,fill='#17191C');d.text((12,43),title+' · 按点击时刻近似对齐',font=small,fill='#555');im.paste(refs[min(77,round((.24+t)/.04))],(8,77));im.paste(frames[min(idx,len(frames)-1)],(376,77));d.text((12,878),'实际模拟器录屏；保留原始帧，未补帧',font=small,fill='#555');proc.stdin.write(im.tobytes())
proc.stdin.close();error=proc.stderr.read();assert proc.wait()==0,error
print(json.dumps({'package':package,'runtime':checks},ensure_ascii=False))
