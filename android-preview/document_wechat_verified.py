from pathlib import Path
from rebuild_ui import run
import json,time
p=Path('rhine_exact/output/dock-phone-fix-20260914')
d={'status':'verified on physical phone','date':'2026-09-14','device':'16c18d67','original_cause':'OPEN_LINK weixin:// reached WXCustomSchemeEntryActivity, then HyperOS denied subsequent main UI start','discarded_attempt':'Intent text in OPEN_LINK was treated as a web link; Chrome confirmation was rejected','fix':'All 9 WeChat touch regions changed to LAUNCH_APP with explicit com.tencent.mm/com.tencent.mm.ui.LauncherUI intent','verified_readback':{'wechat_native_actions':9,'group_children':106,'root_layers':64},'actual_button_test':'topResumedActivity com.tencent.mm/.ui.LauncherUI t4203','saved_on_phone':True,'other_events_and_geometry':'preserved from live clipboard backup','root_group_order':'replacement touch group appended at root; existing visibility limits it to terminal page, no visual artwork changed','backup':'terminal-touches-before.clip.txt','verified_clip':'terminal-wechat-roundtrip.clip.txt'}
(p/'wechat-fix.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
s=Path('rhine_exact/output/free-editor-rebuild/sync-status.json');v=json.loads(s.read_text(encoding='utf8'));v['wechat_direct_launch']={'saved':True,'action':'LAUNCH_APP','component':'com.tencent.mm/com.tencent.mm.ui.LauncherUI','touch_regions':9,'validation':'actual theme button launched WeChat LauncherUI; native actions round-trip verified','legacy_global':'wechat no longer used by terminal WeChat touch actions'};s.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
run('shell','input','keyevent',3);time.sleep(1)
print('Verified native WeChat launch and returned phone to desktop.')
