# Ledger rules (adopted 22 October 2026, from the owner's instruction)

1. `reports/LEDGER.md` holds: certain facts (C), logical exclusions with scope (X), an exhaustive hypothesis set including "other" and the hypotheses not hoped for, priors with agreed ranges and reasons, and an update log.
2. Update: new odds = old odds × Bayes factor, renormalise. Fixed scale only: weak ×3, moderate ×10, strong ×30, decisive ×100; never more than ×100 from one test; reasoning for the size written down.
3. Pre-registration: before a scored test, a prereg file with question, data, procedure, outcome table and the Bayes factor for each outcome (including "no update"); `chmod 444` the prereg and the script; both sha256 in the commit message; everything already seen disclosed. Factors never chosen after results.
4. Gate: a scored test runs only if some outcome can move a hypothesis by ≥ ×3. Otherwise it is a measurement: it may add facts, it moves no probability. Say which up front.
5. No double counting: same data or same signal = one cluster, scored once. Only tests with decision rules fixed before the result are scored; earlier unregistered results inform priors and facts only. Never multiply weak factors from correlated tests.
6. Positive controls: a test for meaning or structure must first detect it in a known text of the same kind; if the control fails the test is VOID.
7. Robustness: a result within ~0.5 sd of its threshold gets a replicate check (e.g. 10 fresh seeds, ≥ 8 agree) before scoring, built into the rule from the start; a lucky run is withdrawn by reversing its factor, logged not deleted.
8. Model-hunting: declare in advance how many variants will be tried; disclose every try; discount factors (×10 → ×3) when more than one was needed.
9. Fragility after each update: priors at range edges, and the most influential test dropped; if the ranking flips, say "neither is clearly ahead".
10. Language: the leader is "the best surviving explanation"; say how much of its lead is from removed objections versus positive matches; a probability for language says nothing about which language.
11. Occam: test the simplest hypothesis first; add a layer only when a measured fact forces it; count layers.
12. Failures are results: every null and every withdrawal stays in the ledger.
