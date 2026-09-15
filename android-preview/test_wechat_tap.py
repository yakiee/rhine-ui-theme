from rebuild_ui import run
import time
run('shell','input','tap',1070,1520);time.sleep(1)
a=run('shell','dumpsys','activity','activities').decode(errors='replace');print('\n'.join(x for x in a.splitlines() if 'topResumedActivity' in x))
l=run('logcat','-d','-t','600').decode(errors='replace');print('\n'.join(x for x in l.splitlines() if any(w in x.lower() for w in ['kustom','weixin://','wxcustomscheme','background activity','background start','backgroundstart','bal_block','launcherui'])))
