from rebuild_ui import run
for line in run('shell','dumpsys','wallpaper').decode(errors='replace').splitlines():
 if any(v in line for v in ['mWallpaperComponent','mNextWallpaperComponent','mName=','mWidth=','mHeight=','mWallpaperInfo','mXOffset','mXStep']):print(line)
