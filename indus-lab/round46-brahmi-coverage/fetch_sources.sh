#!/usr/bin/env bash
# Restores the third-party files that round 46 inspected but that this public repo does not redistribute
# (no licence is stated upstream). Hashes of the 2026-10-17 snapshot are in docs/excluded-files-manifest.json.
# Upstream may have changed since; a hash mismatch means you are looking at a newer version, not a corrupt file.
set -euo pipefail
cd "$(dirname "$0")"
TR=https://tejesh-raut.github.io/indus-valley-script
curl -fsSL "$TR/"              -o explorer.html
curl -fsSL "$TR/app.js"        -o app.js
curl -fsSL "$TR/data/icit.js"  -o icit.js
curl -fsSL "$TR/data/signs.js" -o signs.js
curl -fsSL "$TR/data/tree.json" -o tree.json || echo "tree.json not available at that path; not needed by audit.py"
curl -fsSL https://raw.githubusercontent.com/yajnadevam/lipi/fc8813a52e183d19c441631dc26c33a4dccbea39/src/pages/index.vue -o lipi-index.vue
python3 - <<'PY'
import hashlib, json, pathlib
m = {f['path'].split('/')[-1]: f['sha256'] for f in json.load(open('../../docs/excluded-files-manifest.json'))['files'] if 'round46' in f['path']}
for name, want in m.items():
    p = pathlib.Path(name)
    if not p.exists(): print(f'missing  {name}'); continue
    got = hashlib.sha256(p.read_bytes()).hexdigest()
    print(('match    ' if got == want else 'CHANGED  ') + name)
PY
