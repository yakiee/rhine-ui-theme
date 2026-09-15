from pathlib import Path
import os
import subprocess,xml.etree.ElementTree as ET,sys,time,re
ADB=os.environ.get("RHINE_ADB") or str(Path(__file__).resolve().parent/'sdk/platform-tools/adb.exe')
SERIAL=os.environ.get("RHINE_DEVICE_SERIAL", "16c18d67")
LOG=Path(__file__).resolve().parent/'logs/rebuild-ui.xml'
LOG.parent.mkdir(parents=True, exist_ok=True)
def run(*args):
 r=subprocess.run([ADB,'-s',SERIAL,*map(str,args)],capture_output=True,timeout=25)
 if r.returncode:raise RuntimeError(r.stderr.decode(errors='replace') or r.stdout.decode(errors='replace'))
 return r.stdout

def snapshot():
 remote='/sdcard/Download/klwp-rebuild-ui.xml'
 result=run('shell','uiautomator','dump',remote)
 if b'dumped' not in result:raise RuntimeError(result.decode(errors='replace'))
 xml=run('shell','cat',remote);LOG.write_bytes(xml)
 root=ET.fromstring(xml)
 for node in root.iter('node'):
  label=node.get('text') or node.get('content-desc')
  if label:print(label,'|',node.get('resource-id'),'|',node.get('bounds'),flush=True)
 return root
if __name__=='__main__':
 action=sys.argv[1] if len(sys.argv)>1 else 'snapshot'
 if action=='tap':run('shell','input','tap',*sys.argv[2:4])
 elif action=='back':run('shell','input','keyevent','4')
 elif action=='text':run('shell','input','text',sys.argv[2])
 elif action=='key':run('shell','input','keyevent',sys.argv[2])
 elif action=='swipe':run('shell','input','swipe',*sys.argv[2:])
 if action!='snapshot':time.sleep(.3)
 snapshot()
