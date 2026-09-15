from pathlib import Path
p=Path('rhine_exact/src/build_drag_dock.py');s=p.read_text(encoding='utf-8-sig').replace('v0.13.48','v0.13.49').replace("r[1]=text_layer;r[23]['viewgroup_items'][3]['viewgroup_items']=[]", "r[1]=copy.deepcopy(r[23]);r[1]['internal_title']='Dock 底板 · 桌面滚动同步';r[1]['viewgroup_items'][3]['viewgroup_items']=[];r[23]=text_layer")
p.write_text(s,encoding='utf-8')
