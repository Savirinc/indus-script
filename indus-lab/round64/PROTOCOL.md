# Round 64: If the script is logosyllabic, can its sound signs be cracked? (pre-registered measurement)

Written 28 October 2026, before `run64.py` exists. Disclosed in advance:
- **Rounds 63 and 63b have been seen in full.** With the right language and every sign treated as a sound sign, decoding needs ≤ 528 signs with word boundaries and ≤ 414 without; Indus has 541 after a defensible merge.
- **Indus frequency profile, computed today** (`FC.TRAIN`, 8,726 tokens):

  | Most frequent signs | Share of tokens | Mean uses per sign |
  |---|---|---|
  | top 50 | 70% | 122 |
  | top 100 | 84% | 73 |
  | top 150 | 89% | 52 |
  | top 200 | 92% | 40 |

- **The Linear B word list has 919 words, all distinct**, with 3,451 syllable tokens (mean 3.76 per word). A word written with a word sign therefore occurs exactly once.

## Question
Many specialists hold the Indus script to be **logosyllabic**: a small set of frequent sound signs, mixed with many word signs. Rounds 63 and 63b treated all signs as sound signs. Here Linear B is rebuilt as a logosyllabic script at the Indus mix, and the question is whether the solver, given the right language, still recovers the **sound signs** when word signs are interleaved and no word dividers are written.

## Ledger status (rule 4)
**Measurement, cluster K3 (continued).** It moves no probability, because it is about recoverability under an assumed script type. If both controls pass it adds fact C22.

## Construction (Linear B made logosyllabic)
- **Word signs.**
  - A fraction **q** of the 919 words, chosen at random, are written as one word sign each (seed: layout + 300).
  - The fraction **q = 0.42** is fixed so that word signs make up about 16% of tokens. That matches the Indus share outside its top 100 signs: q·919 / (q·919 + (1 − q)·3,451) ≈ 0.16.
  - The control and baseline use **q = 0**.
- **Sound signs.**
  - The remaining words are spelled syllable by syllable, with homophones assigned by round 32's `sweep_exploratory` rule over the syllables that remain.
  - Targets **S = 70, 100, 130 and 160** sound-sign IDs. At S = 70 there is one sign per value.
  - The x-axis is **u = sound tokens ÷ sound-sign IDs that occur**.
- **Regimes.** R2 (1–3 words per text, no dividers; primary) and R1 (one word per text).
- **Solver:** round 32 v2, imported unchanged, with 4 chains (seeds 64300–64303) and 600k steps.

## Solver variants
- **Opaque rule (primary).**
  - Any sign that occurs **at most 2 times** in the cipher corpus is treated as a word sign. Texts are split at it and it is removed, so a word sign acts as a whole word, with a word ending before it and a word starting after it.
  - The same rule can be applied to Indus as it stands (302 of its 582 signs occur at most twice).
  - It also drops rare homophonous sound signs. Those tokens count as wrong.
- **Naive (comparison only).** All signs are treated as sound signs, as in round 63b.

## Statistic
**Sound-token accuracy** is the share of all sound-sign tokens in the corpus whose sign is decoded to its true syllable. Tokens dropped by the opaque rule count as wrong.

The median is taken over 5 layouts (seeds 64001–64005; token-to-homophone seed layout + 500; grouping seed layout + 900). A level is **recovered** if the median is ≥ 0.50.

## Runs (all 600k steps, 5 layouts each)
| Set | Lexicon | q | Regime | Solver | S |
|---|---|---|---|---|---|
| P: primary | Greek | 0.42 | R2 | opaque | 70, 100, 130, 160 |
| K: kind | Greek | 0.42 | R1 | opaque | 70, 100, 130, 160 |
| B: no word signs | Greek | 0 | R2 | opaque | 70, 100, 130, 160 |
| V: naive | Greek | 0.42 | R2 | naive | 70, 100, 130, 160 |
| Positive control | Greek | 0 | R1 | opaque | 70 |
| Negative control | Finnish (round 63 spelling) | 0.42 | R2 | opaque | 70 |

## Controls (rule 6, VOID if either fails)
- **Positive:** median ≥ 0.70.
- **Negative:** median ≤ 0.15.

## Verdict, fixed now (set P)
**u\*** is the lowest u in the contiguous recovered run that starts at S = 70, the densest level.

| Verdict | Condition |
|---|---|
| **SOUND PART RECOVERABLE** | u\* exists. The sound part of a logosyllabic script at the Indus word-sign share is recovered at ≥ u\* uses per sound sign. The report gives N\*, the largest N for which the Indus top-N signs have mean uses ≥ u\*, as the size of sound-sign set the Indus corpus could carry. |
| **NOT RECOVERED IN RANGE** | Even S = 70 is not recovered. The Linear B corpus cannot simulate the Indus top-100 density (73 uses per sign), so this does not exclude Indus. It says only that the test cannot show it. |
| **VOID** | Either control fails. |

**Robustness:** as in round 63. If a bracketing median lies in [0.45, 0.55], 5 further layouts (seeds 64006–64010) are run, and the level is recovered only if at least 6 of 10 are ≥ 0.50.

## What this can and cannot show
- **Kinder than Indus, and stated now:**
  - Every simulated word sign occurs exactly once, so the opaque rule separates word signs from sound signs almost perfectly. In Indus, some frequent signs (for example 740, the jar) may be word signs, and some rare signs may be sound signs.
  - The language is supplied.
  - Linear B's sound values are known to be about 70.
- **Harder than Indus:**
  - The corpus is small. u tops out near 29 uses per sound sign, against 73 for the Indus top 100.
- **Cannot:** show which Indus signs are sound signs, which language they spell, or that the script is logosyllabic at all.
- **Can:** show whether interleaved word signs at the Indus share destroy the sound-sign recovery that rounds 63 and 63b found possible.

## Outputs
`run64.py`, `results.json`, `run64.log`, `REPORT.md`; STATUS, ledger, CLAUDE.md, README and CITATION (0.64.0). Expected compute: 90 runs at 600k on 8 processes, about 15 minutes.
