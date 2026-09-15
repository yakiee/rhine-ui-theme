from pathlib import Path
import json,zipfile
with zipfile.ZipFile('rhine_exact/output/hyperos-klwp-v0.13.51/Rhine-UI-HyperOS-v0.13.51.klwp') as z:p=json.loads(z.read('preset.json'))
r=p['preset_root']
for k in ['page','view','origin','homepg','mode','dock','menu']:
 print('GLOBAL',k,r['globals_list'].get(k))
for i in [1,3,51]:
 n=r['viewgroup_items'][i]
 print('ROOT',i, json.dumps({k:v for k,v in n.items() if k!='viewgroup_items'},ensure_ascii=False))
