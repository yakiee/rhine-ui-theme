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
 cls=dex.get_class('Lorg/kustom/config/v1;')
 if not cls:continue
 for m in cls.get_methods():
  if m.get_name() in ('<init>','I'):
   print(m.get_name(),m.get_descriptor());print('\n'.join(i.get_name()+' '+i.get_output() for i in m.get_instructions()))
 break

