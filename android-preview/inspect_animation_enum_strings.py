import zipfile,struct
from pathlib import Path
with zipfile.ZipFile('android-preview/apps/KLWP-3.82-huawei.apk') as archive:
    found=set()
    for name in archive.namelist():
        if not name.endswith('.dex'):continue
        data=archive.read(name)
        size,offset=struct.unpack_from('<II',data,56)
        for index in range(size):
            position=struct.unpack_from('<I',data,offset+4*index)[0]
            while data[position]&128:position+=1
            position+=1
            end=data.find(b'\0',position)
            text=data[position:end].decode('utf-8',errors='replace')
            if ('FADE' in text or 'AnimationAction' in text or 'ANIMATION' in text) and len(text)<180:
                found.add(text)
print('\n'.join(sorted(found)))
