from pathlib import Path
import subprocess,time,io,json
from PIL import Image,ImageDraw
adb=str(Path('android-preview/sdk/platform-tools/adb.exe').resolve())
out=Path('rhine_exact/output/battery-cells-v0.13.21/verification');out.mkdir(exist_ok=True)
def run(*args):return subprocess.check_output([adb,'-s','emulator-5580',*args],timeout=20)
images=[]
try:
 for level in [100,50]:
  run('shell','dumpsys','battery','set','level',str(level));time.sleep(2)
  im=Image.open(io.BytesIO(run('exec-out','screencap','-p'))).convert('RGB')
  im.save(out/f'terminal-{level}.png')
  crop=im.crop((289,385,327,415)).resize((228,180))
  tile=Image.new('RGB',(228,215),'#202224');tile.paste(crop,(0,30));ImageDraw.Draw(tile).text((8,8),str(level)+'%',fill='white')
  images.append(tile)
finally:
 run('shell','dumpsys','battery','reset')
sheet=Image.new('RGB',(456,215));
for i,im in enumerate(images):sheet.paste(im,((i%2)*228,(i//2)*215))
sheet.save(out/'cells-check.jpg')
print(run('shell','dumpsys','battery').decode())
