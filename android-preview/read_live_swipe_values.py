from pathlib import Path
import time,io,base64
from PIL import Image,ImageDraw
from rebuild_ui import run
out=Path('rhine_exact/output/open-dock-swipe-20260915')
def guard():
    assert any(b'topResumedActivity' in s and b'com.miui.home/.launcher.Launcher' in s for s in run('shell','dumpsys','activity','activities').splitlines())
def cmd(*args):guard();run('shell','input',*args)
shots=[]
def shot(name):
    guard();raw=run('exec-out','screencap','-p');(out/(name+'.png')).write_bytes(raw);shots.append((name,Image.open(io.BytesIO(raw)).convert('RGB')))
cmd('tap',140,1150);time.sleep(.4);cmd('tap',1010,1971);time.sleep(.6);shot('diag-open')
cmd('swipe',160,1150,1040,1150,700);time.sleep(1.6);shot('diag-right-away')
cmd('swipe',1040,1150,160,1150,700);time.sleep(1.1);shot('diag-right-return')
cmd('tap',140,1150);time.sleep(.4);cmd('tap',1010,1971);time.sleep(.6)
cmd('swipe',1040,1150,160,1150,700);time.sleep(1.6);shot('diag-left-away')
cmd('swipe',160,1150,1040,1150,700);time.sleep(1.1);shot('diag-left-return')
sheet=Image.new('RGB',(600,500),'#222');d=ImageDraw.Draw(sheet)
for i,(name,im) in enumerate(shots):
    crop=im.crop((0,170,1200,360)).resize((600,95));sheet.paste(crop,(0,i*100));d.text((0,i*100),name,fill='#FF8080')
sheet.save(out/'live-state-strip.jpg');buf=io.BytesIO();sheet.save(buf,format='JPEG',quality=60)
print('IMAGE:'+base64.b64encode(buf.getvalue()).decode())
