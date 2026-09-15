import time
import re
import xml.etree.ElementTree as ET
from rebuild_ui import run

def tree():
    run('shell', 'uiautomator', 'dump', '/sdcard/rhine-performance-ui.xml')
    return ET.fromstring(run('shell', 'cat', '/sdcard/rhine-performance-ui.xml'))

def tap_label(label):
    root = tree()
    node = next(n for n in root.iter('node') if n.get('text') == label)
    x1, y1, x2, y2 = map(int, re.findall(r'\d+', node.get('bounds')))
    run('shell', 'input', 'tap', (x1+x2)//2, (y1+y2)//2)
    time.sleep(.7)

run('shell', 'am', 'start', '-W', '-n', 'org.kustom.wallpaper.huawei/org.kustom.app.OnBoardingActivity')
time.sleep(.8)
activity = run('shell', 'dumpsys', 'activity', 'activities').decode(errors='replace')
assert any('topResumedActivity' in line and 'LoaderActivity' in line for line in activity.splitlines())
run('shell', 'input', 'tap', '1128', '212')
time.sleep(.6)
tap_label('应用设置')
tap_label('高级选项')
tap_label('屏幕刷新率')
print('Opened refresh rate choices without changing the selected value')
