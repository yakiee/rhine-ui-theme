def formula(item,field,value):
    item.setdefault('internal_toggles',{})[field]=10
    item.setdefault('internal_formulas',{})[field]=value if value.startswith('$') else '$'+value+'$'

def walk(item):
    yield item
    for child in item.get('viewgroup_items',[]):
        yield from walk(child)

def normalize_nested_positions(node):
    converted = []
    for child in node.get('viewgroup_items', []):
        child.setdefault('position_anchor', 'CENTER')
        placement = {'internal_type': 'OverlapLayerModule', 'internal_title': '定位容器',
                     'position_anchor': 'CENTER', 'viewgroup_items': [child]}
        shifted = False
        for axis, positive, negative in [('x', 'left', 'right'), ('y', 'top', 'bottom')]:
            field = 'position_offset_' + axis
            expression = child.get('internal_formulas', {}).pop(field, None)
            child.get('internal_toggles', {}).pop(field, None)
            value = child.pop(field, 0)
            if expression:
                shifted = True
                expression = expression.strip('$')
                formula(placement, 'position_padding_' + positive, 'mu(max,0,2*(' + expression + '))')
                formula(placement, 'position_padding_' + negative, 'mu(max,0,-2*(' + expression + '))')
            elif value:
                shifted = True
                placement['position_padding_' + positive] = max(0, 2 * value)
                placement['position_padding_' + negative] = max(0, -2 * value)
        normalize_nested_positions(child)
        converted.append(placement if shifted else child)
    if 'viewgroup_items' in node:
        node['viewgroup_items'] = converted