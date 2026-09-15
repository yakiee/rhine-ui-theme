from pathlib import Path
from rebuild_ui import run
p=Path('android-preview/add_follow_scroll_animation.py')
s=p.read_text(encoding='utf-8')
assert "run('shell','input','tap','84','216')" in s
s=s.replace("run('shell','input','tap','84','216')", "run('shell','input','keyevent','KEYCODE_BACK')")
p.write_text(s,encoding='utf-8')
run('shell','input','keyevent','KEYCODE_BACK')
print('Corrected parent navigation and closed the drawer')
