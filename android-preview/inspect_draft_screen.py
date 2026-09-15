from rebuild_ui import run
from PIL import Image
import base64,io
print('ACTIVITY', '\n'.join(x for x in run('shell','dumpsys','activity','activities').decode(errors='replace').splitlines() if 'topResumedActivity' in x))
png=run('exec-out','screencap','-p')
im=Image.open(io.BytesIO(png)); im.thumbnail((400,1100)); out=io.BytesIO(); im.convert('RGB').save(out,format='JPEG',quality=60)
print('IMAGE:'+base64.b64encode(out.getvalue()).decode())
