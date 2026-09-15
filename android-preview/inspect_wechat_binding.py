import json,zipfile
with zipfile.ZipFile('rhine_exact/output/hyperos-klwp-v0.13.51/Rhine-UI-HyperOS-v0.13.51.klwp') as z:r=json.loads(z.read('preset.json'))['preset_root']
for k,v in r['globals_list'].items():
 if any(s in str(v).lower()+k.lower() for s in ['wechat','weixin','微信','com.tencent.mm']):print('GLOBAL',k,v)
def walk(n,path):
 for e in n.get('internal_events',[]):
  if any(s in str(e).lower() for s in ['wechat','weixin','微信','com.tencent.mm']):print('EVENT',path,n.get('internal_title'),json.dumps(e,ensure_ascii=False))
 for i,c in enumerate(n.get('viewgroup_items',[])):walk(c,path+'/'+str(i))
walk(r,'root')
