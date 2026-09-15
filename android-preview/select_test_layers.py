from rebuild_ui import run,snapshot
run('shell','input','keyevent',4)
for y in [2135,2254,2373]:run('shell','input','tap',1146,y)
run('shell','input','swipe',630,2100,630,2500,550)
snapshot()
