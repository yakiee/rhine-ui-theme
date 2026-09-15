from pathlib import Path
source=Path('android-preview/repair_swipe_unconditional_exit.py').read_text(encoding='utf-8')
source=source.replace("exec(compile(source,__file__,'exec'))", "source=source.replace('checks[1]','checks[0]').replace(\"endswith('/checkbox')][1]\",\"endswith('/checkbox')][0]\")\nexec(compile(source,__file__,'exec'))")
exec(compile(source,__file__,'exec'))
