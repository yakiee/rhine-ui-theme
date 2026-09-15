from PIL import Image
import io,base64
im=Image.open('rhine_exact/output/dock-phone-fix-20260914/second-page-only/live-diagnostic.png').convert('RGB').crop((300,270,900,530));im.thumbnail((600,260));b=io.BytesIO();im.save(b,format='JPEG',quality=55);print('IMAGE:'+base64.b64encode(b.getvalue()).decode())

