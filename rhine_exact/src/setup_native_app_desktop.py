from pathlib import Path
import subprocess,time
adb=str(Path('android-preview/sdk/platform-tools/adb.exe').resolve())
def run(*a):subprocess.run([adb,'-s','emulator-5580',*a],capture_output=True,check=True)
for sx,sy,dx,dy in [(445,300,270,650),(270,1020,445,650),(615,1020,615,650),(105,1020,105,920),(615,780,270,920),(270,540,445,920),(105,300,615,920)]:
 run('shell','input','swipe','360','1350','360','430','400');time.sleep(1)
 run('shell','input','draganddrop',str(sx),str(sy),str(dx),str(dy),'1200');time.sleep(1)
print('Native shortcuts placed')
