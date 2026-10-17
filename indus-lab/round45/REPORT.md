# Round 45 — Bias check: Finnish fits as well as Dravidian → ARTEFACT. Anchor-rebus branch parked.

13 October 2026. Protocol: `PROTOCOL.md`, written before fitting.

## Result
The same test as round 43: 24 anchor signs, 10 fresh splits, 60 shared shuffles. Only the language changes.

| Language | Could it be Harappan? | Real values beat shuffles (per split, of 60) | Mean percentile | Pooled p |
|---|---|---|---:|---:|
| Proto-Dravidian (round 43) | candidate | 58, 60, 55, 55, 58, 58, 57, 58, 55, 57 | 0.95 | 0.066 |
| **Finnish (control)** | no | 59, 58, 57, 57, 58, 57, 57, 59, 60, 60 | **0.97** | **0.016** |
| Basque (control) | no | 21, 19, 12, 7, 13, 23, 22, 25, 22, 23 | 0.31 | 0.72 |

Pre-registered rule: if either control reaches pooled p ≤ 0.15, the result is **ARTEFACT**. Finnish reached p = 0.016, stronger than Dravidian.

## What this means
- The method rewards something other than the true language. A language with no possible connection to the Indus valley "fits" the inscriptions better than Proto-Dravidian.
- Rounds 41–43 (p ≈ 0.19, 0.06, 0.07 for Dravidian) are therefore **not evidence for Dravidian**. The negative control did its job.
- Basque's failure shows the artefact is not universal. Some property of a language's anchor words, plausibly word shape (CV(C)CV words, numeral lengths), interacts with the sign contexts. That property has nothing to do with being the right language.
- Exploratory diagnostic (after the decision): the real keys give same-concept signs (e.g. 001/031) the same value, which shuffles break. The correlation of "pairs kept" with shuffle score is weak (PDr 0.21, FIN −0.10, EUS −0.22), so this does not explain the result on its own. The mechanism is not identified.

## Decision
Per the protocol and CLAUDE-PROMPT ("park a branch if it yields no discriminating prediction"), the anchor-rebus branch (rounds 41–45) is **parked**. Round 44 (copper tablets) will not run on this basis.

Files: `PROTOCOL.md`, `run45.py`, `analyze45.py`, `diag45.py`, `split_*.json`, `results.json`.
