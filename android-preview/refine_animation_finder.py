from pathlib import Path
p=Path('android-preview/add_follow_scroll_animation.py')
s=p.read_text(encoding='utf-8')
start=s.index('def find_module(title):')
end=s.index('\nfor index in map',start)
s=s[:start]+'''def find_module(title):
    root = open_root()
    ordering = {node['internal_title']: index for index,node in enumerate(source)}
    target_index = ordering[title]
    for attempt in range(40):
        nodes = [n for n in root.iter('node') if n.get('resource-id','').endswith(':id/module_title')]
        match = next((n for n in nodes if n.get('text')==title and int(re.findall(r'\\d+',n.get('bounds'))[3])-int(re.findall(r'\\d+',n.get('bounds'))[1])>30),None)
        if match is not None:
            click(match)
            return
        visible_indices = [ordering[n.get('text')] for n in nodes if n.get('text') in ordering]
        assert visible_indices, 'No known root modules in current list'
        first = min(visible_indices)
        distance = target_index-first
        step = 300 if abs(distance)>6 else 115
        if distance<0:
            run('shell','input','swipe','650','2190','650',str(2190+step),'850')
        else:
            run('shell','input','swipe','650','2470','650',str(2470-step),'850')
        time.sleep(1)
        root,raw = tree()
    raise RuntimeError('Target root group not found: '+title)
''' + s[end:]
p.write_text(s,encoding='utf-8')
print('Root navigation now checks visible module indices and can correct overshoot')
