import json
p=json.load(open('rhine_exact/output/native-desktop-navigation-v0.13.46/preset.json',encoding='utf-8'))
for i in [23,24]:
 r=p['preset_root']['viewgroup_items'][i]
 print(i,r.get('internal_formulas'))
 print('animations',[(a.get('type'),a.get('formula'),a.get('internal_formulas')) for a in r['internal_animations']])
 print('children',[(j,c.get('internal_title'),c.get('internal_formulas')) for j,c in enumerate(r['viewgroup_items'])])
