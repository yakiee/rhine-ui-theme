"""Use scrcpy's official control socket for Unicode clipboard input only."""
from pathlib import Path
import os
import subprocess,socket,struct,time,sys,json
BASE=Path(__file__).resolve().parent
(BASE/'logs').mkdir(parents=True, exist_ok=True)
ADB=os.environ.get("RHINE_ADB") or str(BASE/'sdk/platform-tools/adb.exe')
SERIAL=os.environ.get("RHINE_DEVICE_SERIAL", "16c18d67")
class ClipboardControl:
 def __enter__(self):
  self.server=None;self.sock=None;self.port=None
  def adb(*args):
   result=subprocess.run([ADB,'-s',SERIAL,*args],capture_output=True,timeout=20)
   if result.returncode:raise RuntimeError(result.stderr.decode(errors='replace'))
   return result.stdout
  self.adb=adb
  adb('push',str(BASE/'scrcpy/scrcpy-server-v4.1'),'/data/local/tmp/rhine-scrcpy-input.jar')
  with socket.socket() as port_probe:
   port_probe.bind(('127.0.0.1',0));self.port=port_probe.getsockname()[1]
  adb('forward','tcp:'+str(self.port),'localabstract:scrcpy_01510911')
  self.log=(BASE/'logs/scrcpy-input.log').open('ab')
  command='CLASSPATH=/data/local/tmp/rhine-scrcpy-input.jar app_process / com.genymobile.scrcpy.Server 4.1 scid=01510911 video=false audio=false control=true tunnel_forward=true clipboard_autosync=false send_device_meta=false cleanup=false power_on=false'
  self.server=subprocess.Popen([ADB,'-s',SERIAL,'shell',command],stdout=self.log,stderr=self.log,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
  for attempt in range(30):
   try:
    candidate=socket.create_connection(('127.0.0.1',self.port),timeout=1)
    if candidate.recv(1)==b'\x00':self.sock=candidate;break
    candidate.close()
   except OSError:pass
   time.sleep(.1)
  if self.sock is None:
   self.__exit__(None,None,None);raise RuntimeError('Control socket did not start; see scrcpy-input.log')
  self.sock.settimeout(5)
  return self
 def read(self,length):
  data=b''
  while len(data)<length:
   chunk=self.sock.recv(length-len(data))
   if not chunk:raise EOFError('Control connection closed')
   data+=chunk
  return data
 def get(self):
  self.sock.sendall(bytes([8,0]))
  if self.read(1)!=b'\x00':raise RuntimeError('Unexpected clipboard response')
  length=struct.unpack('>I',self.read(4))[0]
  return self.read(length).decode('utf-8')
 def set(self,text,paste=False):
  raw=text.encode('utf-8')
  if len(raw)>262130:raise ValueError('Clipboard payload exceeds official control limit')
  self.sock.sendall(struct.pack('>BQB I',9,1,int(paste),len(raw))+raw)
  event=self.read(1)
  if event!=b'\x01':raise RuntimeError('Expected clipboard acknowledgement: '+repr(event))
  if struct.unpack('>Q',self.read(8))[0]!=1:raise RuntimeError('Wrong acknowledgement')
 def __exit__(self,*args):
  if self.sock:self.sock.close()
  if self.server:
   try:self.server.wait(timeout=2)
   except subprocess.TimeoutExpired:self.server.terminate()
  if hasattr(self,'log'):self.log.close()
  if self.port:self.adb('forward','--remove','tcp:'+str(self.port))
if __name__=='__main__':
 with ClipboardControl() as control:
  if sys.argv[1]=='get':
   text=control.get()
   Path(sys.argv[2]).write_text(text,encoding='utf-8')
   print('Copied editor component: bytes',len(text.encode('utf-8')),'preview',text[:1000])
  elif sys.argv[1]=='set':
   control.set(Path(sys.argv[2]).read_text(encoding='utf-8-sig'),paste='--paste' in sys.argv)
   print('Theme text copied to Android clipboard')
