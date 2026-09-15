from pathlib import Path
import urllib.request,urllib.parse,zipfile,hashlib,json,concurrent.futures,time,os
BASE=Path(__file__).resolve().parent
items=json.loads((BASE/'downloads/packages.json').read_text())
klwp=json.loads((BASE/'downloads/klwp.json').read_text())
items.append({'path':'klwp','url':klwp['url']})
state={}

def download(item):
    name=item['path'].replace(';','_')
    target=BASE/('apps/KLWP-aosp.apk' if name=='klwp' else 'downloads/'+name+'.zip')
    expected=item.get('size')
    if not target.exists() or (expected and target.stat().st_size!=expected):
        partial=target.with_suffix(target.suffix+'.part')
        request=urllib.request.Request(item['url'],headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(request,timeout=45) as response,partial.open('wb') as output:
            total=int(response.headers.get('Content-Length') or expected or 0); count=0;last=0
            while chunk:=response.read(1024*1024):
                output.write(chunk);count+=len(chunk)
                state[name]={'bytes':count,'total':total,'phase':'download'}
                if total and count/total>=last+.2:
                    last=count/total;print(name+': '+str(round(100*last))+'%',flush=True)
        partial.replace(target)
    if expected and target.stat().st_size!=expected:raise RuntimeError(name+' size mismatch')
    if item.get('checksum'):
        digest=hashlib.new(item['checksum_type'])
        with target.open('rb') as stream:
            for block in iter(lambda:stream.read(8*1024*1024),b''):digest.update(block)
        if digest.hexdigest()!=item['checksum']:raise RuntimeError(name+' checksum mismatch')
    if not zipfile.is_zipfile(target):raise RuntimeError(name+' is not an APK/ZIP file')
    if name!='klwp':
        destination=BASE/'sdk'
        if name.startswith('system-images'):destination=destination/'system-images/android-30/google_apis'
        destination.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(target) as archive:
            for entry in archive.infolist():
                resolved=(destination/entry.filename).resolve()
                if not resolved.is_relative_to(destination.resolve()):raise RuntimeError('Unsafe archive path')
            archive.extractall(destination)
    state[name]={'phase':'installed' if name!='klwp' else 'downloaded','file':str(target),'bytes':target.stat().st_size}
    print(name+': complete',flush=True)
    return state[name]

with concurrent.futures.ThreadPoolExecutor(4) as pool:
    jobs={pool.submit(download,item):item['path'] for item in items}
    while jobs:
        done,_=concurrent.futures.wait(jobs,timeout=5,return_when=concurrent.futures.FIRST_COMPLETED)
        for future in done:
            name=jobs.pop(future)
            try:future.result()
            except Exception as error:
                state[name.replace(';','_')]={'phase':'error','message':str(error)};print(name+': '+str(error),flush=True)
        (BASE/'logs/install-progress.json').write_text(json.dumps(state,indent=2),encoding='utf-8')
print(json.dumps(state,ensure_ascii=True),flush=True)
