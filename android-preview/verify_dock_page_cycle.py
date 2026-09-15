from rebuild_ui import run
from pathlib import Path
from PIL import Image
import time,io,base64,json

out=Path('rhine_exact/output/dock-page-lifecycle-20260914')
out.mkdir(parents=True,exist_ok=True)
def capture(name):
    raw=run('exec-out','screencap','-p')
    (out/(name+'.png')).write_bytes(raw)
    im=Image.open(io.BytesIO(raw)).convert('RGB')
    im.thumbnail((420,1000))
    buf=io.BytesIO();im.save(buf,'JPEG',quality=82)
    print(json.dumps({'stage':name,'image':base64.b64encode(buf.getvalue()).decode()}),flush=True)

run('shell','input','swipe',1040,1160,160,1160,400)
time.sleep(.8)
capture('left-to-page3')
run('shell','input','swipe',160,1160,1040,1160,400)
time.sleep(1)
capture('returned-page2')
