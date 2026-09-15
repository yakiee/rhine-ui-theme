from pathlib import Path
import urllib.request,concurrent.futures,json,hashlib,zipfile,time,threading
BASE=Path(__file__).resolve().parent
packages=[p for p in json.loads((BASE/'downloads/packages.json').read_text()) if p['path']!='platform-tools']
progress={}; lock=threading.Lock()

def install(p):
    name=p['path'].replace(';','_');target=BASE/'downloads'/(name+'.zip');partial=target.with_suffix('.zip.part')
    prefix=target.stat().st_size if target.exists() else (partial.stat().st_size if partial.exists() else 0)
    size=p['size'];chunk_size=32*1024*1024
    progress[name]={'bytes':prefix,'total':size,'phase':'download'}
    ranges=[(start,min(start+chunk_size-1,size-1)) for start in range(prefix,size,chunk_size)]
    def fetch(part):
        start,end=part;file=BASE/'downloads'/(name+'.'+str(start)+'.chunk')
        expected=end-start+1
        if file.exists() and file.stat().st_size==expected:
            with lock:progress[name]['bytes']+=expected
            return file
        for retry in range(3):
            try:
                received=file.stat().st_size if file.exists() else 0
                current=start+received
                req=urllib.request.Request(p['url']+'?rhine_segment='+str(current)+'_'+str(end),headers={'User-Agent':'Mozilla/5.0','Range':'bytes='+str(current)+'-'+str(end),'Cache-Control':'no-cache'})
                with urllib.request.urlopen(req,timeout=45) as r,file.open('ab') as out:
                    if r.status!=206 or r.headers.get('Content-Range')!='bytes '+str(current)+'-'+str(end)+'/'+str(size):raise RuntimeError('Unexpected range response')
                    for block in iter(lambda:r.read(256*1024),b''):out.write(block)
                if file.stat().st_size!=expected:raise RuntimeError('Incomplete segment')
                with lock:progress[name]['bytes']+=expected
                return file
            except Exception as error:
                print(name+' segment '+str(start)+' retry '+str(retry)+': '+str(error),flush=True)
                if retry==2:raise
                time.sleep(1)
    if ranges:
        with concurrent.futures.ThreadPoolExecutor(6) as pool:
            pieces=list(pool.map(fetch,ranges))
        with partial.open('ab') as out:
            for file in pieces:
                with file.open('rb') as inp:
                    for block in iter(lambda:inp.read(8*1024*1024),b''):out.write(block)
        partial.replace(target)
    digest=hashlib.new(p['checksum_type'])
    with target.open('rb') as inp:
        for block in iter(lambda:inp.read(8*1024*1024),b''):digest.update(block)
    if target.stat().st_size!=size or digest.hexdigest()!=p['checksum']:raise RuntimeError(name+' checksum mismatch')
    progress[name]['phase']='extracting'
    destination=BASE/'sdk'
    if name.startswith('system-images'):destination=destination/'system-images/android-30/google_apis'
    destination.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(target) as archive:
        if any(not (destination/n.filename).resolve().is_relative_to(destination.resolve()) for n in archive.infolist()):raise RuntimeError('Unsafe archive path')
        archive.extractall(destination)
    progress[name]['phase']='installed';print(name+': installed and checksum verified',flush=True)

with concurrent.futures.ThreadPoolExecutor(2) as pool:
    jobs={pool.submit(install,p):p['path'].replace(';','_') for p in packages}
    tick=0
    while jobs:
        done,_=concurrent.futures.wait(jobs,timeout=5,return_when=concurrent.futures.FIRST_COMPLETED)
        for job in done:
            name=jobs.pop(job)
            try:job.result()
            except Exception as error:progress[name]['phase']='error';progress[name]['error']=str(error);print(name+': '+str(error),flush=True)
        (BASE/'logs/install-progress.json').write_text(json.dumps(progress,indent=2),encoding='utf-8')
        tick+=1
        if tick%6==0:print(json.dumps(progress),flush=True)
print(json.dumps(progress),flush=True)
