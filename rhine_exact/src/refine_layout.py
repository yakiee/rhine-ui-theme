from pathlib import Path
import json,math
base=Path('rhine_exact');p=json.loads((base/'src/preset-revision-wip.json').read_text(encoding='utf-8'))
# Header reference: thin return construction and tabs at measured baseline, not a Unicode arrow.
for g in p['preset_root']['viewgroup_items']:
 name=g.get('internal_title','')
 if name.startswith('12 返回'):
  def move(v):
   if isinstance(v,dict):
    if isinstance(v.get('position_offset_y'),(int,float)) and v.get('internal_type') in ['TextModule','ShapeModule','BitmapModule']:v['position_offset_y']+=40
    for x in v.values():move(x)
   elif isinstance(v,list):
    for x in v:move(x)
  move(g)
  g['viewgroup_items']=[n for n in g['viewgroup_items'] if n.get('text_expression')!='←']
  ev=[{'type':'SINGLE_TAP','action':'SWITCH_GLOBAL','switch':'prev','switch_text':'$gv(page)$'},{'type':'SINGLE_TAP','action':'SWITCH_GLOBAL','switch':'page','switch_text':'0'}]
  for a,b in [((67,182),(93,154)),((67,182),(191,182))]:
   dx=b[0]-a[0];dy=b[1]-a[1]
   g['viewgroup_items'].append({'internal_type':'ShapeModule','shape_type':'RECT','shape_width':math.hypot(dx,dy),'shape_height':2,'position_anchor':'CENTER','position_offset_x':(a[0]+b[0])/2-360,'position_offset_y':(a[1]+b[1])/2-800,'shape_rotate_mode':'MANUAL','shape_rotate_offset':math.degrees(math.atan2(dy,dx)),'internal_toggles':{'paint_color':10},'internal_formulas':{'paint_color':'$if(gv(dark),#FFF0F0F2,#FF17191C)$'},'internal_events':ev})
 if name.startswith('21 年进度'):g['internal_formulas']['position_offset_y']='$-120*mu(min,si(rwidth)/720,si(rheight)/1600)$'
 if name.startswith('22 日程卡片'):g['internal_formulas']['position_offset_y']='$-96*mu(min,si(rwidth)/720,si(rheight)/1600)$'
 if name.startswith('20 月历'):
  def shrink(v):
   if isinstance(v,dict):
    value=v.get('position_offset_y');yy=value+800 if isinstance(value,(int,float)) else -10000
    if v.get('internal_type') not in ['OverlapLayerModule'] and 339<=yy<=850 and v.get('paint_color')!='#00000000':
     v['position_offset_y']=310+(yy-339)*.79-800
     if v.get('shape_height',0)<100:v['shape_height']=v.get('shape_height',0)*.79
    for x in v.values():shrink(x)
   elif isinstance(v,list):
    for x in v:shrink(x)
  shrink(g)
(base/'src/preset-revision-wip.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
report='''# 一比一还原返工记录

上一版 v0.1 是风格近似，不能算一比一，本轮不继续把它当作合格成品。

## 已重新核对的证据

- 小红书原片 8.7 秒，另外找到了作者公开商品页中的 1080×1920、30fps、9.23秒演示视频。
- 小程序 5 段动图共393帧，已全部展开到固定屏幕坐标，分镜表覆盖每160ms及最后一帧。
- 以小红书蓝紫版本为外观主参照。金色、红色展示仅补充动作，不把不同壁纸版本混用。

## 已纠正的误判

1. 应用页是4列×2行，且打开后侧栏隐去。旧版做成了2列×4行，并且保留侧栏。
2. 白色大分格属于原壁纸，不是主题额外的线框。旧版错误添加了线框。
3. Dock有大面积渐变光带、点阵和电池图标；角度和垂直位置会随应用页一起变化，不能只把一个黑条旋转15度。
4. 控制卡是分阶段展开，文字、背景和遮罩出现时机不同，并存在卡片姿态变化；不是所有部件统一淡入。
5. 音乐封面从细线展开；前面有定位点和斜纹，后续有标题遮罩、歌词和播放控制的不同阶段。
6. 天气卡从中间窄条展开，空气质量连线和标签分批出现；详情为卡内右侧遮罩。
7. 功能页之间切换不重复全屏加载。全屏加载是可选的首页入口效果，视频里使用的配置也不同。
8. 月历、年进度和日程卡的纵向位置在旧版偏低，已经重新按画面测量修订源稿。

## 已完成的具体返工

[应用动画测量对照](../output/app-motion-calibration.gif) 左侧是原始动图，右侧是测量图，不是运行中的新主题。低置信度的检测被排除。可靠匹配段的相关系数约0.82–0.97；这仅表示图标定位可靠，不能当作整体还原相似度。

[动画参数表](motion-spec.json) 记录每个动作的来源帧、阶段、位置与不确定性。[原生动画定义](../src/native-motion-definitions.json) 把测得的应用缩放、位移和Dock角度写成了Kustom关键帧。[返工源稿](../src/preset-revision-wip.json) 已改为4×2图标位、修正侧栏和加载状态、去除错误边框，并调整功能页布局。源稿尚未打包为成品。

## 当前仍未达到一比一

原视频提供的是合成后的有限角度画面。原始蓝紫壁纸的被遮挡部分、完整字体和图标资源、航拍背景、加载标志原矢量、未展示的设置切换与传感器参数，尚未取得或无法确认。返工源稿已清空这些未确认的壁纸/图标绑定，不再用生成插画或字母图标代替。

本轮也没有安卓/KLWP运行环境可验证原生渲染，尚未完成真实主题与原片的逐帧差异验收。因此，这些资料是返工进度，不是“一比一完成”的交付。

精确的源代码和完整原资源无法从这些视频唯一反推；可继续重建可见部分，但不能将推测的未展示细节称为严格一致。

公开补充来源：[糖果城莱茵UI商品页](https://www.tgcday.com/h-pd-501.html)。
'''
(base/'analysis/reconstruction-status.md').write_text(report,encoding='utf-8',newline='\n')
print('Saved corrected native source and explicit one-to-one acceptance gaps.')