# Round 42 — Dravidian anchors, expanded to 24 signs, 100 permutations (pre-registered)

Written 12 October 2026 before fitting. Same model, split, inventory, steps (60,000) and code as round 41, except for the following.

## Anchor selection rule (applied before fitting)
1. Use the Krishnamurti 2003 reconstruction whose meaning is exactly the concept.
2. Otherwise, use the first `pdr_04.csv` row (file order) whose meaning's first word is the concept, excluding forms marked "(?)".
3. Otherwise, drop the concept.

## Anchors
- The 17 signs from round 41, unchanged.
- Added:
  - 740 jar/pot = *agal* (agál- 'pot (earthen)', rule 2)
  - 803 and 806 leaf = *elay* (*el-ay, Krishnamurti, rule 1)
  - 269 bird = *pitt* (piṭṭ- 'bird', rule 2)
  - 004, 014, 034 four = *naal* (nāl- 'four', rule 2)
- Total: 24 signs.

## Permutation groups
- Numerals: values shuffled among the 15 numeral signs.
- Pictographs: values shuffled among the 9 picture signs.

## Test
- Indus: 100 permuted-anchor refits (seeds 42100–42199). p = (1 + #null ≥ real) / 101.
- Linear B control: the 24 most frequent sign IDs with their true values; 30 permutations (seeds 42300–42329). PASS if p ≤ 1/31.

## Decision
- **SUPPORTED:** the control passes AND Indus p ≤ 0.05 → proceed to Step 3 (copper-tablet picture test).
- **SUGGESTIVE:** 0.05 < p ≤ 0.15.
- Otherwise NOT SUPPORTED: the Dravidian rebus values for these signs do not fit the inscriptions better than misassigned values, at this power.
