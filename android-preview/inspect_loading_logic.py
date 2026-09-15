from pathlib import Path
import json,zipfile
p=Path('rhine_exact/output/free-editor-rebuild/rebuild-plan.json');d=json.loads(p.read_text(encoding='utf8'));print('FLOWS',json.dumps(d.get('flows'),ensure_ascii=False))
with zipfile.ZipFile('rhine_exact/output/hyperos-klwp-v0.13.51/Rhine-UI-HyperOS-v0.13.51.klwp') as z:root=json.loads(z.read('preset.json'))['preset_root']
print('ROOT KEYS',root.keys())
for k,v in root.get('globals',{}).items():
 if any(w in k for w in ['load','view','origin','page','home','target']):print(k,v)
for n in root['viewgroup_items']:
 if any(w in n.get('internal_title','') for w in ['加载','入口','返回']):
  print('MODULE',json.dumps({k:v for k,v in n.items() if k!='viewgroup_items'},ensure_ascii=False))
  for c in n.get('viewgroup_items',[]):
   if c.get('internal_taps'):print(c.get('internal_title'),c['internal_taps'])
