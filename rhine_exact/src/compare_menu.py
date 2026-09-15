from pathlib import Path
import sys,json,subprocess,bisect
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path('rhine_exact/tools').resolve()));import cv2
out=Path('rhine_exact/output/comparison-v0.4')
pts=json.loads((out/'current-frame-times.json').read_text());v=cv2.VideoCapture('rhine_exact/output/perspective-v0.4/interaction-preview.mp4');current=[]
while True:
 ok,a=v.read()
 if not ok:break
 current.append(Image.fromarray(cv2.cvtColor(a,cv2.COLOR_BGR2RGB)).crop((0,36,540,1164)).resize((360,800)))
v.release();refs=[Image.open(f'rhine_exact/analysis/frames/f_000019/{i:03d}.png').convert('RGB') for i in range(39)]
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',21);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',15)
ffmpeg='C:/Users/yakieewang/.codex/skills/video-batch-download/tools/ffmpeg-9.0.1-essentials_build/bin/ffmpeg.exe'
proc=subprocess.Popen([ffmpeg,'-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','744x900','-r','25','-i','-','-c:v','libx264','-crf','20','-preset','fast','-movflags','+faststart','-pix_fmt','yuv420p',str(out/'menu-opening-comparison.mp4')],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
# Align the first visible terminal panel: reference 0.24s, current capture 1.170s.
# Repeated source frames preserve recorded cadence; no invented intermediate frames.
for mode,speed,length in [('原速',1,2.4),('半速',.5,4)]:
 for i in range(round(length*25)):
  elapsed=min(i/25*speed,1.52);ref=refs[min(38,int(elapsed/.04))]
  desired=.93+elapsed;idx=max(0,bisect.bisect_right(pts,desired)-1);cur=current[idx]
  canvas=Image.new('RGB',(744,900),'#F3F4F5');d=ImageDraw.Draw(canvas)
  d.text((12,12),'原主题参考动图',font=font,fill='#15181C');d.text((385,12),'当前 v0.4 模拟器',font=font,fill='#15181C')
  d.text((12,43),f'{mode} · 按终端面板首次可见时刻对齐',font=small,fill='#575E65')
  canvas.paste(ref,(8,77));canvas.paste(cur,(376,77))
  d.text((12,879),'已排除模拟器状态栏；比例归一化，非像素级重合',font=small,fill='#575E65')
  proc.stdin.write(canvas.tobytes())
proc.stdin.close();errors=proc.stderr.read();assert proc.wait()==0,errors
metrics={'canvas':[360,800],'normalization':'reference GIF already normalized; current screen excludes y<48 and y>=1552, resized to 360x800','reference_frame':28,'reference_time_s':1.12,'terminal_visible_width_px':{'reference_at_least':226,'current':167,'current_narrower_percent':26.1},'search_visible_width_px':{'reference':99,'current':70},'settings_visible_width_px':{'reference':120,'current':102},'terminal_top_y':{'reference':229,'current':214},'bottom_row_bottom_y':{'reference':521,'current':475},'precision_note':'Threshold-derived visible bounds; source is compressed, terminal right edge is cropped. Approximate comparison, not preset parameters.','motion_alignment':{'reference_first_panel_s':.24,'current_first_captured_panel_s':1.170,'current_recording_frame_spacing_s':.117,'caveat':'Recorded emulator motion has about 117ms between frames in this segment; do not infer sub-frame easing from this recording.'}}
(out/'comparison-measurements.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf8')
report='''# 原主题与 v0.4 效果比对

结论：主菜单的透视方向已接近参考，但尺寸、布局和组件分层动画仍有明显差异，不能算一比一还原。

## 比对依据

1. 用户提供的小红书视频：约 2.2–3.3 秒展示 Dock 主菜单，约 4.4–4.95 秒展示应用页，约 6.05 秒开始进入天气页。
2. 原主题清晰动图 f_000019：用于排除实拍手机倾斜影响，并查看主菜单逐层展开。静止画面对比选第 28 帧（1.12 秒）。
3. 当前 v0.4 的实际模拟器截图和录屏。

左右对比图 menu-side-by-side.jpg；逐帧展开图 menu-motion-frames.jpg；对齐动画 menu-opening-comparison.mp4，先原速后半速。

## 当前最明显的差异

| 项目 | 参考效果 | 当前 v0.4 | 影响 |
| --- | --- | --- | --- |
| 菜单尺寸 | 终端卡可见宽度至少 226 px，右侧超出画面 | 167 px | 当前窄约 26%，视觉分量偏小 |
| 菜单位置 | 终端顶部 y≈229，下方按钮结束 y≈521 | 顶部 y≈214，下方结束 y≈475 | 当前整体偏上，下方展开范围明显偏短 |
| 透视关系 | 搜索与设置可见宽度约 99 / 120 px | 70 / 102 px | 当前左侧被压得更窄，不能只再统一放大 |
| 主菜单展开 | 面板先出现，文字、小图标、数字分批进入；下方按钮陆续展开 | 文字与面板被放在同一动画组缩放，终端先变成窄条再撑开 | 分层与进入轨迹不一致，是主要动效差异 |
| 终端内容 | 有设备轮廓、状态小图标、较粗的标题和小标签 | 设备轮廓与部分图标缺失，文字更细，信息密度较低 | 即便对齐外框，也仍会显得不同 |
| 支付快捷栏 | 独立的深色标题条、细边和分区 | 基本为整块蓝色平板加白字 | 层次较少 |
| 首页其他部分 | 原图中人像更靠前、时钟更大，侧栏和底部点阵另有比例 | 临时重建壁纸与组件比例有差异 | 整体观感仍不同 |

所有像素尺寸均在 360×800 归一画布上统计。当前截图去掉系统状态栏与导航栏后归一；原动图有压缩和裁切，以上为可见边界约测，不是原作者参数。参考终端卡右侧被裁切，因此 226 px 是可见宽度下限。

## 动画判断的边界

原参考动图每帧 40 ms。当前录屏在展开段相邻帧约隔 117 ms，只能判断明显的进入顺序和轨迹，不能从该录屏精确推断更细的缓动曲线。对比视频以终端面板首次可见时刻对齐，保留原录屏帧，不做补帧；所以不能把左右流畅度差异完全归因于主题本身。

## 后续修改顺序

1. 先按参考对齐整组菜单的投影、各列宽度与纵向范围。
2. 把终端、搜索、设置、支付栏拆成底板、文字、数字、图标等独立可动画层。
3. 按参考逐帧设置各层的开始时间和展开方向，再复核收起过程。
4. 补齐设备轮廓、状态图标、标题条、字体与间距。

本轮完成比对与差异记录，未修改 v0.4 主题。
'''
(out/'效果比对.md').write_text(report,encoding='utf8',newline='\n')
print('Comparison video, measurements and report saved.')
