from pathlib import Path
import json,zipfile
base=Path('rhine_exact');out=base/'output/native-desktop-navigation-v0.13.46';report=[]
for suffix in ('','-off'):
 with zipfile.ZipFile(out/f'Rhine-UI-native-desktop-navigation{suffix}-v0.13.46.klwp') as z:
  assert z.testzip() is None;p=json.loads(z.read('preset.json'))
 r=p['preset_root']['viewgroup_items'];g=p['preset_root']['globals_list']
 assert len(r)==64 and g['homepg']['value']=='2'
 assert 'gv(view)>0' in g['page']['value'] and 'si(screen)-1' not in g['page']['value']
 assert any(e.get('switch')=='view' and e.get('switch_text')=='1' for e in r[51]['viewgroup_items'][6]['viewgroup_items'][0]['internal_events'])
 assert r[52]['viewgroup_items'][5]['internal_formulas']['config_visible']=='$ALWAYS$'
 assert all('si(screen)=gv(homepg)' in n.get('internal_formulas',{}).get('config_visible','') for n in r[2:])
 if suffix:assert 'GYRO' not in json.dumps(p)
 report.append(dict(edition=suffix or 'normal',archive='valid',root_count=len(r),home_screen=2,native_screen_controls='hidden',dock_target='terminal'))
(out/'verification/structure-check.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(base/'analysis/当前主题版本.txt').write_text('当前采用 native-desktop-navigation-v0.13.46/Rhine-UI-native-desktop-navigation-v0.13.46.klwp，已应用模拟器。\n桌面第 2 页为斜条主页，右划进入第 1 页启动器原生 App 桌面；四宫格 Dock 入口在当前桌面打开终端，终端返回收起。\n功能页记录来源：从终端打开音乐、日历后返回终端；从主页打开后返回主页。跨桌面滑动会收起主题界面。\n原生应用页已配置浏览器、时钟、相册、设置、电话、短信、文件、日历，图标由启动器管理。主题配置入口移到终端右上角。\n操作说明和验证截图见本版输出目录。终端按钮视觉沿用 v0.13.42，不调整原布局比例。v0.13.44/45 为交互测试中间版，不使用。v0.13.46 用 -1 标识普通桌面，避免误触发功能页动画导致返回时出现暗色残影。\n',encoding='utf-8')
print(report)
