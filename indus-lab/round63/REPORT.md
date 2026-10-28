# Round 63: Decipherability threshold with replicates: VOID

28 October 2026. Protocol `PROTOCOL.md` (sha256 e2a3ccb3…2a66df, locked at c5f4b4c; Amendment 1 at aa4f453). Script `run63.py` (amended sha256 in aa4f453). 145 runs, 8 processes.

## Verdict: VOID (rule 6)

| Control | Bar | Result | |
|---|---|---|---|
| Positive: Greek lexicon, R1, target 170 (182 IDs, 19.0 tokens/sign), **150k steps**, 5 draws | median ≥ 0.70 | **0.271** | **FAIL** |
| Negative: Finnish lexicon, R1, target 120 (134 IDs), 600k steps, 5 draws | median ≤ 0.15 | 0.031 (draws 0.000–0.051) | pass |

The positive control failed, so by the protocol's own rule nothing below is a verdict.

**The fault is in the protocol, and it is mine.** I set the control at 150k steps to match round 32, where 150k gave 83% at 173 IDs. That 83% came from one homophone layout. With five fresh layouts, 150k steps under-searches: the same five layouts at 600k reach a median of 0.833 (0.70–0.86). The control tested search length, not whether the solver can decode Linear B. Reading it at 600k now would be a post hoc rescue, so it is not done.

**Amendment 1 and determinism.** The first full run crashed while writing `results.json` (numpy booleans), after all fits had finished. Only the traceback was read. The dump line was fixed and recorded before any result was read, and the run was repeated. All 145 per-run lines of attempt 1 (`run63_attempt1.log`) and attempt 2 (`run63.log`) are identical.

## Descriptive results (not scored, no verdict word)
Median token accuracy over 5 draws at 600k steps, with the 150k median in brackets. "True ≥ best" counts the draws in which the true key's score was at least that of the best key the search found.

| Target | Sign IDs | Tokens/sign | R1: words with boundaries | true ≥ best | R2: 1–3 words, no dividers | true ≥ best |
|---:|---:|---:|---:|---:|---:|---:|
| 120 | 134 | 25.8 | 0.857 (0.779) | 0/5 | 0.847 (0.153) | 0/5 |
| 150 | 164 | 21.0 | 0.858 (0.355) | 0/5 | 0.777 (0.115) | 0/5 |
| 170 | 182 | 19.0 | 0.833 (0.271) | 0/5 | 0.353 (0.069) | 1/5 |
| 190 | 200 | 17.3 | 0.756 (0.236) | 0/5 | 0.135 (0.056) | 4/5 |
| 210 | 220 | 15.7 | 0.405 (0.136) | 0/5 | 0.167 (0.079) | 2/5 |
| 230 | 239 | 14.4 | 0.378 (0.117) | 0/5 | 0.122 (0.060) | 0/5 |
| 250 | 260 | 13.3 | 0.195 (0.128) | 0/5 | 0.066 (0.051) | 0/5 |

Under the protocol's definitions:
- **R1:** the threshold falls at **17.3 tokens/sign**, so an Indus list of at most about **505 signs** would be needed.
- **R2:** it falls at **21.0 tokens/sign**, so at most about **414 signs**. A level between 21.0 and 19.0 was not tested.
- **Indus:** raw is 15.0 tokens/sign (582 signs) and the defensible merge is 16.1 (541). Both sit below both thresholds. If the control had passed, the locked rule would have given OUT OF REACH. It did not pass, so this is description only.

Further observations:
- **Search versus model.**
  - In R2 at 17.3 and 15.7 tokens/sign, the true key scores at or above the best key found in 4 of 5 and 2 of 5 draws. There the model prefers the truth and the annealer fails to reach it, so a stronger search could lower the R2 threshold.
  - At the dense levels the reverse holds. The search finds keys that score above the truth while still reaching 85% accuracy, which is overfitting at the margin, as in round 32.
- **150k against 600k.** The steep gap shows that search length dominates in the no-divider regime: 0.153 against 0.847 at 25.8 tokens/sign.
- **Long tail.** In these Linear B layouts only 2–4% of sign IDs occur at most twice. In Indus it is 52%. By that measure the Linear B thresholds are kinder than the Indus case.

## What this means
- **Nothing is scored.** The ledger is unchanged apart from a VOID row under K3.
- **The description agrees with round 32.** The only defensible sign merge available today (Bourdeau's groups, without the numeral merges) moves Indus from 15.0 to 16.1 tokens/sign. On this description that is not enough even with word boundaries known and the right language supplied.
- **The no-divider regime is the Indus-like one.** It points to a sign list near 414 signs, about the size of the most compact published Indus sign lists (Mahadevan 1977 lists 417). Whether a list that compact is palaeographically defensible is a question for epigraphers, not for this harness.

## Next step
Round 63b: the same ladder with fresh layout seeds and the positive control specified at 600k steps, pre-registered before running. It takes about 15 minutes of compute. Its R2 ladder adds a level between 19 and 21 tokens/sign.

## Reproduce
`cd indus-lab/round63 && ../../ext/venv/bin/python run63.py`. This needs numpy (`ext/venv`), NeuroDecipher data and lexibank IDS (`setup/setup_external.sh`). Set `R63_PROCS` to change the number of processes.
