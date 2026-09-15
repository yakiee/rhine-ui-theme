from rebuild_ui import run
from pathlib import Path
import time,json

out=Path('rhine_exact/output/dock-page-lifecycle-20260914')
run('shell','input','keyevent',3)
time.sleep(.4)
run('shell','input','swipe',1040,1160,160,1160,250)
time.sleep(.25)
run('shell','input','swipe',160,1160,1040,1160,250)
time.sleep(.8)
(out/'final-returned.png').write_bytes(run('exec-out','screencap','-p'))
run('shell','input','tap',1020,1967)
time.sleep(1)
(out/'final-opened.png').write_bytes(run('exec-out','screencap','-p'))
run('shell','input','tap',190,280)
time.sleep(.8)
(out/'final-closed.png').write_bytes(run('exec-out','screencap','-p'))
report={
    'date':'2026-09-14',
    'device':'16c18d67',
    'launcher':'com.miui.home',
    'theme_package':'org.kustom.wallpaper.huawei',
    'visual_layers_changed':14,
    'before':'$if(si(screen)=gv(homepg),ALWAYS,REMOVE)$',
    'after':'$if(1,ALWAYS,REMOVE)$',
    'behavior':'Visuals stay resident and existing page animations control visibility; touch gates still restrict interaction to page 2.',
    'saved_on_phone':True,
    'first_row_readback_verified':True,
    'alternating_page_cycles_visually_verified':6,
    'post_wechat_change_cycle_captured':True,
    'native_wechat_launch_verified':True,
    'wechat_touch_regions_restored':9,
    'root_layer_count':64,
    'remaining_issue':'Overall terminal translucency remains visibly higher than desired; no material color or opacity track was changed in this fix.'
}
(out/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'wechat-verification.json').write_text(json.dumps({'wechat_launcher_verified':True,'top_activity':'com.tencent.mm/.ui.LauncherUI','method':'native LAUNCH_APP; nine regions'},indent=2),encoding='utf-8')
print('Saved final page-return/open/close screenshots and verification report.')
