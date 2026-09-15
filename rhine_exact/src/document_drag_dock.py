from pathlib import Path
base=Path('rhine_exact');out=base/'output/drag-dock-v0.13.50'
s=(base/'output/desktop-dock-fold-v0.13.47/操作说明.md').read_text(encoding='utf-8').replace('v0.13.47','v0.13.50').replace('Rhine-UI-desktop-dock-fold','Rhine-UI-drag-dock')
s=s.replace('黑色底条和光带同步向下收起、转为水平','黑色底条和光带按手指带动的桌面滚动进度同步下移、转平，途中回拉会同步恢复').replace('电量和日期文字隐藏','电量和日期文字随拖动逐渐淡出')
(out/'操作说明.md').write_text(s,encoding='utf-8')
(base/'analysis/当前主题版本.txt').write_text('当前采用 drag-dock-v0.13.50/Rhine-UI-drag-dock-v0.13.50.klwp，已应用模拟器。\n斜条折叠改为原生 SCROLL/ADVANCED 背景滚动驱动，中心 homepg，速度固定100（复杂动画按单屏距离计算），不再使用页码触发的固定时长。\n角度0~23.7度、Y位移0~145随单屏滑动进度线性变化；光带同步计算旋转中心和缩放补偿。底板移到原空闲根图层1；根23显示电量日期并在前40%拖动中淡出；根24是光带。\n原主页左上时钟/机型仍未恢复。终端入口、普通原生应用页、返回逻辑与菜单比例不变。\n实测慢速往返录屏、短距离取消滑动、终端展开收起，均通过；验证视频和截图在本版verification目录。v0.13.48/49为开发中间版本，不使用。\n',encoding='utf-8')
(out/'verification/implementation-notes.md').write_text('# 跟手动画验证\n\n原生背景滚动直接驱动动画进度。独立分离底板与文字层，文字前40%淡出；底板与光带使用相同的中心、速度和线性进度，光带每1%关键帧计算旋转中心补偿。\n\n检查通过：慢速正向/反向录屏、短距离取消滑动、终端打开与返回。原始分别注入 motionevent 的测试触发启动器长按，不能作为停住测试证据；以正确连续事件的慢拖录像和取消滑动结果为准。\n\n参考：[Kustom 原生滚动动画说明](https://docs.kustom.rocks/tags/rules/)。本机 AnimationRule.getAmount 按滚动步长计算复杂动画进度，固定speed=100，不乘桌面页数。\n',encoding='utf-8')
print('Documentation updated')
