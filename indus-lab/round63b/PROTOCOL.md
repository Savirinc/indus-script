# Round 63b: Decipherability threshold, replication with a correctly specified control (pre-registered measurement)

Written 28 October 2026, before `run63b.py` exists. Disclosed in advance: **all of round 63 has been seen** (`../round63/REPORT.md`, `results.json`).
- Round 63 was VOID. Its positive control was set at 150k steps, scored 0.271 and failed.
- Descriptively, round 63 put the thresholds at about 17.3 tokens/sign with word boundaries (R1) and 21.0 without dividers (R2). Indus merged sits at 16.1.

Round 63b is the replication. It uses fresh seeds and a control that tests decoding, not search length.

## Question, data, solver
These are unchanged from round 63 (`../round63/PROTOCOL.md`):
- Linear B `linear_b-greek.cog`;
- the Greek cognate lexicon and the Finnish IDS lexicon, with the same spelling rules;
- round 32 v2 solver, imported unchanged, with 4 chains;
- homophones assigned as in `sweep_exploratory.py`;
- regimes R1 (words with boundaries) and R2 (1–3 words per text, no dividers);
- Indus 8,726 tokens: raw 582 signs (15.0 tokens/sign), merged 541 signs (16.1). The merge is Bourdeau's groups without the numeral merges.

## Changes from round 63, all fixed now
1. **Fresh seeds.**
   - Layout seeds 63201–63205. The token-to-homophone seed is layout + 500; the grouping seed is layout + 900.
   - Robustness seeds 63206–63210.
   - Chain seeds 63300–63303.
2. **600k steps only.** Round 63 showed that 150k under-searches, so 150k is dropped.
3. **Ladder.** Two levels are added inside the gaps round 63 left: target **160** (between 21.0 and 19.0 tokens/sign) and target **200** (between 17.3 and 15.7). Targets are 120, 150, 160, 170, 190, 200, 210, 230 and 250, in both regimes.
4. **Positive control:** Greek lexicon, R1, target 170, **600k steps**, 5 draws (these are ladder runs). **Passes if** median token accuracy ≥ 0.70.
5. **Negative control:** unchanged. Finnish lexicon, R1, target 120, 600k, 5 draws (seeds above). **Passes if** median ≤ 0.15.

## Statistic, verdict and robustness
These are unchanged from round 63:
- A level is **recovered** if the median token accuracy over 5 draws is ≥ 0.50.
- **t\*_R** is the sparsest level in the contiguous recovered run that starts at the densest level. **N\*_R** = ⌊8,726 / t\*_R⌋.
- Verdict, against Indus merged (16.1 tokens/sign):

| Verdict | Condition |
|---|---|
| **REACHABLE** | merged ≥ t\*_R2 |
| **KIND-ONLY** | merged ≥ t\*_R1 but < t\*_R2 |
| **OUT OF REACH** | merged < t\*_R1 |
| **VOID** | either control fails |

- If the median at a level bracketing a threshold lies in [0.45, 0.55], 5 more draws are run and the level is recovered only if at least 6 of 10 are ≥ 0.50.
- If merged is within 0.5 tokens/sign of a t\*, the report adds "at the threshold".
- **Replication check, descriptive:** whether each t\* agrees with round 63's description within one ladder step.

## Ledger status
**Measurement, cluster K3 (continued)**, no factor. If both controls pass, the thresholds and the verdict enter `reports/LEDGER.md` as fact C21.

## Caveats, unchanged from round 63
- The test is handed the correct language. It says nothing about which language Indus records.
- Linear B's long tail is milder than Indus's (2–4% of signs occur at most twice against 52%), and its corpus is smaller (3,451 tokens against 8,726). The threshold is a reference point.

## Outputs
`run63b.py`, `results.json`, `run63b.log` and `REPORT.md`; a STATUS row; a ledger row; CLAUDE.md, README and CITATION updates. Expected compute: 95 runs at 600k on 8 processes, about 15–20 minutes.
