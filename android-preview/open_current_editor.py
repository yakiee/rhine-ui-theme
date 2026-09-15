from rebuild_ui import run,snapshot
import contextlib,io,re,time
run('shell','am','start','-W','-n','org.kustom.wallpaper.huawei/org.kustom.app.OnBoardingActivity')
with contextlib.redirect_stdout(io.StringIO()):root=snapshot()
card=next((n for n in root.iter('node') if n.get('resource-id','').endswith('/card_entry_text') and '正在编辑' in n.get('text','')),None)
if card is not None:
 nums=list(map(int,re.findall(r'\d+',card.get('bounds'))));run('shell','input','tap',(nums[0]+nums[2])//2,(nums[1]+nums[3])//2);time.sleep(.5)
snapshot()
