import sys
sys.path.insert(0,'rhine_exact/tools')
from loguru import logger
logger.remove()
from androguard.core.apk import APK
from androguard.core.dex import DEX
app=APK('android-preview/apps/KLWP-3.82-huawei.apk')
for raw in app.get_all_dex():
    dex=DEX(raw)
    for cls in dex.get_classes():
        name=cls.get_name()
        if name.startswith('Lorg/kustom/') and ('Anim' in name or 'anim' in name):
            print('CLASS',name)
            for method in cls.get_methods():
                if method.get_code():
                    instructions=list(method.get_instructions())
                    if any(ins.get_name().startswith('const-string') and any('"'+s+'"' in ins.get_output() for s in ['speed','duration','formula','amount']) for ins in instructions):
                        print('METHOD',method.get_name())
                        for ins in instructions:print(ins.get_name(),ins.get_output())
