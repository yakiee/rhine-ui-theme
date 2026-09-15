import xml.etree.ElementTree as ET
root=ET.parse('android-preview/logs/rebuild-ui.xml')
for n in root.iter('node'):
 if n.get('checkable')=='true': print(n.attrib)
