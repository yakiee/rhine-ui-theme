from pathlib import Path
import json,zipfile,copy,hashlib
base=Path('rhine_exact/output/free-editor-rebuild');clips=base/'clips';clips.mkdir(exist_ok=True)
with zipfile.ZipFile('rhine_exact/output/hyperos-klwp-v0.13.51/Rhine-UI-HyperOS-v0.13.51.klwp') as z:source=json.loads(z.read('preset.json'))
root=source['preset_root'];layers=copy.deepcopy(root['viewgroup_items'])
def encode(data):return '##KUSTOMCLIP##\n'+json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n##KUSTOMCLIP##'
def write(name,items):
 text=encode({'clip_version':1,'clip_cut':[],'clip_modules':items})
 target=clips/name;target.write_text(text,encoding='utf-8')
 return {'file':name,'count':len(items),'bytes':len(text.encode('utf-8')),'titles':[n.get('internal_title','') for n in items]}
# Keep root indices stable; the large dot-light container is filled in smaller native paste batches.
glow_children=layers[24]['viewgroup_items'];layers[24]['viewgroup_items']=[]
plan={'source':'Rhine-UI-HyperOS-v0.13.51.klwp','root_count':len(layers),'global_count':len(root['globals_list']),'root_batches':[],'glow_parent_index':24,'glow_batches':[],'status':'prepared; globals submitted through native editor, page components not yet inserted'}
for collection,label,target in [(layers,'root',plan['root_batches']),(glow_children,'glow',plan['glow_batches'])]:
 batch=[];number=0;start=0
 for index,item in enumerate(collection):
  candidate=batch+[item]
  if batch and len(encode({'clip_version':1,'clip_cut':[],'clip_modules':candidate}).encode('utf-8'))>180000:
   entry=write(f'{label}-{number:02}.clip.txt',batch);entry['start_index']=start;target.append(entry)
   number+=1;start=index;batch=[]
  batch.append(item)
 if batch:
  entry=write(f'{label}-{number:02}.clip.txt',batch);entry['start_index']=start;target.append(entry)
plan['flows']=root.get('internal_flows',[]);plan['background_color']=root.get('background_color')
(base/'rebuild-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print('Root batches',[(v['file'],v['count'],v['bytes']) for v in plan['root_batches']])
print('Glow batches',[(v['file'],v['count'],v['bytes']) for v in plan['glow_batches']])
print('Original component tree and animations preserved; only native insertion batches split.')
