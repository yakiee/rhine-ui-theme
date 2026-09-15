"""Arknights reference: native month board and forecast mission-node view."""
from pathlib import Path
import copy,json,zipfile,math
BASE=Path(__file__).resolve().parents[1]
SOURCE=BASE/'output/pressure-v0.12.0'
VERSION='0.13.0'
OUT=BASE/f'output/calendar-weather-v{VERSION}';OUT.mkdir(exist_ok=True)
S='mu(min,1,si(sheight)*720/si(swidth)/1600)'
WHITE='#FFF0F1EF';GREY='#FF9DA3A5';YELLOW='#FFF5BE00';BLUE='#FF13ACE0'
FONT='kfile://org.kustom.provider/fonts/Rajdhani-SemiBold.ttf'

def formula(n,k,v):
 n.setdefault('internal_toggles',{})[k]=10;n.setdefault('internal_formulas',{})[k]='$'+v.strip('$')+'$';return n

def rect(w,h,color,stroke=0):
 n={'internal_type':'ShapeModule','position_anchor':'CENTER','shape_type':'RECT','shape_width':w,'shape_height':h,'paint_color':color}
 if stroke:n.update(paint_style='STROKE',paint_stroke=stroke)
 return n

def circle(size,color,stroke=0):
 n=rect(size,size,color,stroke);n['shape_type']='CIRCLE';return n

def path(w,h,data,color=WHITE,stroke=2):
 n=rect(w,h,color,stroke);n.update(shape_type='PATH',shape_path=data,shape_path_scale='FIT_XY');return n

def label(value,size,width,color=WHITE,align='CENTER',font=None,lines=1):
 n={'internal_type':'TextModule','position_anchor':'CENTER','text_expression':value,'text_size':size,'text_width':width,'text_size_type':'FIXED_WIDTH','text_lines':lines,'text_align':align,'paint_color':color}
 if font:n['text_family']=font
 return n

def group(children):return {'internal_type':'OverlapLayerModule','position_anchor':'CENTER','viewgroup_items':children}

def at(node,x,y):
 n=group([node]);n.update(position_padding_left=max(0,x*2),position_padding_right=max(0,-x*2),position_padding_top=max(0,y*2),position_padding_bottom=max(0,-y*2));return n

def add(n,item,x=0,y=0):n['viewgroup_items'].append(at(item,x,y));return item

def animation(condition,duration=3.6,dx=0,dy=18,scale=.98):
 keys=[]
 for position,opacity,ratio in [(0,100,0),(36,20,.7),(72,0,1.02),(100,0,1)]:
  for prop,value in [('OPACITY',opacity),('SCALE_XY',scale+(1-scale)*ratio),('X_OFFSET',dx*(1-ratio)),('Y_OFFSET',dy*(1-ratio))]:keys.append({'position':position,'property':prop,'value':value,'ease':'NORMAL'})
 return {'type':'FORMULA','formula':'$'+condition+'$','action':'ADVANCED','anchor':'MODULE_CENTER','duration':duration,'delay':0,'ease':'STRAIGHT','animator':keys}

def root(title,condition,motion=True,dx=0,dy=18):
 n=group([rect(720,1600,'#00000000')]);n['internal_title']=title;formula(n,'config_scale_value','100*'+S)
 if motion:n['internal_animations']=[animation(condition,dx=dx,dy=dy)];n['config_visible']='ALWAYS'
 else:formula(n,'config_visible',f'if({condition},ALWAYS,REMOVE)')
 return n

def switch(name,value):return {'type':'SINGLE_TAP','action':'SWITCH_GLOBAL','switch':name,'switch_text':str(value)}

def hit(n,x,y,w,h,events,condition=None):
 item=rect(w,h,'#00000000');item['internal_events']=copy.deepcopy(events);holder=at(item,x,y)
 if condition:formula(holder,'config_visible',f'if({condition},ALWAYS,REMOVE)')
 n['viewgroup_items'].append(holder)

def pulse(n,key):
 keys=[]
 for pos,scale in [(0,1),(35,.988),(50,.984),(65,.988),(100,1)]:keys.append({'position':pos,'property':'SCALE_XY','value':scale,'ease':'NORMAL'})
 n['internal_animations'].append({'type':'FORMULA','formula':f'$gv({key})=1$','action':'ADVANCED','anchor':'MODULE_CENTER','duration':2.4,'delay':0,'ease':'STRAIGHT','animator':keys})

def wallpaper(blur,dark):
 bmp={'internal_type':'BitmapModule','position_anchor':'CENTER','bitmap_width':780,'bitmap_height':1720,'bitmap_scale_mode':'CENTER_CROP','bitmap_blur':blur}
 formula(bmp,'bitmap_bitmap','gv(wall)')
 return group([rect(720,1600,'#FF141A1E'),bmp,rect(780,1720,dark)])

HEX='M 50 1 L 93 25 L 93 75 L 50 99 L 7 75 L 7 25 Z'
CAL='M 8 18 L 92 18 L 92 92 L 8 92 Z M 8 36 L 92 36 M 27 3 L 27 27 M 73 3 L 73 27 M 24 50 L 36 50 M 44 50 L 56 50 M 64 50 L 76 50 M 24 66 L 36 66 M 44 66 L 56 66 M 64 66 L 76 66 M 24 82 L 36 82 M 44 82 L 56 82'
CLOUD='M 20 75 C -1 73 -1 42 20 39 C 17 2 74 1 78 38 C 108 32 110 77 82 77 Z'
SUN='M 50 25 A 25 25 0 1 1 49.9 25 M 50 0 L 50 14 M 50 86 L 50 100 M 0 50 L 14 50 M 86 50 L 100 50 M 15 15 L 25 25 M 75 75 L 85 85 M 15 85 L 25 75 M 75 25 L 85 15'
SNOW='M 50 0 L 50 100 M 7 25 L 93 75 M 7 75 L 93 25 M 35 9 L 50 23 L 65 9 M 35 91 L 50 77 L 65 91'

def weather_icon(day,size,color=WHITE):
 n=group([rect(size,size,'#00000000')]);known=f'gv(weatherok) & {day}<wi(pdays) & wf(icon,{day})!=UNKNOWN'
 for shape,cond in [(SUN,f'wf(icon,{day})=CLEAR'),(SNOW,f'wf(icon,{day})=SNOW | wf(icon,{day})=LSNOW'),(CLOUD,f'wf(icon,{day})!=CLEAR & wf(icon,{day})!=SNOW & wf(icon,{day})!=LSNOW')]:
  item=group([path(size,size,shape,color,2.2)]);formula(item,'config_visible',f'if({known} & ({cond}),ALWAYS,REMOVE)');n['viewgroup_items'].append(item)
 unknown=group([label('—',size*.65,size,GREY)]);formula(unknown,'config_visible',f'if({known},REMOVE,ALWAYS)');n['viewgroup_items'].append(unknown)
 return n

def forecast_text(expr,day,unit=''):
 return f'$if(gv(weatherok) & {day}<wi(pdays),{expr}+"{unit}","—")$'

def build():
 for suffix in ['', '-off']:
  with zipfile.ZipFile(SOURCE/f'Rhine-UI-pressure{suffix}-v0.12.0.klwp') as source:
   preset=json.loads(source.read('preset.json'));r=preset['preset_root']['viewgroup_items'];g=preset['preset_root']['globals_list']
   for key,title in [('wpulse','天气节点选择反馈'),('cpulse','月历日期选择反馈')]:g[key]={'index':len(g),'type':'TEXT','title':title,'value':'0'}
   for index in [25,26]:
    for a in r[index].get('internal_animations',[]):
     if a.get('type')=='FORMULA':a['formula']='$('+a['formula'].strip('$')+') & gv(page)!=3 & gv(page)!=5$'
   formula(r[53],'config_visible','if(gv(page)>=3 & gv(page)!=3 & gv(page)!=5 & gv(loading)=0,ALWAYS,REMOVE)')
   cal='gv(page)=5 & gv(loading)=0';weather='gv(page)=3 & gv(loading)=0';detail=weather+' & gv(detail)=1';overview=weather+' & gv(detail)=0'
   back=[switch('detail',0),switch('view',0)]
   # Calendar month board: large quiet dates, yellow rail and a raised selection panel.
   board=root('日历 · 方舟月历面板',cal,dy=-18);add(board,wallpaper(28,'#B80D1014'))
   add(board,rect(664,850,'#DE2D3031'),0,-230);add(board,rect(664,8,YELLOW),0,-655)
   add(board,path(42,42,CAL,WHITE,3),-274,-603);add(board,label('$df(M月,gv(base))$ · 日历',30,390,WHITE,'LEFT'),-24,-603)
   add(board,circle(64,'#FF515654'),303,-650);add(board,label('×',45,60),303,-650)
   add(board,label('$df(yyyy年,gv(base))$',23,215,GREY,'LEFT'),-185,-544)
   for x,t in [(171,'‹'),(260,'›')]:add(board,rect(70,54,'#663F4445'),x,-544);add(board,label(t,40,60),x,-544)
   for col,day in enumerate(['日','一','二','三','四','五','六']):add(board,label(day,21,70,GREY),-264+88*col,-470)
   datehits=root('日历 · 日期点击',cal,False)
   for index in range(42):
    col=index%7;row=index//7;x=-264+88*col;y=-390+96*row
    offset=f'({index}-df(f,gv(base))%7)'
    stamp=f'dp(df(yyyy,gv(base))+"y"+df(M,gv(base))+"M1d12h0m0s"+if({offset}>=0,"a","r")+mu(abs,{offset})+"d")'
    selected=f'df(yyyyMMdd,{stamp})=df(yyyyMMdd,gv(daydate))';today=f'df(yyyyMMdd,{stamp})=df(yyyyMMdd)';inmonth=f'df(yyyyMM,{stamp})=df(yyyyMM,gv(base))'
    fill=rect(76,86,'#223A3F40');formula(fill,'paint_color',f'if({selected},#C1C49B09,#103D4344)');add(board,fill,x,y)
    rim=rect(76,86,'#00000000',2.5);formula(rim,'paint_color',f'if({selected},#FFF4F4EE,{today},#FFF5BE00,#00000000)');add(board,rim,x,y)
    number=label(f'$df(d,{stamp})$',43,72,GREY,'LEFT',FONT);formula(number,'paint_color',f'if({selected},#FFFFFFFF,{inmonth},#FF9C9F9F,#FF515556)');add(board,number,x+3,y-9)
    mark=label(f'$if({today},"今日",ci(ecount,{stamp})+ci(acount,{stamp})>0,"•","")$',14,66,YELLOW)
    add(board,mark,x,y+26)
    hit(datehits,x,y,84,90,[switch('date','$'+stamp+'$'),switch('event',0),switch('cpulse','$1-gv(cpulse)$')])
   add(board,label('点选日期查看当天日程',20,540,GREY,'LEFT'),-5,170)
   r[41]=board;r[57]=datehits
   selectedpanel=root('日历 · 黄色侧轨与日期详情',cal,dx=20,dy=0);pulse(selectedpanel,'cpulse')
   add(selectedpanel,rect(664,454,YELLOW),0,422)
   add(selectedpanel,rect(630,334,'#AA000000'),-8,375)
   add(selectedpanel,rect(628,334,'#FF303333'),-18,364)
   add(selectedpanel,rect(112,30,WHITE),-236,222);add(selectedpanel,label('所选日期',19,108,'#FF282E30'),-236,222)
   add(selectedpanel,label('$df(dd,gv(daydate))$',104,186,WHITE,'LEFT',FONT),-183,322)
   add(selectedpanel,label('$df(yyyy / MM,gv(daydate))$',23,210,GREY,'LEFT',FONT),-170,395)
   add(selectedpanel,label('$df(EEEE,gv(daydate))$',24,210,WHITE,'LEFT'),-170,443)
   add(selectedpanel,rect(1.5,205,'#FF565A5A'),-58,365)
   add(selectedpanel,rect(220,68,'#FF2C3336'),191,592);add(selectedpanel,label('系统日历  ›',26,206),191,592)
   add(selectedpanel,path(27,27,CAL,'#FF282D2E',2),-267,592);add(selectedpanel,label('回到今天',24,198,'#FF262C2E','LEFT'),-135,592)
   r[42]=selectedpanel
   agenda=root('日历 · 当天日程',cal,dx=20,dy=0);pulse(agenda,'cpulse')
   count='ci(ecount,gv(daydate))+ci(acount,gv(daydate))';event=f'mu(max,0,mu(min,gv(event),{count}-1))'
   add(agenda,label('日程',24,282,WHITE,'LEFT'),107,267)
   add(agenda,label(f'$if({count}>0,tc(ell,ci(title,{event},gv(daydate)),30),"暂无可读取日程")$',25,282,WHITE,'LEFT',lines=2),107,340)
   add(agenda,label(f'$if({count}>0,if(ci(allday,{event},gv(daydate)),"全天",df(HH:mm,ci(start,{event},gv(daydate)))+" — "+df(HH:mm,ci(end,{event},gv(daydate)))),"以系统日历为准")$',19,282,GREY,'LEFT'),107,406)
   add(agenda,label(f'$if({count}>0,(gv(event)+1)+" / "+({count}),"—")$',19,150,GREY,'LEFT',FONT),41,480)
   for x,t in [(183,'‹'),(264,'›')]:add(agenda,rect(62,48,'#FF464A4B'),x,480);add(agenda,label(t,33,54),x,480)
   r[43]=agenda
   nav=root('日历 · 关闭与月份导航',cal,False)
   hit(nav,303,-650,76,76,back)
   for x,offset in [(171,-1),(260,1)]:hit(nav,x,-544,82,70,[switch('month',f'$gv(month)+({offset})$'),switch('event',0)])
   hit(nav,-150,592,310,86,[switch('month',0),switch('date',0),switch('event',0),switch('cpulse','$1-gv(cpulse)$')])
   hit(nav,191,592,238,86,[{'type':'SINGLE_TAP','action':'LAUNCH_ACTIVITY','intent':'intent:#Intent;action=android.intent.action.MAIN;category=android.intent.category.APP_CALENDAR;end'}])
   r[58]=nav
   agenda_nav=root('日历 · 日程翻页',cal,False)
   hit(agenda_nav,183,480,76,64,[switch('event','$mu(max,0,gv(event)-1)$')]);hit(agenda_nav,264,480,76,64,[switch('event',f'$mu(min,mu(max,0,{count}-1),gv(event)+1)$')]);r[59]=agenda_nav
   # Forecast map and the selected-node briefing use the same reference hierarchy.
   scene=root('天气 · 节点地图背景与导航',weather,dy=0);add(scene,wallpaper(1,'#BF070D12'))
   add(scene,rect(190,1600,'#4F000000'),-265,0)
   add(scene,path(400,1050,'M 0 0 L 70 0 L 100 28 L 35 68 L 98 100 L 30 100 L 0 72 L 57 29 Z','#243AA8C0',0),135,-60)
   add(scene,rect(318,74,'#E7323739'),-159,-664);add(scene,label('‹',49,80),-276,-664);add(scene,rect(2,56,'#FF171C1D'),-222,-664)
   add(scene,label('天气预报',29,194),-110,-664);add(scene,label('$df(MM/dd HH:mm)$',23,250,WHITE,'RIGHT',FONT),197,-664)
   add(scene,label('FORECAST / 05 DAYS',18,600,GREY,'LEFT',FONT),-7,-575)
   add(scene,label('$if(gv(weatherok),li(loc),"天气尚未更新")$',36,620,WHITE,'LEFT'),0,-531)
   add(scene,rect(620,1,'#FF465055'),0,213)
   r[27]=scene
   route=root('天气 · 连线与六边形节点',weather,dy=12)
   points=[(-212,-330),(104,-413),(179,-199),(-102,-62),(124,109)]
   starts=[(-365,-221),*points,(353,34)]
   for (x1,y1),(x2,y2) in zip(starts,starts[1:]):
    lo_x=min(x1,x2);lo_y=min(y1,y2);w=abs(x2-x1);h=abs(y2-y1)
    data=f'M {0 if x1<x2 else 100} {0 if y1<y2 else 100} L {100 if x1<x2 else 0} {100 if y1<y2 else 0}'
    add(route,path(w,h,data,'#DFEBEEED',4),lo_x+w/2,lo_y+h/2)
   routehits=root('天气 · 节点点击与日期范围',weather,False)
   for index,(x,y) in enumerate(points):
    day=f'(gv(forecast)+{index})';chosen=f'gv(detail)=1 & gv(selected)={day}'
    add(route,rect(202,73,'#9B000000'),x+5,y+6)
    plate=rect(198,68,WHITE);formula(plate,'paint_color',f'if({chosen},#FFF2F4F1,#DD303A40)');add(route,plate,x,y)
    add(route,rect(150,17,'#FF151D22'),x+24,y-35)
    add(route,label(f'FORECAST  {index+1:02d}',12,140,WHITE,'CENTER',FONT),x+24,y-35)
    rim=rect(202,72,'#00000000',2);formula(rim,'paint_color',f'if({chosen},#FF20BCED,#00000000)');add(route,rim,x,y)
    hexfill=path(48,54,HEX,'#FF18ADDC',0);formula(hexfill,'paint_color',f'if({chosen},#FF13ACE0,#FF46565F)');add(route,hexfill,x-82,y)
    add(route,path(48,54,HEX,WHITE,2),x-82,y);add(route,weather_icon(day,24),x-82,y)
    number=label(f'$df(M/d,a+{day}+d)$',33,136,WHITE,'CENTER',FONT);formula(number,'paint_color',f'if({chosen},#FF18232A,#FFF1F3F1)');add(route,number,x+19,y-3)
    add(route,label(forecast_text(f'wf(max,{day})+" / "+wf(min,{day})',day,'°'),19,174,WHITE,'RIGHT',FONT),x+8,y+56)
    hit(routehits,x,y,216,100,[switch('selected','$'+day+'$'),switch('detail',1),switch('wpulse','$1-gv(wpulse)$')])
   r[28]=route;r[54]=routehits
   briefing=root('天气 · 当前概况',overview,dy=20)
   add(briefing,rect(664,396,'#E6293238'),0,438);add(briefing,rect(664,6,BLUE),0,238)
   add(briefing,label('当前天气',24,400,WHITE,'LEFT'),-89,282)
   add(briefing,label('$if(gv(weatherok),wi(temp)+"°"+wi(tempu),"—")$',82,270,WHITE,'LEFT',FONT),-139,377)
   add(briefing,label('$if(gv(weatherok),wi(cond),"等待天气数据")$',29,282,WHITE,'LEFT'),161,354)
   add(briefing,label('$if(gv(weatherok),"体感 "+wi(flik)+"°  湿度 "+wi(hum)+"%","更新后显示真实预报")$',20,282,GREY,'LEFT',lines=2),161,405)
   add(briefing,rect(594,1,'#FF4D565B'),0,474)
   add(briefing,label('点击上方日期节点',26,530,WHITE,'LEFT'),-22,526)
   add(briefing,label('查看当天温度、降水与风况',22,530,GREY,'LEFT'),-22,568)
   add(briefing,label('$if(gv(weatherok),"更新 "+df(M/d HH:mm,wi(updated)),"暂无数据时显示 —")$',18,580,GREY,'LEFT',FONT),0,615)
   r[29]=briefing
   info=root('天气 · 所选节点详情',detail,dx=50,dy=0);pulse(info,'wpulse')
   add(info,rect(674,414,'#97000000'),4,445);add(info,rect(664,406,'#F1273036'),0,434)
   add(info,rect(664,7,BLUE),0,232)
   add(info,label('DAILY FORECAST',16,300,GREY,'LEFT',FONT),-132,263)
   add(info,label('$df(M月d日 EEE,a+gv(selected)+d)$',29,550,WHITE,'LEFT'),-6,300)
   add(info,circle(46,'#FF485057'),288,274);add(info,label('×',31,44),288,274)
   add(info,weather_icon('gv(selected)',58,BLUE),-267,373)
   add(info,label(forecast_text('wf(cond,gv(selected))','gv(selected)'),28,190,WHITE,'LEFT'),-122,365)
   add(info,label(forecast_text('wf(max,gv(selected))+" / "+wf(min,gv(selected))','gv(selected)','°'),42,294,WHITE,'RIGHT',FONT),153,370)
   for x,title,expression in [(-206,'降水概率','$if(gv(weatherok) & gv(selected)<wi(pdays) & wi(prainc),wf(rainc,gv(selected))+"%","—")$'),(0,'风速','$if(gv(weatherok) & gv(selected)<wi(pdays),wf(wspeed,gv(selected))+" "+li(spdu),"—")$'),(206,'湿度',forecast_text('wf(hum,gv(selected))','gv(selected)','%'))]:
    add(info,rect(190,113,'#FF333D44'),x,477);add(info,label(title,19,177,GREY),x,449);add(info,label(expression,27,177,WHITE,'CENTER',FONT),x,490)
   for x in [-105,105]:add(info,rect(1,113,'#FF566169'),x,477)
   add(info,rect(290,64,'#FFF0F1ED'),-154,594);add(info,label('‹  上一天',25,260,'#FF243039'),-154,594)
   add(info,rect(310,64,'#FF119BCD'),157,594);add(info,label('下一天  ›',25,280),157,594)
   r[30]=info
   weather_nav=root('天气 · 返回与详情操作',weather,False)
   hit(weather_nav,-267,-664,115,88,back)
   hit(weather_nav,288,274,66,66,[switch('detail',0)],detail)
   hit(weather_nav,-154,594,290,80,[switch('selected','$mu(max,0,gv(selected)-1)$'),switch('wpulse','$1-gv(wpulse)$')],detail)
   hit(weather_nav,157,594,310,80,[switch('selected','$mu(min,4,gv(selected)+1)$'),switch('wpulse','$1-gv(wpulse)$')],detail)
   r[55]=weather_nav
   preset['preset_info'].update(title=f'Rhine UI · 月历与天气节点 v{VERSION}'+(' · 无重力视差' if suffix else ''),description='方舟签到面板式月历、六边形天气日期节点与独立预报详情；保留真实日期数据及终端方位按压。')
   target=OUT/f'Rhine-UI-calendar-weather{suffix}-v{VERSION}.klwp'
   with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as dest:
    for name in source.namelist():dest.writestr(name,json.dumps(preset,ensure_ascii=False) if name=='preset.json' else source.read(name))
   if not suffix:(OUT/'preset.json').write_text(json.dumps(preset,ensure_ascii=False,indent=2),encoding='utf8')
   print(target)

if __name__ == "__main__":
 build()
