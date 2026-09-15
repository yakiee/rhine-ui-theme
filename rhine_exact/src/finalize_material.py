from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,zipfile,hashlib,shutil,numpy as np
out=Path('rhine_exact/output/material-v0.7');prev=Path('rhine_exact/output/details-v0.6')
def shot(folder,name):return Image.open(folder/'screens'/(name+'.png')).convert('RGB').crop((0,48,720,1552)).resize((360,800))
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',21)
im=Image.new('RGB',(1440,855),'#ECEFF1');d=ImageDraw.Draw(im)
for j,(title,old,new)in enumerate([('主菜单','01-dock-menu','01-menu'),('设置页','02-settings-center','02-appearance')]):
 x=j*720;d.text((x+10,10),title+'：v0.6 / v0.7',font=font,fill='#17191C');im.paste(shot(prev,old),(x,48));im.paste(shot(out,new),(x+360,48))
im.save(out/'material-before-after.jpg',quality=92)
refs=Path('rhine_exact/reference/arknights');refs.mkdir(exist_ok=True)
original=Path('C:/Users/yakieewang/Documents/xwechat_files/wxid_5nuko049yolm11_1dbf/temp/RWTemp/2026-09/1f1804fd0f464ba9bd6147f46979d091')
for src,dst in [('09f953e9462faac52593c19bd6d6f140.jpg','roster.jpg'),('7f6c471297eb439d32ec053bcbfbadfb.jpg','settings.jpg'),('13205c825584583f74f03494fdfc1046.jpg','home.jpg')]:
 if (original/src).exists():shutil.copyfile(original/src,refs/dst)
with zipfile.ZipFile(out/'Rhine-UI-material-v0.7.klwp')as z:
 assert z.testzip()is None;p=json.loads(z.read('preset.json'));names=set(z.namelist())
 def walk(n):
  yield n
  for c in n.get('viewgroup_items',[]):yield from walk(c)
 nodes=list(walk(p['preset_root']));links={v.removeprefix('kfile://org.kustom.provider/')for n in nodes for v in n.values()if isinstance(v,str)and v.startswith('kfile://org.kustom.provider/')};assert not links-names,links-names
 roots=p['preset_root']['viewgroup_items'];assert len(roots)==64 and p['preset_info']['version']==17
 check={'archive_valid':True,'embedded_assets_complete':True,'format':17,'roots':len(roots),'nodes':len(nodes),'animated_roots':sum(bool(n.get('internal_animations'))for n in roots),'sha256':hashlib.sha256((out/'Rhine-UI-material-v0.7.klwp').read_bytes()).hexdigest()}
(out/'package-check.json').write_text(json.dumps(check,indent=2),encoding='utf8')
print(check)
