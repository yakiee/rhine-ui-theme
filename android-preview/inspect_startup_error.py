import sys
from pathlib import Path
sys.path.insert(0,str(Path('rhine_exact/tools').resolve()))
from loguru import logger
logger.remove()
from androguard.core.apk import APK
apk=APK('android-preview/apps/KLWP-aosp.apk')
r=apk.get_android_resources()
for pkg in r.get_packages_names():
 for loc in r.get_locales(pkg):
  data=r.get_string_resources(pkg,loc).decode('utf-8')
  for line in data.splitlines():
   if any(k in line.lower() for k in ['bad store','pirat','此版本','problematic store']): print(loc,line)
