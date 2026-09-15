from pathlib import Path
import subprocess,time,json
base=Path(__file__).resolve().parent
adb=str(base/'sdk/platform-tools/adb.exe')
serial='emulator-5580'
def run(*args,timeout=40):
    result=subprocess.run([adb,'-s',serial,*args],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=timeout)
    if result.returncode:raise RuntimeError(result.stdout+result.stderr)
    return result.stdout.strip()
print('Waiting for Android to finish booting...',flush=True)
for attempt in range(120):
    try:
        if run('shell','getprop','sys.boot_completed',timeout=5)=='1':break
    except Exception:pass
    time.sleep(3)
else:raise RuntimeError('Android has not finished booting.')
print(run('install','-r',str(base/'apps/KLWP-aosp.apk'),timeout=120),flush=True)
run('shell','mkdir','-p','/sdcard/Download/RhineTheme')
package=base.parent/'rhine_exact/output/native-theme-v0.2/Rhine-UI-native-v0.2-unfinished.klwp'
print(run('push',str(package),'/sdcard/Download/RhineTheme/Rhine-UI.klwp'),flush=True)
print(run('shell','am','start','-a','android.intent.action.MAIN','-c','android.intent.category.LAUNCHER','-p','org.kustom.wallpaper'),flush=True)
(base/'logs/app-setup.json').write_text(json.dumps({'klwp_installed':True,'theme_on_device':'/sdcard/Download/RhineTheme/Rhine-UI.klwp','theme_imported':False},indent=2),encoding='utf-8')
