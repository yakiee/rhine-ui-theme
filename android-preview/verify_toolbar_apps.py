import json,time,re
import xml.etree.ElementTree as ET
from pathlib import Path
from rebuild_ui import run

OUT=Path('rhine_exact/output/toolbar-five-apps-20260915')

def foreground():
    raw=run('shell','dumpsys','activity','activities').decode(errors='replace')
    return next(line.strip() for line in raw.splitlines() if 'topResumedActivity=' in line)

def home_page():
    assert 'com.miui.home/' in foreground(), 'Stopped: phone left launcher'
    run('shell','uiautomator','dump','/sdcard/rhine-toolbar-check.xml')
    root=ET.fromstring(run('shell','cat','/sdcard/rhine-toolbar-check.xml'))
    return next(n.get('content-desc') for n in root.iter('node') if re.fullmatch(r'第 \d+ 页共 \d+ 页',n.get('content-desc','')))

results=[]
for name,y,package in [('phone',1587,'com.android.contacts'),('sms',1680,'com.android.mms'),('browser',1778,'com.android.browser'),('camera',1878,'com.android.camera')]:
    assert home_page()=='第 2 页共 4 页'
    run('shell','input','tap',1010,y)
    time.sleep(1)
    top=foreground()
    result={'entry':name,'opened':package+'/' in top,'activity':top}
    results.append(result)
    (OUT/'app-verification.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(result),flush=True)
    assert result['opened'], 'Unexpected foreground; no further input'
    run('shell','input','keyevent','KEYCODE_HOME')
    time.sleep(.7)
print('All four application destinations verified; no app content inspected')
