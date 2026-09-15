import sys
from pathlib import Path
sys.path.insert(0,str(Path('rhine_exact/tools').resolve()))
from loguru import logger
logger.remove()
from androguard.core.dex import DEX
d=DEX(Path('rhine_exact/analysis/effects.dex').read_bytes())
for c in d.get_classes():
 if c.get_name() in ['Lorg/kustom/lib/options/AnimationType;','Lorg/kustom/lib/options/AnimationRule;','Lorg/kustom/lib/options/AnimationCenter;']:
  print(c.get_name(),[f.get_name() for f in c.get_fields()])
print('candidates',[(c.get_name()) for c in d.get_classes() if 'animat' in c.get_name().lower() and 'editor' not in c.get_name().lower()][:60])
