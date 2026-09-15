from PIL import Image,ImageDraw
from pathlib import Path
import io,base64
p=Path('rhine_exact/output/dock-opacity-20260914');c=Image.new('RGB',(700,560),'white');d=ImageDraw.Draw(c)
for i,n in enumerate(['before','reopened']):
 im=Image.open(p/(n+'.png')).convert('RGB').crop((280,650,1200,1650));im.thumbnail((350,520));c.paste(im,(350*i,24));d.text((350*i+6,5),n,fill='black')
b=io.BytesIO();c.save(b,format='JPEG',quality=55);print(base64.b64encode(b.getvalue()).decode())
