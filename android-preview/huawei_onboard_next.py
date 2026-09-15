import subprocess,time,xml.etree.ElementTree as ET
from pathlib import Path
adb=str(Path('android-preview/sdk/platform-tools/adb.exe').resolve())
def run(args):return subprocess.run([adb,'-s','16c18d67']+args,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=20).stdout
run(['shell','input','tap','600','2380'])
time.sleep(1)
run(['shell','uiautomator','dump','/sdcard/Download/klwp-diagnostic-ui.xml'])
for node in ET.fromstring(run(['shell','cat','/sdcard/Download/klwp-diagnostic-ui.xml'])).iter('node'):
 text=node.get('text') or node.get('content-desc')
 if text:print(text,node.get('bounds'))
