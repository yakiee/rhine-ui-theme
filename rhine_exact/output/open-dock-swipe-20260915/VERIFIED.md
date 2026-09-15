# Dock 打开时翻页：最终实机状态

2026-09-15，设备 16c18d67，原生澎湃桌面，主题页为第 2 页。

## 已复现的问题

原配置依靠背景滚动轨道淡出 Dock，但打开状态可能继续保留；滑回主题页会重新出现 Dock，底条和侧工具栏恢复也受到影响。仅修改流程触发或增加刷新监测，在多轮实测中均有漏关，不能作为有效修复。

## 最终修改

- 在 KLWP 原生全局变量界面创建 `docklive`，类型为 On/Off 开关。自动开启：手动；自动关闭：手动和公式。公式为 `$si(screen)!=gv(homepg) | gv(view)=0 | si(visible)=0$`。默认关闭。
- `page` 仅在 `view=1`（终端）时读取 `docklive`，其余内部页面仍使用原来的 `view`：`$if(si(screen)!=gv(homepg),-1,gv(origin)=si(screen) & gv(view)>0,if(gv(view)=1,gv(docklive),gv(view)),0)$`。
- 侧工具栏最后一项原有打开动作后，增加一次 `SWITCH_GLOBAL docklive`。电话、信息、浏览器、相机跳转配置未改。
- 原 PageSync 流程已改成页码变化写入 `view=0`，但 Dock 的关闭不再只依赖这个流程。
- 底条三层的 Dock 动画、背景滚动几何、侧工具栏缩放淡出参数保持上一轮版本。
- 临时可见诊断条、透明监测模块以及壁纸后方的监测文字均已移除；背景组恢复为原来的单张位图子项。

注意：以后 `view=1` 而 `docklive=0`、`page=0` 是已经关闭 Dock 的有效状态，不能仅凭 `view` 判断残留。

## 关键文件

- 当前终端入口点击模块：`toolbar-touch-with-latch.clip.txt`（原 root 51）。
- 当前 page 全局变量：`page-with-native-latch.clip.txt`。
- 页码流程：`page-flow-unconditional.clip.txt`。
- `docklive` 为通过原生界面创建的开关，参数见上；尚未单独复制其原生剪贴板 JSON。
- 变更完成记录：`latch-install-state.json`。

旧的 tick、unconditional、watcher、occluded 测试目录保留用于排查，其中存在失败案例，不是最终结果。

## 验证

最终保存后重新加载 KLWP 主屏幕壁纸，确认月球超级壁纸仍作为独立锁屏。验证期间没有再打开编辑器。

- `native-latch/*-opened.png`：四轮翻页前均确认 Dock 已经打开。
- `native-latch/*-returned.png`：左/右普通翻页及左/右快速往返四轮，返回后均为 Dock 关闭、侧工具栏和底条完整恢复。
- `native-latch/partial-cancelled.png`：小幅拖动后也收起 Dock，未出现残留按钮。
- `after-native-latch.mp4`：最终打开 Dock 后滑走并返回的录像；Dock 消退后未在返回时重新弹出，底条和工具栏恢复。
- `after-native-latch-returned.png`：最后一次复测的返回状态；手机留在第 2 页，Dock 关闭。

此验证覆盖上述操作，不代表已测量全部帧率或所有系统生命周期情况。
