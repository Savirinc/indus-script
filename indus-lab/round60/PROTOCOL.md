# Round 60: Does sign order matter under the atlas key? (pre-registered measurement)

Written 24 October 2026, before `run60.py` exists. Nothing in this round has been run yet. Disclosed in advance:
- The readings atlas (`indus-lab/readings-atlas`, commit 5091d3a) has already measured dictionary coverage under the atlas key: 69.0% for the atlas key against a mean of 67.6% for 20 scrambled keys (ledger C19). That test changed the values and kept the order.
- No order-permuted reading has been computed or looked at.

## Question
Arham's point: in a language, order carries meaning. *rat*, *art* and *tar* are words and *atr* is not, and the scribes chose one order. So **keep the atlas key exactly as it is, and change only the order of the signs inside each inscription.** Does the true order give more Sanskrit dictionary words than reordered versions of the same signs? Is that gain larger for the atlas key than for keys known to be wrong?

## Ledger status (rule 4)
**Measurement.** It adds a fact and moves no probability.
- The key is Yajnadevam's expanded key and the corpus is the one cluster K7 has already used (rounds 47, 49, 57, 59). Rule 5 therefore rules out a fresh score.
- The order-gain statistic has no calibration from known scripts read with wrong keys, apart from the control below.
- An ORDER SIGNAL would justify a separately pre-registered, scored follow-up on held-out inscriptions.

## Data
- **Inscriptions:** the readings-atlas records (`build_atlas.CAND`, signs in reading order via `signs_of`). Kept are records in which every sign has an atlas value and that have at least 3 signs, deduplicated by sign sequence. One- and two-sign texts have too few orders to test.
- **Reading and scoring:** unchanged from the atlas.
  - The reading is `build_atlas.reading` (Yajnadevam's vowel rule).
  - Coverage is `build_atlas.gloss`: the share of letters covered by DCS dictionary words of three or more letters, under the author's sound grouping.
- **Keys:**
  - the atlas key;
  - the atlas's 20 scrambled keys: round 47 `shuffle_key`, frequency bins over all atlas records, seeds 46901–46920, exactly as in `build_atlas.main`.

## Procedure
1. **Orders.** For each inscription:
   - (a) the true order;
   - (b) the reversed order;
   - (c) 20 random permutations of its signs. They are drawn once with seed 60101 and are the same for every key, so all comparisons are paired. A permutation may reproduce the true order; it is kept.
2. **Statistics, for each key k:**
   - `T_k` is the mean coverage in the true order. `P_kj` is the mean coverage under permutation set j.
   - `G_k = T_k − mean_j P_kj` is the order gain. `Grev_k = T_k − mean coverage reversed`.
   - `pct_k` is the share of the 20 `P_kj` strictly below `T_k`. `z_k = G_k / sd_j(P_kj)`.
   - The result for the atlas key is set against the same statistics for the 20 scrambled keys.
3. **Per inscription (descriptive, `order_ledger.csv`):**
   - coverage in the true order and when reversed;
   - the mean over permutations;
   - the share of permutations scoring at or above the true order.

## Controls (must pass, or the round is VOID: rule 6)
- **Positive control: real Sanskrit, with Indus-length windows.**
  - Text: round 58 `controls/RAM_S1.txt` (Rāmāyaṇa, written syllables, one verse line per row).
  - Windows: for each Indus inscription of length n, draw one random line with at least n units and take n consecutive units (seed 60201). Units are concatenated as the reading.
  - Orders: the same scheme as step 1, with 20 permutations (seed 60202).
  - "Wrong keys": 20 substitutions of syllable types within frequency bins of 20. These use round 47 `freq_bins`/`shuffle_key` on the identity key, seeds 60401–60420.
  - **Passes if** `pct = 1.0`, `z ≥ 3`, and `G` for the true text exceeds `G` for all 20 substitutions.
- **Negative control: order-free strings.**
  - Units are drawn independently from the RAM_S1 unit frequencies, with the same lengths (seed 60301) and 20 permutations (seed 60302).
  - **Passes if** `|z| < 3`. True order should not stand out where order carries nothing.

## Verdict for the atlas key, fixed now
| Verdict | Condition |
|---|---|
| **ORDER SIGNAL** | `pct = 1.0`, `z ≥ 3`, and `G_atlas` above the `G` of all 20 scrambled keys |
| **ORDER, NOT KEY** | `pct = 1.0` and `z ≥ 3`, but 2 or more scrambled keys have `G ≥ G_atlas` (Indus sign order is regular whichever key reads it) |
| **NO ORDER EFFECT** | `pct < 1.0` or `z < 3` |

**Robustness (rule 7).**
- If exactly 1 of 20 scrambled keys has `G ≥ G_atlas`, 20 further keys (seeds 46921–46940) are drawn. ORDER SIGNAL stands if no more than 2 of the 40 are at or above.
- If `z` for the atlas key is between 2.5 and 3.5, the 20 permutations are redrawn 10 times (seeds 60111–60120). The verdict stands only if at least 8 of 10 agree.

## Outputs
`run60.py`, `results.json`, `order_ledger.csv`, `run60.log`, `REPORT.md`; a row in `docs/STATUS.md`; a fact in `reports/LEDGER.md` (no factor).
