from pathlib import Path
p=Path('rhine_exact/src/verify_native_navigation_structure.py');s=p.read_text(encoding='utf-8-sig').replace('v0.13.45','v0.13.46').replace('v0.13.44 为返回热区未修正的中间测试版，不使用。','v0.13.44/45 为交互测试中间版，不使用。v0.13.46 用 -1 标识普通桌面，避免误触发功能页动画导致返回时出现暗色残影。');p.write_text(s,encoding='utf-8')
