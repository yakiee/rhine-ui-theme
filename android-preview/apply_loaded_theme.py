from pathlib import Path
import subprocess,time
ADB=str(Path('android-preview/sdk/platform-tools/adb.exe').resolve())
def run(*args):
 r=subprocess.run([ADB,'-s','emulator-5580',*args],capture_output=True,timeout=20)
 if r.returncode:raise RuntimeError(r.stderr)
 return r.stdout
activity=run('shell','dumpsys','activity','activities').decode(errors='replace')
assert 'WpAdvancedEditorActivity' in activity
run('shell','input','tap','480','96');time.sleep(1)
run('shell','am','start','-a','android.service.wallpaper.CHANGE_LIVE_WALLPAPER','--ecn','android.service.wallpaper.extra.LIVE_WALLPAPER_COMPONENT','org.kustom.wallpaper/.WpGLService');time.sleep(1.5)
run('shell','input','tap','360','1438');time.sleep(.7)
run('shell','input','tap','280','774');time.sleep(1)
run('shell','input','keyevent','3');time.sleep(2)
print('Applied loaded KLWP preset')
