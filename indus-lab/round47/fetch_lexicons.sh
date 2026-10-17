#!/usr/bin/env bash
# Round 47 lexicons, pinned. Downloads into ../../ext/lexicons (gitignored). Stdlib verification of hashes after first run.
set -euo pipefail
OUT="$(cd "$(dirname "$0")/../.." && pwd)/ext/lexicons"; mkdir -p "$OUT"
get () { [ -s "$OUT/$2" ] && { echo "= $2"; return; }; echo "+ $2"; curl -fsSL "$1" -o "$OUT/$2"; }
# Monier-Williams (Cologne Digital Sanskrit Lexicon), SLP1 markup; headwords in <k1>. CC BY-SA 4.0
get https://raw.githubusercontent.com/sanskrit-lexicon/MWS/f2c7c640cb63c0c9585b3e4b9315ac24891bda68/mwtranscode/mw.txt mw.txt
# Kotus Nykysuomen sanalista via hugovk/everyfinnishword. LGPL-2.1
get https://raw.githubusercontent.com/hugovk/everyfinnishword/d4df6e4efdce54c10197cf151a5cd0638d99860a/kaikkisanat.txt kaikkisanat.txt
# Xuxen Basque hunspell via wooorm/dictionaries. GPL
get https://raw.githubusercontent.com/wooorm/dictionaries/8cfea406b505e4d7df52d5a19bce525df98c54ab/dictionaries/eu/index.dic eu.dic
cd "$OUT" && shasum -a 256 mw.txt kaikkisanat.txt eu.dic | tee SHA256SUMS
