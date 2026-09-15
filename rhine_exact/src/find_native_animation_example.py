import zipfile
with zipfile.ZipFile('android-preview/apps/KLWP-aosp.apk') as z:
 print('\n'.join(n for n in z.namelist() if n.endswith(('.klwp','.json')) and ('asset' in n)))
