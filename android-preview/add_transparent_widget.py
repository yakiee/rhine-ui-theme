from pathlib import Path
import subprocess,time
adb=str(Path('android-preview/sdk/platform-tools/adb.exe').resolve())
def run(*a):subprocess.run([adb,'-s','emulator-5580',*a],capture_output=True,check=True)
def tap(x,y):run('shell','input','tap',str(x),str(y));time.sleep(.6)
run('shell','input','swipe','100','1000','100','1000','1000');time.sleep(.6);tap(210,770);tap(230,324);run('shell','input','text','Transparent');time.sleep(.7);tap(300,485);tap(350,730);tap(360,950)
