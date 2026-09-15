import contextlib,io,json
from pathlib import Path
from toolbar_native import tree,click,run
raw=run('shell','dumpsys','activity','activities').decode(errors='replace')
assert any('topResumedActivity' in s and 'com.miui.home/' in s for s in raw.splitlines())
run('shell','input','keyevent',3)
with contextlib.redirect_stdout(io.StringIO()):exec(Path('android-preview/open_current_editor.py').read_text(encoding='utf-8'))
module={'internal_type':'OverlapLayerModule','internal_title':'SWIPE DIAGNOSTIC REMOVE','position_anchor':'TOP','position_offset_y':105,'viewgroup_items':[{'internal_type':'ShapeModule','shape_type':'RECT','shape_width':620,'shape_height':42,'paint_color':'#FF101010'},{'internal_type':'TextModule','text_expression':'S=$si(screen)$ H=$gv(homepg)$ P=$gv(page)$ V=$gv(view)$ $df(ss)$','text_size':23,'paint_color':'#FFFFFFFF'}]}
path=Path('rhine_exact/output/open-dock-swipe-20260915/diagnostic.clip.txt');path.write_text('##KUSTOMCLIP##\n'+json.dumps({'clip_version':1,'clip_modules':[module]})+'\n##KUSTOMCLIP##',encoding='utf-8')
run('push',path.resolve(),'/data/local/tmp/rhine-editor-input.txt')
run('shell','CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar:/data/local/tmp/rhine-theme-input.zip app_process / ThemeClipboard KUSTOM_MODULES /data/local/tmp/rhine-editor-input.txt')
click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_paste')))
click(next(n for n in tree().iter('node') if n.get('resource-id','').endswith('/action_save')))
run('shell','input','keyevent',3);run('shell','am','force-stop','org.kustom.wallpaper.huawei')
run('shell','am','start','-W','-a','android.service.wallpaper.CHANGE_LIVE_WALLPAPER','--ecn','android.service.wallpaper.extra.LIVE_WALLPAPER_COMPONENT','org.kustom.wallpaper.huawei/org.kustom.wallpaper.WpGLService')
exec(compile(Path('android-preview/apply_saved_home_wallpaper.py').read_text(encoding='utf-8'),'apply-home','exec'))
print('Temporary live page diagnostic applied')
