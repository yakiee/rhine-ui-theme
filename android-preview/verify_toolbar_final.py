from pathlib import Path
source=Path('android-preview/verify_toolbar_transitions.py').read_text(encoding='utf-8')
source=source.replace("capture('01-toolbar-visible')","touch('tap',140,1150)\ncapture('01-toolbar-visible')")
source=source.replace("print('IMAGE:'+base64.b64encode(buf.getvalue()).decode())","touch('tap',140,1150)\nprint('Saved six transition screenshots; returned to closed Dock on theme page')")
exec(source)
