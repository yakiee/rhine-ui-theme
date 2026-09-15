import json
p=json.load(open('rhine_exact/output/drag-dock-v0.13.50/preset.json',encoding='utf-8'));ev=[]
def walk(n):
 for e in n.get('internal_events',[]):
  if e.get('action') not in ('SWITCH_GLOBAL',):
   if e not in ev:ev.append(e)
 for c in n.get('viewgroup_items',[]):walk(c)
walk(p['preset_root']);print(json.dumps(ev,ensure_ascii=False,indent=2))
