from rebuild_ui import run,snapshot
import time
run('shell','input','tap',400,658)
run('shell','input','keycombination',113,29)
run('shell','input','text','2')
run('shell','input','tap',1128,216)
time.sleep(.7)
snapshot()
