from rebuild_ui import run,snapshot
print(run('shell','am','start','-W','-a','android.service.wallpaper.LIVE_WALLPAPER_CHOOSER').decode())
snapshot()
