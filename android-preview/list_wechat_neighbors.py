import json,zipfile
with zipfile.ZipFile('rhine_exact/output/hyperos-klwp-v0.13.51/Rhine-UI-HyperOS-v0.13.51.klwp') as z:r=json.loads(z.read('preset.json'))['preset_root']
for k,v in r['globals_list'].items():
 if 20<=v.get('index',0)<=62:print(k,v.get('index'),v.get('title'))
