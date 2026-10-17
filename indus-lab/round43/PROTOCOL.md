# Round 43 — Replication of round 42 on fresh splits (pre-registered)

Written 12 October 2026 before any fitting.

## Question
Round 42 (one split, seed 41001) gave p = 0.059. Was that a property of the Dravidian anchors, or the luck of one division of the inscriptions?

## Unchanged from round 42
Anchors (24 signs), permutation groups (numerals among numerals, pictures among pictures), PDr trigram LM, 150-chunk inventory, homophonic emission term, 60,000 annealing steps, fit seed 41050, 80/20 split with near-duplicate removal, held-out statistic (mean per-text log-likelihood). Code: round 41 `anchored.py`, imported unchanged.

## New
- **10 fresh splits**, seeds 43001–43010. The round 42 split (41001) is excluded.
- **60 permutations**, seeds 43100–43159. Permutation k is the same shuffled anchor key on every split.
- **Linear B control:** the same 10 splits, 20 permutations (seeds 43300–43319), 24 true values.

## Statistics
- **Pooled (primary):**
  - T_real = the mean over the 10 splits of the held-out log-likelihood with the real anchors.
  - T_k = the same mean for permutation k.
  - p = (1 + #{k : T_k ≥ T_real}) / 61.
  - The splits overlap, so pooling over a shared permutation is the valid test; per-split p-values are not independent.
- **Per split (secondary):**
  - The percentile of the real anchors among that split's 60 permutations.
  - The count of splits where the real anchors beat the null median.

## Gate
The Linear B control must pass: pooled p = 1/21, i.e. it beats all 20 permutations. If it fails, the Indus result is uninformative.

## Decision
- **REPLICATED:** the control passes, AND the Indus pooled p ≤ 0.05, AND the real anchors beat the null median on ≥ 8 of 10 splits. → Proceed to Step 3 (copper-tablet picture test), with its own pre-registration.
- **SUGGESTIVE:** pooled p ≤ 0.15.
- **NOT REPLICATED:** otherwise. Rounds 41–42 are then read as split luck, and the anchor-rebus branch is parked.
