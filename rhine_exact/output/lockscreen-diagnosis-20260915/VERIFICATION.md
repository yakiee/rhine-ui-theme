# 月球锁屏恢复验证

日期：2026-09-15。

- 恢复前：主屏幕为 KLWP；锁屏为 MiuiKeyguardPictorialWallpaper，配置仍标记 super_wallpaper。用户报告锁屏黑底。
- 通过系统动态壁纸列表打开“月球超级壁纸”，预览正常。
- 在系统“设置壁纸”选择框中选择“锁定的屏幕”，未选择主屏幕或两者。
- 恢复后主屏幕 id=34，仍为 org.kustom.wallpaper.huawei/org.kustom.wallpaper.WpGLService。
- 恢复后锁屏 id=35，mWhich=2、SET_LIVE，组件为 com.miui.miwallpaper.moon/com.miui.miwallpaper.moon.superwallpaper.MoonSuperWallpaper。
- 实际熄屏、亮屏后已看到月球锁屏背景和时钟，黑底问题修复。
- lock_screen_allow_private_notifications 仍为 0。没有执行修改私人通知显示的操作；此前自动审批拒绝该修改，待用户明确同意。
- 系统快捷 CHANGE_LIVE_WALLPAPER 入口未成功打开月球预览；从 LIVE_WALLPAPER_CHOOSER 列表点击成功。退出原因未确认。

配置证据：wallpaper-after-moon-lock.txt。视觉验证：moon-lock-verified.png（包含锁屏系统提示和媒体控件，仅用于本地验证）。
