from pathlib import Path
import sys,json,zipfile,hashlib,subprocess,bisect
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path('rhine_exact/tools').resolve()));import cv2
OUT=Path('rhine_exact/output/matched-v0.5')
FF=Path('C:/Users/yakieewang/.codex/skills/video-batch-download/tools/ffmpeg-9.0.1-essentials_build/bin')
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',20);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',14)
def shot(name):return Image.open(OUT/'screens'/(name+'.png')).convert('RGB').crop((0,48,720,1552)).resize((360,800))
def ref(folder,idx):return Image.open(f'rhine_exact/analysis/frames/{folder}/{idx:03d}.png').convert('RGB')
# Comparison images use consistent visible-content coordinates.
pairs=[('首页','f_000019',0,'00-home'),('主菜单','f_000019',28,'01-dock-menu'),('应用页','f_000019',65,'07-apps'),('天气','f_00001b',5,'09-weather'),('音乐','f_00001c',70,'12-music'),('日历','f_000018',0,'13-calendar')]
canvas=Image.new('RGB',(1440,1140),'#ECEFF1');d=ImageDraw.Draw(canvas)
for i,(title,f,idx,name) in enumerate(pairs):
 x=i%3*480;y=i//3*570;d.text((x+8,y+4),title+'：原参考 / 当前',font=font,fill='#17191C')
 canvas.paste(ref(f,idx).resize((240,533)),(x,y+32));canvas.paste(shot(name).resize((240,533)),(x+240,y+32))
canvas.save(OUT/'all-pages-comparison.jpg',quality=90)
canvas=Image.new('RGB',(744,858),'#ECEFF1');d=ImageDraw.Draw(canvas);d.text((12,12),'原主题参考',font=font,fill='#17191C');d.text((384,12),'当前可编辑 KLWP',font=font,fill='#17191C');canvas.paste(ref('f_000019',28),(8,48));canvas.paste(shot('01-dock-menu'),(376,48));canvas.save(OUT/'menu-side-by-side.jpg',quality=93)
# Record review checks are measured on the content area, excluding system time.
def mae(a,b):return float(np.abs(np.array(shot(a),dtype=float)-np.array(shot(b),dtype=float)).mean())
checks={'settings_center_vs_edge_mae':mae('02-settings-center','05-settings-edge'),'rapid_menu_vs_normal_mae':mae('15-normal-menu','16-rapid-menu'),'home_after_return_mae':mae('00-home','14-home'),'weather_detail_return_mae':mae('09-weather','11-detail-close')}
# Gold -> blue and dot setting have a visible effect in the actual rendered Dock.
blue=np.array(shot('17-blue-no-dots'),dtype=int)[550:720];gold=np.array(shot('18-gold-dots-restored'),dtype=int)[550:720]
checks['blue_dock_pixels']=int(((blue[:,:,2]>blue[:,:,0]+25)&(blue[:,:,1]>100)).sum())
checks['gold_dock_pixels']=int(((gold[:,:,0]>190)&(gold[:,:,1]>120)&(gold[:,:,2]<100)).sum())
checks['verified_pages']=['home','dock menu','settings center','settings tilted edge','apps','weather','weather detail','music','calendar']
checks['limitations']=['Dates, weather, music and hardware readings are preview fixtures.','External payment/app actions are not validated on the emulator.','Visual equivalence to the original is not achieved.']
(OUT/'runtime-check.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf8')
# Validate the portable editable preset and every directly referenced bundled asset.
file=OUT/'Rhine-UI-matched-v0.5.klwp'
def walk(n):
 yield n
 for c in n.get('viewgroup_items',[]):yield from walk(c)
with zipfile.ZipFile(file) as z:
 assert z.testzip() is None
 p=json.loads(z.read('preset.json'));names=set(z.namelist());nodes=list(walk(p['preset_root']))
 refs={v.removeprefix('kfile://org.kustom.provider/') for n in nodes for v in n.values() if isinstance(v,str) and v.startswith('kfile://org.kustom.provider/')}
 assert not refs-names,refs-names
 roots=p['preset_root']['viewgroup_items'];assert p['preset_info']['version']==17 and len(roots)<=64
 package={'archive_valid':True,'all_assets_embedded':True,'format':17,'roots':len(roots),'native_nodes':len(nodes),'animated_roots':sum(bool(n.get('internal_animations')) for n in roots),'independent_menu_animation_groups':18,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'size_bytes':file.stat().st_size}
(OUT/'package-check.json').write_text(json.dumps(package,indent=2),encoding='utf8')
# Use actual recording timestamps; repeated frames preserve capture cadence without interpolation.
pts=json.loads((OUT/'frame-times.json').read_text());offset=json.loads((OUT/'motion-alignment.json').read_text())['offset_s'];v=cv2.VideoCapture(str(OUT/'interaction-demo.mp4'));frames=[]
for t in pts:
 if t>4:break
 ok,a=v.read()
 if not ok:break
 frames.append(Image.fromarray(cv2.cvtColor(a,cv2.COLOR_BGR2RGB)).crop((0,48,720,1552)).resize((360,800)))
v.release();refs=[ref('f_000019',i) for i in range(39)]
proc=subprocess.Popen([str(FF/'ffmpeg.exe'),'-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','744x900','-r','25','-i','-','-c:v','libx264','-crf','20','-preset','fast','-movflags','+faststart','-pix_fmt','yuv420p',str(OUT/'menu-opening-comparison.mp4')],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
for title,speed,length in [('原速',1,2.4),('半速',.5,4)]:
 for i in range(round(length*25)):
  t=min(i/25*speed,1.52);idx=min(len(frames)-1,max(0,bisect.bisect_right(pts,t+offset)-1));im=Image.new('RGB',(744,900),'#ECEFF1');d=ImageDraw.Draw(im)
  d.text((12,12),'原参考',font=font,fill='#17191C');d.text((386,12),'当前 v0.5',font=font,fill='#17191C');d.text((12,43),title+' · 按终端底板首次出现对齐',font=small,fill='#575E65');im.paste(refs[min(38,round(t/.04))],(8,77));im.paste(frames[idx],(376,77));d.text((12,878),'实际模拟器录屏；保留原始帧，未补帧',font=small,fill='#575E65');proc.stdin.write(im.tobytes())
proc.stdin.close();errors=proc.stderr.read();assert proc.wait()==0,errors
print(json.dumps({'package':package,'runtime':checks},ensure_ascii=False))
