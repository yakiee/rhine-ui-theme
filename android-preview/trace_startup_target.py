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
 for cls in dex.get_classes():
  if not cls.get_name().startswith('Lorg/kustom/'):continue
  for m in cls.get_methods():
   if not m.get_code():continue
   ins=list(m.get_instructions());lines=[i.get_name()+' '+i.get_output() for i in ins]
   if any('dialog_corrupted' in s or '7f130138' in s or '2131951928' in s for s in lines):
    print('METHOD',cls.get_name(),m.get_name());print('\n'.join(lines))
