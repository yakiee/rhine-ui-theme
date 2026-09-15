import sys,zipfile,re
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
            if not any(s in cls.get_name().lower() for s in ['global','touch','event']):continue
            for method in cls.get_methods():
                code=[ins.get_name()+' '+ins.get_output() for ins in method.get_instructions()]
                strings=[s for s in code if s.startswith('const-string')]
                if any(any(term in s.lower() for term in ['switch','autooff','auto_off','on_formula','off_formula']) for s in strings):
                    rows.append(cls.get_name()+'->'+method.get_name()+method.get_descriptor()+'\n'+'\n'.join(code))
Path('rhine_exact/output/open-dock-swipe-20260915/native-switch.txt').write_text('\n\n'.join(rows),encoding='utf-8')
print('\n\n'.join(row.splitlines()[0]+'\n'+'\n'.join(s for s in row.splitlines() if s.startswith('const-string')) for row in rows))
