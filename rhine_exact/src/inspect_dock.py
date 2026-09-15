import json
p=json.load(open('rhine_exact/output/interaction-cleanup-v0.13.43/preset.json',encoding='utf-8'));r=p['preset_root']['viewgroup_items']
def walk(n,path):
 print(path, n.get('internal_title',''),n.get('internal_type'),{k:v for k,v in n.items() if k in ['text_expression','shape_width','shape_height','position_padding_top','position_padding_bottom','position_padding_left','position_padding_right','internal_formulas','internal_events','internal_animations']})
 for i,c in enumerate(n.get('viewgroup_items',[])):walk(c,path+'.'+str(i))
walk(r[3],'3')
for i in [23,24,52,53,55,58]:
 print('META',i,{k:v for k,v in r[i].items() if k!='viewgroup_items'})
print('FLOW',p['preset_root']['internal_flows'])
