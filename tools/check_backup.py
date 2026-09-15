"""Check the curated repository without connecting to a phone or changing Git."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'rhine_exact/CURRENT_PHONE_THEME.md',
    'rhine_exact/assets/zhuangfangyi/wallpaper-portrait.png',
    'rhine_exact/assets/zhuangfangyi/terminal-cover.png',
    'rhine_exact/output/hyperos-klwp-v0.13.51/Rhine-UI-HyperOS-v0.13.51.klwp',
    'rhine_exact/output/open-dock-swipe-20260915/toolbar-touch-with-latch.clip.txt',
    'rhine_exact/output/open-dock-swipe-20260915/page-with-native-latch.clip.txt',
    'rhine_exact/output/open-dock-swipe-20260915/page-flow-unconditional.clip.txt',
    'rhine_exact/output/dock-toolbar-motion-20260915/root-3-after.clip.txt',
    'rhine_exact/output/system-statusbar-contrast-20260915/top-scrim.clip.txt',
    *[f'rhine_exact/output/dock-toolbar-motion-20260915/root-{index}-dock-after.clip.txt'
      for index in (1, 23, 24)],
]
SECRET_PATTERNS = [
    re.compile(r'gh[pousr]_[A-Za-z0-9]{30,}'),
    re.compile(r'github_pat_[A-Za-z0-9_]{40,}'),
    re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    re.compile(r'AKIA[0-9A-Z]{16}'),
    re.compile(r'(?i)(?:authorization\s*[:=]\s*[\"\x27]?bearer\s+)[A-Za-z0-9_.-]{24,}'),
]


def main():
    result = subprocess.run(
        ['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'],
        cwd=ROOT, capture_output=True, check=True,
    )
    names = sorted(set(result.stdout.decode('utf-8').strip('\0').split('\0')))
    names = [name for name in names if name and (ROOT / name).is_file()]
    errors = []
    for name in REQUIRED:
        if name not in names:
            errors.append(f'Missing or excluded required file: {name}')
    entries = []
    clips = 0
    for name in names:
        path = ROOT / name
        data = path.read_bytes()
        if len(data) >= 100 * 1024 * 1024:
            errors.append(f'File exceeds repository size policy: {name}')
        if path.suffix in {'.py', '.json', '.txt', '.md', '.ps1', '.cmd', '.svg'}:
            text = data.decode('utf-8-sig', errors='replace')
            if any(pattern.search(text) for pattern in SECRET_PATTERNS):
                errors.append(f'Potential credential (contents withheld): {name}')
            if name.endswith('.clip.txt'):
                try:
                    json.loads(text.strip().removeprefix('##KUSTOMCLIP##').removesuffix('##KUSTOMCLIP##').strip())
                    clips += 1
                except ValueError:
                    errors.append(f'Invalid clipboard JSON: {name}')
        if path.suffix == '.klwp':
            try:
                with zipfile.ZipFile(path) as archive:
                    bad_member = archive.testzip()
                    if bad_member:
                        errors.append(f'Damaged preset member: {name}: {bad_member}')
                    json.loads(archive.read('preset.json'))
            except (ValueError, KeyError, zipfile.BadZipFile) as exc:
                errors.append(f'Invalid preset: {name}: {type(exc).__name__}')
        entries.append({'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    report = {'files': entries, 'count': len(entries), 'bytes': sum(item['bytes'] for item in entries),
              'valid_clipboards': clips, 'errors': errors,
              'scope': 'Curated local files; not a complete export of the live phone theme.'}
    destination = ROOT / 'docs/backup-manifest.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in report.items() if key != 'files'}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
