import sys
from pathlib import Path
sys.path.insert(0,str(Path('rhine_exact/tools').resolve()))
from loguru import logger
logger.remove()
from androguard.core.apk import APK
from androguard.core.dex import DEX
apk=APK('android-preview/apps/KLWP-aosp.apk')
for raw in apk.get_all_dex():
 dex=DEX(raw)
 found=False
 for name in ['Lorg/kustom/config/u1;','Lorg/kustom/config/v1;']:
  cls=dex.get_class(name)
  if not cls:continue
  found=True
  for m in cls.get_methods():
   if not m.get_code():continue
   lines=[i.get_name()+' '+i.get_output() for i in m.get_instructions()]
   if name.endswith('/u1;') or any('country' in s.lower() or 'locale' in s.lower() for s in lines):
    print(name,m.get_name());print('\n'.join(lines))
 if found:
  Path('android-preview/logs/xiaomi-startup/config-dex.bin').write_bytes(raw)
  break
