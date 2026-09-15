import json,time,sys
from toolbar_native import OUT,tree,click,select_root,guard,run

for index in map(int,sys.argv[1:]):
    marker=OUT/f'root-{index}-applied.json'
    assert not marker.exists(), 'Already applied; inspect before repeating'
    path=OUT/f'root-{index}-after.clip.txt'
    assert path.exists() and (OUT/f'root-{index}-before.clip.txt').exists()
    select_root(index)
    root=tree()
    click(next(n for n in root.iter('node') if n.get('resource-id','').endswith('/action_delete')))
    root=tree()
    positive=next((n for n in root.iter('node') if n.get('resource-id')=='android:id/button1'),None)
    if positive:click(positive)
    root=tree()
    assert any(n.get('text')=='根目录' for n in root.iter('node'))
    run('push',str(path.resolve()),'/data/local/tmp/rhine-editor-input.txt')
    run('shell','CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard KUSTOM_MODULES /data/local/tmp/rhine-editor-input.txt')
    time.sleep(.3)
    root=tree()
    click(next(n for n in root.iter('node') if n.get('resource-id','').endswith('/action_paste')))
    marker.write_text(json.dumps({'root':index,'action':'replaced backed-up native group; appended to root','saved':False}),encoding='utf-8')
    print('REPLACED',index,flush=True)
