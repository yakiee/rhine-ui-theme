from PIL import Image,ImageDraw
import io,base64
from pathlib import Path
p=Path('rhine_exact/output/dock-phone-fix-20260914/second-page-only')
c=Image.new('RGB',(448,560),'white');d=ImageDraw.Draw(c)
for i,n in enumerate(['page3','page2']):
 im=Image.open(p/(n+'.png')).crop((860,1450,1140,2120));im.thumbnail((224,536));c.paste(im,(224*i,24));d.text((224*i+8,5),n,fill='black')
b=io.BytesIO();c.save(b,format='JPEG',quality=65);print(base64.b64encode(b.getvalue()).decode())
