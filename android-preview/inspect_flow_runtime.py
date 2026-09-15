import sys,zipfile,re,json
from pathlib import Path
sys.path.insert(0,'rhine_exact/tools')
from loguru import logger
logger.remove()
from androguard.core.dex import DEX
rows=[]
with zipfile.ZipFile('android-preview/apps/KLWP-3.82-huawei.apk') as archive:
    for name in archive.namelist():
        if not re.fullmatch(r'classes\d*\.dex',name):continue
        dex=DEX(archive.read(name))
        for cls in dex.get_classes():
            if 'flow' not in cls.get_name().lower():continue
            for method in cls.get_methods():
                code=[ins.get_name()+' '+ins.get_output() for ins in method.get_instructions()]
                if any(any(term in line for term in ['ON_CHANGE','T_FORMULA','store_mode']) for line in code):
                    rows.append(cls.get_name()+'->'+method.get_name()+method.get_descriptor()+'\n'+'\n'.join(code))
Path('rhine_exact/output/open-dock-swipe-20260915/flow-runtime.txt').write_text('\n\n'.join(rows),encoding='utf-8')
print('\n'.join(row.splitlines()[0] for row in rows))
