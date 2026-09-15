from pathlib import Path
import zipfile,json,collections
base=Path('rhine_exact/output/free-editor-rebuild');base.mkdir(exist_ok=True)
source=Path('rhine_exact/output/hyperos-klwp-v0.13.51/Rhine-UI-HyperOS-v0.13.51.klwp')
with zipfile.ZipFile(source) as z:
 p=json.loads(z.read('preset.json'));root=p['preset_root']
 for name in z.namelist():
  if name.startswith(('bitmaps/','fonts/','licenses/')):
   dest=base/'assets'/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(z.read(name))
 def clip(data):return '##KUSTOMCLIP##\n'+json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n##KUSTOMCLIP##'
 globals_map=root['globals_list']
 for key,value in globals_map.items():value['key']=key
 (base/'globals.clip.txt').write_text(clip({'clip_version':1,'KUSTOM_GLOBAL':globals_map}),encoding='utf-8')
 print('globals clipboard bytes',len((base/'globals.clip.txt').read_bytes()),'types',dict(collections.Counter(v['type'] for v in globals_map.values())))
 for i,node in enumerate(root['viewgroup_items']):
  print(i,len(clip({'clip_version':1,'clip_cut':[],'clip_modules':[node]}).encode()),node.get('internal_title'))
 print('root flows',json.dumps(root.get('internal_flows'),ensure_ascii=False)[:7000])
 print('root events',json.dumps(root.get('internal_events'),ensure_ascii=False)[:2000])
 print('resource globals',json.dumps([(k,v) for k,v in globals_map.items() if v.get('type') in ['BITMAP','FONT']],ensure_ascii=False))
