"""Export the current editable preset with configurable Xiaomi app targets."""
from pathlib import Path
import json,zipfile,copy,re,hashlib
BASE=Path('rhine_exact'); SRC=BASE/'output/drag-dock-v0.13.50'; OUT=BASE/'output/hyperos-klwp-v0.13.51'; OUT.mkdir(exist_ok=True)
def walk(n):
 yield n
 for c in n.get('viewgroup_items',[]):yield from walk(c)
def strings(n):
 if isinstance(n,str):yield n
 elif isinstance(n,dict):
  for v in n.values():yield from strings(v)
 elif isinstance(n,list):
  for v in n:yield from strings(v)
def app_url(key):return '$"android-app://"+gv('+key+')+"#Intent;action=android.intent.action.MAIN;category=android.intent.category.LAUNCHER;end"$'
reports=[]
for suffix in ('','-off'):
 source=SRC/f'Rhine-UI-drag-dock{suffix}-v0.13.50.klwp'
 with zipfile.ZipFile(source) as z:
  p=json.loads(z.read('preset.json')); original=copy.deepcopy(p); g=p['preset_root']['globals_list']
  for key,title,value in [('galleryapp','相册 · 自定义 App 包名','com.miui.gallery'),('fileapp','文件 · 自定义 App 包名','com.android.fileexplorer')]:
   g[key]=dict(index=max(v['index'] for v in g.values())+1,type='TEXT',title=title,value=value,description='默认小米系统应用；可改为手机上其他已安装应用的包名。',global_formula='')
  counts=dict(phone=0,files=0,gallery=0)
  for n in walk(p['preset_root']):
   for e in n.get('internal_events',[]):
    intent=e.get('intent','')
    if e.get('action')!='LAUNCH_ACTIVITY':continue
    if 'component=com.android.dialer/' in intent:
     e['intent']='intent:#Intent;action=android.intent.action.DIAL;end';counts['phone']+=1
    elif 'component=com.google.android.documentsui/' in intent:
     e.pop('intent');e.update(action='OPEN_LINK',url=app_url('fileapp'));counts['files']+=1
    elif 'category=android.intent.category.APP_GALLERY;' in intent:
     e.pop('intent');e.update(action='OPEN_LINK',url=app_url('galleryapp'));counts['gallery']+=1
  assert counts['phone']==9 and counts['files']==9 and counts['gallery']>0,counts
  # Only app actions and added configuration change; geometry, data and animation stay identical.
  a=list(walk(original['preset_root']));b=list(walk(p['preset_root']));assert len(a)==len(b)
  for old,new in zip(a,b):
   for key in set(old)|set(new):
    if key not in ('globals_list','internal_events','viewgroup_items'):assert old.get(key)==new.get(key),(key,old.get('internal_title'))
  p['preset_info'].update(title='Rhine UI · 小米 KLWP v0.13.51'+(' · 无重力视差' if suffix else ''),description='保留 v0.13.50 跟手斜条与终端交互；相册和文件管理默认为小米应用，支持全局配置。需 KLWP 与支持壁纸滚动的启动器。')
  dest=OUT/f'Rhine-UI-HyperOS{suffix}-v0.13.51.klwp'
  with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as target:
   for name in z.namelist():target.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else z.read(name))
  with zipfile.ZipFile(dest) as check:
   assert check.testzip() is None
   refs={ref for s in strings(p) for ref in re.findall(r'kfile://org.kustom.provider/([^"\s]+)',s)}
   assert refs.issubset(set(check.namelist())),refs-set(check.namelist())
   paths=[s for s in strings(p) if re.search(r'(?<![a-z])file://|[A-Z]:[\\/]|/sdcard/|/storage/emulated/',s)]
   assert not paths,paths[:3]
  reports.append(dict(file=dest.name,bytes=dest.stat().st_size,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),resource_count=len(refs),changed_actions=counts,zip_crc='pass',layout_animations_unchanged=True,hyperos_device_tested=False))
(OUT/'export-validation.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(reports,ensure_ascii=False,indent=2))
