# Round 31 — Round 30 survives the transcription check, with one likely pseudo-inscription identified

11 October 2026. See VERIFICATION.md for the per-seal ledger.

## Result
The round-30 model, controls, metric and null were all kept unchanged; only the input texts vary by scenario. The scenarios were defined from the ledger before running.

| Scenario | n | Bigram surprisal, mean percentile | p | Order-only surprisal (M3) |
|---|---:|---:|---:|---:|
| As round 30 | 8 | 0.916 | <1e-4 | 0.883 |
| Drop 5228.1 (likely pseudo-script, Laursen no. 11) | 7 | 0.943 | <1e-4 | 0.907 |
| 3898.1 read as Mahadevan (5 signs) | 8 | 0.916 | <1e-4 | 0.882 |
| 3898.1 read as Gadd's 4 characters | 8 | 0.914 | <1e-4 | 0.881 |
| Drop all conflicted readings (5228, 3863, 5232) | 5 | 0.932 | 1e-4 | 0.917 |
| Only seals with some independent support (3897, 3898 per Mahadevan, 5227, 5229) | 4 | 0.926 | 5e-4 | 0.901 |

The statistical anomaly does not depend on any disputed reading or on the likely pseudo-inscription.

## What changed in our understanding
1. **Pseudo-script is real in this group but not the whole story.** One of the eight (5228.1) is very probably the seal Laursen identifies as pseudo-script: a twins sign plus random strokes. Removing it makes the group *more* anomalous, not less. So the anomaly is not driven by the one known imitation.
2. **The twins sign (091) is the stable feature across sources.** Laursen's prose, the corpus readings and round 30's within-group test all point to a twins-first convention on Bahrain seals. Even the pseudo-script seal kept it. That is what one would expect if the twins sign were the meaningful element (e.g. a name, title or patronymic) and the rest of the text varied.
3. **Two open conflicts need the actual drawings.** Qala'at al-Bahrain: Laursen says twins-first, but the corpus has a single figure (090). Luristan: Parpola calls it paralleled, while the model finds it highly atypical.

## Status of evidence
- Independent photographic verification at sign level was achieved for no seal. Gadd's 1932 halftones confirm only the larger signs.
- The Bahrain and Luristan readings rest on the corpus plus Laursen's prose.

To settle the conflicts, these are needed:
- Laursen 2010 Figs. 9 and 11 (drawings), PDF pp. 14 and 20;
- Al-Sindi 1999 (*Dilmun Seals*) for Karzakan/Saar;
- Kjærum 1994 figs. 1725–1726 for Qala'at;
- Amiet 1973 pl. 23 for Luristan;
- British Museum photographs of BM 123208.

## Reproduce
`python3 indus-lab/round31/sensitivity.py` (requires round30 outputs). Standard library only.
