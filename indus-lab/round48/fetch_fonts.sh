#!/usr/bin/env bash
# Round 48 inputs: glyph fonts, pinned by commit. Writes ext/fonts/ (git-ignored) and SHA256SUMS here.
# Noto fonts: SIL Open Font License 1.1, from google/fonts at one commit.
# Indus sign font: yajnadevam/lipi src/assets/fonts/indus-font.woff2 at the commit round 46/47 used (no licence stated upstream;
# used locally for shape measurement only, not redistributed). Codepoint = U+E000 + catalogue code (verified: 713/714 map codes have glyphs; 941 absent).
set -euo pipefail
cd "$(dirname "$0")"
ROOT=../..; OUT=$ROOT/ext/fonts; mkdir -p "$OUT"
GF=47d54ca1ebb14fd864695f1d39dc734f39017c33   # google/fonts main, 2026-10-18
LIPI=fc8813a52e183d19c441631dc26c33a4dccbea39
for d in brahmi phoenician lineara oldhungarian olditalic runic cyprominoan oldturkic carian lycian lydian oldsoutharabian \
         imperialaramaic kharoshthi glagolitic gothic oldpermic elbasan osage tifinagh nko samaritan oldnortharabian meroitic; do
  name=$(curl -fsSL "https://api.github.com/repos/google/fonts/contents/ofl/notosans$d?ref=$GF" | python3 -c 'import json,sys;print([f["name"] for f in json.load(sys.stdin) if f["name"].endswith("-Regular.ttf")][0])')
  [ -s "$OUT/$name" ] || curl -fsSL "https://raw.githubusercontent.com/google/fonts/$GF/ofl/notosans$d/$name" -o "$OUT/$name"
done
[ -s "$OUT/NotoSans[wdth,wght].ttf" ] || curl -fsSL "https://raw.githubusercontent.com/google/fonts/$GF/ofl/notosans/NotoSans%5Bwdth%2Cwght%5D.ttf" -o "$OUT/NotoSans[wdth,wght].ttf"
[ -s "$OUT/indus-font.woff2" ] || curl -fsSL "https://raw.githubusercontent.com/yajnadevam/lipi/$LIPI/src/assets/fonts/indus-font.woff2" -o "$OUT/indus-font.woff2"
(cd "$OUT" && shasum -a 256 *.ttf *.woff2) > SHA256SUMS
echo "fetched $(ls "$OUT" | wc -l | tr -d ' ') files; hashes in SHA256SUMS"
