# Round 40 — Is round 39's Dravidian lead a dictionary-size artefact? (pre-registered)

Written 12 October 2026 before running. Uses round 39's code, targets, glosses, baseline and seeds unchanged. Only the lexicon sizes change.

## Design
- Munda has 712 glossed forms. PDR (6,088), EUS (1,340) and FIN (1,592) are each randomly subsampled to 712 forms (without replacement), independently, 100 times (seeds 40000–40099).
- BUR (37 forms) cannot be equalised upward and is excluded from the ranking.
- In each subsample, compute round 39's A_F (mean sound+meaning advantage over the shape-matched Vedic baseline) for:
  - the 41 Dravidian loans (control);
  - the 124 glossed Kuiper words.

## Decision (fixed)
- **Control holds at equal size** if PDR has the highest A among {PDR, MUNDA, EUS, FIN} on the Dravidian loans in ≥ 90% of subsamples.
  - If not, the method lacks power at equal size; the premise check is INCONCLUSIVE.
- **Premise HOLDS** if, on Kuiper's words, A_PDR > A_MUNDA in ≥ 90% of subsamples AND A_PDR > max(A_EUS, A_FIN) in ≥ 90%.
- **Premise FAILS** (the lead was a size artefact) if A_PDR > A_MUNDA in ≤ 60% of subsamples.
- Otherwise WEAKENED.
