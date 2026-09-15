from rebuild_ui import run
from PIL import Image
import io,base64,time
run('shell','input','keyevent',3);time.sleep(.8)
print('\n'.join(x for x in run('shell','dumpsys','activity','activities').decode(errors='replace').splitlines() if 'topResumedActivity' in x))
png=run('exec-out','screencap','-p');im=Image.open(io.BytesIO(png));im.thumbnail((480,1100));out=io.BytesIO();im.convert('RGB').save(out,format='JPEG',quality=65);print('IMAGE:'+base64.b64encode(out.getvalue()).decode())
