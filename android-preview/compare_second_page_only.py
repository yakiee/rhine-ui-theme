from rebuild_ui import run,snapshot
from pathlib import Path
from PIL import Image,ImageDraw
import io,time,base64
out=Path('rhine_exact/output/dock-phone-fix-20260914/second-page-only');out.mkdir(exist_ok=True)
images=[]
for label in ['page3','page2']:
 if label=='page2':run('shell','input','swipe',160,1160,1040,1160,650);time.sleep(1)
 raw=run('exec-out','screencap','-p');(out/(label+'.png')).write_bytes(raw)
 im=Image.open(io.BytesIO(raw));im=im.crop((860,1450,1140,2120));im.thumbnail((224,536));images.append(im)
canvas=Image.new('RGB',(448,560),'white');draw=ImageDraw.Draw(canvas)
for i,im in enumerate(images):canvas.paste(im,(i*224,24));draw.text((i*224+8,5),['Page 3','Page 2'][i],fill='black')
b=io.BytesIO();canvas.save(b,format='JPEG',quality=75)
snapshot()
print('IMAGE:'+base64.b64encode(b.getvalue()).decode())
