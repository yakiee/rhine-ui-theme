import sys
from pathlib import Path
sys.path.insert(0,str(Path('rhine_exact/tools').resolve()))
from loguru import logger
logger.remove()
from androguard.core.dex import DEX
from zipfile import ZipFile
path=Path(sys.argv[1])
with ZipFile(path) as archive:
 for name in archive.namelist():
  if not name.endswith('.dex'):continue
  dex=DEX(archive.read(name))
  cls=dex.get_class('Lorg/kustom/app/MarketActivity;')
  if cls:
   print('APK',path,'DEX',name)
   for method in cls.get_methods():
    if method.get_name()=='onCreate':
     print('\n'.join(i.get_name()+' '+i.get_output() for i in method.get_instructions()))
   break
