from PIL import Image,ImageDraw
from pathlib import Path
import base64,io
out=Path('rhine_exact/output/dock-page-lifecycle-20260914')
canvas=Image.new('RGB',(840,600),'#202020')
for i in range(6):
    im=Image.open(out/f'cycle-{i+1}-opened.png').convert('RGB')
    im=im.crop((250,400,1200,1700));im.thumbnail((280,280))
    x=(i%3)*280;y=(i//3)*300
    canvas.paste(im,(x,y+20));ImageDraw.Draw(canvas).text((x+5,y+3),'cycle '+str(i+1),fill='white')
buf=io.BytesIO();canvas.save(buf,'JPEG',quality=65)
print(base64.b64encode(buf.getvalue()).decode())
