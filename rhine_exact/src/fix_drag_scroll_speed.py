from pathlib import Path
p=Path('rhine_exact/src/build_drag_dock.py');s=p.read_text(encoding='utf-8').replace('v0.13.49','v0.13.50').replace("internal_toggles={'center':10,'speed':10},internal_formulas={'center':'$\"SCREEN\"+gv(homepg)$','speed':'$mu(max,1,si(screenc)-1)*100$'}", "internal_toggles={'center':10},internal_formulas={'center':'$\"SCREEN\"+gv(homepg)$'}")
p.write_text(s,encoding='utf-8')
