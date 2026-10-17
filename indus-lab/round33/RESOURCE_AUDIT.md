# Round 33 — Audit of Bourdeau's cyphersolver Indus work as a resource

11 October 2026.
- Repo: https://github.com/dbourdeau/cyphersolver commit 843165c369a9c35658b1a7656860e06abd7a5de3.
- Licence: code MIT, text CC BY 4.0.
- Indus material: `targets/indus/` (430 scripts, about 410 result/notes files, DOSSIER.md, NOTES.md, PREDICTIONS.md).
- Write-ups index: https://dbourdeau.github.io/cyphersolver/writeups.html. That page holds 261 entries, nearly all Renaissance diplomatic ciphers. The Indus, Linear A and Voynich entries are the relevant ones.

## What ran end to end here (separate copy; his repo untouched)

| Script | Input | Result |
|---|---|---|
| `allographs.py` | our `raw/sk_indus_script-webfont.ttf` | `results/allographs.md` byte-identical to his published file |
| `gulf.py` | our `raw/inscriptions.csv` (same ICIT/indusscript.net export format) | Same findings. His export has 1 more West Asian object (a Dilmun SEAL:C) and 2 more home objects; counts shift slightly (Fisher p 0.007 → 0.012; familiar pairs 45% → 47%). |

The extra West Asian object is a **Dilmun round seal reading 415-803-001-717-354**. Its first three signs equal the opening of Ur U.17649 (415-803-001-328-004-002). This is a candidate shared name/title formula across Gulf-type seals.

The export difference (a few rows) is consistent with the known 5,679 vs 5,680 row discrepancy noted in CURRENT-STATUS. It is not fully reconciled.

## What needs external inputs he keeps locally (not in the repo)
- **`bench.py`, `fit_holdout.py`, `matched_holdout.py`:**
  - Monier-Williams (`mw.txt`; Cologne Digital Sanskrit Lexicon);
  - DEDR forms (Dravidian Database v1.1, now downloaded to `external/dravidian_db_v1.1/` with hashes);
  - ePSD2 Sumerian glossary;
  - optionally a "scout" folder: JAMBU Munda/Burushaski, Madras Tamil Lexicon Sangam entries, Hallock Elamite, Elamicon Linear Elamite.
- **`linb_control.py`:** DAMOS Linear B lines, syllabogram table, Greek transliteration wordlist.
- **`meluhha_oracc.py`:** an ORACC/CDLI export of Meluhha attestations.

## Conclusions of his that bear directly on our rounds

| His finding | Relation to our work |
|---|---|
| "A key fitted to the corpus reads about 93% of it in any language"; fitted keys generalise in every language | Same phenomenon as round 32. Round 32 adds the mechanism (sign IDs per token below the identifiability threshold) and the anchor curve. |
| His bench cannot recognise the correct Linear B key (11–41 of 100 shuffles as good) | Consistent with round 32. His scoring (consonant-skeleton coverage) is weaker than a likelihood objective, but the conclusion is the same. |
| West Asian seals follow other rules (Rao et al. 2009; `gulf.py`) | Round 30 is a replication with a stronger design, not a first. Corrected in round30/REPORT.md. |
| Only Nanaza and Samar are probable Meluhhan names; a full CDLI search (223 texts) adds none | Seriously weakens the Meluhha-name anchor route. Dilmun names are a separate pool, still to check. |
| Merging all look-alike sign pairs reduces 223 common signs only to 180 | Weakens round 32's "fewer free signs" lever: about 20% fewer, not 2×. |
| Seven "firm" sign = image equations from copper tablets | CONFLICTS with this project's own earlier audit (rounds 17/24: 45/46 object-leaveout but 15/26 family-heldout; composite animals). Not adopted as anchors without re-review. |
| Grammar tests favour Dravidian (class suffix + possessor-first); registered Dravidian predictions failed | Typological, not phonetic. Useful constraints; not anchors. |

## Status
Usable as a source of tested structural constraints, reproducible scripts and a large pre-registered prediction ledger. It does not supply anchored sign values, and its author states that no sign value is established.
