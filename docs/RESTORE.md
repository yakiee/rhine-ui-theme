# 在另一台电脑继续修改

## 同一部手机，换电脑

1. 克隆私有仓库，然后在 Codex 中打开仓库文件夹。
2. 安装 Python（原环境为 3.12）和 Git。布局脚本按需安装 `requirements-theme.txt`；不要复制原电脑整个运行库。
3. 如需操作手机，将 Android Platform Tools 解压到 `android-preview/sdk/platform-tools/`。剪贴板同步还需要官方 scrcpy 4.1 的 `scrcpy-server-v4.1`，放到 `android-preview/scrcpy/`。当前控制协议按该版本实现，不能随意换服务端版本。
4. 连接手机并在手机上允许本电脑 USB 调试。不要导入旧预设覆盖手机正在运行的主题。
5. 共享辅助模块支持 `RHINE_ADB` 和 `RHINE_DEVICE_SERIAL` 环境变量。新电脑先设置这两项，再检查待运行脚本是否还有独立写死的路径、设备号及坐标。历史脚本并非通用安装器。
6. 先读取当前状态，明确将替换哪个组件，再做局部修改和验证。不要按文件名顺序批量运行历史修复脚本。

PowerShell 配置示例（替换为自己的路径和 `adb devices` 显示的设备号）：

```powershell
$env:RHINE_ADB = 'D:\Android\platform-tools\adb.exe'
$env:RHINE_DEVICE_SERIAL = '你的设备号'
python tools/check_backup.py
```

原验证环境：Xiaomi 17 Ultra，HyperOS 3.0.309，1200×2608，4 页原生桌面，第 2 页为主题页；KLWP Huawei 3.82b610514huawei。其他屏幕尺寸、桌面版本和应用包名须重新校准。

## 当前配置的优先级

`rhine_exact/CURRENT_PHONE_THEME.md` 顶部记录 > 最近 VERIFIED.md > 历史导出包。

| 部分 | 当前来源，相对 `rhine_exact/output/` |
| --- | --- |
| root 3 侧工具栏视觉 | `dock-toolbar-motion-20260915/root-3-after.clip.txt` |
| root 51 五项点击区域 | `open-dock-swipe-20260915/toolbar-touch-with-latch.clip.txt` |
| page 全局变量 | `open-dock-swipe-20260915/page-with-native-latch.clip.txt` |
| 页码变化流程 | `open-dock-swipe-20260915/page-flow-unconditional.clip.txt` |
| root 1、23、24 底条的 Dock 动画 | `dock-toolbar-motion-20260915/root-{1,23,24}-dock-after.clip.txt` |
| 顶部系统时间栏背景遮罩 | `system-statusbar-contrast-20260915/top-scrim.clip.txt` |
| 完整旧基底 | `hyperos-klwp-v0.13.51/Rhine-UI-HyperOS-v0.13.51.klwp` |

上表不是全部历史补丁的自动安装顺序；根编号是原始逻辑编号，经过移动后不等于列表位置。当前根顺序：原 0..63 去掉 3、50、51，末尾追加 50、64、3、51，共 65 项。按标题和内容辨认，避免按当前序号覆盖错误组件。

原生 `docklive` 开关在手机上手动创建，尚未保存其原生剪贴板 JSON。已确认参数：

- 类型：On/Off，默认关闭。
- 自动开启：手动；自动关闭：手动和公式。
- 自动关闭公式：`$si(screen)!=gv(homepg) | gv(view)=0 | si(visible)=0$`。
- 原 root 51 最后一项已有打开动作后追加切换 `docklive`。
- `view=1`、`docklive=0`、`page=0` 是合法关闭状态。

## 空白手机或手机数据丢失

当前仓库提供可重建的素材、基底与修改记录，但**尚没有包含所有实机修改的完整导出，也没有经过验证的一键恢复流程**。需要在官方允许的编辑能力内重建并逐项核对；仓库本身不会解除 KLWP Pro 的导入限制。

`android-preview/rebuild_prepare.py` 可从保存的旧基底提取字体、位图和初始全局配置，它不包含后续全部手机修改。重新绑定庄方宜背景和终端封面、补齐当前组件及原生开关后才能验证，不能只导入基底就视为恢复完成。

## 验证与已知问题

- 分别检查第二页工具栏、打开 Dock、向两侧翻页、快速往返和从 App 返回。
- 检查电话、信息、浏览器、相机，以及 Dock 内各 App 的实际包名。
- 保存主题后曾出现动画整体半透明的运行状态异常。已验证的恢复方式是最终保存后重新加载当前 KLWP **主屏幕**壁纸，然后不再进入编辑器保存，完成桌面验证。
- 锁屏必须保留独立月球超级壁纸；不要将 KLWP 同时应用到锁屏。
- `.clip.txt` 是原生编辑组件，不是 APK，也不是绕过付费限制的安装包。

## 仓库和原电脑的区别

仓库不包含模拟器、SDK、安装器、第三方运行库、原始视频、屏幕转储和调试录屏。历史构建脚本可能依赖未保留的前一版 `.klwp` 或原电脑路径，不能假定每个历史版本都能直接重新构建。继续维护当前主题时，使用当前配置来源和对应模块。

尚未验证：在全新电脑、全新手机上的端到端恢复。可在另一台电脑克隆后先运行离线完整性检查，再连接仍保留主题的手机接手。
