import json,zipfile
with zipfile.ZipFile('rhine_exact/output/hyperos-klwp-v0.13.51/Rhine-UI-HyperOS-v0.13.51.klwp') as z:r=json.loads(z.read('preset.json'))['preset_root']
def walk(n,p):
 vals={k:v for k,v in n.items() if k in ['paint_color','config_alpha','config_opacity','config_filter','config_bitmap_mode']}
 formulas={k:v for k,v in n.get('internal_formulas',{}).items() if any(s in k for s in ['paint','alpha','filter','opacity'])}
 if vals or formulas: print(p,n.get('internal_title'),vals,formulas)
 for i,c in enumerate(n.get('viewgroup_items',[])):walk(c,p+'/'+str(i))
for i in [4,5,10]:walk(r['viewgroup_items'][i],str(i))
print('HIT0',r['viewgroup_items'][50]['viewgroup_items'][0])
