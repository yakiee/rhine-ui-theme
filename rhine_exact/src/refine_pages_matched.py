"""Reference-measured native details for the weather, calendar and music pages."""
from copy import deepcopy
from static_helpers import walk,formula,normalize_nested_positions
from refine_homepage import shape,at,label
S='mu(min,1,si(sheight)*720/si(swidth)/1600)'
def placed(node,x,y):
 root={'viewgroup_items':[at(node,(x-180)/.47,(y-400)*2)]};normalize_nested_positions(root);return root['viewgroup_items'][0]
def rect(x,y,w,h,color,path=None):return placed(shape(w/.47,h*2,color,path),x,y)
def text(x,y,w,size,value,color='#FF202329'):
 node=label(value,w/.47,size*2,'#FFFFC229' if color=='accent' else color)
 if color=='accent':formula(node,'paint_color','gv(accent)')
 return placed(node,x,y)
def shift(node,dy):
 y=(node.get('position_padding_top',0)-node.get('position_padding_bottom',0))/2+dy
 node.update(position_padding_top=max(0,2*y),position_padding_bottom=max(0,-2*y))
def xexpand(root):
 for n in walk(root):
  if n.get('shape_width')==720 and n.get('shape_height')==1600:continue
  for k in ['position_padding_left','position_padding_right','shape_width','bitmap_width','text_width']:
   if k in n:n[k]*=1/.94

def refine_pages(old):
 # Reference cards run from x=28 to x=334. Apply the same transform to hit surfaces.
 for i in [12,13,14,16,17,18,19,20,21,22,32,33,34,35,36,37,38]:xexpand(old[i])
 for i in [13,16,17,33,34]:
  for child in old[i].get('viewgroup_items',[])[1:]:shift(child,20)
 for child in old[14]['viewgroup_items'][1:]:shift(child,-8)
 for n in walk(old[14]):
  if n.get('shape_height')==1:n['paint_color']='#FF54585B'
 # Forecast badges and page marks have visible outlines in the supplied reference.
 for n in walk(old[13]):
  if n.get('shape_width',100)>0 and n.get('shape_width',100)<20 and n.get('shape_height',100)<20:
   n['paint_stroke']=2
 # The bottom weather module has a white card and an independent high/low badge.
 b=deepcopy(old[15]['viewgroup_items'][0]);a=[b]
 a += [rect(181,675.5,306,111,'#EFFFFFFF'),rect(181,640,306,40,'#FF202329'),rect(79,605,80,16,'#FF202329'),text(79,605,78,12,'24 / 21°C','#FFFFFFFF')]
 warning=shape(23/.47,21*2,'#FFB6D819','M 50 0 L 100 100 L 0 100 Z M 45 27 L 55 27 L 55 63 L 45 63 Z M 45 77 L 55 77 L 55 89 L 45 89 Z')
 a += [placed(warning,52,641),text(87,695,67,57,'[b]21[/b]'),text(135,703,38,28,'°C','#FF8B8E8E'),text(244,698,157,8,'气压 1016.3  体感22°C  湿度80%'),text(86,716,70,5,'RHINE WEATHER')]
 old[15]['viewgroup_items']=a
 # Progress plate: stepped arrow, shield, tick marks and highlighted remaining days.
 r=old[21];items=r['viewgroup_items'];items[1]['viewgroup_items'][0].update(shape_type='PATH',shape_path='M 0 0 L 90 0 L 100 50 L 90 100 L 0 100 Z',shape_path_scale='FIT_XY')
 for n in walk(items[8]):
  if 'bitmap_width' in n:n['bitmap_width']*=1.6;n['bitmap_height']*=1.6
 for idx in [3,7]:
  for n in walk(items[idx]):
   if n.get('text_expression'):n['text_expression']=''
 start=len(items)
 items += [rect(59,481,59,18,'accent'),text(59,481,57,13,'◉ 87天'),text(59,461,43,11,'10/5','accent')]
 shield=shape(23/.47,25*2,'accent','M 0 0 L 100 0 L 100 70 L 50 100 L 0 70 Z');shield.update(paint_style='STROKE',paint_stroke=2)
 items += [placed(shield,59,437),text(59,435,22,13,'24','accent'),text(180,481,153,8,'1       4       7       10')]
 for child in items[start:]:shift(child,120)
 # Schedule controls remain at their visible click targets; transform the original hit layer too.
 for root in [old[22],old[38]]:
  for child in root['viewgroup_items'][1:]:shift(child,28)
 items=old[22]['viewgroup_items']
 for n in walk(items[2]):
  if 'shape_height'in n:n['shape_height']=204
 for n in walk(items[3]):
  if 'shape_height'in n:n['shape_height']=204
 for n in walk(items[4]):
  if 'text_expression'in n:n['text_size']=34;n['text_width']=240
 items[4]['position_padding_left']=46;items[4]['position_padding_right']=0
 for idx in [10,11]:
  for n in walk(items[idx]):
   if 'shape_height'in n:n['shape_height']=204
   if n.get('text_expression')=='↗':n['text_expression']='▱';n['text_size']=65
 for n in walk(items[1]):
  if 'text_expression'in n:n['text_expression']=''
 for idx in [10,11]:shift(items[idx],-22)
 start=len(items)
 items += [rect(89,576,81,16,'#FF202329'),text(89,576,79,11,'SCHEDULE','#FFFFFFFF'),text(99,640,77,34,'＋−'),text(99,660,75,8,'RHINE UI.KLWP'),text(296,681,52,7,'SCHEDULE','#FFB5DE16')]
 for child in items[start:]:shift(child,96)
 # The lime controls sit in front of the dark schedule rail.
 items[11]['viewgroup_items']=[shape(35/.47,35*2,'#FFFFFFFF','M 80 10 L 92 22 L 45 69 L 27 75 L 33 57 Z M 63 22 L 14 22 L 14 91 L 83 91 L 83 46')]
 items[11]['viewgroup_items'][0].update(paint_style='STROKE',paint_stroke=4)
 old[22]['viewgroup_items']=items[:6]+items[10:12]+items[6:10]+items[12:]
 for n in walk(old[20]):
  if n.get('text_expression')=='OCTOBER':n['text_expression']='[b]OCTOBER[/b]';n['text_size']=47
 # Slight rounding masks compression-contaminated icon corners while keeping individual bitmaps.
 for n in walk(old[8]):
  if n.get('fx_mask')=='CLIP_NEXT':n['shape_corners']=22
