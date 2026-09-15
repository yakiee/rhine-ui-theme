from pathlib import Path
import json
p=Path('rhine_exact/output/free-editor-rebuild/rebuild-validation.json')
v=json.loads(p.read_text(encoding='utf-8'))
v.update(phone_components_inserted=0,phone_globals_submitted=226,phone_saved_theme='Current editing draft saved; globals verified after leaving and reopening editor; no page components yet',phone_visual_verification='Not ready: preview empty because components have not been inserted')
v.pop('waiting_for_user',None)
p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
print('Draft status corrected and saved.')
