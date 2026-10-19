# Round 53 — Multi-sign words or one sign per word: METHOD-FAIL (segmenter does not work at this corpus size)

Protocol `PROTOCOL.md` (committed ad6d5e2 before code; Amendment 1 before any statistic). Code `extract53.py`, `run53.py`; `results.json`, `run53.log`. Seed 53001, B = 100 samples per control, N = 8,726 tokens, units of 2–13 signs, τ calibrated on the four cuneiform corpora with gold word boundaries before Indus was scored.

## Verdict
**METHOD-FAIL.** The pre-registered positive control required the PMI segmenter to beat random boundaries by at least 0.15 F1 on three of four gold-labelled corpora. It did so on one.

| Control (gold words) | F1 at τ* = 3.25 | random F1 at same rate | margin |
|---|---|---|---|
| SEAL cuneiform seal legends | 0.626 | 0.446 | **0.180** pass |
| SUX Ur III lines | 0.570 | 0.523 | 0.047 fail |
| OBL Old Babylonian letters | 0.438 | 0.366 | 0.072 fail |
| OAL Old Assyrian letters | 0.464 | 0.437 | 0.027 fail |

So nothing is concluded about whether Indus texts contain multi-sign words. The statistics below are description.

## Why it failed
Pointwise mutual information needs pair counts. At 8,726 tokens with 250 to 420 sign types, most adjacent pairs occur once and are assigned a boundary by rule, and the rest are estimated from two or three occurrences. On Sumerian and Akkadian lines the segmenter is then little better than random. It works on seal legends because they are formulaic (the same name-plus-title patterns recur), which is also why the seal corpus is the right genre control; but one passing corpus does not meet the rule.

A second symptom shows the instrument is not measuring words at all at this size: the Shijing, where nearly every character is a word, scores a **higher** mean segment length (1.50) than two of the cuneiform corpora whose words average 2.5 to 2.9 signs (Old Babylonian 1.28, Old Assyrian 1.19). Collocation and formula are what PMI finds, and a literary text has more of them than a letter.

## Description (not a verdict)
| Corpus | mean segment length S | share of units with a multi-sign segment M |
|---|---|---|
| **Indus** | **1.255** | **0.567** |
| SEAL | 1.443 | 0.911 |
| SUX | 1.581 | 0.818 |
| OBL | 1.281 | 0.772 |
| OAL | 1.190 | 0.669 |
| CHN (single-sign words) | 1.499 | 0.657 |
| OBI (unknown) | 1.614 | 0.808 |

Indus segments: 5,518 of length 1, 1,165 of length 2, 224 of length 3, 37 of length 4, 11 longer. Shuffling sign order within Indus texts drops S to 1.05 and M to 0.19, so the cohesion the segmenter finds in the Indus corpus is real order structure, consistent with rounds 27 and 29. Whether it is word structure cannot be said with this instrument.

The most cohesive Indus pairs by PMI are mostly rare pairs seen twice; among those seen more often: 171-035 (9 occurrences, PMI 8.6), 484-337 (5, 9.2), 510-460 (6, 7.9). These are candidates for round 54's distributional grid, not findings.

## What would work
Word segmentation at small corpus sizes is a solved problem in a different way: a lexicon-induction model that scores whole segmentations by description length (minimum description length, or a Dirichlet-process unigram model in the Goldwater style) uses every recurrence of a candidate word, not pairwise counts, and is known to work on a few thousand tokens. A round 53b with such a segmenter, the same gold corpora, the same rule, and the same 0.15 margin is the honest next attempt. It is more code (dynamic programming over segmentations, standard library is enough) and is pre-registered before it is written.

## On the "monosyllabic" reading
The question that motivated this round, whether each Indus sign is one one-syllable word as in Old Chinese, stays open. Rounds 52–52b exclude a pure syllabary; they do not distinguish one-sign-per-word from mixed logosyllabic writing, and round 53's instrument could not either. Round 53b is the direct test; round 54's grid is the indirect one (syllabic signs combine freely, word-signs sit in slots).

## Data
`controls/` with word boundaries marked ` | `: SEAL 5,098 seals / 42,087 signs; OBL 39,137 lines; OAL 21,975; CHN 7,295 clauses; OBI 6,571 sentences (no gold, each sign its own unit); SUX 934,414 lines (git-ignored, hash in `SHA256SUMS`). Extraction rules as in rounds 52–52b; determinatives are inside their word; numerals are words of their own in the ATF spacing.
