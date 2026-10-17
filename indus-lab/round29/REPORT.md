# Round 29 — Exact conditional-order test: MIXED (pre-registered); exploratory result favours adjacency over position

11 October 2026. Independent audit round. No sound, meaning or language is inferred.

## Audit of inputs (before testing)
- `verify_manifest.py`: 400 files, 0 mismatches. `raw/inscriptions.csv` SHA256 matches the handoff (c22d39c3…3429).
- Round 27 (`cross_city.py`, `robustness.py`) rerun in a separate copy: all four output files byte-identical to the shipped ones.
- Round 28 (`joint_control.py`) rerun: `results.json` byte-identical. Its 2×2 checkerboard swap is accepted only when two same-length texts hold the same two signs crosswise, which explains the 0.4–1.6% movement. The sampler limitation in the round-28 report is accurate.

## Design (see PROTOCOL.md, written before execution)
Instead of sampling rearranged training corpora, condition on each test inscription's own sign multiset and compute, exactly, how much probability a source-city model puts on the true order versus every other distinct ordering. The sum over orderings uses dynamic programming over (remaining multiset, previous sign); it was checked against brute-force enumeration on 60 texts (max difference 1.4e-14). Splits are the frozen round-27 one-edit-excluded test sets. Texts longer than 9 signs (5–22 per condition) and single-ordering texts (0–4) were excluded, as specified.

Lower = better. U = log2(number of distinct orderings) = uniform guess.

## Pre-registered primary result: MIXED

| Train → test | Subset | n | U | POS (exact-length slots) | BIG | POS+BIG | POS − POS+BIG, 95% CI |
|---|---|---:|---:|---:|---:|---:|---|
| Harappa → Mohenjo-daro | all | 717 | 8.00 | 8.68 | 5.74 | 8.20 | +0.48 [0.10, 0.84] |
| Mohenjo-daro → Harappa | all | 420 | 6.04 | 8.29 | 6.33 | 9.90 | −1.61 [−2.37, −0.84] |
| Harappa → Mohenjo-daro | SEAL:S | 598 | 7.40 | 6.87 | 4.75 | 6.30 | +0.57 [0.24, 0.90] |
| Mohenjo-daro → Harappa | SEAL:S | 118 | 8.07 | 8.12 | 4.89 | 7.25 | +0.88 [−0.15, 1.82] |

Mean bits per text to identify the true order given its signs. Two conditions above 0, one below and one including 0: under the decision rule this is MIXED.

Controls behaved as required in all four conditions. Negative control (orders resampled from POS): POS+BIG never beat POS, with differences of −4.2 to −5.3 bits. So the metric is not biased toward bigrams. Positive control (orders resampled from BIG): POS+BIG beat POS by +2.5 to +3.5 bits, so the test had power.

## Flaw in my own primary design
The exact-length slot model (POS) is **worse than a uniform guess** in 3 of 4 conditions. Exact-length slot counts are too sparse to transfer across cities. A product with a badly calibrated expert also degrades BIG: POS+BIG is worse than BIG alone everywhere. So "BIG beyond POS" was a weak benchmark. The MIXED verdict mainly reflects that weakness. It is not evidence that position explains order.

## Exploratory follow-up (post hoc; NOT pre-registered)
POS3 is a length-independent initial/medial/final position model with the same smoothing.

| Condition | U | POS3 | BIG | U − BIG (95% CI) | U − POS3 (95% CI) |
|---|---:|---:|---:|---|---|
| all H→M | 8.00 | 7.52 | 5.74 | +2.26 [1.85, 2.65] | +0.47 [0.15, 0.77] |
| all M→H | 6.04 | 7.05 | 6.33 | −0.28 [−1.08, 0.48] | −1.01 [−1.53, −0.51] |
| SEAL:S H→M | 7.40 | 6.28 | 4.75 | +2.65 [2.28, 3.03] | +1.12 [0.80, 1.41] |
| SEAL:S M→H | 8.07 | 6.62 | 4.89 | +3.18 [2.09, 4.29] | +1.45 [0.81, 2.00] |

Reading: given only which signs an unseen inscription contains, a bigram model from the other city recovers its order 2.3–3.2 bits better than chance in 3 of 4 conditions. That is roughly a 5–9× higher probability on the true order. In those conditions it also beats the best tested position-only model by about 1.5–1.8 bits. The exception is Mohenjo-daro → Harappa on all object types, where nothing beats chance. A plausible cause is Harappa's large non-seal component (tablets and other types with different conventions), but this is untested.

## What this changes
- Round 28's "joint composition + position" explanation is not supported for the tested position models: with composition held exactly fixed, slot position transfers weakly or not at all, while adjacency transfers strongly on seals.
- This holds only for the position models tested. A richer template model (e.g. sign-class grammars, formula fragments longer than 2) is not excluded.
- Every statistic here is unchanged by any relabelling of sign IDs. It says nothing about sounds or language family. Structured nonlinguistic systems can also show strong adjacency structure.
- The prior literature already reports sequential structure in Indus texts. This round adds a cross-city, composition-conditioned, near-duplicate-excluded measurement. It does not add a reading.

## Reproduce
From the folder containing `indus-lab`: `python3 indus-lab/round29/conditional_order.py` (about 35 s), then `python3 indus-lab/round29/exploratory.py`. Standard library only. Outputs: `results.json`, `per_text_*.json`, `exploratory_results.json`.
