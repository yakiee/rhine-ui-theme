from pathlib import Path
p=Path('rhine_exact/src/build_native_desktop_navigation.py');s=p.read_text(encoding='utf-8-sig').replace('v0.13.44','v0.13.45');s=s.replace("r[52]['internal_title']='终端 · 返回主页与主题配置'", "r[52]['internal_title']='终端 · 返回主页与主题配置'\n  formula(r[52]['viewgroup_items'][5],'config_visible','ALWAYS')")
p.write_text(s,encoding='utf-8')
