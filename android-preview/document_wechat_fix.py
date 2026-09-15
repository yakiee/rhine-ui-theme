from pathlib import Path
import json
p=Path('rhine_exact/output/dock-phone-fix-20260914/wechat-fix.json')
d={'cause_evidence':'Original weixin:// tap reached WXCustomSchemeEntryActivity, then MIUILOG Permission Denied Activity for com.tencent.mm/.ui.LauncherUI and launcher remained foreground. Click hit area works.','before':'weixin://','after':Path('rhine_exact/output/dock-phone-fix-20260914/wechat-direct-intent.txt').read_text(encoding='utf8'),'saved_on_phone':True,'binding_verified_in_editor':True,'actual_tap_verification':'not completed: physical device disconnected before tap; adb only emulator remains','next':'Reconnect physical device 16c18d67; tap terminal WeChat at observed coordinates and verify top activity without reading chats.'}
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
p=Path('rhine_exact/output/free-editor-rebuild/sync-status.json');s=json.loads(p.read_text(encoding='utf8'));s['wechat_direct_launch']={'saved':True,'global':'wechat','value':d['after'],'validation':'pending phone reconnect'};p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Saved exact change and pending verification.')
