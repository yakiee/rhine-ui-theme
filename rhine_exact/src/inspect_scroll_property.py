exec(open('rhine_exact/src/inspect_scroll_schema.py',encoding='utf-8-sig').read().split('for c in d.get_classes():')[0])
for c in d.get_classes():
 if c.get_name()=='Lorg/kustom/lib/animator/c;':
  for m in c.get_methods():
   if m.get_name() in ('b','<init>'):
    print(m.get_name(),m.get_descriptor());print('\n'.join(i.get_name()+' '+i.get_output() for i in m.get_instructions()))
