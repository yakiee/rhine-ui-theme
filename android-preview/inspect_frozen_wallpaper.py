from rebuild_ui import run
from pathlib import Path
p=run('shell','pidof','org.kustom.wallpaper').decode().strip();print('PID',p)
if p:
 s=run('logcat','-d','--pid='+p,'-t','500').decode(errors='replace');Path('rhine_exact/output/dock-opacity-20260914/wallpaper-log.txt').write_text(s,encoding='utf8');print('\n'.join(x for x in s.splitlines() if any(w in x.lower() for w in ['error','exception','pause','resume','render','memory','fps','surface','glthread']))[-16000:])
print(run('shell','dumpsys','activity','exit-info','org.kustom.wallpaper.huawei').decode()[:2100])
