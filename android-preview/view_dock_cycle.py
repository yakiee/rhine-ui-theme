from PIL import Image,ImageOps,ImageDraw
from pathlib import Path
import base64,io
out=Path('rhine_exact/output/dock-page-lifecycle-20260914')
names=['left-to-page3','returned-page2']
canvas=Image.new('RGB',(600,672),'#202020')
for i,name in enumerate(names):
    im=Image.open(out/(name+'.png')).convert('RGB');im.thumbnail((300,652))
    canvas.paste(im,(i*300,20))
    ImageDraw.Draw(canvas).text((i*300+5,3),name,fill='white')
buf=io.BytesIO();canvas.save(buf,'JPEG',quality=65)
print(base64.b64encode(buf.getvalue()).decode())
