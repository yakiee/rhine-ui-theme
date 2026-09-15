from PIL import Image
import io,base64
im=Image.open('rhine_exact/output/dock-phone-fix-20260914/second-page-only/terminal-after-service-restart.png').convert('RGB');im.thumbnail((400,900));b=io.BytesIO();im.save(b,format='JPEG',quality=55);print(base64.b64encode(b.getvalue()).decode())

