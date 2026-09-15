from pathlib import Path
source=Path('android-preview/repair_open_dock_page_flow.py').read_text(encoding='utf-8')
source=source.replace("'org.kustom.wallpaper.huawei/' in s for s", "('org.kustom.wallpaper.huawei/' in s or 'com.miui.home/' in s) for s")
source=source.replace("assert flow['t'][0]['params']['formula']=='$si(screen)$'", "assert flow['t'][0]['params']['formula']=='$if(gv(view)>0,si(screen)+\":\"+df(ss),\"idle\")$'")
source=source.replace("'page-flow-before.clip.txt'", "'page-flow-tick-trial.clip.txt'")
source=source.replace("flow['t'][0]['params']['formula']='$if(gv(view)>0,si(screen)+\":\"+df(ss),\"idle\")$'", "flow['t'][0]['params']['formula']='$si(screen)$'\nflow['a'][0]['params']['formula']='0'")
source=source.replace("'page-flow-after.clip.txt'", "'page-flow-unconditional.clip.txt'")
source=source.replace('Saved page flow with active-Dock time dependency;', 'Saved unconditional page-change exit;')
exec(compile(source,__file__,'exec'))
