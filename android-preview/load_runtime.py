from pathlib import Path
import subprocess,sys
base=Path(__file__).resolve().parent
adb=str(base/'sdk/platform-tools/adb.exe')
preset=Path(sys.argv[1]).resolve()
remote='/sdcard/Kustom/wallpapers/'+preset.name
for args in [('push',str(preset),remote),('shell','am','force-stop','org.kustom.wallpaper'),('shell','am','start','-n','org.kustom.wallpaper/org.kustom.lib.editor.WpAdvancedEditorActivity','-d','kfile://org.kustom.sdcard.000/wallpapers/'+preset.name)]:
 r=subprocess.run([adb,'-s','emulator-5580',*args],capture_output=True,timeout=30)
 if r.returncode:raise RuntimeError(r.stderr.decode(errors='replace'))
 print(r.stdout.decode(errors='replace'))
