"""Independently authored KLWP layout; one scene specification drives package and previews."""
from pathlib import Path
import json, math, zipfile, shutil, calendar, datetime, re
from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE=Path(__file__).resolve().parents[1]
ASSETS=BASE/'assets'
OUT=BASE/'previews'
W,H=720,1600
LAYERS=[]
FONT='kfile://org.kustom.provider/fonts/Rajdhani-SemiBold.ttf'
FONTPATH=ASSETS/'Rajdhani-SemiBold.ttf'
CN=Path('C:/Windows/Fonts/msyh.ttc')
COLORS={'ink':('#FF17191C','#FFF0F0F2'),'muted':('#FF72757C','#FF9FA4AC'),'line':('#FFB9BDC4','#FF474B52'),'card':('#E8FFFFFF','#F022252C'),'bg':('#F7F4F3F6','#F814161B'),'accent':('#FF527AFF','#FF527AFF'),'green':('#FFAADE00','#FFB4EF00')}
GLOBALS={}
def glob(key,value,title=None,kind='TEXT',desc=''):
    GLOBALS[key]={'index':len(GLOBALS),'type':kind,'title':title or key,'value':value,'description':desc,'global_formula':''}
for key,val,title in [('page','0','页面 0首页 1控制 2应用 3天气 4音乐 5日历 6外观 7功能'),('mode','0','深色模式 0浅色 1深色 2日出日落'),('style','1','光条 0金色 1蓝色 2壁纸取色'),('palette','0','取色 0主导 1温和 2活力'),('dots','1','光点'),('load','1','加载动画'),('dock','1','Dock 0关闭 1日期 2图标'),('avoid','0','避开启动器Dock'),('blank','1','点击空白返回'),('gyro','0','重力视差'),('detail','0','预报详情'),('forecast','0','预报起始日'),('selected','0','选中预报日'),('start','0','切页时间戳'),('date','0','选中日期 时间戳'),('event','0','日程序号'),('month','0','月份偏移'),('so2','—','SO₂ 外部数据入口'),('lyrics','','歌词 外部同步文本'),('alert','','天气预警 外部数据入口')]:glob(key,val,title)
glob('wall','kfile://org.kustom.provider/bitmaps/wallpaper.png','主页壁纸','BITMAP')
glob('cover','kfile://org.kustom.provider/bitmaps/wallpaper.png','默认音乐封面','BITMAP')
glob('scene','kfile://org.kustom.provider/bitmaps/weather-grid.png','预报卡背景','BITMAP')
glob('dark','$if(gv(mode)=1,1,gv(mode)=2,1-ai(isday),0)$','计算：深色状态')
glob('loading','$gv(load)=1 & gv(page)>=3 & gv(page)<=5 & df(S)-gv(start)<2$','计算：加载状态')
glob('accent','$if(gv(style)=0,#FFFFBB27,gv(style)=1,#FF527AFF,bp(if(gv(palette)=0,dominant,gv(palette)=1,muted,vibrant),gv(wall),#FF527AFF))$','计算：强调色')
glob('base','$dp("1d0h0m0s"+if(gv(month)>=0,"a","r")+mu(abs,gv(month))+"M")$','计算：月首')
glob('daydate','$if(gv(date)=0,dp(),gv(date))$','计算：所选日期')
# User-visible links are editable because app schemes differ among Android ROMs.
links={'search':('https://www.baidu.com','搜索链接'),'alipay':('alipays://platformapi/startapp','支付宝入口'),'apay':('alipays://platformapi/startapp?appId=20000056','支付宝付款码链接'),'ascan':('alipays://platformapi/startapp?appId=10000007','支付宝扫一扫链接'),'wechat':('weixin://','微信入口'),'wxpay':('weixin://','微信付款码：默认打开微信，可替换快捷方式'),'wxscan':('weixin://','微信扫一扫：默认打开微信，可替换快捷方式')}
for k,(v,t) in links.items():glob(k,v,t)
apps=[('微信','W','weixin://'),('支付宝','A','alipays://platformapi/startapp'),('浏览器','B','https://www.baidu.com'),('相机','C','intent:#Intent;action=android.media.action.STILL_IMAGE_CAMERA;end'),('日历','D','content://com.android.calendar/time/$df(S)*1000$'),('音乐','M',''),('设置','S','intent:#Intent;action=android.settings.SETTINGS;end'),('电话','P','tel:')]
for i,(name,letter,url) in enumerate(apps):glob('app'+str(i),url,name+' 启动链接')

def event(key,val):return {'type':'SINGLE_TAP','action':'SWITCH_GLOBAL','switch':key,'switch_text':str(val)}
def nav(page):return [event('detail',0),event('start','$df(S)$'),event('page',page)]
def url_event(url):return [{'type':'SINGLE_TAP','action':'OPEN_LINK','url':url}]
def music(action=None):return [{'type':'SINGLE_TAP','action':'MUSIC',**({'music_action':action} if action else {})}]
def launch_intent(intent):return [{'type':'SINGLE_TAP','action':'LAUNCH_APP','intent':intent}]
EDITOR=launch_intent('intent:#Intent;action=android.intent.action.MAIN;component=org.kustom.wallpaper/org.kustom.lib.editor.WpAdvancedEditorActivity;end')

def layer(name,condition,pages,delay=0,height=H,cy=800,rotate=False):
    v={'name':name,'condition':condition,'pages':pages,'delay':delay,'height':height,'cy':cy,'rotate':rotate,'nodes':[]}
    LAYERS.append(v);return v

def add(g,kind,x,y,w,h,color='ink',**kw):
    n={'kind':kind,'x':x,'y':y,'w':w,'h':h,'color':color,**kw};g['nodes'].append(n);return n

def rect(g,x,y,w,h,color='ink',**kw):return add(g,'rect',x,y,w,h,color,**kw)
def circle(g,x,y,d,color='ink',**kw):return add(g,'circle',x,y,d,d,color,**kw)
def text(g,label,x,y,w,h,size=24,color='ink',**kw):return add(g,'text',x,y,w,h,color,text=label,size=size,**kw)
def pic(g,path,x,y,w,h,**kw):return add(g,'image',x,y,w,h,path=path,**kw)
def line(g,x1,y1,x2,y2,color='line',width=1,**kw):return add(g,'line',x1,y1,x2-x1,y2-y1,color,stroke=width,**kw)
def button(g,label,x,y,w,h,ev,color='card',fg='ink',size=24,**kw):
    rect(g,x,y,w,h,color,events=ev,**kw);text(g,label,x+8,y,w-16,h,size,fg,align='CENTER',events=ev)
def themed(k):
    if k=='accent':return '$gv(accent)$'
    if k in COLORS:return '$if(gv(dark),'+COLORS[k][1]+','+COLORS[k][0]+')$'
    return k

def make_assets():
    # Original vector-like UI art, not edits of reference screenshots.
    im=Image.new('RGBA',(720,1600));d=ImageDraw.Draw(im)
    for yy in range(0,1600,8):
      for xx in range(0,720,8):d.ellipse((xx,yy,xx+1,yy+1),fill=(100,105,120,38))
    im.save(ASSETS/'microdots.png')
    im=Image.new('RGB',(600,360),(42,50,67));d=ImageDraw.Draw(im)
    for yy in range(-200,600,35):d.line((0,yy,600,yy+300),fill=(68,79,96),width=1)
    for xx in range(-600,1000,35):d.line((xx,0,xx+340,360),fill=(68,79,96),width=1)
    for i in range(33):
      xx=(i*83)%600;yy=(i*47)%330;hh=15+(i*17)%75
      d.polygon([(xx,yy),(xx+20,yy-10),(xx+45,yy+3),(xx+25,yy+15)],fill=(104,112,126))
      d.polygon([(xx,yy),(xx+25,yy+15),(xx+25,yy+hh),(xx,yy+hh-15)],fill=(55,62,76))
    im.save(ASSETS/'weather-grid.png')
make_assets()

home=layer('01 首页时钟与框线','gv(page)<=2',[0,1,2])
rect(home,0,0,720,350,'#1A04091D')
line(home,48,280,690,280,'#DDFFFFFF',2)
line(home,290,70,290,320,'#E6FFFFFF',2)
line(home,300,320,695,320,'#99FFFFFF',1)
circle(home,46,90,175,'#88131B36',events=nav(1));circle(home,46,90,175,'accent',stroke=3,events=nav(1))
text(home,'$df(HH:mm)$',53,127,160,70,55,'#FFFFFFFF',sample='18:31',align='CENTER',latin=True,events=nav(1))
text(home,'$df(A)$',73,195,120,32,22,'#FFFFFFFF',sample='PM',align='CENTER',latin=True)
text(home,'RHINE UI / KLWP',43,285,242,33,23,'#FFFFFFFF',latin=True)
text(home,'PERSONAL TERMINAL',310,290,310,27,16,'#EEFFFFFF',latin=True)

hubdim=layer('02 控制中心遮罩','gv(page)=1',[1])
rect(hubdim,0,0,W,H,'#77050611',events=nav(0))
metrics=layer('03 控制中心设备状态','gv(page)=1',[1],.2)
text(metrics,'$df(yyyy/MM/dd HH:mm)$',275,406,390,30,19,'#FFFFFFFF',sample='2026/09/08 18:31',align='RIGHT',latin=True)
text(metrics,'CPU $if(rm(cused)>=0,rm(cused),"—")$%   RAM $if(rm(mtot)>0,mu(round,100*rm(mused)/rm(mtot)),"—")$%   SD $if(rm(fstot,int)>0,mu(round,100*rm(fsused,int)/rm(fstot,int)),"—")$%',196,442,480,32,18,'#FFFFFFFF',sample='CPU 43%     RAM 49%     SD 78%',latin=True)
terminal=layer('04 终端卡片','gv(page)=1',[1],.5)
rect(terminal,225,489,441,170,'#F1FFFFFF')
text(terminal,'$bi(temp)$',245,497,145,106,82,'#FF12151B',sample='37',latin=True,align='CENTER')
rect(terminal,245,604,145,34,'#FF1D2029');text(terminal,'电池 / °C',245,604,145,34,20,'#FFFFFFFF',align='CENTER')
text(terminal,'终端',410,508,190,67,53,'#FF12151B')
text(terminal,'Android $si(aver)$',412,584,210,32,23,'#FF22262E',sample='Android 16',latin=True)
rect(terminal,225,654,441,5,'accent')
row=layer('05 搜索与主题设置','gv(page)=1',[1],.9)
button(row,'搜索',192,677,214,102,url_event('$gv(search)$'),color='#F0FFFFFF',fg='#FF15171C',size=36)
button(row,'设置',420,677,246,102,nav(6),color='#F0FFFFFF',fg='#FF15171C',size=36)
text(row,'主题管理',483,746,124,23,16,'#FF5B5E67',align='CENTER',events=nav(6))
pay=layer('06 支付宝快捷栏','gv(page)=1',[1],1.2)
rect(pay,238,801,428,108,'#FF11AEE6')
text(pay,'快捷支付',380,804,266,29,18,'#FFFFFFFF',align='CENTER')
for lbl,xx,ww,key in [('支付宝',240,121,'alipay'),('付款码',367,140,'apay'),('扫一扫',515,146,'ascan')]:text(pay,lbl,xx,837,ww,66,27,'#FFFFFFFF',align='CENTER',events=url_event('$gv('+key+')$'))
wx=layer('07 微信快捷栏','gv(page)=1',[1],1.5)
for lbl,xx,ww,key in [('付款码',198,151,'wxpay'),('扫一扫',362,165,'wxscan'),('微信',542,124,'wechat')]:
    button(wx,lbl,xx,930,ww,111,url_event('$gv('+key+')$'),color='#F0FFFFFF' if key!='wechat' else '#FF14171D',fg='#FF17191C' if key!='wechat' else '#FFFFFFFF',size=27)
text(wx,'应用内打开',202,1039,323,24,15,'#DFFFFFFF')

app=layer('08 应用页','gv(page)=2',[2],.3)
rect(app,0,340,720,970,'#33000519')
text(app,'APPLICATIONS',55,392,485,47,38,'#FFFFFFFF',latin=True)
for i,(name,letter,url) in enumerate(apps):
    col=i%2;row=i//2;xx=210+col*198;yy=512+row*176
    ev=music('OPEN_APP') if i==5 else url_event('$gv(app'+str(i)+')$')
    if i in [3,6]:ev=launch_intent(url)
    circle(app,xx,yy,104,'#EAF5F7FC',events=ev)
    text(app,letter,xx,yy,104,100,54,'#FF171D2D',align='CENTER',latin=True,events=ev)
    text(app,name,xx-14,yy+110,132,35,23,'#FFFFFFFF',align='CENTER',events=ev)

sidebar=layer('09 菱形功能侧栏','gv(page)<=2',[0,1,2],.2)
rect(sidebar,581,1025,89,269,'#F00C101A')
tri=add(sidebar,'triangle',581,1283,89,46,'#F00C101A',rotate=180)
for i,(lbl,page) in enumerate([('W',3),('M',4),('C',5),('⊞',2)]):
    text(sidebar,lbl,586,1035+i*62,79,62,30,'#FFFFFFFF',align='CENTER',latin=i<3,events=nav(page))
rect(sidebar,589,1296,70,6,'accent')

# Dock is a separate root group so the complete date/battery assembly can rotate.
dock=layer('10 斜向Dock','gv(page)<=2 & gv(dock)!=0',[0,1,2],height=228,cy=1403,rotate=True)
rect(dock,0,0,720,228,'#F70B0F1A',events=nav('$if(gv(page)=1,0,1)$'))
rect(dock,0,0,720,8,'accent')
for xx in range(0,720,20):
    circle(dock,xx,14,4,'accent',show='gv(dots)=1')
circle(dock,34,37,152,'#FF131B30');circle(dock,34,37,152,'accent',stroke=4)
text(dock,'BAT',66,52,88,29,19,'#FFFFFFFF',latin=True,align='CENTER')
text(dock,'$bi(level)$',40,78,139,91,76,'#FFFFFFFF',sample='45',latin=True,align='CENTER')
text(dock,'$tc(up,df(EEEE))$',214,59,460,89,61,'#FFFFFFFF',sample='TUESDAY',latin=True,show='gv(dock)=1')
text(dock,'$df(yyyy.M.d)$',313,145,292,43,28,'#FFFFFFFF',sample='2026.9.8',latin=True,align='CENTER',show='gv(dock)=1')
for lbl,xx,pg in [('WEATHER',212,3),('MUSIC',367,4),('CALENDAR',498,5)]:
    text(dock,lbl,xx,87,157,78,25,'#FFFFFFFF',latin=True,align='CENTER',show='gv(dock)=2',events=nav(pg))

bg=layer('11 功能页底板','gv(page)>=3',list(range(3,8)))
rect(bg,0,0,720,1600,'bg')
pic(bg,'microdots.png',0,0,720,1600)
# Touch applies to genuine empty areas, not the entire foreground group.
for yy,hh in [(690,48),(1060,74),(1460,100)]:
    rect(bg,35,yy,650,hh,'#00FFFFFF',show='gv(blank)=1 & gv(page)<=5',events=nav(0))
header=layer('12 返回与功能标签','gv(page)>=3 & gv(loading)=0',list(range(3,8)),.1)
text(header,'←',54,87,125,77,54,'ink',events=nav(0))
for lbl,xx,pg in [('天气',414,3),('音乐',496,4),('日历',579,5)]:
    text(header,lbl,xx,104,80,47,21,'ink',align='CENTER',events=nav(pg),show='gv(page)<=5')
    rect(header,xx+18,159,44,2,'ink',show='gv(page)='+str(pg))
text(header,'设置 / SETTINGS',315,105,348,48,26,'ink',align='RIGHT',show='gv(page)>=6')

weather=layer('13 多日天气曲线','gv(page)=3 & gv(loading)=0',[3],.5)
pic(weather,'weather-grid.png',54,205,612,397,bind='scene')
rect(weather,54,205,612,397,'#44101625')
text(weather,'FORECAST / $li(loc)$',70,219,470,30,20,'#FFFFFFFF',sample='FORECAST / LOCAL',latin=True)
# Each point's vertical position and each connecting segment are live formulas.
ys=[390,358,372,321,341]
for i in range(5):
    xx=87+i*129
    day='mu(min,gv(forecast)+'+str(i)+',mu(max,wi(pdays)-1,0))'
    fy='(425-mu(min,45,mu(max,-10,wf(max,'+day+')))*2)'
    if i<4:
      nxt='mu(min,gv(forecast)+'+str(i+1)+',mu(max,wi(pdays)-1,0))'
      ny='(425-mu(min,45,mu(max,-10,wf(max,'+nxt+')))*2)'
      line(weather,xx+20,ys[i]+20,xx+149,ys[i+1]+20,'#FFF1F4FF',2,live_line=(str(xx+20),fy+'+20',str(xx+149),ny+'+20'))
    circle(weather,xx,ys[i],41,'accent',yformula='$'+fy+'$',events=[event('selected','$'+day+'$'),event('detail',1)])
    text(weather,'$wf(max,'+day+')$°',xx-18,480,86,42,28,'#FFFFFFFF',sample=str([28,31,29,33,32][i])+'°',latin=True,align='CENTER',events=[event('selected','$'+day+'$'),event('detail',1)])
    text(weather,'$df(M/d,a+'+day+'+d)$',xx-22,534,92,29,19,'#FFFFFFFF',sample=['9/8','9/9','9/10','9/11','9/12'][i],latin=True,align='CENTER')
text(weather,'‹',65,555,60,48,44,'#FFFFFFFF',align='CENTER',events=[event('forecast','$mu(max,0,gv(forecast)-1)$')])
text(weather,'›',599,555,60,48,44,'#FFFFFFFF',align='CENTER',events=[event('forecast','$mu(min,mu(max,wi(pdays)-5,0),gv(forecast)+1)$')])
for i in range(5):
    rect(weather,306+i*21,632,10,10,'ink',stroke=1)
text(weather,'点击温度节点展开详情',205,661,310,28,17,'muted',align='CENTER')

aq=layer('14 空气质量','gv(page)=3 & gv(loading)=0',[3],1.1)
rect(aq,279,730,163,33,'ink')
text(aq,'空气指数 $if(aq(level)=NA,"—",aq(index))$',280,730,161,33,17,'card',sample='空气指数 25',align='CENTER')
for x1,y1,x2,y2 in [(60,836,245,836),(245,836,319,910),(60,1034,245,1034),(245,1034,320,960),(660,845,469,845),(469,845,401,910),(660,1034,470,1034),(470,1034,403,960)]:line(aq,x1,y1,x2,y2,'line',1)
circle(aq,302,878,117,'#FF202329');circle(aq,338,900,46,'#FF202329')
text(aq,'↗',326,895,65,61,40,'#FF202329',align='CENTER')
for label,form,xx,yy,sample in [('NO2','$if(aq(level)=NA,"—",aq(no2))$',61,794,'9'),('SO2','$gv(so2)$',485,803,'—'),('PM2.5','$if(aq(level)=NA,"—",aq(pm25))$',61,990,'16'),('PM10','$if(aq(level)=NA,"—",aq(pm10))$',483,990,'23')]:
    text(aq,label,xx,yy,96,37,24,'ink');text(aq,form,xx+98,yy,68,37,25,'ink',sample=sample,latin=True)
text(aq,'ug/m3 · 数据不可用时显示 —',154,1072,412,25,16,'muted',align='CENTER')

bottom=layer('15 当天天气与提示','gv(page)=3 & gv(loading)=0',[3],1.5)
rect(bottom,54,1215,612,54,'#FF202329')
text(bottom,'△',64,1219,54,42,28,'green',align='CENTER')
text(bottom,'$if(gv(alert)!="",gv(alert),"暂无已接入的预警信息")$',130,1220,523,40,22,'#FFFFFFFF',sample='暂无已接入的预警信息')
text(bottom,'$wi(temp)$',55,1283,187,122,96,'ink',sample='28',latin=True)
text(bottom,'°$wi(tempu)$',225,1331,83,48,35,'muted',sample='°C',latin=True)
text(bottom,'$wf(max,0)$ / $wf(min,0)$°  $wi(cond)$',331,1296,323,34,22,'ink',sample='31 / 26°  晴')
text(bottom,'体感 $wi(flik)$°   湿度 $wi(hum)$%',331,1342,325,31,19,'muted',sample='体感 30°   湿度 65%')
text(bottom,'风速 $wi(wspeed)$ $li(spdu)$',331,1386,325,31,19,'muted',sample='风速 8 km/h')
line(bottom,54,1440,666,1440,'line')
text(bottom,'$wi(provider)$ · $df(HH:mm,wi(updated))$',54,1453,500,24,16,'muted',sample='天气来源 · 最近更新时间')
text(bottom,'↻',611,1450,55,44,30,'ink',align='CENTER',events=[{'type':'SINGLE_TAP','action':'KUSTOM_ACTION','kustom_action':'WEATHER_UPDATE'}])

detail=layer('16 预报详情面板','gv(page)=3 & gv(detail)=1 & gv(loading)=0',[3],.3)
rect(detail,347,205,319,397,'#F40D1018',events=[event('detail',0)])
text(detail,'$df(M/d EEE,a+gv(selected)+d)$',370,229,247,39,29,'#FFFFFFFF',sample='9/10 THU',latin=True)
text(detail,'×',615,218,42,44,28,'#FFFFFFFF',align='CENTER',events=[event('detail',0)])
text(detail,'$wf(cond,gv(selected))$',370,292,260,45,28,'#FFFFFFFF',sample='晴转多云')
text(detail,'$wf(max,gv(selected))$° / $wf(min,gv(selected))$°',370,354,266,61,43,'#FFFFFFFF',sample='29° / 25°',latin=True)
text(detail,'降水概率 $wf(rainc,gv(selected))$%',370,436,270,33,21,'#FFFFFFFF',sample='降水概率 20%')
text(detail,'风速 $wf(wspeed,gv(selected))$ $li(spdu)$',370,478,277,34,20,'#FFFFFFFF',sample='风速 10 km/h')
text(detail,'方向 $wf(wdir,gv(selected))$°',370,520,277,34,20,'#FFFFFFFF',sample='方向 135°')
text(detail,'点击收起  /  CLOSE',370,563,275,26,17,'#FF9FB8FF',latin=True)

cover=layer('17 音乐封面与曲目','gv(page)=4 & gv(loading)=0',[4],.5)
pic(cover,'wallpaper.png',54,204,612,409,formula='$if(mi(cover)!="",mi(cover),gv(cover))$')
text(cover,'$if(mi(title)!="",tc(ell,mi(title),30),"等待音乐播放")$',54,660,609,55,37,'ink',sample='等待音乐播放')
text(cover,'$if(mi(artist)!="",tc(ell,mi(artist),40),"打开常用播放器，开始播放后自动显示")$',55,722,610,43,23,'muted',sample='打开常用播放器，开始播放后自动显示')
line(cover,54,803,666,803,'line',1);circle(cover,54,796,14,'ink')
lyric=layer('18 歌词区域','gv(page)=4 & gv(loading)=0',[4],1.1)
text(lyric,'$if(gv(lyrics)!="",gv(lyrics),"歌词尚未接入")$',54,886,610,236,27,'ink',sample='歌词尚未接入',lines=6)
text(lyric,'$if(gv(lyrics)="","可在全局变量中接入播放器或 Tasker 文本","")$',54,1125,612,33,18,'muted',sample='可在全局变量中接入播放器或 Tasker 文本')
transport=layer('19 音乐播放控制','gv(page)=4 & gv(loading)=0',[4],1.5)
text(transport,'$tf(mi(pos),mm:ss)$ / $tf(mi(len),mm:ss)$',382,1232,283,36,25,'ink',sample='00:00 / 00:00',latin=True,align='RIGHT')
rect(transport,54,1290,612,2,'line')
rect(transport,54,1289,160,4,'ink',wformula='$612*mu(max,0,mu(min,100,mi(percent)))/100$')
circle(transport,204,1281,19,'ink',xformula='$45+612*mu(max,0,mu(min,100,mi(percent)))/100$')
for lbl,xx,ev in [('◀◀',113,music('PREVIOUS')),('$if(mi(state)=PLAYING,"Ⅱ","▶")$',308,music()),('▶▶',503,music('NEXT'))]:
    text(transport,lbl,xx,1360,100,86,39,'ink',align='CENTER',events=ev,sample='▶' if xx==308 else lbl)

cal=layer('20 月历','gv(page)=5 & gv(loading)=0',[5],.6)
text(cal,'$tc(up,df(MMMM,gv(base)))$',54,205,464,63,49,'ink',latin=True,sample='SEPTEMBER')
text(cal,'‹',547,206,53,60,42,'ink',align='CENTER',events=[event('month','$gv(month)-1$')])
text(cal,'›',611,206,53,60,42,'ink',align='CENTER',events=[event('month','$gv(month)+1$')])
for i,lbl in enumerate(['SUN','MON','TUE','WED','THU','FRI','SAT']):text(cal,lbl,54+i*88,298,82,31,18,'ink',latin=True,align='CENTER')
for i in range(42):
    xx=54+(i%7)*88;yy=339+(i//7)*83
    dates='df(S,gv(base))+('+str(i)+'-df(f,gv(base))%7)*86400'
    dateform='$'+dates+'$'
    ev=[event('date',dateform),event('event',0)]
    rect(cal,xx,yy,82,76,'card',events=ev)
    text(cal,'$df(d,'+dates+')$',xx+8,yy+6,64,54,31,'ink',sample=str((datetime.date(2026,9,1)-datetime.timedelta(days=2)+datetime.timedelta(days=i)).day),latin=True,events=ev,colorformula='$if(df(M,'+dates+')!=df(M,gv(base)),gv(dark),0)$' if False else None)
    rect(cal,xx,yy,82,76,'ink',stroke=2,show='df(yyyyMMdd,'+dates+')=df(yyyyMMdd,gv(daydate))',events=ev)
    circle(cal,xx+36,yy+62,5,'accent',show='ci(ecount,'+dates+')+ci(acount,'+dates+')>0')
progress=layer('21 年进度','gv(page)=5 & gv(loading)=0',[5],1)
rect(progress,54,938,612,170,'card')
rect(progress,54,938,111,170,'#FF202329')
text(progress,'$df(M/d)$',62,991,93,41,28,'green',sample='9/8',latin=True,align='CENTER')
text(progress,'$df(yyyy)$年已经过$mu(round,100*df(D)/df(D,12M31d))$%',189,968,397,41,29,'ink',sample='2026年已经过69%')
rect(progress,187,1030,377,15,'line');rect(progress,187,1030,260,15,'accent',wformula='$377*df(D)/df(D,12M31d)$')
text(progress,'$df(D,12M31d)-df(D)$ 天',64,1055,96,35,22,'green',sample='114 天',align='CENTER')
text(progress,'❯',594,967,61,94,66,'ink',align='CENTER',events=[event('month',0),event('date',0),event('event',0)])
agenda=layer('22 日程卡片','gv(page)=5 & gv(loading)=0',[5],1.5)
text(agenda,'SCHEDULE',81,1212,221,30,22,'ink',latin=True)
rect(agenda,54,1260,612,180,'card');rect(agenda,54,1260,12,180,'green')
text(agenda,'$if(ci(ecount,gv(daydate))+ci(acount,gv(daydate))>0,tc(ell,ci(title,gv(event),gv(daydate)),19),"暂无日程安排")$',91,1310,420,48,28,'ink',sample='暂无日程安排')
text(agenda,'$if(ci(ecount,gv(daydate))+ci(acount,gv(daydate))>0,df(HH:mm,ci(start,gv(event),gv(daydate))),df(M/d,gv(daydate)))$',91,1366,414,35,21,'muted',sample='9/8')
button(agenda,'−',525,1270,60,45,[event('event','$mu(max,0,gv(event)-1)$')],color='green',fg='#FF1E2423')
button(agenda,'+',593,1270,61,45,[event('event','$mu(min,mu(max,0,ci(ecount,gv(daydate))+ci(acount,gv(daydate))-1),gv(event)+1)$')],color='green',fg='#FF1E2423')
button(agenda,'↗',528,1330,126,101,url_event('content://com.android.calendar/time/$gv(daydate)*1000$'),color='#FF202329',fg='#FFFFFFFF',size=41)

settings=layer('23 外观设置','gv(page)=6',[6],.2)
settings2=layer('24 功能设置','gv(page)=7',[7],.2)
for g,active in [(settings,6),(settings2,7)]:
    button(g,'外观设置',54,221,306,68,nav(6),color='ink' if active==6 else 'card',fg='card' if active==6 else 'ink',size=28)
    button(g,'功能设置',362,221,304,68,nav(7),color='ink' if active==7 else 'card',fg='card' if active==7 else 'ink',size=28)

def setting(g,y,title,key,options,desc):
    text(g,title,55,y,605,46,30,'ink')
    text(g,desc,55,y+53,605,40,18,'muted')
    ww=600/len(options)
    for i,lbl in enumerate(options):
      ev=[event(key,i)]
      rect(g,55+i*ww,y+110,ww-9,63,'card',events=ev)
      rect(g,55+i*ww,y+110,ww-9,63,'ink',stroke=2,show='gv('+key+')='+str(i),events=ev)
      text(g,lbl,59+i*ww,y+112,ww-17,59,24,'ink',align='CENTER',events=ev)
    line(g,55,y+200,665,y+200,'line')
setting(settings,351,'主页光条风格','style',['六星','赛博','取色'],'金色 / 蓝色 / 从当前壁纸提取强调色')
setting(settings,584,'光条光点','dots',['关闭','开启'],'控制斜向 Dock 边缘的光点装饰')
setting(settings,817,'壁纸取色模式','palette',['主导','温和','活力'],'光条风格选择「取色」时生效')
setting(settings,1050,'加载动画','load',['关闭','开启'],'天气、音乐、日历入场前显示扫描过渡')
button(settings,'更换壁纸  /  打开 KLWP',55,1341,609,86,EDITOR,size=25)
# Compact functional tab to preserve all four observed rows plus additional global access.
def compact(g,y,title,key,opts,desc):
    text(g,title,55,y,590,40,28,'ink');text(g,desc,55,y+44,600,28,16,'muted')
    width=600/len(opts)
    for i,lbl in enumerate(opts):
      ev=[event(key,i)];rect(g,55+i*width,y+85,width-8,54,'card',events=ev)
      rect(g,55+i*width,y+85,width-8,54,'ink',stroke=2,show='gv('+key+')='+str(i),events=ev)
      text(g,lbl,55+i*width,y+85,width-8,54,23,'ink',align='CENTER',events=ev)
compact(settings2,337,'深色模式','mode',['浅色','深色','自动'],'自动模式按当地日出、日落切换')
compact(settings2,526,'Dock 栏样式','dock',['关闭','日期','图标'],'图标模式提供天气、音乐和日历入口')
compact(settings2,715,'避开 Dock 栏','avoid',['关闭','开启'],'为启动器底部图标保留额外空间')
compact(settings2,904,'全屏返回','blank',['关闭','开启'],'点击功能页空白区域返回首页')
compact(settings2,1093,'重力视差','gyro',['关闭','开启'],'通过手机传感器轻微移动壁纸')
button(settings2,'其他设置  /  打开 KLWP',55,1355,609,86,EDITOR,size=25)

loading=layer('25 扫描加载过渡','gv(loading)=1',[3,4,5])
rect(loading,0,0,720,1600,'#F2C6DCEE')
text(loading,'RHINE / TERMINAL',72,351,570,35,25,'#FF182D36',latin=True)
text(loading,'INITIALIZING INTERFACE',72,399,570,25,18,'#FF597581',latin=True)
for x1,y1,x2,y2 in [(246,649,286,649),(246,649,246,690),(477,649,435,649),(477,649,477,690),(246,925,246,884),(246,925,286,925),(477,925,435,925),(477,925,477,884)]:line(loading,x1,y1,x2,y2,'#FF263A44',2)
circle(loading,266,710,132,'#FF344D5A',stroke=2);circle(loading,327,710,132,'#FF344D5A',stroke=2)
text(loading,'R',290,716,139,130,88,'#FF344D5A',latin=True,align='CENTER')
rect(loading,154,1000,411,2,'#FF7D9CA6');rect(loading,154,999,265,4,'#FF233C47',wformula='$411*mu(min,1,(df(S)-gv(start))/2)$')
text(loading,'$mu(min,100,mu(max,0,(df(S)-gv(start))*50))$ %',478,1020,88,33,24,'#FF233C47',sample='50 %',latin=True,align='RIGHT')
text(loading,'LOADING / PLEASE WAIT',154,1100,411,35,20,'#FF4D6A77',latin=True)
text(loading,'点击跳过',265,1365,190,70,24,'#FF344D5A',align='CENTER',events=[event('start',0)])

scan=layer('26 天气提示条入场扫描','gv(page)=3 & gv(loading)=0',[3])
rect(scan,54,1215,612,54,'green')
scan['transient']=True

# Small original UI symbols avoid dependence on font glyph coverage.
def icon_asset(name):
    im=Image.new('RGBA',(96,96));d=ImageDraw.Draw(im);c=(255,255,255,255)
    if name=='apps':
      for x in [18,54]:
       for y in [18,54]:d.rectangle((x,y,x+23,y+23),outline=c,width=5)
    elif name in ['play','next','previous']:
      if name=='play':d.polygon([(30,16),(30,80),(77,48)],fill=c)
      else:
       d.polygon([(15,20),(15,76),(49,48)],fill=c);d.polygon([(48,20),(48,76),(83,48)],fill=c)
       if name=='previous':im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    elif name=='pause':d.rectangle((23,20,36,76),fill=c);d.rectangle((60,20,73,76),fill=c)
    elif name=='weather':
      d.ellipse((37,12,66,41),outline=c,width=4);d.rounded_rectangle((14,40,82,68),radius=14,outline=c,width=4)
      d.line((33,79,29,87),fill=c,width=4);d.line((53,79,49,87),fill=c,width=4)
    elif name=='headphones':
      d.arc((15,15,81,82),180,360,fill=c,width=5);d.rounded_rectangle((12,45,29,79),radius=4,outline=c,width=5);d.rounded_rectangle((67,45,84,79),radius=4,outline=c,width=5)
    elif name=='calendar':
      d.rectangle((17,23,79,79),outline=c,width=4);d.line((17,38,79,38),fill=c,width=4)
      for x in [30,65]:d.line((x,12,x,30),fill=c,width=5)
      for x in [31,50,67]:
       for y in [50,65]:d.rectangle((x,y,x+4,y+4),fill=c)
    elif name=='leaf':
      d.polygon([(15,71),(20,44),(41,24),(79,13),(73,48),(51,73),(27,81)],fill=c);d.line((23,79,62,35),fill=(0,0,0,0),width=6)
    elif name=='refresh':
      d.arc((19,19,78,78),35,315,fill=c,width=5);d.polygon([(64,9),(84,17),(72,38)],fill=c)
    elif name=='chevron':d.line((32,16,64,48,32,80),fill=c,width=10)
    im.save(ASSETS/('icon-'+name+'.png'))
for name in ['apps','play','pause','next','previous','weather','headphones','calendar','leaf','refresh','chevron']:icon_asset(name)
for g in LAYERS:
    for n in g['nodes']:
      if n['kind']!='text':continue
      label=n['text'];name=None
      if g is sidebar:name={'W':'weather','M':'headphones','C':'calendar','⊞':'apps'}.get(label)
      elif label=='◀◀':name='previous'
      elif label=='▶▶':name='next'
      elif label=='↻':name='refresh'
      elif label=='❯':name='chevron'
      elif g is aq and label=='↗':name='leaf';n['color']='green'
      elif g is transport and 'mi(state)' in label:name='play'
      if name:
        size=42 if g is sidebar else 54
        cx=n['x']+n['w']/2;cy=n['y']+n['h']/2
        n.update(kind='image',path='icon-'+name+'.png',x=cx-size/2,y=cy-size/2,w=size,h=size,tint=True)
        if g is transport and name=='play':n['formula']='$if(mi(state)=PLAYING,"kfile://org.kustom.provider/bitmaps/icon-pause.png","kfile://org.kustom.provider/bitmaps/icon-play.png")$'
# Native staged construction: real root animations, not animations hidden in nested groups.

# Kustom serialization. Preview-only samples are deliberately never serialized as data.
def formula(obj,key,value):
    obj.setdefault('internal_toggles',{})[key]=10
    obj.setdefault('internal_formulas',{})[key]=value

def export_node(n,gh):
    k=n['kind'];w=n['w'];h=n['h'];x=n['x'];y=n['y']
    base={'internal_title':re.sub(r'\$[^$]*\$', '',n.get('text',k))[:65] or k,'position_anchor':'CENTER','position_offset_x':x+w/2-W/2,'position_offset_y':y+h/2-gh/2}
    if k in ('rect','circle','triangle','line'):
      if k=='line':
        length=math.hypot(w,h);base['position_offset_x']=x+w/2-W/2;base['position_offset_y']=y+h/2-gh/2
        base.update(internal_type='ShapeModule',shape_type='RECT',shape_width=length,shape_height=n.get('stroke',1),shape_rotate_mode='MANUAL',shape_rotate_offset=math.degrees(math.atan2(h,w)))
        if n.get('live_line'):
          x1,y1,x2,y2=n['live_line'];dx=f'({x2})-({x1})';dy=f'({y2})-({y1})'
          formula(base,'shape_width',f'$mu(sqrt,mu(pow,{dx},2)+mu(pow,{dy},2))$')
          formula(base,'shape_rotate_offset',f'$mu(atan,({dy})/({dx}))$')
          formula(base,'position_offset_y',f'$(({y1})+({y2}))/2-{gh/2}$')
      else:
        base.update(internal_type='ShapeModule',shape_type={'rect':'RECT','circle':'CIRCLE','triangle':'TRIANGLE'}[k],shape_width=w,shape_height=h)
        if n.get('stroke'):base.update(paint_style='STROKE',paint_stroke=n['stroke'])
        if n.get('rotate'):base.update(shape_rotate_mode='MANUAL',shape_rotate_offset=n['rotate'])
      color=themed(n['color'])
      if color.startswith('$'):formula(base,'paint_color',color)
      else:base['paint_color']=color
    elif k=='text':
      base.update(internal_type='TextModule',text_expression=n['text'],text_size=n['size'],text_width=w,text_size_type='FIXED_WIDTH',text_lines=n.get('lines',1),text_align=n.get('align','LEFT'))
      if n.get('latin'):base['text_family']=FONT
      color=themed(n['color'])
      if color.startswith('$'):formula(base,'paint_color',color)
      else:base['paint_color']=color
    elif k=='image':
      base.update(internal_type='BitmapModule',bitmap_bitmap='kfile://org.kustom.provider/bitmaps/'+n['path'],bitmap_width=w,bitmap_height=h,bitmap_scale_mode='CENTER_CROP')
      if n.get('bind'):formula(base,'bitmap_bitmap','$gv('+n['bind']+')$')
      if n.get('formula'):formula(base,'bitmap_bitmap',n['formula'])
      if n.get('tint'):
        base['bitmap_filter']='COLORIZE'
        formula(base,'bitmap_filter_color',themed(n['color']))
    for source,target in [('wformula','shape_width'),('xformula','position_offset_x'),('yformula','position_offset_y')]:
      if n.get(source):
        expression=n[source]
        if source=='xformula':expression='$('+expression.strip('$')+')+'+str(w/2-W/2)+'$'
        if source=='yformula':expression='$('+expression.strip('$')+')+'+str(h/2-gh/2)+'$'
        formula(base,target,expression)
        if source=='wformula':formula(base,'position_offset_x','$'+str(x-W/2)+'+('+expression.strip('$')+')/2$')
    if n.get('show'):
      wrapper={'internal_type':'OverlapLayerModule','viewgroup_items':[base],'internal_title':'显示条件','position_anchor':'CENTER'}
      # Child positions must stay relative to full canvas bounds. Wrap with the full bounds.
      wrapper['viewgroup_items'].insert(0,{'internal_type':'ShapeModule','shape_type':'RECT','shape_width':W,'shape_height':gh,'paint_color':'#00000000'})
      formula(wrapper,'config_visible','$if('+n['show']+',ALWAYS,REMOVE)$')
      if n.get('events'):base['internal_events']=n['events']
      return wrapper
    if n.get('events'):base['internal_events']=n['events']
    return base

SCALE='mu(min,si(rwidth)/720,si(rheight)/1600)'
def export_layer(g):
    gh=g['height']
    bounds={'internal_type':'ShapeModule','shape_type':'RECT','shape_width':W,'shape_height':gh,'paint_color':'#00000000'}
    obj={'internal_type':'OverlapLayerModule','internal_title':g['name'],'position_anchor':'CENTER','viewgroup_items':[bounds]+[export_node(n,gh) for n in g['nodes']]}
    formula(obj,'config_scale_value','$100*'+SCALE+'$')
    formula(obj,'config_visible','$if('+g['condition']+',ALWAYS,REMOVE)$')
    offset=g['cy']-800
    formula(obj,'position_offset_y','$('+str(offset)+('-if(gv(avoid),90,0)' if g['rotate'] else '')+')*'+SCALE+'$')
    # All animations are root-level; Kustom ignores animation definitions inside groups.
    if g['delay']:
      obj['internal_animations']=[{'type':'FORMULA','formula':'$'+g['condition']+'$','action':'FADE_INVERTED','duration':2.8,'delay':g['delay'],'ease':'NORMAL'}]
    if g['delay']:
      obj['internal_animations'].append({'type':'FORMULA','formula':'$'+g['condition']+'$','action':'ADVANCED','duration':3.5,'delay':g['delay'],'anchor':'MODULE_CENTER','ease':'NORMAL','animator':[{'position':0,'property':'Y_OFFSET','value':42,'ease':'NORMAL'},{'position':100,'property':'Y_OFFSET','value':0,'ease':'NORMAL'}]})
    if g['rotate']:
      obj['internal_animations']=[{'type':'FORMULA','formula':'$gv(page)=2$','action':'ADVANCED','duration':4,'anchor':'MODULE_CENTER','ease':'NORMAL','animator':[{'position':0,'property':'ROTATE','value':15,'ease':'NORMAL'},{'position':100,'property':'ROTATE','value':0,'ease':'NORMAL'}]}]
    if g.get('transient'):
      obj['internal_animations']=[{'type':'FORMULA','formula':'$'+g['condition']+'$','action':'FADE','duration':4,'delay':2,'ease':'NORMAL'}]
    return obj

wall={'internal_type':'BitmapModule','internal_title':'00 可替换壁纸 / 重力视差','bitmap_width':720,'bitmap_height':1600,'bitmap_scale_mode':'CENTER_CROP','bitmap_bitmap':'kfile://org.kustom.provider/bitmaps/wallpaper.png'}
formula(wall,'bitmap_bitmap','$gv(wall)$');formula(wall,'bitmap_width','$si(rwidth)$');formula(wall,'bitmap_height','$si(rheight)$')
wall['internal_animations']=[{'type':'GYRO','action':'SCROLL','angle':0,'speed':8,'limit':12,'internal_toggles':{'speed':10},'internal_formulas':{'speed':'$if(gv(gyro),8,0)$'}}]
preset={'preset_info':{'title':'Rhine UI · Video Study','description':'独立复刻初版：8类页面/面板，动态数据与可替换壁纸。尚待目标手机导入验收。','author':'Personal DIY','version':1,'width':360,'height':800,'xscreens':1,'yscreens':1,'features':'MUSIC WEATHER CALENDAR','locked':False,'pflags':0},'preset_root':{'internal_type':'RootLayerModule','background_color':'#FF0C101C','globals_list':GLOBALS,'viewgroup_items':[wall]+[export_layer(g) for g in LAYERS]}}
(BASE/'preset.json').write_text(json.dumps(preset,ensure_ascii=False,indent=2),encoding='utf-8')
(BASE/'src'/'scene.json').write_text(json.dumps(LAYERS,ensure_ascii=False,indent=2),encoding='utf-8')

# Reference renderer: uses the exact geometry, but explicit sample values. Not an Android screenshot.
def rgba(c,dark):
    if c in COLORS:c=COLORS[c][int(dark)]
    s=c.lstrip('#')
    if len(s)==8:return tuple(int(s[i:i+2],16) for i in (2,4,6,0))
    return tuple(int(s[i:i+2],16) for i in (0,2,4))+(255,)

def visible(expr,page,dark,details,load):
    if not expr:return True
    vals={'page':page,'dark':int(dark),'detail':int(details),'loading':int(load),'dots':1,'dock':1,'avoid':0,'blank':1,'style':1,'palette':0,'load':1,'mode':int(dark),'gyro':0}
    if 'df(' in expr:
        match=re.search(r'\+\((\d+)-df',expr)
        return bool(match and int(match.group(1))==9)
    if 'ci(' in expr:return False
    out=expr
    for key,val in vals.items():out=out.replace('gv('+key+')',str(val))
    out=out.replace('&',' and ').replace('|',' or ')
    out=re.sub(r'(?<![<>=!])=(?!=)','==',out)
    try:return bool(eval(out,{'__builtins__':{}},{}))
    except Exception:return True

def draw_node(im,n,dark):
    d=ImageDraw.Draw(im);x,y,w,h=[n[z] for z in ('x','y','w','h')];c=rgba(n['color'],dark);kind=n['kind']
    if kind=='rect':d.rectangle((x,y,x+w,y+h),outline=c,width=max(1,int(n.get('stroke',0)))) if n.get('stroke') else d.rectangle((x,y,x+w,y+h),fill=c)
    elif kind=='circle':d.ellipse((x,y,x+w,y+h),outline=c,width=max(1,int(n.get('stroke',0)))) if n.get('stroke') else d.ellipse((x,y,x+w,y+h),fill=c)
    elif kind=='triangle':d.polygon([(x,y),(x+w,y),(x+w/2,y+h)],fill=c)
    elif kind=='line':d.line((x,y,x+w,y+h),fill=c,width=max(1,int(n.get('stroke',1))))
    elif kind=='image':
      asset=Image.open(ASSETS/n['path']).convert('RGBA');asset=ImageOps.fit(asset,(int(w),int(h)))
      if n.get('tint'):
        colored=Image.new('RGBA',asset.size,c);colored.putalpha(asset.getchannel('A'));asset=colored
      im.alpha_composite(asset,(int(x),int(y)))
    elif kind=='text':
      label=n.get('sample',n['text']);label=label if '$' not in label else '—'
      font=ImageFont.truetype(str(FONTPATH if n.get('latin') else CN),int(n['size']))
      lines=label.split('\n');lines=lines[:n.get('lines',1)]
      yy=y+(h-len(lines)*n['size']*1.28)/2
      for label in lines:
        while d.textlength(label,font=font)>w and len(label)>1:label=label[:-2]+'…'
        tw=d.textlength(label,font=font);xx=x+(w-tw)/2 if n.get('align')=='CENTER' else x+w-tw if n.get('align')=='RIGHT' else x
        d.text((xx,yy),label,font=font,fill=c,stroke_width=0);yy+=n['size']*1.28

def render(page,dark=False,details=False,load=False):
    im=ImageOps.fit(Image.open(ASSETS/'wallpaper.png').convert('RGBA'),(W,H))
    for g in LAYERS:
      if g.get('transient'):continue
      if page not in g['pages'] or not visible(g['condition'],page,dark,details,load):continue
      slab=Image.new('RGBA',(W,g['height']))
      for n in g['nodes']:
        if visible(n.get('show'),page,dark,details,load):
          nodeim=Image.new('RGBA',slab.size);draw_node(nodeim,n,dark);slab.alpha_composite(nodeim)
      if g['rotate'] and page!=2:slab=slab.rotate(-15,resample=Image.Resampling.BICUBIC,expand=True)
      im.alpha_composite(slab,((W-slab.width)//2,int(g['cy']-slab.height/2)))
    return im.convert('RGB')

views=[('01-home',0,False,False,False,'01 首页'),('02-control',1,False,False,False,'02 控制中心'),('03-apps',2,False,False,False,'03 应用页'),('04-weather',3,False,False,False,'04 天气'),('05-forecast-detail',3,False,True,False,'05 天气详情'),('06-music',4,False,False,False,'06 音乐'),('07-calendar',5,False,False,False,'07 日历'),('08-appearance',6,False,False,False,'08 外观设置'),('09-function',7,False,False,False,'09 功能设置'),('10-loading',5,False,False,True,'10 加载状态'),('11-dark-weather',3,True,True,False,'11 深色天气'),('12-dark-calendar',5,True,False,False,'12 深色日历')]
for name,pg,dk,dt,ld,title in views:render(pg,dk,dt,ld).save(OUT/(name+'.jpg'),quality=94)
atlas=Image.new('RGB',(1800,1638),(225,229,234));dd=ImageDraw.Draw(atlas);font=ImageFont.truetype(str(CN),22)
for i,(name,*rest) in enumerate(views):
    xx=18+(i%6)*298;yy=16+(i//6)*810
    dd.text((xx+3,yy),rest[-1],font=font,fill=(26,34,45))
    thumb=Image.open(OUT/(name+'.jpg'));thumb.thumbnail((276,744));atlas.paste(thumb,(xx,yy+44))
    dd.text((xx+3,yy+671),'布局预览 · 示例数据',font=ImageFont.truetype(str(CN),14),fill=(95,105,120))
atlas.save(OUT/'all-screens.jpg',quality=94)

with zipfile.ZipFile(BASE/'Rhine-UI-Study-v0.1.klwp','w',zipfile.ZIP_DEFLATED) as z:
    z.write(BASE/'preset.json','preset.json')
    z.write(OUT/'01-home.jpg','preset_thumb_portrait.jpg')
    z.write(OUT/'01-home.jpg','preset_thumb_landscape.jpg')
    for p in ASSETS.iterdir():
      if p.suffix in ['.png','.jpg']:z.write(p,'bitmaps/'+p.name)
    z.write(FONTPATH,'fonts/'+FONTPATH.name)
    z.write(ASSETS/'FONT-LICENSE.txt','FONT-LICENSE.txt')
print(json.dumps({'root_layers':len(preset['preset_root']['viewgroup_items']),'globals':len(GLOBALS),'preview_count':len(views),'package':str(BASE/'Rhine-UI-Study-v0.1.klwp')},ensure_ascii=False))