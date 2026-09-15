from rebuild_ui import run,snapshot
import subprocess,time,sys
subprocess.run([sys.executable,'-X','utf8','android-preview/open_current_editor.py'],check=True,stdout=subprocess.DEVNULL)
run('shell','input','swipe',1134,354,1134,354,650)
snapshot()
