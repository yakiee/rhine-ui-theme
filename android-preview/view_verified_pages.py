from PIL import Image,ImageDraw
import io,base64
from pathlib import Path
p=Path('rhine_exact/output/dock-phone-fix-20260914/second-page-only')
c=Image.new('RGB',(672,430),'white');d=ImageDraw.Draw(c)
for i in range(4):
 im=Image.open(p/f'verified-page{i+1}.png').crop((860,1450,1140,2120));im.thumbnail((168,402));c.paste(im,(168*i,24));d.text((168*i+8,5),f'Page {i+1}',fill='black')
b=io.BytesIO();c.save(b,format='JPEG',quality=65);print(base64.b64encode(b.getvalue()).decode())
