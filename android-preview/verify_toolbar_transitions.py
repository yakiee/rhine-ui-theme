import io,time,base64
from PIL import Image,ImageDraw
from toolbar_native import OUT,run
frames=[]
def guard():
    raw=run('shell','dumpsys','activity','activities').decode(errors='replace')
    assert any('topResumedActivity' in s and 'com.miui.home/.launcher.Launcher' in s for s in raw.splitlines()),'Phone left desktop; stopping'
def capture(label):
    guard()
    raw=run('exec-out','screencap','-p')
    (OUT/(label+'.png')).write_bytes(raw)
    im=Image.open(io.BytesIO(raw)).convert('RGB');im.thumbnail((220,480))
    frame=Image.new('RGB',(220,510),'#222222');frame.paste(im,(0,25));ImageDraw.Draw(frame).text((8,5),label,fill='white');frames.append(frame)
def touch(*args):
    guard();run('shell','input',*args);time.sleep(.7)
capture('01-toolbar-visible')
touch('tap',1010,1971)
capture('02-dock-open')
touch('tap',140,1150)
capture('03-toolbar-return')
touch('swipe',1040,1150,160,1150,650)
capture('04-next-page')
touch('swipe',160,1150,1040,1150,650)
capture('05-page-return')
touch('tap',1010,1971)
touch('swipe',1040,1150,160,1150,650)
touch('swipe',160,1150,1040,1150,650)
capture('06-dock-swipe-return')
sheet=Image.new('RGB',(220*len(frames),510))
for i,im in enumerate(frames):sheet.paste(im,(i*220,0))
sheet.save(OUT/'transition-check.jpg',quality=80)
buf=io.BytesIO();sheet.save(buf,format='JPEG',quality=65)
print('IMAGE:'+base64.b64encode(buf.getvalue()).decode())
