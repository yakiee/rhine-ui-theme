"""Bind editable theme fields to the Android device running Kustom."""
from pathlib import Path
import json, zipfile, copy
BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / 'output/dock-edges-v0.8.7'
OUT = BASE / 'output/live-data-v0.9.2'
OUT.mkdir(exist_ok=True)

def formula(node, field, expression):
    node.setdefault('internal_toggles', {})[field] = 10
    node.setdefault('internal_formulas', {})[field] = '$' + expression.strip('$') + '$'

def clear_formula(node, field):
    node.get('internal_toggles', {}).pop(field, None)
    node.get('internal_formulas', {}).pop(field, None)

def position(node, axis, expression):
    positive, negative = ('left', 'right') if axis == 'x' else ('top', 'bottom')
    formula(node, 'position_padding_' + positive, 'mu(max,0,2*(' + expression + '))')
    formula(node, 'position_padding_' + negative, 'mu(max,0,-2*(' + expression + '))')

def center(node, axis):
    a, b = ('left', 'right') if axis == 'x' else ('top', 'bottom')
    return (node.get('position_padding_' + a, 0) - node.get('position_padding_' + b, 0)) / 2

def switch(name, value):
    return {'type': 'SINGLE_TAP', 'action': 'SWITCH_GLOBAL', 'switch': name, 'switch_text': value}

def hit_from(holder, events, width=76, height=64):
    node = {k: copy.deepcopy(v) for k,v in holder.items() if k.startswith('position_')}
    node.update(internal_type='OverlapLayerModule', viewgroup_items=[{'internal_type':'ShapeModule','position_anchor':'CENTER','shape_type':'RECT','shape_width':width,'shape_height':height,'paint_color':'#00000000','internal_events':events}])
    return node

for suffix in ['', '-off']:
    with zipfile.ZipFile(SOURCE / f'Rhine-UI-dock-edges{suffix}-v0.8.7.klwp') as source:
        p = json.loads(source.read('preset.json'))
        r = p['preset_root']['viewgroup_items']
        g = p['preset_root']['globals_list']
        original_animations = [copy.deepcopy(n.get('internal_animations')) for n in r]
        def node(path):
            current = r[path[0]]
            for index in path[1:]: current = current['viewgroup_items'][index]
            return current
        def text(path, value):
            target = node(path)
            assert target['internal_type'] == 'TextModule', (path, target['internal_type'])
            target['text_expression'] = value
            clear_formula(target, 'text_expression')
        def global_value(name, value, title=None):
            if name not in g:
                g[name] = {'index':max(v['index'] for v in g.values())+1,'type':'TEXT','description':'','global_formula':''}
            g[name]['value'] = value
            if title: g[name]['title'] = title
        global_value('dark', '$if(gv(mode)=2,si(darkmode),gv(mode)=1,1,0)$')
        g['mode']['value'] = '2'
        g['mode']['title'] = '深色模式 0浅色 1深色 2跟随系统'
        global_value('playing', '$if(mi(state)=PLAYING,1,0)$', '计算：实际播放状态')
        global_value('base', '$dp("1d0h0m0s"+if(gv(month)>=0,"a","r")+mu(abs,gv(month))+"M")$')
        global_value('daydate', '$if(gv(date)=0,dp(),gv(date))$')
        for key in ['month','date','event','forecast','selected','detail','pick','page']: global_value(key,'0')
        global_value('weatherok', '$if(wi(pdays)>0 & df(S,wi(updated))>0,1,0)$', '计算：天气数据可用')
        global_value('aqok', '$if(aq(level)!=NA & aq(level)!="",1,0)$', '计算：空气数据可用')
        global_value('yearpct', '$mu(max,0,mu(min,1,(df(D)-1)/df(D,12M31d)))$', '计算：实际年进度')
        # The installed device supplies its own locale, clock, battery and system metrics.
        text([1,4,0], '$df(hh:mm)$')
        text([1,5,0], '$df(a)$')
        text([1,7,0], '$tc(ell,si(model),24)$')
        text([4,1,0], '$df(yyyy/MM/dd hh:mm)$')
        text([4,2,0], 'CPU $if(rm(cused)>=0,mu(round,rm(cused))+"%","—")$')
        text([4,3,0], 'RAM $if(rm(mtot)>0,mu(round,100*rm(mused)/rm(mtot))+"%","—")$')
        text([4,4,0], 'ROM $if(rm(fstot,int)>0,mu(round,100*rm(fsused,int)/rm(fstot,int))+"%","—")$')
        text([7,2,0], 'Android $si(aver)$')
        text([8,2,0], '电池 / °C')
        text([9,1,0], '[i]$bi(tempc)$[/i]')
        text([23,7,1,0], '$tc(up,df(EEEE))$')
        text([23,8,1,0], '$df(yyyy.M.d)$')
        # Forecast cards and their connecting curve use the same measured temperatures.
        highs = [f'wf(max,gv(forecast)+{i})' for i in range(3)]
        lowest, highest = 'mu(min,'+','.join(highs)+')', 'mu(max,'+','.join(highs)+')'
        for index in range(3):
            day = f'gv(forecast)+{index}'
            global_value(f'fy{index}', f'$if(gv(weatherok),-280-120*({highs[index]}-{lowest})/mu(max,1,{highest}-{lowest}),-320)$', '计算：预报曲线高度')
            start = 4 + 5*index
            old_y = center(r[27]['viewgroup_items'][start], 'y')
            for offset in range(5):
                holder = r[27]['viewgroup_items'][start+offset]
                position(holder, 'y', f'gv(fy{index})+({center(holder,"y")-old_y})')
            text([27,start+2,0], f'$if(gv(weatherok),if(wf(icon,{day})=CLEAR,"☀",wf(icon,{day})=RAIN,"☂",wf(icon,{day})=SNOW,"❄","☁"),"—")$')
            text([27,start+3,0], f'$if(gv(weatherok),wf(max,{day})+" / "+wf(min,{day})+"°","— / —")$')
            text([27,start+4,0], f'$df(yyyy/MM/dd,a+(gv(forecast)+{index})+d)$')
            h = r[54]['viewgroup_items'][index]
            position(h, 'y', f'gv(fy{index})')
            h['viewgroup_items'][0]['internal_events'] = [switch('selected', '$'+day+'$'),switch('detail','1')]
        for index, line_index in enumerate([2,3]):
            line = r[27]['viewgroup_items'][line_index]
            dx = center(r[27]['viewgroup_items'][10+5*index], 'x') - center(r[27]['viewgroup_items'][5+5*index], 'x')
            dy = f'(gv(fy{index+1})-gv(fy{index}))'
            position(line, 'y', f'(gv(fy{index})+gv(fy{index+1}))/2')
            formula(line['viewgroup_items'][0], 'shape_width', f'mu(sqrt,{dx}*{dx}+{dy}*{dy})')
            formula(line['viewgroup_items'][0], 'shape_rotate_offset', f'mu(atan,{dy}/{dx})')
        text([27,21,0], '')
        for index,delta in [(19,-1),(20,1)]:
            r[54]['viewgroup_items'].append(hit_from(r[27]['viewgroup_items'][index],[switch('forecast',f'$mu(max,0,mu(min,mu(max,0,wi(pdays)-3),gv(forecast)+({delta})))$'),switch('detail','0')]))
        for index in range(5):
            formula(node([27,24+index,0]),'paint_color',f'if(gv(forecast)%5={index},gv(accent),#55777777)')
        text([28,2,0], '空气指数 $if(gv(aqok),aq(index),"—")$')
        for path, label, parameter in [(14,'NO₂','no2'),(20,'PM₂.₅','pm25'),(23,'PM₁₀','pm10')]:
            text([28,path,0], f'[b]{label} $if(gv(aqok),aq({parameter}),"—")$[/b]')
        text([28,17,0], '[b]SO₂ $gv(so2)$[/b]')
        for index in [16,22,25]: text([28,index,0], '$if(gv(aqok),"更新 "+df(M/d hh:mm,aq(updated)),"等待空气质量数据")$')
        text([28,19,0], '当前数据源未提供 SO₂')
        text([29,4,0], '$if(gv(weatherok),wf(max,0)+" / "+wf(min,0)+"°"+wi(tempu),"— / —")$')
        text([29,6,0], '[b][i]$if(gv(weatherok),wi(temp),"—")$[/i][/b]')
        text([29,7,0], '°$wi(tempu)$')
        text([29,8,0], '$if(gv(weatherok),"气压 "+wi(press)+" hPa  体感 "+wi(flik)+"°  湿度 "+wi(hum)+"%","等待定位与天气数据")$')
        text([29,9,0], '$if(gv(weatherok),wi(provider),"WEATHER")$')
        text([30,2,0], '$df(M/d EEE,a+gv(selected)+d)$')
        text([30,4,0], '$if(gv(weatherok),wf(cond,gv(selected)),"暂无天气数据")$')
        text([30,5,0], '$if(gv(weatherok),wf(max,gv(selected))+" / "+wf(min,gv(selected))+"°","— / —")$')
        text([30,6,0], '降水概率 $if(gv(weatherok) & wi(prainc),wf(rainc,gv(selected))+"%","—")$')
        text([30,7,0], '风速 $if(gv(weatherok),wf(wspeed,gv(selected))+" "+li(spdu),"—")$')
        text([30,8,0], '风向 $if(gv(weatherok),wf(wdir,gv(selected))+"°","—")$')
        # Remove the sample album and lyrics; retain all existing entrance animations.
        cover = node([31,1,0])
        cover['viewgroup_items'] = [
            {'internal_type':'ShapeModule','position_anchor':'CENTER','shape_type':'RECT','shape_width':646.8085106383,'shape_height':398,'paint_color':'#FF25282E'},
            {'internal_type':'BitmapModule','position_anchor':'CENTER','bitmap_width':646.8085106383,'bitmap_height':398,'bitmap_scale_mode':'CENTER_CROP'}]
        formula(cover['viewgroup_items'][1], 'bitmap_bitmap', 'mi(cover)')
        text([32,1,0], '[b]$if(mi(title)!="",mi(title),"等待音乐播放")$[/b]')
        text([32,2,0], '$if(mi(artist)!="",mi(artist),"打开播放器后显示歌曲信息")$')
        for index in [1,2,4,5]: text([39,index,0], '')
        text([39,3,0], '$if(gv(lyrics)!="",gv(lyrics),"暂无同步歌词")$')
        text([40,1,0], '$if(mi(title)!="" & mi(len)>1,tf(mi(pos),mm:ss)+" / "+tf(mi(len),mm:ss),"— / —")$')
        ratio='if(mi(title)!="" & mi(len)>1,mu(max,0,mu(min,1,mi(percent)/100)),0)'
        formula(node([40,3,0]), 'shape_width', f'651.063829787234*({ratio})')
        position(node([40,3]), 'x', f'-325.531914893617+325.531914893617*({ratio})')
        position(node([40,4]), 'x', f'-325.531914893617+651.063829787234*({ratio})')
        r[56]['viewgroup_items'] = []
        for index,action in [(5,'PREVIOUS'),(6,None),(7,'NEXT')]:
            event={'type':'SINGLE_TAP','action':'MUSIC'}
            if action: event['music_action']=action
            r[56]['viewgroup_items'].append(hit_from(r[40]['viewgroup_items'][index],[event]))
        # The old pseudo waveform is now a quiet track with a real position marker.
        for index in [1,2,3]:
            shape = node([33,index,0])
            shape['shape_type']='RECT';shape['shape_height']=1
            shape.pop('shape_path',None)
        position(node([33,4]), 'x', f'-300+600*({ratio})')
        text([41,1,0], '[b]$tc(up,df(MMMM,gv(base)))$[/b]')
        r[57]['viewgroup_items'] = r[57]['viewgroup_items'][:2]
        for index in range(42):
            offset=f'({index}-df(f,gv(base))%7)'
            date=f'dp(df(yyyy,gv(base))+"y"+df(M,gv(base))+"M1d12h0m0s"+if({offset}>=0,"a","r")+mu(abs,{offset})+"d")'
            start=11+4*index
            text([41,start+1,0], '$df(d,'+date+')$')
            formula(node([41,start,0]),'paint_color',f'if(df(yyyyMMdd,{date})=df(yyyyMMdd),#887A9121,#1F777777)')
            formula(node([41,start+1,0]),'paint_color',f'if(df(M,{date})!=df(M,gv(base)),#88777777,gv(dark),#FFF0F0F2,#FF17191C)')
            formula(node([41,start+2]),'config_visible',f'if(df(yyyyMMdd,{date})=df(yyyyMMdd,gv(daydate)),ALWAYS,REMOVE)')
            formula(node([41,start+3]),'config_visible',f'if(ci(ecount,{date})+ci(acount,{date})>0,ALWAYS,REMOVE)')
            r[57]['viewgroup_items'].append(hit_from(node([41,start]),[switch('date','$'+date+'$'),switch('event','0')],87.234,60.04))
        text([42,5,0], '$df(yyyy)$年已经过$mu(round,100*gv(yearpct))$%')
        text([42,11,0], '◉ $df(D,12M31d)-df(D)$天')
        text([42,12,0], '$df(M/d)$')
        text([42,14,0], '$df(yy)$')
        formula(node([42,7,0]),'shape_width','401.063829787234*gv(yearpct)')
        position(node([42,7]),'x','16.4893617021-200.531914893617+200.531914893617*gv(yearpct)')
        count='ci(ecount,gv(daydate))+ci(acount,gv(daydate))'
        eventindex=f'mu(max,0,mu(min,gv(event),{count}-1))'
        text([43,4,0], f'$if({count}>0,tc(ell,ci(title,{eventindex},gv(daydate)),22),"暂无可读取日程")$')
        text([43,5,0], f'$if({count}>0,df(hh:mm,ci(start,{eventindex},gv(daydate)))+" — "+df(hh:mm,ci(end,{eventindex},gv(daydate))),df(yyyy/M/d,gv(daydate)))$')
        node([43,4,0])['text_size']=26
        node([43,5,0])['text_width']=240
        position(node([43,5]),'x','23')
        text([45,46,0], '重力视差 · $if(gv(gyro),"已开启","已关闭")$')
        for weekday in range(7):
            text([41,4+weekday,0], '$tc(up,df(EEE,df(S,gv(base))+('+str(weekday)+'-df(f,gv(base))%7)*86400))$')
        def walk(n):
            yield n
            for c in n.get('viewgroup_items',[]): yield from walk(c)
        for n in walk(p['preset_root']):
            if n.get('internal_type')=='TextModule' and ('日出' in n.get('text_expression','') or '日落' in n.get('text_expression','')):
                n['text_expression']='自动模式跟随系统深浅色设置'
        # Live system dark mode also requires readable labels on unboxed content.
        for root_index in [28,32,39]:
            for item in walk(r[root_index]):
                if item.get('internal_type')=='TextModule':
                    formula(item,'paint_color','if(gv(dark),#FFF0F0F2,#FF202329)')
        for child in [14,15]:
            formula(node([43,child,0]),'paint_color','if(gv(dark),#FFF0F0F2,#FF202329)')
        for child in [1,2,3,4]:
            formula(node([33,child,0]),'paint_color','if(gv(dark),#FF9FA4AC,#FF777777)')
        # Core invariant: data wiring must not disturb the already matched motion.
        assert len(r)==64
        assert [n.get('internal_animations') for n in r] == original_animations
        p['preset_info']['title']='Rhine UI · 设备实时数据 v0.9.2'+(' · 无重力视差' if suffix else '')
        p['preset_info']['description']='读取运行 KLWP 的安卓设备时间、日期、电量、温度、型号和系统资源；天气、音乐、日历接原生数据源，缺失数据保留空状态。保留 Dock 贴合与边角修复。'
        target=OUT/f'Rhine-UI-live-data{suffix}-v0.9.2.klwp'
        with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
            for name in source.namelist():
                z.writestr(name,json.dumps(p,ensure_ascii=False) if name=='preset.json' else source.read(name))
        if not suffix:
            (OUT/'preset.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
        print(target)
