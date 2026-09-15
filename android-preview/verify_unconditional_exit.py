import sys
from pathlib import Path
exec(compile(Path('android-preview/apply_saved_home_wallpaper.py').read_text(encoding='utf-8'),'apply-saved-home','exec'))
source=Path('android-preview/stress_open_dock_swipe.py').read_text(encoding='utf-8')
source=source.replace("OUT=Path('rhine_exact/output/open-dock-swipe-20260915')", "OUT=Path('rhine_exact/output/open-dock-swipe-20260915/unconditional');OUT.mkdir(exist_ok=True)")
exec(compile(source,'stress-unconditional','exec'))
