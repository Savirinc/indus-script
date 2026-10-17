# Round 43 — Fresh-split replication of round 42: SUGGESTIVE again (pooled p = 0.066; bar 0.05)

12 October 2026. Protocol: `PROTOCOL.md`, written before fitting. Round 44 (`../round44/PROTOCOL.md`), the copper-tablet test, was pre-registered while this ran but is NOT triggered.

## Result

| | Real anchors (mean held-out LL, 10 splits) | Shuffled anchors (same shuffle across splits) | Pooled p | Splits above null median | Verdict |
|---|---:|---|---:|---:|---|
| Linear B control (true values) | −19.21 | mean −21.88, best −21.32 (of 20) | 1/21 | 10/10 | PASS |
| **Indus (24 Dravidian values)** | **−46.13** | mean −48.75; 3 of 60 better (best −45.51) | **0.066** | **10/10** | **SUGGESTIVE** |

Per split, the Dravidian values beat 55, 60, 55, 55, 58, 58, 57, 58, 55 and 57 of 60 shuffles (split 0 first). In the table's order (splits 0–9):

| Split | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| Shuffles beaten (of 60) | 58 | 60 | 55 | 55 | 58 | 58 | 57 | 58 | 55 | 57 |

The splits overlap, so the pooled test is the one that counts.

## Diagnostic (after the decision; does not change it)
- One might suspect the 3 winning shuffles were near-copies of the real key, since numeral shuffles can leave values in place. They are not: they leave 7, 2 and 1 of the 24 values unchanged. The correlation between "values left unchanged" and score is 0.11.
- So a few genuinely wrong assignments fit as well as the Dravidian one.

## Reading
- **Not split luck.** On every one of 10 new divisions the Dravidian values rank in the top ~8% of reassignments. The ranking is stable.
- **Not decisive.** About 1 in 20 random reassignments of the same 14 Dravidian words does as well. The test cannot distinguish "these are the right sound values" from "these words have phonotactic shapes that happen to suit these signs' contexts".
- Three related tests (rounds 41–43) all landed at p ≈ 0.05–0.19, always on the positive side. That is consistent with a weak real signal or with a mild systematic bias in the method. The method's ceiling at 24 anchors has been reached; more runs of the same design will not settle it.

## Deviations
- The LM's memo cache was cleared before each fit to stop memory exhaustion. One process was OOM-killed and restarted. Results are unchanged: round 42's −46.888 / −19.093 were reproduced exactly with the fix.

Files: `PROTOCOL.md`, `run43.py`, `analyze43.py`, `split_*.json`, `results.json`.
