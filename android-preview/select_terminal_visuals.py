from rebuild_ui import run
import time

def tap(x, y):
    run('shell','input','tap',x,y)
    time.sleep(.15)

for _ in range(8):
    run('shell','input','swipe',650,2100,650,2500,120)
time.sleep(.4)
for y in (2355,2475): tap(1146,y)
for positions in ((2263,2383,2503),(2283,2403,2523),(2308,2428),(2453,)):
    run('shell','input','swipe',650,2480,650,2120,800)
    time.sleep(.3)
    for y in positions: tap(1146,y)
run('shell','input','swipe',650,2480,650,2120,800)
time.sleep(.3)
tap(1146,2475)
run('shell','input','swipe',650,2480,650,2240,800)
time.sleep(.3)
for y in (2383,2503): tap(1146,y)
print('Selected terminal visual layers; inspect toolbar before proceeding.')
