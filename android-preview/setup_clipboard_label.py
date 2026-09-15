from pathlib import Path
import urllib.request
base=Path('android-preview/scrcpy')
for name in ['ClipboardManager.java','ServiceManager.java','FakeContext.java']:
 path='server/src/main/java/com/genymobile/scrcpy/'+('wrappers/' if name!='FakeContext.java' else 'util/')+name
 try:
  raw=urllib.request.urlopen('https://raw.githubusercontent.com/Genymobile/scrcpy/v4.1/'+path,timeout=20).read();(base/name).write_bytes(raw)
  print(name,len(raw))
 except Exception as e:print(name,e)
jar=base/'r8-2.2.66.jar'
if not jar.exists():jar.write_bytes(urllib.request.urlopen('https://storage.googleapis.com/r8-releases/raw/2.2.66/r8.jar',timeout=30).read())
print('r8 bytes',jar.stat().st_size)
