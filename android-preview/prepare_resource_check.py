from pathlib import Path
import json
clip={'clip_version':1,'clip_modules':[{'internal_type':'BitmapModule','internal_title':'SYNC RESOURCE CHECK','bitmap_bitmap':'kfile://org.kustom.sdcard/bitmaps/wall-reconstructed.png','bitmap_width':100}]}
Path('rhine_exact/output/free-editor-rebuild/resource-check.clip.txt').write_text('##KUSTOMCLIP##\n'+json.dumps(clip)+'\n##KUSTOMCLIP##',encoding='utf8')
from rebuild_ui import run,snapshot
run('shell','input','swipe',200,2010,1080,2010,350)
run('shell','input','tap',140,2010)
snapshot()
