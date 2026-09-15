from pathlib import Path
import json,zipfile,re,collections,datetime,calendar
base=Path('rhine_theme');p=json.loads((base/'preset.json').read_text(encoding='utf-8'));glob=p['preset_root']['globals_list'];issues=[];stats=collections.Counter();forms=[];refs=[];events=[]
def walk(v,path='root',depth=0):
 if isinstance(v,dict):
  if 'internal_type' in v:stats[v['internal_type']]+=1
  if 'internal_animations' in v and path.count('viewgroup_items')>1:issues.append('Nested animation: '+path)
  events.extend(v.get('internal_events',[]))
  for k,x in v.items():walk(x,path+'.'+k,depth+1)
 elif isinstance(v,list):
  for i,x in enumerate(v):walk(x,path+'['+str(i)+']',depth+1)
 elif isinstance(v,str):
  refs.extend(re.findall(r'kfile://org\.kustom\.provider/((?:bitmaps|fonts)/[^"$,)\s]+)',v))
  if '$' in v:
   if v.count('$')%2:issues.append('Unclosed formula '+path)
   for expr in re.findall(r'\$([^$]*)\$',v):
    forms.append(expr);level=0;quote=False
    for ch in expr:
     if ch=='"':quote=not quote
     elif not quote:
      if ch=='(':level+=1
      elif ch==')':level-=1
      if level<0:issues.append('Unbalanced expression '+expr);break
    if level!=0 or quote:issues.append('Unbalanced expression '+expr)
    for key in re.findall(r'gv\(([a-zA-Z][a-zA-Z0-9_-]*)\)',expr):
     if key not in glob:issues.append('Missing global '+key)
walk(p)
package=base/'Rhine-UI-Study-v0.1.klwp'
with zipfile.ZipFile(package) as z:
 if z.testzip():issues.append('Corrupt zip')
 for ref in set(refs):
  if ref not in z.namelist():issues.append('Missing resource '+ref)
 if json.loads(z.read('preset.json'))!=p:issues.append('Stale package JSON')
for ev in events:
 if ev.get('action')=='SWITCH_GLOBAL' and ev.get('switch') not in glob:issues.append('Unknown target global '+str(ev))
roots=len(p['preset_root']['viewgroup_items'])
if roots>64:issues.append('Root layer limit exceeded')
pages=set(int(e['switch_text']) for e in events if e.get('switch')=='page' and e.get('switch_text','').isdigit())
if pages!=set(range(8)):issues.append('Unreachable page')
# Independent date arithmetic checks against Python month calendars, including leap years.
checked=0
for year in [2024,2026,2027,2028,2100]:
 for month in range(1,13):
  first=datetime.date(year,month,1);offset=first.isoweekday()%7
  actual=[first+datetime.timedelta(days=i-offset) for i in range(42)]
  current=[d.day for d in actual if d.month==month and d.year==year]
  if current!=list(range(1,calendar.monthrange(year,month)[1]+1)):issues.append('Calendar arithmetic failure')
  checked+=1
report={'status':'PASS' if not issues else 'FAIL','validation_scope':'ZIP/JSON/resource/global/formula-delimiter checks and independent date arithmetic; NOT Android import or Kustom formula execution','root_layers':roots,'node_counts':stats,'formula_count':len(forms),'touch_action_count':len(events),'unique_resources':len(set(refs)),'reachable_page_ids':sorted(pages),'calendar_month_cases':checked,'unverified':['KLWP import on target device','Kustom formula engine results','launcher touch handling','media/calendar/weather permissions','payment links','animation timing and reverse transitions','screen cutout/navigation inset fit'],'issues':issues}
(base/'docs'/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
