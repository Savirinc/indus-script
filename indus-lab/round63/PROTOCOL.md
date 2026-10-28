# Round 63: Is the Indus corpus big enough to be deciphered at all? (pre-registered measurement)

Written 28 October 2026, before `run63.py` exists. Nothing in this round has been run. Disclosed in advance:
- **Round 32 results are known.** Linear B, related-language lexicon, word boundaries, 150k steps, one homophone draw:
  - 173 sign IDs (20 tokens/sign): 83% token accuracy;
  - 239 IDs (14 tokens/sign): 18%, and 30% at 600k steps;
  - 373 IDs: 8%.
- **A timing check was run on 28 October 2026.** The round 32 `sweep_exploratory.py` at target 200 (209 IDs, about 16.5 tokens/sign) gave 7.6% at 10k steps with 1 chain, and 9.2% at 150k steps with 4 chains, taking 18 s. This is the only new number seen.
- **Indus counts were computed** (`FC.TRAIN`, 1,936 texts):
  - 582 sign types, 8,726 tokens, so 15.0 tokens/sign;
  - 302 signs occur at most twice;
  - mean text length 4.51.
- **Bourdeau's allograph merge (round 33, `allographs.md`) was applied to the corpus.**
  - All 30 groups give 539 signs, or 16.2 tokens/sign.
  - Without the two groups that merge numerals (1~2, 3~4) it gives 541 signs, or 16.1 tokens/sign. Merging numerals with different stroke counts is not defensible, so 541 is the merged figure used here.
  - His merge covers only the 223 signs with 5 or more tokens. It does not touch the long tail.

## Question
Arham's mission question: could the Indus script be deciphered from the material that exists? Round 32 says decoding collapses somewhere between 20 and 14 tokens per sign, and Indus sits at 15. That threshold rests on one draw at each of four points, and it was measured with word boundaries. Indus has none.

This round measures **where the threshold lies, with replicates, under two regimes**:
- **R1 (kind):** words with boundaries, as in round 32's sweep.
- **R2 (Indus-like):** 1–3 words run together per text with no dividers, as in round 32's condition D.

It then places the Indus corpus on that curve, raw and merged, and states **how many signs the Indus list would need to shrink to** for decoding to become possible. The test can only say what a corpus of this density allows when the right language is supplied. It cannot say which language that is.

## Ledger status (rule 4)
**Measurement, cluster K3 (continued).** It adds a fact (C21) and moves no probability. Recoverability bears on what can be learned, not on what the signs encode, under any hypothesis (N, R, L or O).

## Data
- **Cipher text:** NeuroDecipher `linear_b-greek.cog` (commit 480bad2), 919 words, about 3,451 sign tokens. This is the same file as round 32; its sha256 goes in `results.json`.
- **Lexicons:**
  - **Greek (true language):** round 32 `lex_cognate` over all words. These are the 1,432 forms produced by round 32's fixed Greek-to-Linear B spelling rules.
  - **Finnish (impossible language, negative control):** all 1,727 IDS Finnish forms (lexibank IDS, `Language_ID` 128, column `Form`). They are spelled with the same syllabifier:
    1. NFD normalisation, then drop combining marks; æ→a, ü→u, ö→o.
    2. Map consonants: b→p, g→k, f→p, v→w, l→r, h dropped; all other letters unchanged.
    3. Feed the resulting string through round 32's `to_lb` syllabification. Its vowel and consonant-cluster rules are unchanged.
    4. Forms that give nothing are dropped.
- **Solver:** round 32 `benchmark.py` v2 (bigram LM, simulated annealing with the homophonic emission term), imported unchanged. T0 3.0, T1 0.05, k 0.1, 4 chains.

## Procedure
1. **Sign-ID ladder.**
   - Seven target sizes: **120, 150, 170, 190, 210, 230, 250** sign IDs.
   - Homophones are assigned exactly as in `sweep_exploratory.py`: k signs per value, proportional to frequency and capped at 11.
   - The realised ID count and the tokens/sign (tokens ÷ IDs) are recorded. The tokens/sign figure, not the target, is the x-axis.
2. **Draws.**
   - For each target and regime, 5 independent homophone layouts (layout seeds 63001–63005; the token-to-homophone seed is layout seed + 500).
   - For R2, the grouping of words into texts uses seed layout seed + 900.
   - Chain seeds are 63100–63103.
3. **Search length.**
   - **Primary: 600k steps.** It is the stronger search; round 32 showed that 150k under-searches at 239 IDs.
   - Every draw is also run at 150k and reported, but it does not enter the verdict.
4. **Per run**, record:
   - token accuracy;
   - type accuracy (signs with 5 or more tokens);
   - the best objective and the true key's objective;
   - whether the true key scores at or above the best key found;
   - frequency-baseline accuracy.
5. **Recovered level.**
   - A level is **recovered** in a regime if the **median token accuracy over its 5 draws is ≥ 0.50**.
   - **t\*_R** is the lowest tokens/sign at which that level and every denser level (higher tokens/sign) are recovered.
   - **N\*_R = 8,726 / t\*_R** is the largest Indus sign inventory the threshold allows, rounded down.
6. **Indus placement.**
   - Compare against Indus raw (15.0 tokens/sign, 582 signs) and Indus merged (16.1, 541 signs).
   - Descriptively, give the share of signs seen at most twice in each Linear B layout against Indus (52%). This shows how far the frequency profile differs.

## Controls (must pass, or the round is VOID: rule 6)
- **Positive control (replicates round 32).**
  - Setup: R1, target 170, Greek lexicon, 150k steps, 5 draws.
  - **Passes if** median token accuracy ≥ 0.70. Round 32 got 83% at 173 IDs with one draw.
- **Negative control (impossible language).**
  - Setup: R1, target 120 (the easiest level), Finnish lexicon, 600k steps, 5 draws.
  - **Passes if** median token accuracy ≤ 0.15.
  - Accuracy must come from the right language, not from frequency or solver structure. Round 45 is the reason this control exists.

## Verdict, fixed now
Here "merged" means Indus at 16.1 tokens/sign (541 signs).

| Verdict | Condition |
|---|---|
| **REACHABLE** | Merged ≥ t\*_R2. The existing corpus, after defensible merging, is dense enough even without word dividers, given the right language. |
| **KIND-ONLY** | Merged ≥ t\*_R1 but < t\*_R2. Reachable only if word boundaries were known. |
| **OUT OF REACH** | Merged < t\*_R1. Even the kind regime needs a smaller sign list or more text than exists. |

If a regime never reaches 0.50, even at target 120, it is reported as **no threshold in range** for that regime, with N\* below 8,726 / (tokens/sign at target 120).

**Robustness (rule 7).**
- If the median at either level bracketing a threshold lies in [0.45, 0.55], 5 further draws are run there (seeds 63006–63010).
- The level counts as recovered only if at least 6 of the 10 draws are ≥ 0.50.
- If Indus merged falls within 0.5 tokens/sign of a t\*, the report says "at the threshold" next to the verdict word.

## What this can and cannot show
- **Cannot:** which language the Indus script records, or whether it is language at all. Every run is handed the correct language.
- **Linear B is a pure syllabary, cleaner than Indus.**
  - Its long tail is milder: homophones are spread by frequency, while 52% of Indus signs occur at most twice.
  - Its corpus is smaller: 3,451 tokens against 8,726. The same tokens/sign in a larger corpus may be easier.
  - The direction of the overall bias is not known. The threshold is a reference point, not a guarantee.
- **Can:** turn "decipherable in principle?" into a number. That number is the sign count the Indus list would have to reach, which palaeographers can check against published sign lists. It also says whether the merge available today closes the gap.

## Outputs
`run63.py`, `results.json`, `run63.log` and `REPORT.md`, plus:
- a row in `docs/STATUS.md`;
- fact C21 and a K3 row in `reports/LEDGER.md` (no factor);
- updates to the CLAUDE.md round list, the README tables and CITATION.cff (version 0.63.0).

Expected compute: about 155 runs at 18–75 s each, in 4 parallel processes, about 40 minutes.

## Amendment 1 (28 October 2026, before any result was read)
The first full run (log kept as `run63_attempt1.log`) completed every fit but crashed on writing `results.json`: numpy booleans are not JSON-serialisable. The only result seen was the traceback. Fix: `json.dumps(..., default=lambda o: o.item())` on that one line; nothing else in the script changed. New `run63.py` sha256 e3170197ca6400b8b0889f803e0e475216eec16f2c7828e38b930ef31420a917 (was 32d480e8…5d3b). All runs are seeded, so the rerun must reproduce the per-run lines of attempt 1 exactly; this is checked and reported.
