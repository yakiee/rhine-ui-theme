import sys,zipfile,re
from pathlib import Path
sys.path.insert(0,'rhine_exact/tools')
from loguru import logger
logger.remove()
from androguard.core.dex import DEX
out=[]
with zipfile.ZipFile('android-preview/apps/KLWP-3.82-huawei.apk') as z:
 for name in z.namelist():
  if not re.fullmatch(r'classes\d*\.dex',name):continue
  dex=DEX(z.read(name))
  for cls in dex.get_classes():
   if cls.get_name()!='Lorg/kustom/lib/KContext$a;':continue
   for m in cls.get_methods():
    rows=[cls.get_name()+'->'+m.get_name()+m.get_descriptor()]
    rows.extend(i.get_name()+' '+i.get_output() for i in m.get_instructions());out.append('\n'.join(rows))
text='\n\n'.join(out);Path('rhine_exact/output/dock-phone-fix-20260914/klwp-context.txt').write_text(text,encoding='utf8')
print(next(t for t in out if '->D0(' in t))
