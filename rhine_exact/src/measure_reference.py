from pathlib import Path
import sys,json,math
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path('rhine_exact/tools').resolve()));import cv2
base=Path('rhine_exact');out=base/'analysis';allframes=out/'frames';allframes.mkdir(exist_ok=True)
rois={'f_000018':[103,80,285,619],'f_000019':[94,72,267,576],'f_00001a':[94,72,267,576],'f_00001b':[104,80,286,622],'f_00001c':[94,72,267,576]}
manifest=[]
for name,(x,y,w,h) in rois.items():
 src=Image.open(Path('rhine_reference/animated_previews')/(name+'.gif'));dest=allframes/name;dest.mkdir(exist_ok=True);samples=[];prev=None;metrics=[];ms=0
 for i in range(src.n_frames):
  src.seek(i);a=np.array(src.convert('RGB'))[y:y+h,x:x+w];a=cv2.resize(a,(360,800),interpolation=cv2.INTER_CUBIC);cv2.imwrite(str(dest/f'{i:03d}.png'),cv2.cvtColor(a,cv2.COLOR_RGB2BGR))
  gray=cv2.cvtColor(a,cv2.COLOR_RGB2GRAY);diff=float(np.abs(gray.astype(float)-prev).mean()) if prev is not None else 0
  metrics.append({'frame':i,'t_ms':ms,'mean_pixel_delta':round(diff,3)});prev=gray.astype(float);ms+=src.info.get('duration',40)
  if i%4==0 or i==src.n_frames-1:
   small=cv2.resize(cv2.cvtColor(a,cv2.COLOR_RGB2BGR),(144,320));pad=np.full((350,144,3),247,dtype=np.uint8);pad[30:]=small;cv2.putText(pad,f'{i:03d} / {i*.04:.2f}s',(4,20),cv2.FONT_HERSHEY_SIMPLEX,.4,(30,30,30),1);samples.append(pad)
 cols=8;rows=math.ceil(len(samples)/cols);sheet=np.full((rows*350,cols*144,3),245,dtype=np.uint8)
 for i,a in enumerate(samples):sheet[(i//cols)*350:(i//cols+1)*350,(i%cols)*144:(i%cols+1)*144]=a
 cv2.imwrite(str(out/(name+'-measured-storyboard.jpg')),sheet)
 manifest.append({'id':name,'source_crop':[x,y,w,h],'normalized_size':[360,800],'frame_count':src.n_frames,'duration_ms':ms,'metrics':metrics})
video=next(Path('video_results').rglob('*.mp4'));v=cv2.VideoCapture(str(video));v.set(cv2.CAP_PROP_POS_FRAMES,30);ok,a=v.read();v.release()
if ok:
 quad=np.array([[228,189],[582,221],[536,1020],[163,1008]],np.float32)
 dst=np.array([[0,0],[720,0],[720,1600],[0,1600]],np.float32);mat=cv2.getPerspectiveTransform(quad,dst);straight=cv2.warpPerspective(a,mat,(720,1600));cv2.imwrite(str(out/'video-home-rectified.jpg'),straight)
 manifest.append({'id':'video_home_1s','quad':quad.tolist(),'homography':mat.tolist(),'note':'屏幕四角为人工估测，待边缘检查；仅作测量参考，不作为壁纸'})
(out/'measurement-inputs.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Normalized all five GIFs for measurement; original files unchanged.')
