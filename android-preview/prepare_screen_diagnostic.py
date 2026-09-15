from pathlib import Path
import json
clip={'clip_version':1,'clip_modules':[{'internal_type':'TextModule','internal_title':'SYNC DIAGNOSTIC REMOVE','text_expression':'S $si(screen)$ / H $gv(homepg)$ / P $gv(page)$','text_size':20,'paint_color':'#FFFFFFFF','position_anchor':'TOP','position_offset_y':160}]}
Path('rhine_exact/output/free-editor-rebuild/phone-clips/diagnostic.clip.txt').write_text('##KUSTOMCLIP##\n'+json.dumps(clip)+'\n##KUSTOMCLIP##',encoding='utf8')
from rebuild_ui import run,snapshot
print(run('shell','am','start','-W','-n','org.kustom.wallpaper.huawei/org.kustom.app.OnBoardingActivity').decode())
snapshot()
