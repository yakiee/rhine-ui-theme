from pathlib import Path
import urllib.request, zipfile, hashlib
path=Path('android-preview/apps/KLWP-3.81-aosp.apk')
url='https://kustom.rocks/download/klwp/381530516/aosp_release'
if not path.exists():
 request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
 with urllib.request.urlopen(request,timeout=45) as response, path.with_suffix('.part').open('wb') as output:
  while True:
   chunk=response.read(1024*1024)
   if not chunk:break
   output.write(chunk)
 path.with_suffix('.part').replace(path)
print('APK',path,'bytes',path.stat().st_size,'zip',zipfile.is_zipfile(path))
print('sha256',hashlib.sha256(path.read_bytes()).hexdigest())
