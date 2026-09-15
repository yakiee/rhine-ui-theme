from rebuild_ui import run,snapshot
for y in [2119,2238,2357,2476]:run('shell','input','tap',1146,y)
run('shell','input','swipe',630,2480,630,2250,500)
snapshot()
