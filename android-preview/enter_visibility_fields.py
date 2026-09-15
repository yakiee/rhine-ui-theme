from rebuild_ui import run
from rebuild_clipboard import ClipboardControl
import time

with ClipboardControl() as clipboard:
    clipboard.set('$if(si(screen)=gv(homepg),ALWAYS,REMOVE)$', paste=True)
    time.sleep(.6)
    run('shell','input','tap',450,845)
    time.sleep(.4)
    clipboard.set('$if(1,ALWAYS,REMOVE)$', paste=True)
    time.sleep(.6)
print('Both replacement fields filled; keyboard left open for verification.')
