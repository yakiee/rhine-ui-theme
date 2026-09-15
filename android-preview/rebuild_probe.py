from pathlib import Path
import subprocess,xml.etree.ElementTree as ET,time
adb=str(Path('android-preview/sdk/platform-tools/adb.exe').resolve())
def run(args):
 r=subprocess.run([adb,'-s','16c18d67']+args,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=20)
 if r.returncode:raise RuntimeError(r.stderr or r.stdout)
 return r.stdout
print(run(['get-state']))
print(run(['shell','am','start','-W','-n','org.kustom.wallpaper.huawei/org.kustom.app.OnBoardingActivity']))
out=run(['shell','uiautomator','dump','/sdcard/Download/klwp-rebuild-ui.xml'])
if 'dumped' not in out:raise RuntimeError(out)
xml=run(['shell','cat','/sdcard/Download/klwp-rebuild-ui.xml'])
Path('android-preview/logs/rebuild-ui.xml').write_text(xml,encoding='utf-8')
for n in ET.fromstring(xml).iter('node'):
 if n.get('text') or n.get('content-desc'):print({k:n.get(k) for k in ['text','content-desc','resource-id','clickable','bounds']})
