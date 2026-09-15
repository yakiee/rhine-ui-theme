from pathlib import Path
import subprocess,xml.etree.ElementTree as E,sys,time,base64
sys.stdout.reconfigure(encoding='utf-8')
base=Path(__file__).resolve().parent;adb=str(base/'sdk/platform-tools/adb.exe')
def run(*args):
 r=subprocess.run([adb,'-s','emulator-5580',*args],capture_output=True,timeout=20)
 if r.returncode:raise RuntimeError(r.stderr.decode(errors='replace'))
 return r.stdout
if len(sys.argv)>1:
 if sys.argv[1]=='tapshot':run('shell','input','tap',sys.argv[2],sys.argv[3]);time.sleep(0.5)
 if sys.argv[1]=='tap':run('shell','input','tap',sys.argv[2],sys.argv[3])
 if sys.argv[1]=='keyshot':run('shell','input','keyevent',sys.argv[2]);time.sleep(0.5)
 if sys.argv[1]=='swipeshot':run('shell','input','swipe',*sys.argv[2:]);time.sleep(0.5)
 if sys.argv[1]=='swipe':run('shell','input','swipe',*sys.argv[2:])
 if sys.argv[1]=='back':run('shell','input','keyevent','4')
 if sys.argv[1]=='text':run('shell','input','text',sys.argv[2])
if len(sys.argv)>1 and sys.argv[1] in ['screen','tapshot','keyshot','swipeshot']:
 data=run('exec-out','screencap','-p');(base/'logs/current-screen.png').write_bytes(data);from PIL import Image
 import io
 display=io.BytesIO();Image.open(io.BytesIO(data)).convert('RGB').save(display,format='JPEG',quality=85);print(base64.b64encode(display.getvalue()).decode());raise SystemExit
remote='/sdcard/window-'+str(time.time_ns())+'.xml'
result=run('shell','uiautomator','dump',remote)
if b'dumped' not in result:
 print(result.decode(errors='replace'));raise SystemExit

x=run('shell','cat',remote);(base/'logs/android-ui.xml').write_bytes(x)
for n in E.fromstring(x).iter('node'):
 if n.get('text') or n.get('content-desc'):print({k:n.get(k) for k in ['text','content-desc','resource-id','clickable','bounds']})
