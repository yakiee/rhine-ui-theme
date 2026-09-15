import sys
from pathlib import Path
sys.path.insert(0, 'rhine_exact/tools')
from loguru import logger
logger.remove()
from androguard.core.apk import APK
from androguard.core.dex import DEX
app = APK('android-preview/apps/TransparentWidget.apk')
for raw in app.get_all_dex():
    dex = DEX(raw)
    for cls in dex.get_classes():
        if cls.get_name().startswith('Lcom/easwareapps/transparentwidget/'):
            print('\nCLASS', cls.get_name())
            for method in cls.get_methods():
                print('METHOD', method.get_name())
                if method.get_code():
                    for ins in method.get_instructions():
                        print(ins.get_name(), ins.get_output())
