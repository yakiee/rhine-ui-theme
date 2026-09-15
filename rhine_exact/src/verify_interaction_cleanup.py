from pathlib import Path
import subprocess,time,json,zipfile
base=Path.cwd(); adb=str(base/'android-preview/sdk/platform-tools/adb.exe')
def tap(x,y):
 subprocess.run([adb,'-s','emulator-5580','shell','input','tap',str(x),str(y)],check=True);time.sleep(2)
tap(130,206)
tap(595,1128)
tap(219,1356)
tap(645,189)
out=base/'rhine_exact/output/interaction-cleanup-v0.13.43'
shot=subprocess.run([adb,'-s','emulator-5580','exec-out','screencap','-p'],capture_output=True,check=True).stdout
(out/'home.png').write_bytes(shot)
reports=[]
for suffix in ('','-off'):
 old=base/f'rhine_exact/output/status-optical-balance-v0.13.42/Rhine-UI-status-optical-balance{suffix}-v0.13.42.klwp'
 new=out/f'Rhine-UI-interaction-cleanup{suffix}-v0.13.43.klwp'
 with zipfile.ZipFile(old) as z: before=json.loads(z.read('preset.json'))
 with zipfile.ZipFile(new) as z:
  assert z.testzip() is None
  after=json.loads(z.read('preset.json'))
 a=before['preset_root']['viewgroup_items'];b=after['preset_root']['viewgroup_items']
 assert len(a)==len(b)==64
 changed=[i for i in range(64) if a[i]!=b[i]]
 assert changed==[1,51,52,53,55],changed
 assert b[1]['config_visible']=='REMOVE' and not b[1]['viewgroup_items']
 assert all(not b[51]['viewgroup_items'][i]['viewgroup_items'] for i in (1,3,5,7))
 if suffix: assert 'GYRO' not in json.dumps(after)
 reports.append({'edition':suffix or 'normal','roots':64,'changed_roots':changed,'archive_valid':True})
(out/'verification/structure-check.json').write_text(json.dumps(reports,indent=2),encoding='utf-8')
print(json.dumps(reports))
