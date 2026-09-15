from pathlib import Path
from PIL import Image,ImageDraw
import io,base64,sys
p=Path('rhine_exact/output/open-dock-swipe-20260915')/sys.argv[1]
names=['left-normal-returned','right-normal-returned','left-fast-returned','right-fast-returned','partial-cancelled','final-closed']
sheet=Image.new('RGB',(660,1000),'#222222');d=ImageDraw.Draw(sheet)
for i,name in enumerate(names):
    sheet.paste(Image.open(p/(name+'.png')).convert('RGB').resize((218,474)),((i%3)*220,(i//3)*500+22));d.text(((i%3)*220,(i//3)*500),name,fill='white')
sheet.save(p/'stress-contact.jpg');sheet.thumbnail((600,910));b=io.BytesIO();sheet.save(b,format='JPEG',quality=24)
print('IMAGE:'+base64.b64encode(b.getvalue()).decode())
