# Round 55: Do the stroke signs behave like numerals, and what does that do to the repetition argument (X7)? (pre-registered measurement)

Written 22 October 2026. No script for this round exists, and nothing in it has been computed. Disclosed in advance:
- The stroke signs' corpus frequencies, from the `icit_count` column of `raw/icit_m77_map.tsv` (read to identify the signs).
- Round 52b's figures: merging the 17 stroke signs raises the Indus repetition rate from 3.5% to 17.7%, and about one text in seven holds two different stroke signs, often adjacent.
- Round 58's full results.
- The token format of the proto-Elamite and proto-cuneiform control files.

## Ledger status (rule 4)
**This is a measurement, not a scored test.** Numerals are expected under all three hypotheses: tallies under N, quantities with names or commodities under R, numbers within a full script under L. So no outcome here moves L, R, N or O. The outputs are facts, plus a corrected scope for X7.

## Why now
Round 58 excluded bijective Sanskrit and Old Tamil syllabic keys in 10 of 14 conditions. Its scope said "merging the stroke numerals undoes it (17.7%)". That caveat is logically wrong, and the correction is fixed here, before any number is computed:
- Merging all 17 stroke signs into one corresponds to a key that gives one-stroke, two-stroke and three-stroke signs **the same syllable**. That is neither a numeral reading nor any published key.
- Under a **numeral reading**, a stroke sign stands for a number, not a syllable of the text. A one-syllable-per-sign key would then apply only to the other signs. The right comparison removes the stroke signs and measures repetition in what is left.
- Under the **ordinary-sign reading**, round 58 stands as computed.

So two things need measuring:
- **M1:** does the corpus support the numeral reading?
- **M2:** does X7 survive under it?

## The stroke signs (ICIT numbers, as in round 52b's `NUMERALS`; counts from the CISI descriptions via `icit_m77_map.tsv`)
| Count | Short strokes | Tall strokes |
|---|---|---|
| 1 | 001 | 031 |
| 2 | 002 | 032 |
| 3 | 003, 013 | 033 |
| 4 | 004, 014, 034 | – |
| 5 | 005 | 035 |
| 6 | 016 | – |
| 7 | 017 | – |
| 8 | 018 | – |
| unknown | 015, 036 (no Mahadevan equivalent in the map) | |

The set S is all 17 signs. Counts are used only in the descriptive item D1. 015 and 036 are in S but out of D1.

## Data
- **Indus:** `FC.TRAIN` (1,936 texts, 8,726 tokens), as in rounds 52, 52b and 58.
- **Positive-control corpora:** round 52b's PE (proto-Elamite) and U4+U3 (proto-cuneiform, pooled). In each, the numeral control set is the count signs of the basic unit N01: tokens `k(N01)`, k = 1–9. That is the closest known analogue of a set of stroke counts.
- **Sanskrit and Old Tamil units for M2:** round 58's `controls/`, unchanged (sha256 in `round58/SHA256SUMS`).

## M1: do the stroke signs form a substitution class?
Statistic F(S): the share of tokens of S whose frame is also filled, somewhere in the corpus, by a *different* member of S. The frame is the (left neighbour, right neighbour) pair, with text start and end counting as neighbours.

Null: 1,000 random sets matched sign for sign. Each member of S is replaced by a random non-member from the same frequency bin, with bins of 20 signs by frequency rank (round 47's rule) and no sign drawn twice. Indus result: the percentile of F(S) among the 1,000. Seeds 55001–56000.

**Positive control:**
- In each control corpus, draw 20 Indus-shaped samples (round 52's `indus_sample`, seeds 55101+). In each sample, set the numeral control set against 200 matched random sets drawn as above.
- The control passes if the median percentile over the 20 samples is ≥ 0.95, in PE and in U4+U3 separately.
- If either fails, M1 is **VOID** (rule 6), and M2 is still reported, since it does not depend on M1.

**Reading (fixed now):**
- percentile ≥ 0.99: "the stroke signs substitute for one another like a class (as numerals do in PE and proto-cuneiform)";
- below 0.95: "no class behaviour detected";
- in between: "weak".

**Limit stated now:** phonetic classes substitute too. In Greek, for example, vowels fill the same consonant frames. So M1 can show that S is a class. It cannot show that the class is numerals.

## M2: X7 under the numeral reading
1. Remove every member of S from the Indus texts and drop texts left empty. Record the new text count, the token total, the length list, and the repetition rate I_n on texts of two or more signs.
2. Re-run round 58's 14 conditions with the length list and token total of the stripped corpus. Use round 58's code, syllabifications, B = 300, decision rule (EXCLUDED: 0 samples ≤ I_n and gap ≥ 5 sd; NOT EXCLUDED: ≥ 3 samples ≤ I_n; otherwise 10 replicate blocks, ≥ 8 needed) and homophony items, with seeds 56001 + condition × 1000 + sample (replicates 70001 + condition × 1000 + block × 300 + sample).
3. Pipeline check: with the original lengths and seeds 58001–58300, round 58's function must reproduce round 58's stored RV_S1 mean, minimum and maximum exactly. Round 58 stored no per-sample values; this check replaced "first-sample value" before the protocol was locked.

## Decision on X7 wording (fixed now)
X7 is rewritten to state both readings side by side:
> "with stroke signs as ordinary signs: [round 58 list]; with stroke signs as numerals (removed): [M2 list]".

The "merged numerals (17.7%)" caveat is deleted as logically misplaced, for the reason given above, and the deletion is recorded in the ledger. If M1 finds a class (≥ 0.99), the numeral-reading line is marked as the reading the corpus supports. Otherwise both lines stand, unranked.

## Descriptive items (no verdict)
- **D1.** Frequency by stroke count, with same-count signs pooled: Spearman ρ between count (1–8) and frequency. The same for k(N01) in PE and U4+U3. Number words in known languages get rarer as the number grows. These Indus frequencies were partly seen before writing this (above), so D1 is not blind and carries no verdict.
- **D2.** Of the Indus texts with a repeated sign, how many repeat a stroke sign and how many repeat a non-stroke sign.
- **D3.** Position: the share of stroke-sign tokens that are text-initial, medial or final, against all signs.

## Files
`PROTOCOL.md` (this file; `chmod 444`, sha256 in the commit message, once the owner has read it), `run55.py` (`chmod 444`, sha256 in its commit message, committed before it is run), then `results.json`, `run55.log`, `REPORT.md`, a STATUS row, and the LEDGER (X7 rewritten, a new fact, no factor).
