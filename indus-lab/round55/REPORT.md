# Round 55: Stroke signs and the repetition argument. **M1: no numeral-class behaviour (controls passed); M2: under the numeral reading only 5 of 14 conditions stay EXCLUDED** (measurement)

Pre-registered in `PROTOCOL.md` (commit ec8922a; one wording change to the pipeline check made before locking, stated in the protocol). `run55.py` (sha256 in commit 2c9df8c) locked before the run. One run, 623 s. Outputs: `results.json`, `run55.log`.

**Ledger status:** a measurement under rule 4. It moves no probability. X7 is rewritten as fixed in the protocol, C18 is added, and the "merged numerals 17.7%" caveat is deleted as logically misplaced.

## M1: do the 17 stroke signs swap for one another like numerals?
| Corpus | Set | Median percentile vs frequency-matched random sets | Reading |
|---|---|---|---|
| Proto-Elamite (control) | count signs 1–9 of N01 | 1.000 | PASS |
| Proto-cuneiform U4+U3 (control) | count signs 1–9 of N01 | 1.000 | PASS |
| **Indus** | 17 stroke signs | **0.084** (F 0.263 vs null 0.350 ± 0.065) | **no class behaviour detected** |

The instrument finds numerals at once where we know they exist. The Indus stroke signs do **not** behave that way. They share their slots with each other *less* often than random signs of the same frequencies do. In proto-Elamite, "3 sheep" and "5 sheep" put different counts in the same slot all the time. Indus texts rarely show the same neighbours with different stroke counts.

This does not prove the strokes are not numbers. Indus numbers could attach to many different items, for example, so each frame would be rarely repeated. But the clearest numeral signature in the known counting systems is absent.

## M2: the repetition argument with the stroke signs removed
- Removing the 17 stroke signs leaves 1,935 texts and 7,283 tokens.
- The repetition rate falls to **2.64%** (from 3.51%).
- The pipeline check passed: round 58's Ṛgveda RV_S1 mean, minimum and maximum were reproduced exactly.

| Condition | Mean | Lowest | (m − I)/sd | Round 58 (strokes as signs) | **Round 55 (strokes removed)** |
|---|---:|---:|---:|---|---|
| Ṛgveda S1 | 5.6% | 4.0% | 5.1 | EXCLUDED | **EXCLUDED** |
| Ṛgveda S2 | 4.2% | 2.9% | 3.7 | not excluded | not excluded |
| Rāmāyaṇa S1 | 5.4% | 3.9% | 5.3 | EXCLUDED | **EXCLUDED** |
| Rāmāyaṇa S2 | 4.8% | 3.6% | 4.6 | EXCLUDED | not excluded |
| Sanskrit words S1 | 4.1% | 2.9% | 3.3 | not excluded | not excluded |
| Sanskrit words S2 | 4.2% | 2.5% | 3.1 | EXCLUDED | not excluded |
| Sanskrit names S1 | 4.9% | 3.3% | 4.5 | EXCLUDED | not excluded |
| Sanskrit names S2 | 5.1% | 3.7% | 4.7 | EXCLUDED | not excluded (1/10 replicates) |
| Puṟanāṉūṟu S1 | 6.3% | 4.7% | 6.3 | EXCLUDED | **EXCLUDED** |
| Puṟanāṉūṟu S2 | 3.8% | 2.7% | 2.7 | not excluded | not excluded |
| Old Tamil words S1 | 5.1% | 3.9% | 5.1 | EXCLUDED | **EXCLUDED** |
| Old Tamil words S2 | 5.5% | 3.6% | 5.4 | EXCLUDED | **EXCLUDED** |
| Old Tamil names S1 | 5.0% | 3.3% | 4.5 | EXCLUDED | not excluded |
| Old Tamil names S2 | 2.0% | 1.2% | −2.2 | not excluded | not excluded |

**Excluded under both readings (the robust core):**
- Ṛgveda and Rāmāyaṇa in written syllables;
- Puṟanāṉūṟu lines in written syllables;
- Old Tamil words in written and spoken syllables.

**Not excluded under the numeral reading:** every names condition in either language. In 12 of the 14 conditions not a single sample got as low as the stripped Indus rate; most conditions fail only the 5-sd margin. But the rule is the rule.

## Descriptive items (no verdict)
- **D1, frequency by stroke count:**
  - Indus counts 1–8: 248, **700**, 281, 73, 44, 30, 49, 6. Spearman ρ −0.86.
  - PE and proto-cuneiform: ρ −0.98, with 1 the commonest count.
  - In the Indus corpus, *two* strokes are almost three times as common as one. That is unlike the numeral systems used as controls. Not blind (frequencies seen in advance).
- **D2, which signs make the repeats:** of the 68 Indus texts with a repeated sign, 47 repeat only non-stroke signs, 20 only stroke signs, and 1 both.
- **D3, position:** stroke signs sit in the middle of texts 77% of the time, against 56% for all signs, and at the end only 7% (all signs 22%).

## Reading the result honestly
1. **Round 58's main result shrinks.** If the stroke signs are numbers, the black-swan exclusion holds only for keys that read **running text** (verses, poem lines or words) in written syllables, plus Old Tamil words in spoken syllables. It no longer reaches name lists in either language. Since seals most plausibly carry names and titles, the exclusion now misses the most likely kind of content.
2. **The corpus does not say the strokes are numbers.** M1 found no numeral-like swapping, and two strokes being commoner than one is odd for a counting system. So both readings stand unranked, as the protocol fixed in advance, and X7 is stated both ways.
3. **The earlier "merged 17.7%" caveat was wrong and is deleted.** It assumed a key in which every stroke sign has the same sound. No reading does that.

## Ledger
- X7 rewritten with both readings.
- C18 added.
- Cluster K14: no factor.
