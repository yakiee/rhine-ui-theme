from pathlib import Path
p=Path('rhine_exact/src/build_native_desktop_navigation.py');s=p.read_text(encoding='utf-8').replace('v0.13.45','v0.13.46').replace('si(screen)!=gv(homepg),9,','si(screen)!=gv(homepg),-1,');p.write_text(s,encoding='utf-8')
p=Path('rhine_exact/src/write_native_navigation_guide.py');s=p.read_text(encoding='utf-8-sig').replace('v0.13.45','v0.13.46');p.write_text(s,encoding='utf-8')
