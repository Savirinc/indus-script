# Library: the project's source material in one place

Built 29 October 2026 for Arham Partap Jain. Everything here is a **copy** or is **generated**. The working originals stay where the rounds read them (`indus-lab/raw/`, `indus-lab/external/`, `data/derived/`), and those originals are never edited.

## Contents

| Path | What it is |
|---|---|
| `pdf/Indus-Inscriptions-Catalogue.pdf` | Every inscription record (5,679), numbered 1–5,679, with its seal or object number (CISI), ICIT number, site, object, material, direction and sign numbers. Sorted by site, then catalogue number. 111 pages. |
| `pdf/Indus-Language-and-History.pdf` | The civilisation's history and what is true about its language. Each statement is labelled ESTABLISHED, STRONG EVIDENCE, PROPOSED or UNKNOWN, and sourced. 8 pages. |
| `inscriptions/inscriptions.csv` | The same records as the catalogue, as a clean table. The `no` column matches the PDF. The upstream Sanskrit and translation columns are left out. |
| `raw/01-icit-lipi/` | The primary corpus (`inscriptions.csv`), unchanged. |
| `raw/02-bourdeau-cyphersolver/` | Corpus tables in visual and reading order, sign-to-font map, ICIT ↔ Mahadevan sign map. |
| `raw/03-mayig-cisi/` | CISI digitisation in Parpola numbering, and the Parpola sign list. |
| `raw/04-explorer-snapshot/` | Tejesh Raut explorer corpus (5,445 records). Do not pool it with 01. |
| `raw/05-dravidian-db-v1.1/` | Dravidian Database (Proto-Dravidian reconstructions). |
| `raw/06-cdli-dilmun-meluhha/` | Cuneiform lines mentioning Dilmun and related terms (CDLI). |
| `raw/07-kuiper-1991-words/` | Kuiper's 386 foreign words in the Rigveda. |
| `raw/SHA256SUMS` | Hashes of every raw file. Check with `cd library/raw && shasum -a 256 -c SHA256SUMS`. |
| `build/` | `build_library.py` (copies, table, PDFs) and `language-and-history.html` (the source text of the history PDF). |
| `local/` (not in git) | `Indus-Inscriptions-Catalogue-with-signs.pdf`: the same catalogue with the signs drawn (265 pages). It uses the lipi Indus webfont, which has no licence, so it stays on this machine and is not published. |

Each `raw/` folder has a `PROVENANCE.md` giving the source, the licence and the cautions. `THIRD_PARTY_NOTICES.md` at the repo root has the full licence list.

## Rebuild
From the repo root, run `python3 library/build/build_library.py`. It takes about 10 seconds and needs Google Chrome for the PDFs. The glyph edition is built only if `ext/fonts/indus-font.ttf` is present.

To change the history document, edit `build/language-and-history.html` and rebuild. Keep the status labels honest: a claim moves up a label only with evidence.

## Rules carried over
- The upstream `sanskrit` and `translation` columns are proposed readings, never evidence (CLAUDE.md).
- No CISI photographs are reproduced: they are under copyright.
- Records are not independent texts. Moulded tablets and repeated seal texts appear once per object.
