from pathlib import Path
import json
out=Path('rhine_exact/output/dock-phone-fix-20260914')
report={
 'date':'2026-09-14','device_serial':'16c18d67','launcher':'com.miui.home',
 'wallpaper':'org.kustom.wallpaper.huawei/org.kustom.wallpaper.WpGLService',
 'cause':'Dock root and touch targets require si(screen)==gv(homepg). Phone kept fixed homepg=2 while HyperOS reported si(screen)=1, including native page 3 of 4. Global page evaluated to -1, removing Dock.',
 'phone_change':{'global':'homepg','before':'2','after':'$si(screen)$'},
 'authorization':'User chose stable Dock access on all HyperOS pages; defer native page integration.',
 'saved_on_phone':True,'root_layers':64,'diagnostic_formula_saved':False,
 'verification':{'native_page_2':'Dock visible','native_page_3':'Dock visible; overlapped by launcher shortcuts','native_page_4':'screenshot captured','terminal_open':'opened using Dock, Dock hides intentionally','terminal_return':'Dock restored','return_from_system_settings':'Dock visible'},
 'limitations':['KLWP compatibility configuration, not a native MAML migration.','Launcher icons/widgets remain above wallpaper and may obscure/intercept Dock.','Theme is not limited to a single desktop page in this profile.'],
 'rollback':'In KLWP Globals, set homepg back to 2 and save when using a launcher that provides page offsets. Do not restore 2 on this HyperOS setup unless intentionally restoring the previous behavior.'
}
(out/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
(out/'修复记录.md').write_text('''# 侧边工具条消失修复\n\n2026-09-14，已直接保存到手机现有 KLWP 免费编辑主题。系统桌面仍为澎湃。\n\n原因：工具条及点击区域依赖固定主页编号 2，但澎湃桌面传给 KLWP 的页码为 1，主题 page 结果为 -1，整组被隐藏。实际第三页也复现了这个页码不匹配。\n\n按用户选择，将全局 homepg 从 `2` 改为 `$si(screen)$`，允许工具条在各桌面页工作。未修改素材、工具条动画或按钮。原工具条备份见 dock-before.clip.txt。\n\n已验证：第二页显示、第三页显示、四宫格打开终端、返回终端后恢复、从系统设置返回后显示。第四页截图已留存。原生图标、小组件覆盖壁纸时仍会挡住工具条或拦截点击。\n\n这是 KLWP 兼容修复，未完成 MAML 原生移植，也不再保证只在某一桌面页显示。后续改用支持翻页的桌面时，可把 homepg 恢复为 2；澎湃原生方案应另做翻页进度接入。\n''',encoding='utf8')
status_path=Path('rhine_exact/output/free-editor-rebuild/sync-status.json')
s=json.loads(status_path.read_text(encoding='utf8'))
s.update({'flow':'Native flow inserted and round-trip verified in prior sync','saved_and_reopened':'Verified 64 root layers on 2026-09-14','applied_to_wallpaper':True,'current_phone_compatibility':report['phone_change'],'current_launcher':'com.miui.home','last_verified':'2026-09-14'})
status_path.write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf8')
print('Saved fix and rollback records')
