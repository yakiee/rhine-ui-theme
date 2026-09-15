# 动画优化进度

日期：2026-09-15。

## 已生效

KLWP 高级选项的屏幕刷新率从“默认”改为 120Hz。保留禁用并行渲染=true、直接接触模式=false。设置读回记录：refresh-after.xml。

## 观察

默认与 120Hz 使用相同桌面手势录屏。Dock 在桌面滑动过程中仍有停留后再收起的现象，仅刷新率调整未解决全部问题。视频编码帧间隔不能当作 KLWP 实际渲染帧率；SurfaceFlinger 延迟查询返回全零，不作性能改善量化依据。

## 编辑草稿，尚未保存

原生编辑器预览演示动画已暂停，以稳定控件树读取。

给下列源文件索引对应组各追加了一条原生 SCROLL/ADVANCED 渐隐动画：3、2、4、5、6。该动画基于 CENTER/SCREEN2，center 公式沿用 homepg；OPACITY 从中心页的 0（无额外透明）到滑动 45% 时的 100（透明），其余原动画不改。每组追加记录在 scroll-patches.json，前后 XML 和剪贴板保存在同目录。尚未完成效果验证，不能声称修复完成。

尚需处理：7、8、9、10、11、14、17、18、19。脚本 add_follow_scroll_animation.py 会跳过 scroll-patches.json 中已有项目，按名称定位；若用户切换应用会因页面校验失败停止。2026-09-15 处理 7 时检测页面不符，已停止，随后只读确认前台为淘宝 TMSActivity。已请求用户交回手机，等待回复。

恢复后：打开当前编辑草稿，确保演示暂停，然后继续剩余索引；保存，恢复预览动画，回桌面第二页验证开关、两个方向翻页、回到第二页完整性、纸面透明度。必要时才按已有流程重启并仅重新应用 KLWP 主屏幕。月球锁屏应继续保持独立 MoonSuperWallpaper 组件，避免替换锁屏。

主要脚本：android-preview/add_follow_scroll_animation.py；record_dock_performance.py；analyze_dock_performance_video.py。备份与变更应以手机当前草稿为准，不用旧预设覆盖。
