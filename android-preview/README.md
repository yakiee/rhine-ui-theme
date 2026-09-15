# 安卓主题预览环境

Google 官方 Android Emulator，Android 11（API 30），720×1600 竖屏，4GB 内存。

启动入口：`Start-Rhine-Preview.cmd`。首次启动和初始化比后续启动慢。

Windows 虚拟化平台组件已启用，WHPX 加速检查通过；本次开机已成功启动安卓，没有执行重启。

KLWP 官方 AOSP 广告版安装包：`apps/KLWP-aosp.apk`。
主题返工包：工作区 `rhine_exact/output/native-theme-v0.2/Rhine-UI-native-v0.2-unfinished.klwp`。

本环境只用于主题预览与调试。当前主题尚不完整，首页壁纸和应用图标未绑定；空缺不是模拟器故障。

KLWP 已安装，工作目录为安卓内部存储的 Kustom。主题在 KLWP 的 Library 中，名称为 Rhine UI — native theme revision 0.2 (unfinished)。

## 2026-09-08 实际运行结果

安卓模拟器和 KLWP 已安装并启动，桌面快捷方式为“莱茵主题预览”。使用软件渲染及 GLES 3 支持，KLWP 禁用并行渲染。当前预设已导入并设为动态壁纸，61 个根图层被读取。

修复了主题分组缩放循环导致的零缩放。实际桌面仍存在多个页面叠加、动画状态异常，以及默认启动器控件遮挡，未通过视觉和交互验收。原壁纸和应用图标尚未绑定。此版本供继续调试，不能视为莱茵 UI 一比一成品。

记录：`logs/app-setup.json`；实际安卓截图：`logs/theme-on-desktop.png`。
