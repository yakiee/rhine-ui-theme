import json,zipfile
with zipfile.ZipFile('rhine_exact/output/hyperos-klwp-v0.13.51/Rhine-UI-HyperOS-v0.13.51.klwp') as z:r=json.loads(z.read('preset.json'))['preset_root']
def trim(n):
 return {k:([trim(c) for c in v] if k=='viewgroup_items' else v) for k,v in n.items() if k not in ['internal_animations','shape_path']}
print(json.dumps(trim(r['viewgroup_items'][51]),ensure_ascii=False,indent=2)[:22000])
print('EVENTS',json.dumps(r.get('internal_events'),ensure_ascii=False)[:4000])
