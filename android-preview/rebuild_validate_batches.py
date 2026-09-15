from pathlib import Path
import json,zipfile,copy
base=Path('rhine_exact/output/free-editor-rebuild');plan=json.loads((base/'rebuild-plan.json').read_text(encoding='utf-8'))
def decode(name):return json.loads((base/'clips'/name).read_text(encoding='utf-8').replace('##KUSTOMCLIP##',''))['clip_modules']
layers=[]
for item in plan['root_batches']:layers.extend(decode(item['file']))
glow=[]
for item in plan['glow_batches']:glow.extend(decode(item['file']))
layers[24]['viewgroup_items']=glow
with zipfile.ZipFile('rhine_exact/output/hyperos-klwp-v0.13.51/Rhine-UI-HyperOS-v0.13.51.klwp') as z:source=json.loads(z.read('preset.json'))
assert layers==source['preset_root']['viewgroup_items']
report={'batch_reconstruction_exact_match':True,'root_layers':len(layers),'globals':plan['global_count'],'phone_components_inserted':0,'phone_globals_submitted':226,'phone_visual_verification':'pending','phone_saved_theme':'not yet verified','waiting_for_user':'Keep phone in KLWP during UI operations'}
(base/'rebuild-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
