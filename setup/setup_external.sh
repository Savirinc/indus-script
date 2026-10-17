#!/usr/bin/env bash
# Fetch the external datasets used in rounds 29-45, pinned to the exact commits used.
# Run from the folder root:  bash setup/setup_external.sh            (core, ~1 GB, under a minute)
#                            bash setup/setup_external.sh --all      (adds big/optional repos)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EXT="$ROOT/ext"; mkdir -p "$EXT"

clone () {  # clone <url> <dir> <commit> [sparse paths...]
  local url=$1 dir=$2 commit=$3; shift 3
  if [ -d "$EXT/$dir/.git" ]; then echo "= $dir exists"; return; fi
  echo "+ $dir"
  if [ $# -gt 0 ]; then
    git clone --filter=blob:none --no-checkout "$url" "$EXT/$dir"
    git -C "$EXT/$dir" sparse-checkout set "$@"
  else
    git clone --filter=blob:none --no-checkout "$url" "$EXT/$dir"
  fi
  git -C "$EXT/$dir" checkout -q "$commit"
}

# --- core (needed by rounds 32, 36-45) ---
clone https://github.com/lexibank/ids            lexibank_ids   bf6c9f8c7d25c15e61e338f3ed29ae46b844c0f8
clone https://github.com/j-luo93/neurodecipher   neurodecipher  480bad2487820e3737fecfdd108214efa769e34b
# JAMBU / moli-mandala: CDIAL, Munda forms, Burushaski, cross-family comparisons (full repo is ~1.8 GB; sparse)
clone https://github.com/moli-mandala/data       moli-mandala_data 665850cdd1451391dc939063b5ccc972e646f6f6 data/cdial data/munda data/other

if [ "${1:-}" = "--all" ]; then
  clone https://github.com/lexibank/wold                 lexibank_wold        1df62b9bdc7292b35982aea49b4d5bd1951f6f3e
  clone https://github.com/lexibank/asjp                 lexibank_asjp        cf4bf0d13c95256b1b48f440d07c5c098500a770
  clone https://github.com/lexibank/sagartst             lexibank_sagartst    c6df5f38eeef9cf40dbb939e6515f8bf8cd04246
  clone https://github.com/concepticon/concepticon-data  concepticon-data     a89063d5657022a4ac11c557baef4958809e7c91
  clone https://github.com/unicode-org/unihan-database   unihan-database      667c2d180a75ddd749b774dbb7588d4786b63222
  clone https://github.com/cjkvi/cjkvi-ids               cjkvi-ids            86b4d16159f0079437870408f0ca186e529015db
  clone https://github.com/chinese-poetry/chinese-poetry chinese-poetry       b8594f81a89752241442f2ce267d6f66f96704ee
  clone https://github.com/alxdrdelaporte/yunpy          yunpy                fb8eb335c6b2fe12e2231ffe89f53c672961794f
  clone https://github.com/cran/sumer                    sumer                96040e2c78abb14e7d184e9f3b86f4f2bf137914
  # Bourdeau cyphersolver (full repo ~2.4 GB) - only the Indus target + writeups
  clone https://github.com/dbourdeau/cyphersolver        cyphersolver         843165c369a9c35658b1a7656860e06abd7a5de3 targets/indus docs
  # CDLI full ATF dump + catalogue (~240 MB) used in round 35 name search; derived extracts are already in data/derived/
  clone https://github.com/cdli-gh/data                  cdli-data            HEAD
fi

cat <<EOF

Done. Still MANUAL (not on GitHub):
  * Kuiper 1991 'Aryans in the Rigveda' OCR text (archive.org djvu .txt) -> save as $ROOT/data/kuiper.txt
    (rounds 37-45 parse chapter V from it; the parsed 386-word list is in data/derived/kuiper1991_ch5_words.txt)
Then:  source setup/paths.sh
EOF
