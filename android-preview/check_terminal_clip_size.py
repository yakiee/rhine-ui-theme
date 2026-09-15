import json,zipfile
with zipfile.ZipFile('rhine_exact/output/hyperos-klwp-v0.13.51/Rhine-UI-HyperOS-v0.13.51.klwp') as z:r=json.loads(z.read('preset.json'))['preset_root']
n=r['viewgroup_items'][50];print(n['internal_title'],len(json.dumps(n,ensure_ascii=False).encode()))
