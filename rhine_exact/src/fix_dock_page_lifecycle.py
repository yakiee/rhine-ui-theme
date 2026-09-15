"""Keep animated terminal visuals alive across native launcher page changes.

Apply to an already configured preset; preserve device globals, touch actions,
layer order and all existing motion tracks. Touch-only modules remain removed
outside their active desktop page so off-page interactions cannot leak.
"""
import copy

OLD_VISIBILITY = '$if(si(screen)=gv(homepg),ALWAYS,REMOVE)$'
NEW_VISIBILITY = '$if(1,ALWAYS,REMOVE)$'
VISUAL_TITLES = {
    '02 控制中心遮罩',
    '09 菱形层叠入口与侧面厚度',
    '主菜单 · 设备状态',
    '终端 · 设备及电池信息',
    '蓝色独立按钮 · 付款码',
    '第二行 · 灰色装饰方块（无点击）',
    '蓝色独立按钮 · 扫一扫',
    '快捷支付 · 深色标题栏',
    '主菜单 · 搜索底板',
    '主菜单 · 音乐入口',
    '蓝色独立按钮 · 支付宝',
    '主菜单 · 付款码底板',
    '主菜单 · 扫一扫底板',
    '主菜单 · 微信底板',
}

def apply_fix(preset):
    result = copy.deepcopy(preset)
    root = result.get('preset_root', result)
    changed = []
    for module in root['viewgroup_items']:
        title = module.get('internal_title')
        if title not in VISUAL_TITLES:
            continue
        formulas = module.get('internal_formulas', {})
        assert formulas.get('config_visible') in (OLD_VISIBILITY, NEW_VISIBILITY), title
        assert any(
            animation.get('type') == 'FORMULA'
            and animation.get('formula') in ('$gv(page)=0$', '$gv(page)=1$')
            and animation.get('action') == 'ADVANCED'
            for animation in module.get('internal_animations', [])
        ), title
        formulas['config_visible'] = NEW_VISIBILITY
        changed.append(title)
    assert set(changed) == VISUAL_TITLES, sorted(VISUAL_TITLES - set(changed))
    return result, changed
