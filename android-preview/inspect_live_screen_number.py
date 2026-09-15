from rebuild_ui import run
from PIL import Image
import io,base64,time
run('shell','input','tap',696,216);time.sleep(1)
run('shell','input','keyevent',3);time.sleep(1)
png=run('exec-out','screencap','-p');im=Image.open(io.BytesIO(png));im.thumbnail((480,1100));out=io.BytesIO();im.convert('RGB').save(out,format='JPEG',quality=70);print('IMAGE:'+base64.b64encode(out.getvalue()).decode())
