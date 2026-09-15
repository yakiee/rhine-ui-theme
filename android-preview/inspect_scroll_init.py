import sys,zipfile
from pathlib import Path
sys.path.insert(0,'rhine_exact/tools')
from loguru import logger
logger.remove()
from androguard.core.dex import DEX
out=[]
with zipfile.ZipFile('android-preview/apps/HyperOS-Launcher-inspect.apk') as z:
 for name in ['classes.dex','classes2.dex']:
  dex=DEX(z.read(name))
  for cls in dex.get_classes():
   if not any(s in cls.get_name() for s in ['DesktopWallpaperManager','WallpaperUtils','WallpaperScrolled']):continue
   for m in cls.get_methods():
    ins=[i.get_name()+' '+i.get_output() for i in m.get_instructions()]
    if any(any(s in row for s in ['mCanWallpaperScrolled','sIsCurrentWallpaperScrollable','updateWallpaperScrollable','isCurrentWallpaperScrollable']) for row in ins):
     out.append(cls.get_name()+'->'+m.get_name()+m.get_descriptor()+'\n'+'\n'.join(ins))
text='\n\n'.join(out)
Path('rhine_exact/output/dock-phone-fix-20260914/launcher-scroll-init.txt').write_text(text,encoding='utf8');print(text)
