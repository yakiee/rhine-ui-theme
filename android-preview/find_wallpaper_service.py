from rebuild_ui import run
text=run('shell','dumpsys','package','org.kustom.wallpaper.huawei').decode(errors='replace')
lines=text.splitlines()
for i,line in enumerate(lines):
 if 'android.service.wallpaper.WallpaperService' in line:
  print('\n'.join(lines[max(0,i-2):i+9]))
