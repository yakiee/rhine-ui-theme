import json,zipfile
with zipfile.ZipFile('rhine_exact/output/hyperos-klwp-v0.13.51/Rhine-UI-HyperOS-v0.13.51.klwp') as z:r=json.loads(z.read('preset.json'))['preset_root']
needle='$if(si(screen)=gv(homepg),ALWAYS,REMOVE)$'
def walk(n,p):
 if n.get('internal_formulas',{}).get('config_visible')==needle:
  print(p,n.get('internal_title'),[(a.get('type'),a.get('formula'),a.get('action')) for a in n.get('internal_animations',[])[:2]])
 for i,c in enumerate(n.get('viewgroup_items',[])):walk(c,p+'/'+str(i))
walk(r,'root')
