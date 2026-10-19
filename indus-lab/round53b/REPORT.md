# Round 53b — Lexicon-induction segmentation: METHOD-FAIL by 0.001, and the single-sign control is not separable anyway

Protocol `PROTOCOL.md` (committed a0084c1 before code). Code `run53b.py` (Dirichlet-process unigram word model, Gibbs over boundaries, α0 = 20, p# = 0.5, 150 annealed sweeps); `results.json`, `run53b.log`. Seed 53101, B = 30 samples per control, N = 8,726, units of 2–13 signs from `../round53/controls/`. Run time 317 s.

## Verdict
**METHOD-FAIL.** The rule, carried over from round 53, requires a boundary-F1 margin of at least 0.15 over random boundaries at the same rate on three of the four gold corpora.

| Control (gold words) | precision | recall | F1 | random F1 | margin |
|---|---|---|---|---|---|
| SEAL seal legends | 0.503 | 0.750 | 0.602 | 0.406 | **0.196** pass |
| SUX Ur III lines | 0.587 | 0.686 | 0.632 | 0.544 | 0.089 |
| OBL Old Babylonian letters | 0.345 | 0.890 | 0.497 | 0.348 | 0.149 (0.0009 short) |
| OAL Old Assyrian letters | 0.409 | 0.856 | 0.554 | 0.404 | 0.149 (0.0007 short) |

Two corpora miss the line by less than a thousandth. The stopping rule forbids a rerun with other seeds, and the verdict stands as written: the segmenter is a real improvement on round 53 (margins 0.047 and 0.072 become 0.149 on the same letters; recall 0.86–0.89) but it does not meet the bar that was set, and the bar is not moved after the fact.

## The deeper problem: the single-sign control is not separable
Even with a passing control, the verdict rule could not have worked on S. Mean segment length for the Shijing, where nearly every character is a word, is 1.495; for the Akkadian letters, whose words average 2.5 to 2.9 signs, it is 1.483 and 1.484. The model finds collocations in Chinese verse as readily as syllable strings in Akkadian. M separates them a little (Shijing 0.756 against 0.91–0.96 for cuneiform), but the protocol requires S and M to agree. Round 53 showed the same inversion with PMI. Two different segmenters, same conclusion: at 8,726 tokens, unsupervised segmentation cannot tell a one-sign-per-word corpus from a multi-sign-word corpus, because what it recovers is recurrence, and recurrence is a property of genre and formula as much as of word structure.

## Description (not a verdict)
| Corpus | S | M |
|---|---|---|
| **Indus** | **1.423** | **0.733** |
| SEAL | 1.769 | 0.961 |
| SUX | 1.492 | 0.824 |
| OBL | 1.484 | 0.914 |
| OAL | 1.483 | 0.917 |
| CHN (single-sign words) | 1.495 | 0.756 |
| OBI | 1.701 | 0.878 |

Indus shuffled within texts: S 1.073, M 0.236, so the structure found is real sign order. Had the control passed, the rule would have read the Indus values as SINGLE-SIGN-WORDS on both S and M; given the inversion above, that word would have meant little, and it is not issued.

**Induced Indus lexicon** (multi-sign segments, count): 861-002 (106), 817-002 (92), 820-002 (63), 760-740 (58), 176-740 (47), 032-220 (40), 100-740 (34), 740-090 (31), 740-400 (29), 920-060-741 (28), 692-060 (27), 590-390-740 (26), 235-240 (26), 798-740 (25), 220-520 (24), 923-740 (24), 705-033 (24), 415-220 (22), 550-060 (21), 705-033-520 (20). Multi-sign segments cover 54% of tokens. Every entry is a sequence the lab already knew from bigram work: sign-plus-two-strokes pairs, sign-plus-jar endings, the 920-060-741 formula. The model rediscovers the formulae; it does not reveal words behind them.

## Status
Segmentation is closed (rounds 53, 53b). Conjecture A3 is unchanged; the one-sign-per-word reading is neither excluded nor supported. The structural track's tally is five pre-registered rounds, five instrument failures on real controls (52, 52b, 53, 53b, 54), each recorded with what it taught. The methods paper should present them as a series, with the one instrument that works (round 47's shuffle test on keys) and the two facts that survived every control (no alphabet or syllabary; almost no within-text sign repetition).

## One methodological note for the paper
Thresholds set in advance can fall on a knife edge. The right response is not to move them but to report the distance, as here, and to let the reader weigh it. A replication with a different seed set would be legitimate only as a new, pre-registered round that says in advance that it is a replication.
