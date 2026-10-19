#!/usr/bin/env bash
# Round 52 control corpora, pinned. Downloads into $1 (default: ./dl). Nothing here is statistics.
set -euo pipefail
D="${1:-dl}"; mkdir -p "$D"; cd "$D"
get() { curl -sS -L --retry 3 --max-time 900 "$1" -o "$2"; echo "$2"; }
# Greek: Homer, Perseus canonical-greekLit, CC BY-SA 4.0, commit 0189b9c8
P=https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/0189b9c8d8d1f148133f2f0af309b4ee90ea4332/data/tlg0012
get $P/tlg001/tlg0012.tlg001.perseus-grc2.xml iliad.xml
get $P/tlg002/tlg0012.tlg002.perseus-grc2.xml odyssey.xml
# Hebrew: Westminster Leningrad Codex via openscriptures/morphhb, public domain, commit 3d15126f
for b in Gen Exod Lev Num Deut; do get https://raw.githubusercontent.com/openscriptures/morphhb/3d15126fb1ef74867fc1434be1942e837932691f/wlc/$b.xml wlc_$b.xml; done
# Cherokee: bible-corpus, CC0, commit 44e5fca1
get https://raw.githubusercontent.com/christos-c/bible-corpus/44e5fca1bfb369a5da2ee23ebc6f421c88489c5c/bibles/Cherokee-NT.xml Cherokee-NT.xml
# Sumerian: CDLI daily dump, commit d66b12b0 (Git LFS media URLs), plus Oracc sign list commit 6231cc4a
get https://media.githubusercontent.com/media/cdli-gh/data/d66b12b065af39a57d640576b4c7e098db5dac7f/cdliatf_unblocked.atf cdliatf_unblocked.atf
get https://media.githubusercontent.com/media/cdli-gh/data/d66b12b065af39a57d640576b4c7e098db5dac7f/cdli_cat.csv cdli_cat.csv
get https://raw.githubusercontent.com/oracc/ogsl/6231cc4afc5bbbbbacde7aad60c7ec9b1c078add/00lib/osl.asl osl.asl
# Egyptian: AES, CC BY-SA 4.0, commit 35276d25
A=https://raw.githubusercontent.com/simondschweitzer/aes/35276d2527cca1a055e31ed5f6683e777717170f/files/aes
get $A/_aes_bbawgrabinschriften.json _aes_bbawgrabinschriften.json
get $A/_aes_smaek.json _aes_smaek.json
# Oracle bone: OBIMD, CC BY 4.0, Hugging Face revision 4820d2f1
get "https://huggingface.co/datasets/KLOBIP/OBIMD/resolve/4820d2f11a8f45f3347591fdcd5f6466706b0dce/data.json" obimd_data.json
# Shijing: chinese-poetry, MIT, commit b8594f81
get "https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/b8594f81a89752241442f2ce267d6f66f96704ee/%E8%AF%97%E7%BB%8F/shijing.json" shijing.json
sha256sum * 2>/dev/null || shasum -a 256 *
