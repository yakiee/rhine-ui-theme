from pathlib import Path
import json,zipfile
base=Path('rhine_exact');old=base/'output/native-desktop-navigation-v0.13.46';out=base/'output/desktop-dock-fold-v0.13.47';report=[]
for suffix in ('','-off'):
 with zipfile.ZipFile(old/f'Rhine-UI-native-desktop-navigation{suffix}-v0.13.46.klwp') as z:a=json.loads(z.read('preset.json'))
 with zipfile.ZipFile(out/f'Rhine-UI-desktop-dock-fold{suffix}-v0.13.47.klwp') as z:
  assert z.testzip() is None;b=json.loads(z.read('preset.json'))
 ar=a['preset_root']['viewgroup_items'];br=b['preset_root']['viewgroup_items'];changed=[i for i in range(len(ar)) if ar[i]!=br[i]]
 assert changed==[23,24],changed
 assert a['preset_root']['globals_list']==b['preset_root']['globals_list']
 for i in changed:
  assert br[i]['internal_formulas']['config_visible']=='$ALWAYS$'
  assert '(gv(page)=2 | gv(page)=-1)' in br[i]['internal_animations'][1]['formula']
 assert br[23]['viewgroup_items'][3]['internal_formulas']['config_visible']=='$if(gv(page)=0,ALWAYS,REMOVE)$'
 if suffix:assert 'GYRO' not in json.dumps(b)
 report.append(dict(edition=suffix or 'normal',changed_roots=changed,archive_valid=True,navigation_unchanged=True))
(out/'verification').mkdir(exist_ok=True)
(out/'verification/structure-check.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
s=(old/'操作说明.md').read_text(encoding='utf-8').replace('v0.13.46','v0.13.47').replace('Rhine-UI-native-desktop-navigation','Rhine-UI-desktop-dock-fold').replace('其他页只显示壁纸，交给启动器放 App','其他页显示壁纸及底部收平的 Dock 背景，交给启动器放 App')
s=s.replace('主屏底部圆圈显示实际电量，满圈为 100%；旁边显示机器当前星期、日期。这部分用于显示，没有点击动作。','主屏底部圆圈显示实际电量，满圈为 100%；旁边显示机器当前星期、日期。划到其他原生桌面时，黑色底条和光带同步向下收起、转为水平，电量和日期文字隐藏，仅作为 Dock 背景；划回主页恢复。底条本身没有点击动作，不影响启动器图标操作。')
(out/'操作说明.md').write_text(s,encoding='utf-8')
print(report)
