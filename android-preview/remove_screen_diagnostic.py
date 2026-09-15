from rebuild_ui import run,snapshot
import contextlib,io,re
for _ in range(20):run('shell','input','swipe',650,2530,650,2080,80)
with contextlib.redirect_stdout(io.StringIO()):root=snapshot()
n=next(n for n in root.iter('node') if n.get('text')=='SYNC DIAGNOSTIC REMOVE')
b=list(map(int,re.findall(r'\d+',n.get('bounds'))));run('shell','input','tap',1146,(b[1]+b[3])//2)
run('shell','input','tap',1008,216)
run('shell','input','tap',696,216)
snapshot()
