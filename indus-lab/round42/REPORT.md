# Round 42 — 24 Dravidian anchors vs 100 shuffles: SUGGESTIVE (p = 0.059; pre-registered bar 0.05)

12 October 2026.

## Setup
- 24 signs were fixed to Proto-Dravidian words chosen by a rule set before fitting.
- **Pictures:**
  - fish *mīn*
  - man *āḷ*
  - arrow *ampu*
  - jar *agal*
  - leaf *elay* (two signs)
  - bird *piṭṭ-*
- **Numerals 1–8.**
- The other signs were fitted on 80% of the inscriptions and scored on the unseen 20% (226 texts, near-duplicates removed).
- Null: 100 refits with the anchor values shuffled (numerals among numerals, pictures among pictures).

## Result

| Run | Real anchors (held-out log-likelihood) | Shuffled anchors | p | Verdict |
|---|---:|---|---:|---|
| Linear B control (24 true values) | −19.09 | best of 30 = −19.89 | 1/31 | PASS |
| **Indus (24 Dravidian values)** | **−46.89** | mean −49.65; 5 of 100 better (best −46.05) | **0.059** | **SUGGESTIVE** |

## Reading it honestly
- **The good news:** the Dravidian values fit unseen inscriptions better than 95% of misassignments. Round 41 (17 anchors) pointed the same way (3rd of 16).
- **The caveat:** the pre-registered bar (p ≤ 0.05) was not met. A p of 0.06 is borderline, and two related tests leaning the same way are not independent proof. They share the corpus, the split and most anchors.
- Under the protocol, Step 3 (the copper-tablet picture test) is NOT triggered.

## The decisive next step
A pre-registered **replication on fresh splits**: the same anchors and model, on several new train/test divisions of the inscriptions. If the Dravidian values beat ≥95% of shuffles on most new splits, the signal is real. If it scatters, this was the luck of one split.

Files: `PROTOCOL.md`, `run42.py` (reuses round 41's model), `part_*.json`, `results.json`.
