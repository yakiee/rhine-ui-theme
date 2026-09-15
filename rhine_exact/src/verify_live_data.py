from pathlib import Path
import subprocess,time,io
from PIL import Image
ADB=str(Path('android-preview/sdk/platform-tools/adb.exe').resolve());OUT=Path('rhine_exact/output/live-data-v0.9.2')
def run(*args):
 r=subprocess.run([ADB,'-s','emulator-5580',*args],capture_output=True,check=True,timeout=20)
 return r.stdout
def shot(name):
 data=run('exec-out','screencap','-p');Image.open(io.BytesIO(data)).verify();(OUT/(name+'.png')).write_bytes(data)
def tap(x,y):run('shell','input','tap',str(x),str(y));time.sleep(3)
shot('home');tap(360,1390);shot('menu');tap(596,1129);shot('calendar');tap(636,270);shot('calendar-next');tap(622,893);tap(509,491);shot('calendar-selected');tap(622,893);tap(522,204);shot('music');tap(447,204);shot('weather')
print('Saved seven verified PNG screenshots')
