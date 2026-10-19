# Round 52b — Writing-system signature with three classes: METHOD-FAIL again, and the reason is itself the result

Protocol: `PROTOCOL.md` (committed 52ca3ae before code; Amendments 1–3 before any classification, each after a run aborted at extraction). Code: `extract52b.py`, `run52b.py` (imports round 52's features and sampler unchanged); results `results.json`, log `run52b.log`. Seed 52101, B = 300, N = 8,726, Indus text lengths imposed on every corpus. Twelve classified corpora in three classes plus one reference, all excavated except Greek, Hebrew, Cherokee and the Shijing.

## Verdict
**METHOD-FAIL.** Nine of twelve leave-one-corpus-out tests pass at 100%; three fail, and two of the three fail completely.

| Held out | Class | Assigned to | Correct |
|---|---|---|---|
| GRK, HEB | SMALL | SMALL | 1.00, 1.00 |
| CHR Cherokee | SMALL | LARGE-PHON 300/300 | **0.00** |
| SUX, OBL, SEAL, EGY | LARGE-PHON | LARGE-PHON | 1.00 each |
| OAL Old Assyrian letters | LARGE-PHON | SMALL 82/300 | 0.73 |
| OBI oracle bone | LARGE-PHON | ARCHAIC 278/300 | **0.07** |
| U4, U3, PE | ARCHAIC | ARCHAIC | 1.00 each |

Under the pre-registered rule (any corpus below 50% voids the verdict) the Indus class is not declared. The nearest-corpus ranking and range check are reported below as description, not as a verdict.

## Feature table (corpus means over 300 Indus-shaped samples)

| Corpus | class | V | hapax | top10 | H1 | H2/H1 | heaps | repeat | double |
|---|---|---|---|---|---|---|---|---|---|
| **Indus** | ? | **582** | **0.368** | **0.332** | **6.92** | **0.494** | **0.457** | **0.035** | **0.001** |
| GRK | SMALL | 24 | 0 | 0.741 | 4.09 | 0.851 | 0.011 | 0.340 | 0.016 |
| HEB | SMALL | 22 | 0 | 0.757 | 4.08 | 0.926 | 0.001 | 0.338 | 0.025 |
| CHR | SMALL | 81 | 0.017 | 0.410 | 5.62 | 0.734 | 0.053 | 0.139 | 0.007 |
| SUX Ur III accounts | LARGE-PHON | 423 | 0.220 | 0.241 | 7.31 | 0.477 | 0.290 | 0.139 | 0.010 |
| OBL Old Babylonian letters | LARGE-PHON | 250 | 0.250 | 0.327 | 6.43 | 0.634 | 0.266 | 0.134 | 0.006 |
| OAL Old Assyrian letters | LARGE-PHON | 174 | 0.144 | 0.400 | 6.04 | 0.685 | 0.186 | 0.177 | 0.011 |
| SEAL cuneiform seal legends | LARGE-PHON | 304 | 0.206 | 0.448 | 6.27 | 0.508 | 0.279 | 0.139 | 0.020 |
| EGY tomb inscriptions | LARGE-PHON | 411 | 0.277 | 0.436 | 6.39 | 0.562 | 0.379 | 0.276 | 0.047 |
| OBI oracle bone | LARGE-PHON | 669 | 0.368 | 0.323 | 7.23 | 0.461 | 0.448 | 0.030 | 0.001 |
| U4 Uruk IV proto-cuneiform | ARCHAIC | 726 | 0.253 | 0.312 | 7.57 | 0.505 | 0.413 | 0.240 | 0.005 |
| U3 Uruk III proto-cuneiform | ARCHAIC | 857 | 0.361 | 0.276 | 7.82 | 0.512 | 0.456 | 0.178 | 0.009 |
| PE proto-Elamite | ARCHAIC | 905 | 0.358 | 0.317 | 7.53 | 0.469 | 0.508 | 0.224 | 0.004 |
| CHN Shijing | reference | 1,621 | 0.372 | 0.179 | 9.18 | 0.313 | 0.549 | 0.189 | 0.024 |

**Indus nearest corpora** (standardised by between-corpus spread): OBI 0.44, then U3 2.05, SUX 2.11, OBL 2.29, PE 2.39, U4 2.52, SEAL 2.70, OAL 3.43, CHR 4.38, EGY 4.65, CHN 4.74, GRK 6.71, HEB 7.10. The nearest corpus does not change when any one corpus is removed. On the five features that do not depend on inventory splitting the order is OBI 0.34, SUX 1.47, OBL 1.51, U3 1.86, SEAL 2.03.

**Range check** (features on which the Indus value lies inside the span of a class's corpus means): LARGE-PHON 6 of 8; ARCHAIC 2 of 8 (H2/H1 and heaps); SMALL 0 of 8.

## What the failure means
1. **Conditional entropy does not separate phonetic writing from archaic accounting.** H2/H1 for Ur III Sumerian is 0.477, for cuneiform seal legends 0.508, for Egyptian 0.562; for Uruk III proto-cuneiform 0.512, Uruk IV 0.505, proto-Elamite 0.469. At matched size and text length the "linguistic" and the largely non-phonetic administrative systems overlap completely on this statistic, and on unigram entropy and Heaps slope as well. This is the Rao et al. (2009) argument tested against the real systems it should have been tested against, and it does not discriminate. Sproat's objection stands on real data. Consequently the project's conjecture A1 cannot be decided by statistics of this family at all, which is recorded in `docs/CONJECTURES.md`.
2. **Oracle-bone Chinese sits with the archaic systems on these statistics,** although it is phonetic in use. Large inventory, many rare signs (names of diviners, ancestors, places), low repetition: that profile belongs to short formulaic records of a certain kind, not to a system type. The classes "phonetic" and "archaic" as drawn are therefore not what these features measure. What they measure is closer to "record type and inventory size".
3. **Cherokee fails for a simpler reason:** the only syllabary, when removed, leaves a class of two alphabets; a syllabary of 81 signs is nearer Old Assyrian (174) than Greek (24). A class needs more than one exemplar of each sub-type.

## What is robust (description, not verdict)
- **Indus is far from every small-inventory script** on every feature (range check 0 of 8; distances 4.4 to 7.1 against 0.4 to 2.7 for large-inventory corpora). Rounds 52 and 52b agree.
- **Indus is nearest the oracle-bone inscriptions by a factor of four to five** over the next corpus, on all eight features and on the five robust ones. The resemblance is specific: inventory 582 against 669, hapax share 0.368 against 0.368, H1 6.92 against 7.23, H2/H1 0.494 against 0.461, repetition 0.035 against 0.030, doubling 0.001 against 0.001.
- **The repetition rate is the Indus corpus's signature.** Every other corpus repeats a sign in 13% to 34% of texts; Indus and oracle bone in 3%. A key that assigns syllables or letters would have to explain why a text almost never needs the same sign twice; a key that assigns word-signs (names, titles) does not have that problem, and neither does a seal legend made of distinct elements.
- **Numeral diagnostic.** Merging the seventeen stroke numerals into one sign raises the Indus repetition rate from 0.035 to 0.177 and the doubling rate from 0.001 to 0.029: about one Indus text in seven contains two different stroke numerals, often adjacent. The stroke signs are a sub-system of their own, which is what round 55 is for.

## Status of conjectures
- **A1** (the signs encode language): unchanged at OPEN, but its refutation condition is narrowed: entropy and inventory statistics cannot settle it, because real non-phonetic administrative systems match phonetic scripts on them. Round 56's generative-model comparison remains the only statistical route, and it must beat the proto-cuneiform control, not just a shuffle.
- **A3** (logosyllabic): OPEN. The alphabet and syllabary alternatives are excluded by two rounds; among large-inventory systems the statistics place Indus with short formulaic records (oracle bone), consistent with A2 (names and titles) and not decisive for A3.

## Why not run a 52c
A third version with more corpora per sub-type would improve the positive control but would not change what the features measure. The series closes here: structural statistics of this family exclude small-inventory systems and place Indus among short-record large-inventory corpora; they cannot classify further. That is a result worth stating, and stating once.

## Data
New extracts (`controls/`, all CC BY, hashes in `SHA256SUMS`): OBL 348,163 tokens, OAL 174,415, SEAL 68,434 (6,369 seals as units), U4 9,189 (under 2 N; its 300 samples overlap heavily), U3 48,582, PE 16,446. Akkadian Sumerogram markers stripped; sign values mapped through the Oracc sign list (OBL 183 unmapped of 344,227; OAL 24; SEAL 65). Proto-cuneiform and proto-Elamite tokens are ZATU and Dahl sign names with variant suffixes kept.
