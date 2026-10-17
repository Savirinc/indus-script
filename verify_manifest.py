from pathlib import Path
import hashlib,json,sys
root=Path(__file__).resolve().parent
items=json.loads((root/'MANIFEST.json').read_text())
bad=[]
for item in items:
 p=root/item['path']
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:bad.append(item['path'])
print(f'Checked {len(items)} files; mismatches: {len(bad)}')
for p in bad:print(p)
sys.exit(bool(bad))
