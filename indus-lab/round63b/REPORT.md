# Round 63b: Decipherability threshold (replication): OUT OF REACH, at the threshold (R1)

28 October 2026. Protocol and script locked at 48ed157 before any run. 95 runs at 600k steps, 8 processes. No amendments. No robustness draws were triggered: no bracketing median fell in [0.45, 0.55].

## Verdict: OUT OF REACH, at the threshold (R1)

| Control | Bar | Result |
|---|---|---|
| Positive: Greek, R1, target 170 (182 IDs, 19.0 tokens/sign), 600k, 5 draws | median ≥ 0.70 | **0.846**, pass |
| Negative: Finnish, R1, target 120 (134 IDs, 25.8 tokens/sign), 600k, 5 draws | median ≤ 0.15 | **0.024**, pass |

| Regime | t\* (tokens/sign) | N\*: largest decodable Indus sign list | Indus merged (541 signs, 16.1) |
|---|---:|---:|---|
| R1: word boundaries known | **16.5** | **528** | below, by 0.4 tokens/sign (13 signs): "at the threshold" |
| R2: 1–3 words, no dividers (Indus-like) | **21.0** | **414** | below, by 4.9 tokens/sign (127 signs) |

Indus raw (582 signs, 15.0 tokens/sign) is below both thresholds.

## Ladder (median token accuracy over 5 draws, with the range)

| Target | Sign IDs | Tokens/sign | R1 median (range) | R2 median (range) | R2 true ≥ best |
|---:|---:|---:|---|---|---:|
| 120 | 134 | 25.8 | 0.858 (0.86–0.87) | 0.837 (0.83–0.84) | 0/5 |
| 150 | 164 | 21.0 | 0.858 (0.86–0.86) | **0.749** (0.44–0.80) | 0/5 |
| 160 | 173 | 19.9 | 0.861 (0.85–0.86) | 0.267 (0.12–0.77) | 3/5 |
| 170 | 182 | 19.0 | 0.846 (0.82–0.86) | 0.297 (0.09–0.52) | 3/5 |
| 190 | 200 | 17.3 | 0.807 (0.72–0.83) | 0.171 (0.10–0.33) | 4/5 |
| 200 | 209 | 16.5 | **0.636** (0.30–0.72) | 0.184 (0.07–0.43) | 3/5 |
| 210 | 220 | 15.7 | 0.357 (0.24–0.66) | 0.141 (0.11–0.18) | 1/5 |
| 230 | 239 | 14.4 | 0.396 (0.12–0.59) | 0.090 (0.05–0.14) | 1/5 |
| 250 | 260 | 13.3 | 0.222 (0.10–0.24) | 0.070 (0.06–0.13) | 0/5 |

In R1 the true key never scores at or above the best key found (0/5 at every level). The search finds higher-scoring keys that are still about 85% right.

**Replication against round 63 (descriptive).** Round 63 described R1 at 17.3 and R2 at 21.0 tokens/sign. 63b gives R1 16.5, which is the new level 200 that round 63 did not test, so it agrees within one ladder step. R2 is the same 21.0.

## What it means
1. **With the right language, word boundaries known and the best defensible merge, the Indus corpus is just short of decodable.** It needs at most about 528 signs and has 541. Thirteen more justified merges, or about 2.5% more text at 541 signs, would cross the line. That is close, but the margin is within one ladder step, which is why the protocol reports it as "at the threshold".
2. **Without word dividers, which is the actual Indus situation, it is well short.** That needs at most about 414 signs: 127 merges beyond what anyone has shown to be defensible, or about 30% more text at the current sign count.
3. **Past the threshold, the limit is search as much as the model.** In R2 between 16.5 and 19.9 tokens/sign, the true key scores at or above the best key found in 3–4 of 5 draws. A better search than this annealer could move the R2 threshold down. This is a methods lead, not a result.
4. **These are optimistic bounds for Indus.** Every run was given the correct language. Linear B has 2–4% of signs seen at most twice, against 52% for Indus. Its corpus is 3,451 tokens, against 8,726.

**Bearing on the mission.** Decipherment from today's corpus alone, by fitting a language, is out of reach at Indus conditions, even granting the right language. What would bring it within reach, in order of plausibility:
- **Anchors:** round 32 found that about 40 lift recovery to 72% at Indus density.
- **Knowing where words begin and end:** that alone moves the bar from 414 to 528 signs.
- **A palaeographically defended sign list near 414 signs.**
- **About 30% more text.**

## Ledger
Measurement, cluster K3, no factor. Adds fact C21.

## Reproduce
`cd indus-lab/round63b && ../../ext/venv/bin/python run63b.py`. This needs numpy (`ext/venv`), NeuroDecipher data and lexibank IDS. Set `R63_PROCS` to change the number of processes.
