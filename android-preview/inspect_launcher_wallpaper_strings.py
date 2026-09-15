from pathlib import Path
import zipfile,re,struct,json
p=Path('android-preview/apps/HyperOS-Launcher-inspect.apk')
print('APK',p.stat().st_size)
found=[]
with zipfile.ZipFile(p) as z:
 for name in z.namelist():
  if not re.fullmatch(r'classes\d*\.dex',name):continue
  d=z.read(name);size,off=struct.unpack_from('<II',d,0x38)
  for i in range(size):
   start=struct.unpack_from('<I',d,off+4*i)[0]
   while d[start]&128:start+=1
   start+=1;end=d.find(b'\x00',start)
   s=d[start:end].decode('utf8',errors='replace')
   if re.search(r'wallpaper.*(scroll|offset)|(?:scroll|offset).*wallpaper',s,re.I):found.append((name,s))
print(json.dumps(found,ensure_ascii=False,indent=2))
Path('rhine_exact/output/dock-phone-fix-20260914/launcher-wallpaper-strings.json').write_text(json.dumps(found,ensure_ascii=False,indent=2),encoding='utf8')
