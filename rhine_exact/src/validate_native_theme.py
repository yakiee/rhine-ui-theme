"""Check native package structure and layout invariants; not an Android rendering test."""
from pathlib import Path
import json,zipfile,re,math
BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'output/native-theme-v0.2'
p=json.loads((OUT/'preset.json').read_text(encoding='utf-8'))
s=json.loads((BASE/'src/preset-revision-wip.json').read_text(encoding='utf-8'))
c=json.loads((BASE/'analysis/all-page-motion-coverage.json').read_text(encoding='utf-8'))
roots=p['preset_root']['viewgroup_items']; globals_=p['preset_root']['globals_list']
failures=[]; tests={}; position_checks=0

def check(name,value):
    tests[name]=bool(value)
    if not value:failures.append(name)

def walk(node,depth=0):
    yield node,depth
    for child in node.get('viewgroup_items',[]):yield from walk(child,depth+1)

check('root limit',len(roots)<=64)
check('all page coverage',all(any('gv(page)='+str(page) in row['condition'] or (page==0 and 'gv(page)<=2' in row['condition']) for row in c['layers']) for page in range(8)))
check('native visual roots stay present for exit',all(g.get('config_visible')=='ALWAYS' and 'config_visible' not in g.get('internal_formulas',{}) for g in roots[1:]))
all_nodes=[(node,depth) for g in roots for node,depth in walk(g)]
check('no nested animation definitions',all(depth==0 or not n.get('internal_animations') for n,depth in all_nodes))
unknown_globals=set();unbalanced=[]
for node,_ in all_nodes:
    for text in [*node.get('internal_formulas',{}).values(),node.get('text_expression','')]:
        if text.count('$')%2:unbalanced.append(text)
        unknown_globals.update(set(re.findall(r'gv\(([^,)]+)\)',text))-set(globals_))
check('formula delimiters balanced',not unbalanced)
check('formula globals declared',not unknown_globals)
check('no touch events on visible copies',all(not any(n.get('internal_events') for n,_ in walk(child)) for root in roots[1:] for child in root['viewgroup_items'] if child.get('internal_title')!='当前状态触摸区域'))
check('touch copies state gated',all('REMOVE' in n.get('internal_formulas',{}).get('config_visible','') for n,_ in all_nodes if n.get('internal_title')=='当前状态触摸区域'))
for root in roots[1:]:
    for anim in root['internal_animations']:
        keys=anim['animator']
        check(root['internal_title']+' keyframe range',all(0<=k['position']<=100 and math.isfinite(k['value']) for k in keys))
        check(root['internal_title']+' unique keyframes',len({(k['property'],k['position']) for k in keys})==len(keys))

# A split must leave each static numeric leaf at its original settled position.
def leaves(node,px=0,py=0):
    x=node.get('position_offset_x',0);y=node.get('position_offset_y',0)
    if not isinstance(x,(int,float)) or not isinstance(y,(int,float)):return
    px+=x;py+=y
    if node.get('viewgroup_items') is not None:
        for child in node['viewgroup_items']:
            if child.get('paint_color')=='#00000000' and not child.get('internal_formulas'):continue
            yield from leaves(child,px,py)
    else:
        yield node,px,py
bad_positions=[]
for row,root in zip(c['layers'],roots[1:]):
    old=s['preset_root']['viewgroup_items'][row['source_group']]
    for local,original_index in enumerate(row['source_nodes']):
        before=list(leaves(old['viewgroup_items'][original_index]))
        after=list(leaves(root['viewgroup_items'][local+1]))
        if len(before)!=len(after):bad_positions.append([row['layer'],'leaf count']);continue
        for (prev,px,py),(next_,nx,ny) in zip(before,after):
            for dim,pval,nval,offset in [('x',px,nx,row['pivot'][0]),('y',py,ny,row['pivot'][1])]:
                if 'position_offset_'+dim in prev.get('internal_formulas',{}):continue
                position_checks+=1
                if abs(pval-nval-offset)>1e-5:bad_positions.append([row['layer'],dim,pval,nval,offset])
check('split animation pivots preserve static layout',not bad_positions)
with zipfile.ZipFile(OUT/'Rhine-UI-native-v0.2-unfinished.klwp') as z:
    names=z.namelist()
    check('package has unique entries',len(names)==len(set(names)))
    check('package CRC',z.testzip() is None)
    check('package preset matches source',json.loads(z.read('preset.json'))==p)
    check('no substitute wallpaper packaged',not any('wallpaper.png' in name or 'weather-grid.png' in name for name in names))
report={'scope':'Static native package and coordinate invariants only. No KLWP import, formula evaluation, Android touch or motion validation.', 'pass':not failures,'root_count':len(roots),'animated_roots':len(c['layers']),'numeric_coordinate_checks':position_checks,'checks':tests,'failures':failures,'position_mismatches':bad_positions[:20],'unknown_globals':sorted(unknown_globals),'unbound_original_assets':[k for k,v in globals_.items() if v.get('type')=='BITMAP' and not v.get('value')],'runtime_verified':False,'one_to_one_verified':False}
(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['checks','unbound_original_assets']},ensure_ascii=True))
raise SystemExit(bool(failures))
