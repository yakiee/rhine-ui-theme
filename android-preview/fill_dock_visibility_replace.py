from rebuild_ui import run
from rebuild_clipboard import ClipboardControl
import time

# Keep animated visual layers resident; their existing page animations hide them.
# Native touch layers are not selected and remain gated to desktop page two.
with ClipboardControl() as clipboard:
    run('shell', 'input', 'tap', 450, 1210)
    clipboard.set('$if(si(screen)=gv(homepg),ALWAYS,REMOVE)$', paste=True)
    run('shell', 'input', 'keyevent', 4)
    run('shell', 'input', 'tap', 450, 1370)
    clipboard.set('$if(1,ALWAYS,REMOVE)$', paste=True)
    run('shell', 'input', 'keyevent', 4)
print('Exact visual lifecycle replacement entered; awaiting field verification.')
