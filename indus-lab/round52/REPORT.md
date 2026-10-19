# Round 52 — Writing-system signature: METHOD-FAIL (positive control not met), with a robust partial result

Protocol: `PROTOCOL.md` (committed 4f8f48d before code; Amendments 1–2 before results). Code: `extract52.py`, `run52.py`; results `results.json`, log `run52.log`. Seed 52001, B = 300 samples per corpus, N = 8,726 tokens, Indus text-length distribution imposed on every control.

## Verdict
**METHOD-FAIL.** The leave-one-corpus-out control recovers the alphabet class perfectly (Greek 100%, Hebrew 100%) but fails completely on the two large-inventory classes: Sumerian held out is called logographic (0% correct), Egyptian held out is called logographic (0%), oracle-bone Chinese held out is called logosyllabic (0%). Under the pre-registered rule any test below 50% voids the Indus verdict, so no `MATCH` word is issued.

| LOCO test | True class | Assigned | Correct |
|---|---|---|---|
| GRK Homer | alphabet | alphabet 300/300 | 1.00 |
| HEB Pentateuch | alphabet | alphabet 300/300 | 1.00 |
| SUX Ur III | logosyllabic | logographic 300/300 | 0.00 |
| EGY tomb inscriptions | logosyllabic | logographic 300/300 | 0.00 |
| OBI oracle bone | logographic | logosyllabic 300/300 | 0.00 |
| CHN Shijing | logographic | logographic 300/300 | 1.00 |

## What the numbers say anyway (reported, not a verdict)

Eight relabelling-invariant features at matched size and text length. Controls are means over 300 Indus-shaped samples.

| Corpus | class | V | hapax | top10 | H1 | H2/H1 | heaps | repeat | double |
|---|---|---|---|---|---|---|---|---|---|
| **Indus** | ? | **582** | **0.368** | **0.332** | **6.92** | **0.494** | **0.424** | **0.035** | **0.001** |
| GRK | alphabet | 24 | 0 | 0.741 | 4.09 | 0.851 | 0.012 | 0.340 | 0.016 |
| HEB | abjad | 22 | 0 | 0.757 | 4.08 | 0.926 | 0.000 | 0.337 | 0.025 |
| CHR | syllabary | 82 | 0.017 | 0.410 | 5.62 | 0.733 | 0.054 | 0.138 | 0.007 |
| SUX | logosyllabic | 423 | 0.220 | 0.241 | 7.31 | 0.477 | 0.291 | 0.139 | 0.010 |
| EGY | logo-consonantal | 411 | 0.275 | 0.436 | 6.39 | 0.562 | 0.378 | 0.277 | 0.047 |
| OBI | logographic (oracle bone) | 668 | 0.366 | 0.323 | 7.23 | 0.461 | 0.447 | 0.030 | 0.001 |
| CHN | logographic (received text) | 1,621 | 0.372 | 0.179 | 9.18 | 0.313 | 0.547 | 0.189 | 0.024 |

Standardised Euclidean distance from the Indus vector to each corpus mean (all eight features; five features without inventory size in brackets): OBI 18.5 (16.4), SUX 36.5 (29.4), EGY 55.7 (52.6), CHR 106.8 (86.8), CHN 155.6 (118.1), GRK 195.0 (182.5), HEB 206.9 (194.9). For scale, the distance between Sumerian and oracle bone is 36.6 and between Sumerian and Egyptian 68.4.

Three things survive the failed control because they do not depend on the failed distinction:

1. **The Indus corpus is not alphabet-like or syllabary-like at matched size.** Those classes were recovered perfectly, no large-inventory sample was ever assigned to them, and the Indus vector is three to ten times further from them than from any large-inventory corpus. This is the inventory-size argument (Parpola, Mahadevan) now stated with corpus size and text length held equal, on every feature and not only V. It holds on the five features that do not depend on how allographs are split.
2. **The Indus statistics sit among the large-inventory systems, nearest the oracle-bone inscriptions, then Ur III Sumerian.** Oracle-bone texts are short divination records in a sign system with heavy phonetic (rebus) use; Ur III texts are short administrative records. The Indus corpus resembles both more than it resembles Egyptian tomb inscriptions or a received Chinese literary text.
3. **Sign order carries information at the Sumerian level.** Shuffling signs within texts raises Indus H2/H1 from 0.494 to 0.662; the same shuffle on a Sumerian sample raises it from 0.475 to 0.610. The within-text repetition rate is the one feature where Indus is extreme: 3.5% of texts repeat a sign, against 14% for Sumerian, 28% for Egyptian, and 3.0% for oracle bone. Whatever the signs encode, a text rarely uses the same sign twice. This is a constraint any key has to reproduce.

## Why the control failed, and what it teaches
- The classes "logosyllabic" and "logographic" as drawn in the protocol do not separate at 8,726 tokens: oracle-bone Chinese is statistically closer to Ur III Sumerian (distance 36.6) than to the Shijing (138.3). Oracle-bone writing uses phonetic loans extensively, so the label was arguably wrong, and the Shijing, a received literary text in modern character forms, is a poor stand-in for an excavated logographic corpus. With one or two corpora per class, leave-one-out has nothing to generalise from.
- The 99% Mahalanobis region was mis-specified. The class covariance was estimated from resampling the same corpus, so the standard deviations are tiny (V ± 9 for Sumerian, ± 13 for oracle bone) and every distance is in the hundreds or thousands. Between-system variance, which is what a class region should express, cannot be estimated from one or two corpora. This is a lesson for round 52b: either more corpora per class or a continuous placement without class regions.
- Linear B could not be used: no openly licensed corpus of running tablet texts exists (DĀMOS is CC BY-NC-SA with no export; LiBER is non-profit only). Cherokee stood as the syllabary and behaved as expected, but a modern printed syllabary is a weak witness for an excavated one.

## Diagnostics
| Indus variant | H2/H1 | heaps | repeat | double |
|---|---|---|---|---|
| real | 0.494 | 0.424 | 0.035 | 0.001 |
| order shuffled within texts | 0.662 | 0.406 | 0.035 | 0.003 |
| tokens shuffled across texts | 0.686 | 0.423 | 0.173 | 0.022 |

The across-text shuffle shows that the low repetition rate is a property of the texts, not of the frequency distribution: random texts with the same signs and lengths repeat a sign in 17% of cases.

## Status of conjecture A3
A3 ("logosyllabic, like early cuneiform") is unchanged at OPEN. What this round adds: the alphabet and syllabary alternatives are excluded at matched conditions by a control that passed; the logosyllabic-versus-logographic question is not decidable with the corpora used. The refutation condition in `docs/CONJECTURES.md` is updated to say what a decisive version needs.

## Next step
Round 52b, pre-registered: (a) at least three excavated corpora per large-inventory class (add Hittite or Old Akkadian cuneiform, Luwian hieroglyphic, Maya, Chinese bronze inscriptions as they can be found under open licences), so that between-corpus variance is real; (b) replace the 99% class region with a nearest-corpus placement and a bootstrap over corpora; (c) keep the eight features and the Indus-shaped sampling unchanged. The repetition-rate constraint (3.5%) goes into the methods paper as a reproducibility requirement for any proposed key.

## Data and licences
`fetch_controls.sh` pins every source; `SHA256SUMS` lists downloads and extracts. Extracts in `controls/` are committed for GRK (CC BY-SA 4.0), HEB (public domain), CHR (CC0), EGY (CC BY-SA 4.0), OBI (CC BY 4.0), CHN (MIT); SUX (5.1 M tokens, CC BY) is regenerated from the pinned dump and the CC0 Oracc sign list, and its hash is recorded. 4,272,775 Sumerian tokens mapped to sign names, 17,610 kept as values. 10,240 oracle-bone groups were dropped for placeholders; 6,910 remain.
