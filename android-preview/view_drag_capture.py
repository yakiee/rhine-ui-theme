from PIL import Image
import io,base64
im=Image.open('android-preview/logs/launcher-drag.png');im.thumbnail((480,1100));b=io.BytesIO();im.convert('RGB').save(b,format='JPEG',quality=65);print('IMAGE:'+base64.b64encode(b.getvalue()).decode())
