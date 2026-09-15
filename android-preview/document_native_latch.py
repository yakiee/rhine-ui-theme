from pathlib import Path
path=Path('rhine_exact/CURRENT_PHONE_THEME.md')
previous=path.read_text(encoding='utf-8')
note='''# 最新：Dock 打开时翻页逻辑已改为原生自动关闭开关

2026-09-15 晚间更新。优先阅读 `output/open-dock-swipe-20260915/VERIFIED.md`。

- 新增原生 On/Off 全局 `docklive`，离开第 2 页、view=0 或离开桌面时自动关闭。
- `page` 的终端分支由 `docklive` 控制；`view=1`、`docklive=0`、`page=0` 是合法的关闭状态。
- 当前 root 51 点击模块：`output/open-dock-swipe-20260915/toolbar-touch-with-latch.clip.txt`。
- 当前 page 公式：同目录 `page-with-native-latch.clip.txt`。page 全局替换后可能在全局列表末尾，须按名称查找。
- root 3 和底条动画仍使用下面记录的 dock-toolbar-motion 版本。
- 当前根模块顺序（原编号）：原 0..63 去掉 3、50、51 后，末尾为 50、64、3、51；共 65 项。
- 临时诊断和所有监测补丁已移除，root 0 背景组恢复单个位图子项。
- 最终四轮双向/快速翻页均通过；最后录像 `output/open-dock-swipe-20260915/after-native-latch.mp4`。
- 月球锁屏保留；最后已重新加载主屏幕 KLWP，并在验证后保持没有再进入编辑器。

---

'''
if not previous.startswith('# 最新：Dock 打开时翻页逻辑'):
    path.write_text(note+previous,encoding='utf-8')
print('Documented native Dock latch and final on-device verification')
