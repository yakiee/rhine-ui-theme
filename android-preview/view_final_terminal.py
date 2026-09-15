from PIL import Image,ImageDraw
from pathlib import Path
import io,base64
p=Path('rhine_exact/output/dock-phone-fix-20260914/second-page-only');c=Image.new('RGB',(600,676),'white');d=ImageDraw.Draw(c)
for i,n in enumerate(['final-page2','final-terminal']):
 im=Image.open(p/(n+'.png')).convert('RGB');im.thumbnail((300,652));c.paste(im,(300*i,24));d.text((300*i+6,6),n,fill='black')
b=io.BytesIO();c.save(b,format='JPEG',quality=50);print(base64.b64encode(b.getvalue()).decode())
