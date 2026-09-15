import sys,time,json,re
from pathlib import Path
from opacity_navigation import navigate
from toolbar_native import tree,click,run,guard,SOURCE
out=Path('rhine_exact/output/opacity-repair-20260915')
statefile=out/'removed-background-scroll.json'
state=json.loads(statefile.read_text(encoding='utf-8')) if statefile.exists() else {'4':'removed and saved in single-row comparison'}
for index in map(int,sys.argv[1:]):
    if str(index) in state:continue
    r,n=navigate(index);click(n);run('shell','input','tap',755,2010);time.sleep(.3)
    for attempt in range(12):
        r=tree()
        title=next((n for n in r.iter('node') if n.get('resource-id','').endswith('/title') and n.get('text')=='背景滚动' and int(re.findall(r'\d+',n.get('bounds'))[3])-int(re.findall(r'\d+',n.get('bounds'))[1])>35),None)
        if title is not None:break
        guard();run('shell','input','swipe',650,2490,650,2070,100);time.sleep(.5)
    else:raise RuntimeError('Background animation not found: '+str(index))
    (out/f'root-{index}-before-remove.xml').write_text(__import__('xml.etree.ElementTree',fromlist=['tostring']).tostring(r,encoding='unicode'),encoding='utf-8')
    y=sum(int(x) for x in re.findall(r'\d+',title.get('bounds'))[1::2])/2
    checks=[n for n in r.iter('node') if n.get('resource-id','').endswith('/checkbox')]
    check=min(checks,key=lambda n:abs(sum(int(x) for x in re.findall(r'\d+',n.get('bounds'))[1::2])/2-y))
    click(check)
    click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_delete')))
    r=tree();assert not any(n.get('resource-id','').endswith('/title') and n.get('text')=='背景滚动' for n in r.iter('node'))
    click(next(n for n in r.iter('node') if n.get('resource-id','').endswith('/action_save')))
    state[str(index)]={'title':SOURCE[index]['internal_title'],'saved':True}
    statefile.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
    print('REMOVED AND SAVED',index,flush=True)
    run('shell','input','keyevent',4);time.sleep(.5)
print('Batch complete',flush=True)
