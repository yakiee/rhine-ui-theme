from pathlib import Path
import json,collections
n=json.loads(Path('rhine_exact/output/dock-phone-fix-20260914/terminal-touches-fixed.json').read_text(encoding='utf8'));colors=collections.Counter()
def walk(x):
 if 'paint_color' in x:colors[x['paint_color']]+=1
 for c in x.get('viewgroup_items',[]):walk(c)
walk(n);print(colors)
