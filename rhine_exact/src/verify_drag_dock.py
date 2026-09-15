from pathlib import Path
import subprocess,time,io,json,zipfile,math
from PIL import Image
base=Path.cwd();out=base/'rhine_exact/output/drag-dock-v0.13.50';adb=str(base/'android-preview/sdk/platform-tools/adb.exe')
def run(*a):return subprocess.run([adb,'-s','emulator-5580',*a],capture_output=True,check=True).stdout
def shot(n):Image.open(io.BytesIO(run('exec-out','screencap','-p'))).convert('RGB').save(out/'verification'/(n+'.jpg'))
run('shell','input','swipe','80','1000','260','1000','1500');time.sleep(2);shot('cancelled-drag')
run('shell','input','tap','595','1185');time.sleep(2);shot('terminal')
run('shell','input','tap','130','206');time.sleep(2);shot('final-home')
reports=[]
for suffix in ('','-off'):
 with zipfile.ZipFile(out/f'Rhine-UI-drag-dock{suffix}-v0.13.50.klwp') as z:
  assert z.testzip() is None;p=json.loads(z.read('preset.json'))
 with zipfile.ZipFile(base/f'rhine_exact/output/desktop-dock-fold-v0.13.47/Rhine-UI-desktop-dock-fold{suffix}-v0.13.47.klwp') as z:old=json.loads(z.read('preset.json'))
 r=p['preset_root']['viewgroup_items'];before=old['preset_root']['viewgroup_items'];changed=[i for i in range(len(r)) if r[i]!=before[i]];assert changed==[1,23,24]
 assert p['preset_root']['globals_list']==old['preset_root']['globals_list']
 for i in changed:
  tracks=[a for a in r[i]['internal_animations'] if a['type']=='SCROLL'];assert tracks and all(a['speed']==100 and 'duration' not in a for a in tracks)
  assert not any('gv(page)=-1' in a.get('formula','') for a in r[i]['internal_animations'])
 if suffix:assert 'GYRO' not in json.dumps(p)
 reports.append(dict(edition=suffix or 'normal',changed_roots=changed,driver='SCROLL',speed=100,navigation_unchanged=True))
(out/'verification/structure-check.json').write_text(json.dumps(reports,indent=2),encoding='utf-8')
print(reports)
