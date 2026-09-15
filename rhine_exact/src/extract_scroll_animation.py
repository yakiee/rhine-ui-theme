exec(open('rhine_exact/src/inspect_scroll_schema.py',encoding='utf-8-sig').read().split('for c in d.get_classes():')[0])
lines=[]
for c in d.get_classes():
 if c.get_name() in ['Lorg/kustom/lib/render/AnimationModule;','Lorg/kustom/lib/render/AnimationHelper;','Lorg/kustom/lib/options/AnimationRule;']:
  for m in c.get_methods():
   if not m.get_code():continue
   ops=[i.get_name()+' '+i.get_output() for i in m.get_instructions()]
   if any(any(k in line for k in ['AnimationRule','AnimationCenter','"speed"','"center"','->ADVANCED']) for line in ops):
    lines.extend([c.get_name()+' '+m.get_name()+' '+m.get_descriptor(),*ops,''])
Path('rhine_exact/analysis/scroll-animation-schema.txt').write_text('\n'.join(lines),encoding='utf-8')
print('saved',len(lines),'lines')
