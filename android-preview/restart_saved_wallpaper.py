from rebuild_ui import run
from pathlib import Path
import time
print('old pid',run('shell','pidof','org.kustom.wallpaper').decode().strip())
run('shell','am','force-stop','org.kustom.wallpaper.huawei');time.sleep(.5)
print(run('shell','am','start','-W','-n','org.kustom.wallpaper.huawei/org.kustom.app.OnBoardingActivity').decode())
time.sleep(1);run('shell','input','keyevent',3);time.sleep(2)
print('new pid',run('shell','pidof','org.kustom.wallpaper').decode().strip())
