from rebuild_ui import run
import time
run('shell','input','tap',840,216)
time.sleep(2)
run('shell','input','keyevent',3)
time.sleep(3)
exec(open('android-preview/inspect_draft_screen.py',encoding='utf-8').read())
