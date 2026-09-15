from rebuild_ui import run
for namespace in ['system','secure','global']:
 for line in run('shell','settings','list',namespace).decode(errors='replace').splitlines():
  if 'wallpaper' in line.lower() and any(t in line.lower() for t in ['scroll','offset','slide','screen']):print(namespace,line)
