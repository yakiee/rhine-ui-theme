from PIL import Image,ImageDraw
from pathlib import Path
import io,base64
p=Path('rhine_exact/output/dock-phone-fix-20260914/second-page-only');names=['closed-page1','closed-page2','closed-page3','closed-page4','back-page2']
c=Image.new('RGB',(800,390),'white');d=ImageDraw.Draw(c)
for i,n in enumerate(names):
 im=Image.open(p/(n+'.png')).convert('RGB').crop((860,1450,1140,2120));im.thumbnail((160,350));c.paste(im,(160*i,30));d.text((160*i+4,6),n,fill='black')
b=io.BytesIO();c.save(b,format='JPEG',quality=55);print(base64.b64encode(b.getvalue()).decode())
