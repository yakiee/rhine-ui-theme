from rebuild_ui import run
from PIL import Image
import io,base64
im=Image.open(io.BytesIO(run('exec-out','screencap','-p'))).convert('RGB');c=Image.new('RGB',(1200,800));c.paste(im.crop((0,120,1200,320)),(0,0));c.paste(im.crop((0,1980,1200,2580)),(0,200));c.thumbnail((480,320));b=io.BytesIO();c.save(b,format='JPEG',quality=65);print(base64.b64encode(b.getvalue()).decode())
