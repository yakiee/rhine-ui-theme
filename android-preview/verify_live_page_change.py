from rebuild_ui import run
from PIL import Image
import io,base64,time
run('shell','input','swipe',180,1200,1040,1200,550);time.sleep(.8)
png=run('exec-out','screencap','-p');im=Image.open(io.BytesIO(png));im.thumbnail((480,1100));out=io.BytesIO();im.convert('RGB').save(out,format='JPEG',quality=70);print('IMAGE:'+base64.b64encode(out.getvalue()).decode())
