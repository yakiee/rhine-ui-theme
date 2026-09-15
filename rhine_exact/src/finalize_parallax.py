from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,zipfile,hashlib,numpy as np
from static_helpers import walk
OUT=Path('rhine_exact/output/parallax-v0.8');SC=OUT/'screens'
def mae(a,b):
 first=np.array(Image.open(SC/(a+'.png')).convert('RGB'),dtype=float)[70:1500]
 second=np.array(Image.open(SC/(b+'.png')).convert('RGB'),dtype=float)[70:1500]
 return round(float(np.mean(abs(first-second))),4)
with zipfile.ZipFile(OUT/'Rhine-UI-parallax-v0.8.klwp')as z:
 assert z.testzip()is None;p=json.loads(z.read('preset.json'));nodes=list(walk(p['preset_root']));names=set(z.namelist());links={v.removeprefix('kfile://org.kustom.provider/')for n in nodes for v in n.values()if isinstance(v,str)and v.startswith('kfile://org.kustom.provider/')};assert links<=names
roots=p['preset_root']['viewgroup_items'];old=json.loads(Path('rhine_exact/output/material-v0.7/preset.json').read_text(encoding='utf8'))['preset_root']['viewgroup_items']
assert len(roots)==64
assert all([a for a in r.get('internal_animations',[])if a.get('type')!='GYRO']==o.get('internal_animations',[])for r,o in zip(roots,old))
check={'archive_valid':True,'assets_complete':True,'original_page_animations_preserved':True,'roots':64,'sensor_layers':sum(any(a['type']=='GYRO'for a in r.get('internal_animations',[]))for r in roots),'menu_left_right_mae':mae('menu-left','menu-right'),'stationary_left_right_mae':mae('stationary-left','stationary-right'),'sha256':hashlib.sha256((OUT/'Rhine-UI-parallax-v0.8.klwp').read_bytes()).hexdigest()}
assert check['stationary_left_right_mae']<0.1,check
(OUT/'validation.json').write_text(json.dumps(check,indent=2),encoding='utf8');print(check)
im=Image.new('RGB',(1440,835),'#ECEFF1');d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18)
for i,(name,title)in enumerate([('menu-left','左倾'),('menu-right','右倾'),('stationary-left','静止版 · 左倾'),('stationary-right','静止版 · 右倾')]):
 im.paste(Image.open(SC/(name+'.png')).convert('RGB').resize((360,800)),(i*360,35));d.text((i*360+12,8),title,font=font,fill='#17191C')
im.save(OUT/'parallax-review.jpg',quality=90)
