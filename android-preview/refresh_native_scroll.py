from rebuild_ui import run
from pathlib import Path
import json,time
key='pref_key_wallpaper_screen_scrolled_span'
previous=run('shell','settings','get','secure',key).decode().strip()
Path('rhine_exact/output/dock-phone-fix-20260914/scroll-setting-before.json').write_text(json.dumps({'namespace':'secure','key':key,'value':previous}),encoding='utf8')
try:
 run('shell','settings','put','secure',key,'0');time.sleep(.4)
finally:
 run('shell','settings','put','secure',key,'1')
run('shell','input','swipe',1040,1160,160,1160,700);time.sleep(.6)
print('Refreshed scroll setting; final value',run('shell','settings','get','secure',key).decode().strip())
