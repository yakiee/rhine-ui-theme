from pathlib import Path
import json,copy
base=Path('rhine_exact');raw=json.loads((base/'analysis/app-motion-measurements.json').read_text())
valid=[r for r in raw if 55<=r['frame']<=61 and r['template_ncc']>=.8]
points=[]
for r in valid:
 scale=r['icon_width']/55
 points.append({'t_ms':r['t_ms']-2120,'scale_percent':round(scale*100,3),'group_center':[round(r['icon_center'][0]-40.5*scale,3),round(r['icon_center'][1]+46.5*scale,3)],'ncc':r['template_ncc']})
tracks={
 'measurement_notes':['源动图25fps：单帧40ms。数值是画面测量，不是原作者工程参数。','应用轨迹仅使用NCC>=0.8的匹配。首次出现前的位置不确定，不作为已测量数据。','Dock线检测受点阵与透视影响，稳定水平段约±2度；最终水平角按0度约束。'],
 'canvas':{'width':360,'height':800},
 'applications':{'source':'f_000019','grid':{'columns':4,'rows':2,'centers_x':[55,138,221,305],'centers_y':[512,606],'icon_size':55},'touch_estimate_frame':53,'stable_frame':61,'measured_points':points,'onset_uncertainty_ms':40,'sidebar_hidden_when_open':True},
 'dock':{'source':'f_000019','keyframes':[{'t_ms':r['t_ms']-2120,'angle_deg':r['dock_angle_deg']} for r in raw if 53<=r['frame']<=61],'stable_top_y':688,'stable_center_y':744,'source_initial_angle_range':[22,26],'video_initial_angle_estimate':23},
 'music':{'source':'f_00001c','tap_frame':6,'stages':[{'name':'weather_exit','frames':[6,11]},{'name':'guide_points_and_slashes','frames':[21,28]},{'name':'cover_line_to_rectangle','frames':[25,34]},{'name':'title_artist_mask_reveal','frames':[29,38]},{'name':'lyric_lines_appear','frames':[35,55]},{'name':'progress_line_and_transport','frames':[40,49]},{'name':'elapsed_time_mask_reveal','frames':[50,65]}],'final_cover_box':[29,113,302,201],'final_title_origin':[30,349],'progress_line':[30,649,331,649],'transport_centers':[[91,710],[182,710],[272,710]]},
 'calendar_to_weather':{'source':'f_000018','tap_frame':6,'stages':[{'name':'calendar_exit','frames':[6,12]},{'name':'arrows_leaf_placeholders','frames':[16,24]},{'name':'forecast_vertical_slit_to_full','frames':[26,32]},{'name':'forecast_nodes','frames':[33,42]},{'name':'air_quality_connectors_and_labels','frames':[25,56]},{'name':'green_strip_sweep','frames':[43,74]}]},
 'loading':{'source':'f_00001a','optional':True,'only_from_home':True,'stages':[{'name':'wallpaper_wash_and_blur','frames':[5,10]},{'name':'corner_brackets','frames':[12,18]},{'name':'logo_and_scan_marks','frames':[19,27]},{'name':'terminal_text_and_progress','frames':[24,55]},{'name':'calendar_build','frames':[55,87]}]},
 'source_urls':{'official_product':'https://www.tgcday.com/h-pd-501.html','official_video':'https://24147003.s21v.faimallusr.com/58/ABUIABA6GAAg9P6DygYoiL_kbg.mp4'},
 'blockers_to_exact_match':['蓝紫原始壁纸：现有视频只显示被时钟、Dock、导航覆盖的局部。','原始字体与应用图标：低分辨率演示不足以确认全部资源。','预报航拍背景与原加载标志矢量：只有合成画面。','设置操作后的全部动画、动态歌词接口和传感器参数未完整演示。','缺目标手机与KLWP运行环境，无法验证原生渲染是否同帧一致。']
}
(base/'analysis/motion-spec.json').write_text(json.dumps(tracks,ensure_ascii=False,indent=2),encoding='utf-8')
# Export measured trajectories into actual Kustom animation definitions.
def key(pos,prop,value):return {'position':round(pos,4),'property':prop,'value':round(value,4),'ease':'NORMAL'}
keys=[]
for p in points:
 t=p['t_ms']/320*100
 keys.extend([key(t,'SCALE_XY',p['scale_percent']),key(t,'X_OFFSET',(p['group_center'][0]-180)*2),key(t,'Y_OFFSET',(p['group_center'][1]-559)*2)])
# Non-observed launch segment is explicitly labelled, not included in the measured track.
keys.extend([key(0,'OPACITY',0),key(25,'OPACITY',100),key(0,'SCALE_XY',0),key(0,'X_OFFSET',500),key(0,'Y_OFFSET',-250)])
app_anim={'type':'FORMULA','formula':'$gv(page)=2$','action':'ADVANCED','anchor':'MODULE_CENTER','duration':3.2,'ease':'NORMAL','animator':sorted(keys,key=lambda x:(x['position'],x['property']))}
dockkeys=[]
for r in raw:
 if 53<=r['frame']<=61:
  t=(r['t_ms']-2120)/320*100;a=r['dock_angle_deg']
  if a is not None:dockkeys.append(key(t,'ROTATE',max(a,0)))
dockkeys[-1]=key(100,'ROTATE',0)
motions={'applications':app_anim,'dock':{'type':'FORMULA','formula':'$gv(page)=2$','action':'ADVANCED','anchor':'MODULE_CENTER','duration':3.2,'ease':'NORMAL','animator':dockkeys},'music_cover':{'type':'FORMULA','formula':'$gv(page)=4$','action':'ADVANCED','anchor':'MODULE_CENTER','duration':3.6,'delay':7.6,'ease':'NORMAL','animator':[key(0,'SCALE_Y',0),key(100,'SCALE_Y',100)]},'forecast_card':{'type':'FORMULA','formula':'$gv(page)=3$','action':'ADVANCED','anchor':'MODULE_CENTER','duration':2.4,'delay':8,'ease':'NORMAL','animator':[key(0,'SCALE_XY',0),key(1,'SCALE_XY',100),key(1,'SCALE_Y',100),key(100,'SCALE_Y',100)]}}
(base/'src/native-motion-definitions.json').write_text(json.dumps(motions,ensure_ascii=False,indent=2),encoding='utf-8')
# A revision source, not a releasable theme: missing original assets stay explicitly unbound.
p=copy.deepcopy(json.loads(Path('rhine_theme/preset.json').read_text(encoding='utf-8')))
g=p['preset_root']['globals_list'];g['prev']={'index':43,'type':'TEXT','title':'前一个页面','value':'0'};g['load']['value']='0';g['loading']['value']='$gv(load)=1 & gv(prev)<=2 & gv(page)>=3 & gv(page)<=5 & df(S)-gv(start)<2$'
for k in ['wall','cover','scene']:g[k]['value']='';g[k]['description']='待取得原始素材；不得使用生成图片或截图冒充原资源'
root=p['preset_root']['viewgroup_items']
for item in root:
 title=item.get('internal_title','')
 if title.startswith('08 应用页'):item['internal_animations']=[app_anim];item['internal_title']='08 应用页：待按4列2行重排，已测量轨迹'
 if title.startswith('10 斜向Dock'):item['internal_animations']=[motions['dock']]
 if title.startswith('09 菱形功能侧栏'):
  item['internal_formulas']['config_visible']='$if(gv(page)<=1,ALWAYS,REMOVE)$'
def update_events(v):
 if isinstance(v,dict):
  ev=v.get('internal_events',[])
  if any(e.get('action')=='SWITCH_GLOBAL' and e.get('switch')=='page' for e in ev):
   ev.insert(0,{'type':'SINGLE_TAP','action':'SWITCH_GLOBAL','switch':'prev','switch_text':'$gv(page)$'})
  for x in v.values():update_events(x)
 elif isinstance(v,list):
  for x in v:update_events(x)
update_events(p)
p['preset_info']['title']='Rhine UI reconstruction — WIP, not 1:1 verified';p['preset_info']['description']='返工源稿；原始图像未绑定；未打包为成品。应用重排、局部动画和真机验证仍待完成。'
(base/'src/preset-revision-wip.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
print('Saved measured motion spec and Kustom animation definitions. No finished-theme claim.')
