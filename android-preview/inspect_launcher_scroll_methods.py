import sys,zipfile,re
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
   for m in cls.get_methods():
    if m.get_name() in ['canWallpaperScrolled','isCurrentWallpaperScrollable','setIsCurrentWallpaperScrollable','getWallpaperScroll','registerWallpaperScrollableObserver','updateWallpaperScrollable','updateWallpaperScrollableVT','updateWallpaperOffset']:
     rows=[cls.get_name()+'->'+m.get_name()+m.get_descriptor()]
     rows.extend(i.get_name()+' '+i.get_output() for i in m.get_instructions())
     out.append('\n'.join(rows))
text='\n\n'.join(out)
Path('rhine_exact/output/dock-phone-fix-20260914/launcher-scroll-methods.txt').write_text(text,encoding='utf8')
print(text)
