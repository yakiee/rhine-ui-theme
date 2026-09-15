import sys
sys.path.insert(0,'rhine_exact/tools')
from loguru import logger
logger.remove()
from androguard.core.apk import APK
app=APK('android-preview/apps/TransparentWidget.apk')
print(app.get_package(),app.get_androidversion_name(),app.get_permissions())
