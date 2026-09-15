from pathlib import Path
import subprocess,xml.etree.ElementTree as ET
adb=str(Path('android-preview/sdk/platform-tools/adb.exe').resolve())
def run(args):
 r=subprocess.run([adb,'-s','16c18d67']+args,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=20)
 print('ERROR',r.stderr[:700]) if r.returncode else None
 return r.stdout
print('STATE',run(['get-state']).strip())
print('CURRENT', '\n'.join(x for x in run(['shell','dumpsys','activity','activities']).splitlines() if 'topResumedActivity' in x))
print('DRAFT FILES',run(['shell','ls','-lt','/sdcard/Download/Rhine-KLWP/autosave']))
print('WALLPAPERS',run(['shell','ls','-lt','/sdcard/Download/Rhine-KLWP/wallpapers']))
print(run(['shell','am','start','-W','-n','org.kustom.wallpaper.huawei/org.kustom.app.OnBoardingActivity']))
r=subprocess.run([adb,'-s','16c18d67','shell','uiautomator','dump','/sdcard/Download/klwp-rebuild-check.xml'],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=20)
print('DUMP',r.stdout,r.stderr)
if 'dumped' in r.stdout:
 xml=run(['shell','cat','/sdcard/Download/klwp-rebuild-check.xml']);Path('android-preview/logs/rebuild-check.xml').write_text(xml,encoding='utf-8')
 for n in ET.fromstring(xml).iter('node'):
  label=n.get('text') or n.get('content-desc')
  if label:print(label,n.get('bounds'))
