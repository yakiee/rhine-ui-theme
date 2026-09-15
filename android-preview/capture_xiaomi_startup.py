from pathlib import Path
import subprocess,time,xml.etree.ElementTree as ET
adb=str(Path('android-preview/sdk/platform-tools/adb.exe').resolve());base=[adb,'-s','16c18d67'];out=Path('android-preview/logs/xiaomi-startup');out.mkdir(exist_ok=True)
with (out/'klwp-startup.log').open('wb') as stream:
 reader=subprocess.Popen(base+['logcat','--uid=10450','-v','threadtime'],stdout=stream,stderr=subprocess.STDOUT)
 try:
  print(subprocess.run(base+['shell','am','start','-n','org.kustom.wallpaper/org.kustom.app.OnBoardingActivity'],capture_output=True,text=True).stdout)
  time.sleep(6)
  subprocess.run(base+['shell','uiautomator','dump','/sdcard/Download/klwp-diagnostic-ui.xml'],capture_output=True)
  data=subprocess.run(base+['shell','cat','/sdcard/Download/klwp-diagnostic-ui.xml'],capture_output=True).stdout
  (out/'screen.xml').write_bytes(data)
  for n in ET.fromstring(data).iter('node'):
   if n.get('text'):print(n.get('text'),n.get('bounds'))
 finally:reader.terminate();reader.wait(timeout=5)
print('LOG:')
print((out/'klwp-startup.log').read_text(encoding='utf-8',errors='replace')[-16000:])
