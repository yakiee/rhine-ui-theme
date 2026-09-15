import json
p=json.load(open('rhine_exact/output/interaction-cleanup-v0.13.43/preset.json',encoding='utf-8'));r=p['preset_root'];print('root keys',list(r))
for k,v in r.items():
 if k!='viewgroup_items':print(k,str(v)[:18000])
for i in [0,3,23,24,51]:
 print('ROOT',i,json.dumps(r['viewgroup_items'][i],ensure_ascii=False)[:18000])
