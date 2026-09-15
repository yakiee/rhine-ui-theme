from pathlib import Path
import urllib.request,json
base=Path('android-preview/scrcpy');base.mkdir(exist_ok=True)
def get(url):
 return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Rhine-UI-Setup'}),timeout=30).read()
target=base/'scrcpy-server-v4.1'
if not target.exists():target.write_bytes(get('https://github.com/Genymobile/scrcpy/releases/download/v4.1/scrcpy-server-v4.1'))
print('server',target.stat().st_size)
for source in ['doc/develop.md','server/src/main/java/com/genymobile/scrcpy/control/ControlMessageReader.java','server/src/main/java/com/genymobile/scrcpy/device/DesktopConnection.java','server/src/main/java/com/genymobile/scrcpy/Options.java']:
 try:
  raw=get('https://raw.githubusercontent.com/Genymobile/scrcpy/v4.1/'+source)
  target=base/source.split('/')[-1];target.write_bytes(raw)
  print('source',target.name,len(raw))
 except Exception as e:print(type(e).__name__,str(e))
