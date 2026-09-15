from pathlib import Path
import sys,zipfile
sys.path.insert(0,str(Path('rhine_exact/tools').resolve()))
from loguru import logger
logger.remove()
from androguard.core.dex import DEX
with zipfile.ZipFile('android-preview/apps/KLWP-3.82-huawei.apk') as z:
 for name in z.namelist():
  if name.endswith('.dex'):
   raw=z.read(name)
   if b'KUSTOMCLIP' not in raw:continue
   print('DEX',name,flush=True)
   dex=DEX(raw)
   for cls in dex.get_classes():
    if not cls.get_name().startswith('Lorg/kustom/'):continue
    for m in cls.get_methods():
     if not m.get_code():continue
     lines=[i.get_name()+' '+i.get_output() for i in m.get_instructions()]
     if any('KUSTOMCLIP' in s for s in lines):
      print(cls.get_name(),m.get_name(),'\n'+'\n'.join(lines),flush=True)
