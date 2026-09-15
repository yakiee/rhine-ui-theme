from rebuild_ui import run
from rebuild_clipboard import ClipboardControl
import time
run('shell','input','tap',400,780)
time.sleep(.2)
run('shell','input','keycombination',113,29)
with ClipboardControl() as clipboard:
    clipboard.set('$if(gv(page)=1,f,b)$',paste=True)
time.sleep(.3)
print('Entered explicit forward/backward formula.')
