import xml.etree.ElementTree as E
from pathlib import Path
r=E.fromstring(Path('android-preview/logs/rebuild-ui.xml').read_bytes())
for n in r.iter('node'):
 if n.get('class')=='android.widget.EditText':print(n.attrib)
