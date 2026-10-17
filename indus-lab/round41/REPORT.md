# Round 41 — Dravidian rebus anchors vs shuffled anchors on unseen inscriptions: WEAK SUPPORT (pre-registered rule), not convincing

12 October 2026.

## Setup
- 17 signs were fixed to Krishnamurti Proto-Dravidian words: fish *mīn, man *āḷ, arrow *ampu, and the numerals 1, 2, 3, 5, 6, 7, 8.
- The other signs were fitted on 80% of the inscriptions under a Proto-Dravidian sound model.
- The score is how well the fitted key predicts the held-out 20% (226 texts; near-duplicates removed), compared with 15 refits whose anchor values were shuffled.

## Results

| Run | Real anchors (held-out log-likelihood) | Shuffled anchors (15) | p | Verdict |
|---|---:|---|---:|---|
| Linear B control (17 true values) | −19.73 | −20.28 … −22.01 (all worse) | 1/16 | **PASS**: the method can detect correct anchor values |
| Indus (17 Dravidian values) | −43.50 | −42.56 … −46.29; 2 of 15 better (−42.56, −43.23) | **3/16** | **WEAK SUPPORT** by the fixed rule |

## Interpretation
- The Dravidian values do better than most misassignments (13 of 15) but not all.
- A p of 0.19 is well within what chance produces. This is not evidence that the Dravidian values are right. It also does not refute them, because the test has limited power with 17 anchors (jar, the commonest sign, had to be dropped).
- Under the protocol, Step 3 (the copper-tablet picture test) is NOT triggered.

## What would sharpen it
- **More anchors under the same rule.** Add standard Krishnamurti/DEDR forms for jar/pot, leaf, four and bird, chosen by meaning before any refit.
- **More permutations** (e.g. 100) to estimate p precisely.
Both must be pre-registered as a new round.

Files: `PROTOCOL.md` (with the pre-fit anchor amendment), `anchored.py`, `results_lb_60000_15.json`, `results_indus_60000_15.json`.
