import re,time,json
from toolbar_native import SOURCE,tree,click,run,guard
order=[i for i in range(len(SOURCE)) if i not in [3,50,51]]+[50,64,51,3]
names={n['internal_title']:i for i,n in enumerate(SOURCE)}
def navigate(index):
    target=SOURCE[index]['internal_title']
    for attempt in range(30):
        r=tree()
        nodes=[n for n in r.iter('node') if n.get('resource-id','').endswith('/module_title')]
        found=next((n for n in nodes if n.get('text')==target and int(re.findall(r'\d+',n.get('bounds'))[3])-int(re.findall(r'\d+',n.get('bounds'))[1])>35),None)
        if found is not None:return r,found
        indices=[order.index(names[n.get('text')]) for n in nodes if n.get('text') in names]
        assert indices,'Not root module list'
        delta=order.index(index)-min(indices)
        guard()
        if abs(delta)>9:
            run('shell','input','swipe',650,2480 if delta>0 else 2080,650,2080 if delta>0 else 2480,70)
        else:
            step=min(350,max(100,abs(delta)*119))
            run('shell','input','swipe',650,2480 if delta>0 else 2130,650,2480-step if delta>0 else 2130+step,450)
        time.sleep(.6)
    raise RuntimeError('Module not found')
if __name__=='__main__':
    import sys
    r,n=navigate(int(sys.argv[1]));click(n)
    run('shell','input','tap',755,2010)
    print(json.dumps([(n.get('text'),n.get('resource-id'),n.get('bounds')) for n in tree().iter('node') if n.get('text') or n.get('resource-id','').endswith('/checkbox')],ensure_ascii=True))
