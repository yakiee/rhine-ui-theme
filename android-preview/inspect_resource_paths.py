from pathlib import Path
import zipfile,sys
sys.path.insert(0,str(Path('rhine_exact/tools').resolve()))
from loguru import logger
logger.remove()
from androguard.core.dex import DEX
with zipfile.ZipFile('android-preview/apps/KLWP-3.82-huawei.apk') as z:
 for name in z.namelist():
  if not name.endswith('.dex'):continue
  raw=z.read(name)
  if b'org.kustom.space.' not in raw and b'org.kustom.sdcard' not in raw:continue
  dex=DEX(raw)
  for cls in dex.get_classes():
   for m in cls.get_methods():
    if not m.get_code():continue
    lines=[i.get_name()+' '+i.get_output() for i in m.get_instructions()]
    if any('org.kustom.space.' in s or 'org.kustom.sdcard' in s for s in lines):
     print(cls.get_name(),m.get_name(),'\n'+'\n'.join(lines)[:14000])
