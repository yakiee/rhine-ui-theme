from rebuild_ui import run,snapshot
print(run('shell','am','start','-W','-a','android.service.wallpaper.CHANGE_LIVE_WALLPAPER','--ecn','android.service.wallpaper.extra.LIVE_WALLPAPER_COMPONENT','org.kustom.wallpaper.huawei/org.kustom.wallpaper.WpGLService').decode())
snapshot()
