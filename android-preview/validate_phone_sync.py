from pathlib import Path
import zipfile,json,copy,collections
base=Path('rhine_exact/output/free-editor-rebuild');plan=json.loads((base/'rebuild-plan.json').read_text(encoding='utf8'))
def decode(name):return json.loads((base/'phone-clips'/name).read_text(encoding='utf8').replace('##KUSTOMCLIP##',''))['clip_modules']
layers=[]
for b in plan['root_batches']:layers.extend(decode(b['file']))
layers[24]['viewgroup_items']=[n for b in plan['glow_batches'] for n in decode(b['file'])]
with zipfile.ZipFile('rhine_exact/output/hyperos-klwp-v0.13.51/Rhine-UI-HyperOS-v0.13.51.klwp') as z:p=json.loads(z.read('preset.json'))
expected=json.loads(json.dumps(p['preset_root']['viewgroup_items'],ensure_ascii=False).replace('kfile://org.kustom.provider/','kfile://org.kustom.sdcard/'))
assert layers==expected
report={'source':'Rhine-UI-HyperOS-v0.13.51.klwp','root_layers':64,'phone_root_layers_seen':64,'phone_glow_batches_inserted':2,'phone_globals':226,'layout_and_animations_unchanged':True,'resource_change':'Only kfile provider authority mapped to authorized phone work folder; wallpaper selected through Android photo picker','flow':'Native flow clipboard prepared; not yet inserted','saved_and_reopened':'Pending final verification','applied_to_wallpaper':False}
(base/'sync-status.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False))
from rebuild_ui import run,snapshot
run('shell','input','tap',840,216)
snapshot()
