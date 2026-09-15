import sys,zipfile
from pathlib import Path
sys.path.insert(0,str(Path('rhine_exact/tools').resolve()))
from loguru import logger
logger.remove()
from androguard.core.apk import APK
from androguard.core.dex import DEX
apk=APK('android-preview/apps/KLWP-aosp.apk');r=apk.get_android_resources();pkg=apk.get_package()
ids=[]
for line in r.get_public_resources(pkg).decode().splitlines():
 if 'dialog_corrupted_' in line:print(line);ids.append(int(line.split('id="')[1].split('"')[0],16))
for line in r.get_string_resources(pkg).decode().splitlines():
 if 'dialog_corrupted_' in line:print(line)
for raw in apk.get_all_dex():
 dex=DEX(raw)
 for method in dex.get_encoded_methods():
  if method.get_code() is None:continue
  ins=list(method.get_instructions())
  if any(i.get_name().startswith('const') and any(str(rid) in i.get_output() for rid in ids) for i in ins):
   print('METHOD',method.get_class_name(),method.get_name());print('\n'.join(i.get_name()+' '+i.get_output() for i in ins))

