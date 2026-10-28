# Round 65b: How many of the texts' own names must be known from outside before the right language works? (pre-registered measurement)

Written 28 October 2026, before `run65b.py` exists. Disclosed in advance:
- **Round 65 has been seen in full.**
  - In the round 64 logosyllabic Linear B cipher, the plaintext's own Greek words decode the text (0.86) and stand out from 9 wrong languages (first in 4 of 5 layouts by R).
  - An independent Ancient Greek word list (IDS) neither decodes (0.12) nor stands out (first in 1 of 5, R 0.29).
- **Of the 919 Linear B words, 455 have a Greek personal or place-name form** in `ext/neurodecipher/data/linear_b-greek.names.cog`, row-aligned with the main file. This was counted today; no fit has been run with them.

## Question
For Indus, the realistic source of overlap with the texts is **names attested outside the script**:
- Meluhhan persons in Mesopotamian records;
- names on Gulf seals.

These are sound strings, usable whatever language one assumes. The question has two parts:
1. **Decoding.** What fraction of the texts' names must be known for the right-language word list (G-IDS) plus those names to decode the text?
2. **Discrimination.** At what fraction does that lexicon stand out from wrong languages given the *same* names?

## Ledger status (rule 4)
**Measurement, cluster K3 (continued).** It moves no probability about Indus. If the solver control passes it adds fact C25.

## Setup (round 65 unchanged unless stated)
- **Cipher.** `run64.build(0.42, 'R2', 70, seed, True)` and round 65's decoy (within-segment shuffle, seed + 700). Layouts **65001–65005**, the same as round 65 (extra 65006–65010).
- **Solver.** Round 32 v2: 4 chains, seeds 65300–65303, 600k steps.
- **Lexicons.** Round 65's `lexicon()` and spelling rule, imported unchanged.
- **Statistic.** Round 65's **R = D ÷ I** (order gain on the real cipher over the decoy, divided by the lexicon's own order gain), computed with round 65's functions.

## Known names
- **Name pool:** the 455 words with a name form in `names.cog`. Their name forms are spelled with round 32's `to_lb`. Every name form of a sampled word is included.
- **Fractions f = 0.05, 0.10, 0.25, 0.50** of the pool, about 23, 46, 114 and 228 words. Samples are nested (one shuffle of the pool with `random.Random(65950)`; the first ⌈f·455⌉ words are taken). The same set is used in every layout. It is not related to which words became word signs.
- **The names are added to every lexicon:** G-IDS and the 9 wrong languages (Finnish, Basque, Hungarian, Hawaiian, Maori, Spanish, Latin, Sanskrit, Persian). External names do not belong to any language hypothesis.
- **Descriptive extra:** NAMES-only, the known names alone as the lexicon, real cipher only. It asks whether the names decode on their own, as anchors.

## Runs
- **Main set:** 4 fractions × 10 lexicons × 5 layouts × {real, decoy} = 400 fits.
- **NAMES-only:** 4 fractions × 5 layouts, real cipher only = 20 fits.
- **Solver control:** G-same (no names) on the real cipher, 5 layouts = 5 fits. These repeat round 65's runs, and must reproduce its accuracies exactly, which also checks determinism.

## Controls
- **Positive (rule 6):** G-same median accuracy ≥ 0.70. Otherwise the round is VOID.
- **Negative:** the 9 wrong languages, given the same names. Finnish and Basque are among them.

## Statistics and verdict (fixed now)
For each f, compute two things:
- **Decoded at f:** the median, over layouts, of G-IDS + names sound-token accuracy is ≥ 0.50.
- **Discriminates at f:** G-IDS + names has the highest R among the 10 lexicons in ≥ 4 of 5 layouts.

Each threshold is the smallest f such that the condition holds at that f and at every larger f tested:
- **f_dec** for decoding;
- **f_disc** for discrimination.

| Verdict | Condition |
|---|---|
| **NAMES CLOSE THE GAP** | f_disc exists. Report f_disc, f_dec and the number of names they mean. |
| **NAMES DECODE, BUT DO NOT IDENTIFY THE LANGUAGE** | f_dec exists, f_disc does not. Known names make the text readable, but wrong languages given the same names look as good. |
| **NOT CLOSED AT 50%** | Neither exists. |
| **VOID** | The solver control fails. |

**Robustness (rule 7).**
- If, at the fraction bracketing f_disc, G-IDS is first in exactly 3 of 5, run layouts 65006–65010 at that fraction (all 10 lexicons, real and decoy). It passes with ≥ 7 of 10.
- If a bracketing decoding median lies in [0.45, 0.55], run the same 5 extra layouts for G-IDS at that f. It passes if ≥ 6 of 10 are ≥ 0.50.

## Bearing on Indus (stated now)
The number of names at f_dec and f_disc is to be compared with what exists for Indus: a handful of proposed Meluhhan personal names in cuneiform, none tied to a specific seal. If the thresholds need dozens of names, the conclusion is that the external-name route needs far more material than is known.

## Limits, stated now
- **Kinder than Indus:**
  - The known names are spelled exactly as the cipher spells them (`to_lb` is the rule that made the plaintext, with a few exceptions). Cuneiform renderings of foreign names would be noisier.
  - They are known to be in the texts.
- Names that became word signs in a layout cannot help that layout. That loss is part of the measurement.
- The Linear B corpus is about half names, a share close to what is assumed for Indus seals but not known.

## Outputs
`run65b.py`, `results.json`, `run65b.log`, `REPORT.md`; STATUS, ledger (C25 and a K3 row), CLAUDE.md, README and CITATION (0.65.1). Expected compute: 425 fits on 8 processes, about 35 minutes.
