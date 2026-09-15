from rebuild_ui import run
lines=run('shell','logcat','-d','-t','1200').decode(errors='replace').splitlines()
keep=[(i,l) for i,l in enumerate(lines) if any(s in l for s in ['LiveWallpaperChange','WpGLService','WallpaperPreview','FATAL EXCEPTION','Unable to start wallpaper','wallpaper component'])]
for i,l in keep:print(l)
