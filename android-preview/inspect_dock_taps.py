import json,zipfile
with zipfile.ZipFile('rhine_exact/output/hyperos-klwp-v0.13.51/Rhine-UI-HyperOS-v0.13.51.klwp') as z:r=json.loads(z.read('preset.json'))['preset_root']
for name,g in r['globals_list'].items():
 if any(w in name.lower() for w in ['load','view','origin','page','home']):print('GLOBAL',g)
def walk(n):
 for k,v in n.items():
  if 'tap' in k or 'touch' in k:print(n.get('internal_title'),k,json.dumps(v,ensure_ascii=False))
 for c in n.get('viewgroup_items',[]):walk(c)
for i,n in enumerate(r['viewgroup_items']):
 if '交互区域 · 09' in n.get('internal_title','') or '25 加载' in n.get('internal_title',''):print('ROOT',i,n.get('internal_title'));walk(n)

