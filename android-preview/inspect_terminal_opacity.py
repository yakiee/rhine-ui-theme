import json,zipfile
with zipfile.ZipFile('rhine_exact/output/hyperos-klwp-v0.13.51/Rhine-UI-HyperOS-v0.13.51.klwp') as z:r=json.loads(z.read('preset.json'))['preset_root']
for k,v in r['globals_list'].items():
 if any(w in k for w in ['dark','mode','opac','alpha','anim','page','view']):print('GLOBAL',k,v)
for i,n in enumerate(r['viewgroup_items'][:22]):
 print(i,n.get('internal_title'),{k:v for k,v in n.items() if ('config' in k or k=='internal_formulas')})
 if i in [4,5,10]:
  print('ANIM',json.dumps(n.get('internal_animations'),ensure_ascii=False)[:6000])
