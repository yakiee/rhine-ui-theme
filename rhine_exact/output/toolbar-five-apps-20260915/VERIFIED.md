# 静态主题五项工具栏

2026-09-15 已同步到连接的 Xiaomi 17 Ultra（KLWP Huawei）。

## 从上到下

1. 电话：com.android.contacts / TwelveKeyDialer
2. 信息：com.android.mms / MmsTabActivity
3. 浏览器：com.android.browser / launch.SplashActivity
4. 相机：com.android.camera / Camera
5. 打开 Dock：保留现有全局状态操作。

四个应用已逐项启动并只核对前台包名，见 app-verification.json。第五项已验证打开终端 Dock。

## 实际同步的修改

- 原位替换五个工具栏图标为原生矢量路径，统一线宽和视觉大小。
- 前四项直接启动应用，不再从工具栏进入定制天气、音乐、日历页面。
- 图标与点击区使用相同的第二页、Dock 关闭显隐条件。
- 删除工具栏陀螺仪位移及公式透明度动画，避免点击区域漂移和透明度残留。
- 工具栏仅保留一条 SCROLL 缩放动画，幅度 2%；工具栏开关采用整组显隐。
- 底部斜条、其他 Dock 内容、背景、锁屏和系统桌面固定应用均未在本次改动。

## 验证与限制

transition-check.jpg 对照六个状态：工具栏显示、Dock 打开、关闭返回、下一页、返回主题页、Dock 打开时翻页再返回。
可确认工具栏在主题页完整显示、Dock 打开时整组隐藏、其他页隐藏、返回后恢复。最后通过空白处关闭 Dock，将手机留在主题页。

工具栏公式渐隐在当前运行环境复测出现中间透明状态，最终版本明确取消该动画，使用整组显隐；没有声称实现柔和渐隐。未测量帧率或耗电。
现有 Dock 在打开后翻页再回来仍保持打开，这是本轮观察到的原有行为，没有在本次工具栏调整中重写。

## 可恢复资料

- root-3-before.clip.txt / root-51-before.clip.txt：改动前从手机读取的模块备份。
- root-3-final.clip.txt：最终同步的工具栏视觉模块。
- root-51-after.clip.txt：最终同步的五项点击区域。
- 其余 animation clip 为诊断候选，不能当作最终版本使用。
