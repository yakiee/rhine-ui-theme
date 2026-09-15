from pathlib import Path
import subprocess
from rebuild_ui import run

source = Path('android-preview/scrcpy/ThemeClipboard.java')
text = source.read_text()
if '!label.equals("KUSTOM_ANIMATION")' not in text:
    text = text.replace('!label.equals("KUSTOM_GLOBAL")', '!label.equals("KUSTOM_ANIMATION") && !label.equals("KUSTOM_GLOBAL")')
    source.write_text(text, encoding='utf-8')
subprocess.run(['javac', str(source)], check=True)
subprocess.run(['java', '-cp', 'android-preview/scrcpy/r8-2.2.66.jar', 'com.android.tools.r8.D8', '--output', 'android-preview/scrcpy/rhine-theme-input.zip', 'android-preview/scrcpy/ThemeClipboard.class'], check=True)
run('push', 'android-preview/scrcpy/rhine-theme-input.zip', '/data/local/tmp/rhine-theme-input.zip')
print('Native animation clipboard type enabled')
