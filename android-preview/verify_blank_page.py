import json
import time
from pathlib import Path
import xml.etree.ElementTree as ET
from rebuild_ui import run

out = Path('rhine_exact/output/transparent-page2-20260915')
out.mkdir(parents=True, exist_ok=True)

def state(label, page):
    top = run('shell', 'dumpsys', 'activity', 'activities').decode(errors='replace')
    foreground = next(line for line in top.splitlines() if 'topResumedActivity=' in line)
    assert 'com.miui.home/' in foreground, foreground
    run('shell', 'uiautomator', 'dump', '/sdcard/rhine-blank-verify.xml')
    raw = run('shell', 'cat', '/sdcard/rhine-blank-verify.xml')
    root = ET.fromstring(raw)
    descriptions = [node.get('content-desc', '') for node in root.iter('node')]
    current = next(value for value in descriptions if value.startswith('第 ') and '页共' in value)
    assert current == f'第 {page} 页共 4 页', current
    assert not any(node.get('text') == 'Ready' for node in root.iter('node'))
    if page == 2:
        assert 'Transparent Widget' in descriptions
    print(json.dumps({'step': label, 'page': current, 'ready_hidden': True}, ensure_ascii=True), flush=True)

state('before', 2)
run('shell', 'input', 'tap', 165, 280)
run('shell', 'input', 'tap', 165, 280)
time.sleep(.7)
state('double_tap_no_navigation', 2)
run('shell', 'input', 'swipe', 1030, 1100, 180, 1100, 700)
time.sleep(.8)
state('next_page', 3)
run('shell', 'input', 'swipe', 180, 1100, 1030, 1100, 700)
time.sleep(.8)
state('returned', 2)
(out / 'verified-page2.png').write_bytes(run('exec-out', 'screencap', '-p'))
(out / 'VERIFIED.md').write_text('第二页透明占位已完成。\n\n- HyperOS 原生桌面：第 2 页，共 4 页。\n- Transparent Widget 1×1，左上角，无可见文字或图标。\n- 已点击 Ready 完成组件初始化。\n- 双击不跳转；滑至第 3 页再返回，第 2 页及透明组件保留。\n- 原黄色便签组件和辅助应用快捷图标已移除。\n- 未授予相机或设备管理权限。\n', encoding='utf-8')
