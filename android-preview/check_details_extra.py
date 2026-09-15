from pathlib import Path
import subprocess,time
ADB=str(Path('android-preview/sdk/platform-tools/adb.exe').resolve());OUT=Path('rhine_exact/output/details-v0.6/screens')
def run(*args):
 r=subprocess.run([ADB,'-s','emulator-5580',*args],capture_output=True,timeout=30)
 if r.returncode:raise RuntimeError(r.stderr.decode(errors='replace'))
 return r.stdout
def tap(x,y,delay=1):run('shell','input','tap',str(x),str(y));time.sleep(delay)
def shot(name):(OUT/(name+'.png')).write_bytes(run('exec-out','screencap','-p'))
tap(596,1015,2);tap(522,204,2.3);shot('15-music-playing');tap(359,1365);shot('16-music-paused');tap(359,1365);shot('17-music-resumed');tap(605,204,2);tap(158,427);shot('18-calendar-selected');tap(522,204,2.3);shot('19-music-final');print('Playback and date selection checked')
