import json,zipfile
with zipfile.ZipFile('rhine_exact/output/hyperos-klwp-v0.13.51/Rhine-UI-HyperOS-v0.13.51.klwp') as z:r=json.loads(z.read('preset.json'))['preset_root']
n=r['viewgroup_items'][50];print('CHILDREN',len(n['viewgroup_items']))
for i,c in enumerate(n['viewgroup_items']):
 if i>=60:print(i,c.get('internal_title'),len(c.get('viewgroup_items',[])))
