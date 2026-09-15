import json
r=json.load(open('rhine_exact/output/native-desktop-navigation-v0.13.44/preset.json',encoding='utf-8'))['preset_root']['viewgroup_items']
print(json.dumps(r[52],ensure_ascii=False,indent=2))
