from PIL import Image,ImageDraw
from pathlib import Path
import io,base64
p=Path('rhine_exact/output/dock-phone-fix-20260914/second-page-only');c=Image.new('RGB',(480,590),'white');d=ImageDraw.Draw(c)
for i,n in enumerate(['terminal-leave-return','final-settings-return']):
 im=Image.open(p/(n+'.png')).convert('RGB').crop((860,1450,1140,2120));im.thumbnail((240,558));c.paste(im,(240*i,28));d.text((240*i+4,6),n,fill='black')
b=io.BytesIO();c.save(b,format='JPEG',quality=55);print(base64.b64encode(b.getvalue()).decode())
