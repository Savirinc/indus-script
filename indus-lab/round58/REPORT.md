# Round 58: Sanskrit and Tamil syllable repetition at Indus lengths. **PARTIAL: 10 of 14 conditions EXCLUDED** (measurement; all controls passed)

Pre-registered in `PROTOCOL.md` (commit 33baae6). Amendment 1 (Wikisource page formats; extraction only) and the locked `run58.py` (sha256 4d4c0872…) were committed in 513faef before the run. One run, B = 300 per condition, seeds 58001+ (main) and 59001+ (replicates). Run time 333 s. Outputs: `results.json`, `run58.log`.

**Ledger status:** a measurement under rule 4. It moves no probability for L, R, N or O. It adds exclusion X7 and fact C17 to `reports/LEDGER.md`.

## Question
Suppose a key gives every Indus sign one syllable and no two signs the same syllable. Then a seal has a repeated sign exactly when its reading has a repeated syllable. So the share of texts with a repeat must be the same on both sides of the key: 3.51% for the Indus corpus. Does real Sanskrit or Old Tamil, cut to exactly the Indus text lengths, ever repeat syllables that rarely?

## Controls: all passed
| Control | Required | Result |
|---|---|---|
| Syllabifier, 40 hand-checked words × 2 rules | 40/40 | 40/40 |
| Pipeline: Indus rate recomputed; round 52b SEAL sample 0 reproduced | 0.0351; exact | 0.035124; 0.144609 = 0.144609 |
| Sampler on the Indus texts themselves | mean within 0.01 of 0.0351 | 0.0375 (sd 0.0041) |

## Result
I = 0.0351. S1 = written syllable (akṣara, Brahmi-style); S2 = spoken syllable (the more generous rule). In the table, "≤ I" counts the samples, out of 300, that repeat as rarely as the Indus corpus or more rarely.

| Condition | Units | Mean | Lowest | Highest | ≤ I | (m − I)/sd | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| Ṛgveda S1 | 21,253 sentences | 8.1% | 6.5% | 10.1% | 0 | 7.1 | **EXCLUDED** |
| Ṛgveda S2 | | 6.1% | 4.5% | 7.6% | 0 | 4.7 | NOT EXCLUDED (replicates 1/10) |
| Rāmāyaṇa S1 | 38,004 sentences | 7.7% | 6.2% | 9.7% | 0 | 6.4 | **EXCLUDED** |
| Rāmāyaṇa S2 | | 6.7% | 4.8% | 8.1% | 0 | 5.3 | **EXCLUDED** |
| Sanskrit words S1 | 59,257 sentences | 6.2% | 4.5% | 7.7% | 0 | 4.7 | NOT EXCLUDED (replicates 2/10) |
| Sanskrit words S2 | | 6.3% | 5.0% | 8.2% | 0 | 5.2 | **EXCLUDED** |
| Sanskrit names S1 | 24,626 names | 6.9% | 5.5% | 8.7% | 0 | 5.5 | **EXCLUDED** |
| Sanskrit names S2 | | 7.1% | 5.2% | 8.6% | 0 | 6.0 | **EXCLUDED** |
| Puṟanāṉūṟu S1 | 4,729 lines | 9.3% | 7.2% | 11.1% | 0 | 8.8 | **EXCLUDED** |
| Puṟanāṉūṟu S2 | | 5.8% | 4.1% | 7.0% | 0 | 4.3 | NOT EXCLUDED (replicates 0/10) |
| Old Tamil words S1 | 4,729 lines | 7.5% | 5.8% | 9.1% | 0 | 7.3 | **EXCLUDED** |
| Old Tamil words S2 | | 9.0% | 7.4% | 11.6% | 0 | 8.1 | **EXCLUDED** |
| Old Tamil names S1 | 262 names | 7.5% | 6.2% | 9.0% | 0 | 6.9 | **EXCLUDED** |
| Old Tamil names S2 | | **3.2%** | 2.1% | 4.3% | **219** | −0.7 | **NOT EXCLUDED** |

The fallback that joins words or names when no unit is long enough was used for 0.15% of windows in Old Tamil words S2, and never anywhere else.

## Reading the result honestly
1. **Most of the class is closed.** The black-swan exclusion holds in 10 of 14 conditions. In those conditions, no bijective one-syllable-per-sign key can be correct, whatever its values. That covers:
   - Sanskrit in written syllables (Ṛgveda, Rāmāyaṇa, names);
   - Sanskrit in spoken syllables (Rāmāyaṇa, words, names);
   - Old Tamil in written syllables (poem lines, words, names);
   - Old Tamil words in spoken syllables.
2. **Three conditions stay open only because of the safety margin.** In Ṛgveda S2, Sanskrit words S1 and Puṟanāṉūṟu S2, none of the 300 samples was as low as the Indus corpus. Their lowest samples were 4.5%, 4.5% and 4.1%, against 3.5%. But the margin was below the locked 5 sd (4.7, 4.7, 4.3), and the replicates did not reach 8/10. By the rule fixed in advance they stay open. They are not re-scored here.
3. **One condition is a real failure of the idea.** Old Tamil names in spoken syllables (Sangam poets and patrons, e.g. *a·ti·ya·māṉ ne·ṭu·mā·ṉañ·ci*) repeat *less* often than the Indus corpus: 3.2% on average, with 219 of 300 samples at or below 3.5%. A seal corpus of Old Tamil names, written one spoken syllable per sign, would show exactly the Indus repetition rate. The repetition argument cannot exclude that reading. It is the one Dravidian-friendly door this round leaves open, and it is reported here without softening.
4. **The margin is smaller than I said before the run.** Sanskrit and Tamil syllables at seal lengths repeat 6–9%, not the 13–34% of the twelve corpora in X2. Those corpora counted letters or logograms from smaller inventories. Syllables come from inventories of hundreds to thousands, so they repeat less. The pre-run expectation was too optimistic.
5. **Homophony breaks the exclusion easily.** Two interchangeable signs per syllable, chosen at random, bring every condition to the Indus level or below (k = 2 or 3 in every condition; `results.json`). X7 therefore applies only to keys without homophones, as the protocol said.
6. **Merging the numerals reverses everything.** If the 17 stroke numerals are counted as one sign, the Indus rate is 17.7% (fact C4). Every one of the 4,200 samples falls below that. A key that reads the stroke signs as one repeated value cannot be excluded this way.

## Descriptive item 2: Yajnadevam's own readings
His key does use homophones (127 values over 714 signs), so X7 does not reach it. Measured directly, in his own readings:
- **20.4%** of his readings of the 1,934 texts contain a repeated written syllable;
- the same texts in sign space repeat 3.46%;
- real Sanskrit at the same lengths repeats **6.1–8.1%** on average, and **10.1%** in the highest of the 2,400 Sanskrit samples.

So his readings repeat syllables about three times as often as real Sanskrit does. This is not a scored result and not an exclusion. It is one more description in which his output text does not behave like Sanskrit, consistent with round 47.

## What this does not say
- Nothing about the Dravidian, Indo-Aryan or any other language family (ledger section f).
- Nothing about logosyllabic readings.
- Nothing about any key with homophones.
- Nothing about whether the seals record language at all.

## Ledger
- **X7 added:** the 10 conditions above, with scope.
- **C17 added:** the measured rates.
- No Bayes factor (rule 4). L, R, N and O are unchanged.
