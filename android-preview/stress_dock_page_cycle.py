from rebuild_ui import run
from pathlib import Path
import time,json

out=Path('rhine_exact/output/dock-page-lifecycle-20260914')
results=[]
for index in range(6):
    forward=(1040,160) if index%2==0 else (160,1040)
    backward=forward[::-1]
    run('shell','input','swipe',forward[0],1160,forward[1],1160,250)
    time.sleep(.25)
    run('shell','input','swipe',backward[0],1160,backward[1],1160,250)
    time.sleep(.8)
    (out/f'cycle-{index+1}-returned.png').write_bytes(run('exec-out','screencap','-p'))
    run('shell','input','tap',1020,1967)
    time.sleep(1)
    (out/f'cycle-{index+1}-opened.png').write_bytes(run('exec-out','screencap','-p'))
    results.append({'cycle':index+1,'neighbor':3 if index%2==0 else 1,'captured':True})
    print('Captured desktop return and Dock opening, cycle',index+1,flush=True)
(out/'cycles.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
