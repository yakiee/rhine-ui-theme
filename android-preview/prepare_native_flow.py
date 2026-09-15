from pathlib import Path
import json,subprocess
base=Path('android-preview/scrcpy');p=base/'ThemeClipboard.java';text=p.read_text();text=text.replace('!label.equals("Rhine text")','!label.equals("KUSTOM_FLOW") && !label.equals("Rhine text")');p.write_text(text,encoding='utf8')
jdk=Path('C:/Program Files/Eclipse Foundation/jdk-8.0.302.8-hotspot/bin')
subprocess.run([str(jdk/'javac.exe'),'-encoding','UTF-8',str(p)],check=True)
subprocess.run([str(jdk/'java.exe'),'-cp',str(base/'r8-2.2.66.jar'),'com.android.tools.r8.D8','--min-api','26','--output',str(base/'theme-input.zip'),str(base/'ThemeClipboard.class')],check=True)
from rebuild_ui import run
run('push',(base/'theme-input.zip').resolve(),'/data/local/tmp/rhine-theme-input.zip')
out=Path('rhine_exact/output/free-editor-rebuild');flows=json.loads((out/'rebuild-plan.json').read_text(encoding='utf8'))['flows']
(out/'phone-clips/flow.clip.txt').write_text('##KUSTOMCLIP##\n'+json.dumps({'clip_version':1,'KUSTOM_FLOW':{f['id']:f for f in flows}},ensure_ascii=False)+'\n##KUSTOMCLIP##',encoding='utf8')
print('Native flow input prepared.')
