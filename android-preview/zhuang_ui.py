import sys,time,json,re,xml.etree.ElementTree as ET
from pathlib import Path
from rebuild_ui import run
def dump():
    run('shell','uiautomator','dump','/sdcard/rhine-zhuang-ui.xml')
    raw=run('shell','cat','/sdcard/rhine-zhuang-ui.xml')
    Path('rhine_exact/assets/zhuangfangyi/current-ui.xml').write_bytes(raw)
    root=ET.fromstring(raw)
    print(json.dumps([{k:n.get(k) for k in ['text','content-desc','resource-id','bounds']} for n in root.iter('node') if n.get('text') or n.get('content-desc')],ensure_ascii=True),flush=True)
    return root
if __name__=='__main__':
    if len(sys.argv)>1:
        assert 'org.kustom.wallpaper' in run('shell','dumpsys','activity','activities').decode(errors='replace').split('topResumedActivity=')[-1].splitlines()[0]
        run('shell','input',*sys.argv[1:])
        time.sleep(.8)
    dump()
