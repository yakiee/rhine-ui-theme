from pathlib import Path
import zipfile,json
with zipfile.ZipFile('rhine_exact/output/hyperos-klwp-v0.13.51/Rhine-UI-HyperOS-v0.13.51.klwp') as z:p=json.loads(z.read('preset.json'))
r=p['preset_root']
print('ROOT SETTINGS',json.dumps({k:v for k,v in r.items() if k not in ['viewgroup_items','globals_list','internal_flows']},ensure_ascii=False)[:5000])
print('ROOT1 ANIM',json.dumps(r['viewgroup_items'][1].get('internal_animations'),ensure_ascii=False))
