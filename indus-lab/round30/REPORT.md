# Round 30 — Gulf-type round seals are statistically foreign to Indus-valley writing

11 October 2026. Pre-registered test (PROTOCOL.md) **SUPPORTS** a published qualitative claim (Parpola; Vidale 2004; Laursen 2010). No sound, meaning or language is assigned.

## Result

| Test (pre-registered) | Group | n | Mean percentile vs length-matched Indus-valley seal texts | One-sided p | Decision |
|---|---|---:|---:|---:|---|
| P1: bigram surprisal | Round (SEAL:C) seals from Mesopotamia, Bahrain, Luristan | 8 | **0.916** | <5e-5 (floor) | **SUPPORT** |
| P2: bigram surprisal | Square seals/sealing found abroad (Kish, Gonur, Salut, Umma, Altyn Depe) | 5 | 0.606 | 0.21 | not anomalous (underpowered) |
| P3: sign-frequency surprise only | Round foreign seals | 8 | 0.860 | 1e-4 | descriptive |
| P3: order surprise, sign composition fixed | Round foreign seals | 8 | 0.883 | <5e-5 | descriptive |
| All foreign texts | All eligible | 16 | 0.778 | <5e-5 | descriptive |
| Sensitivity: all-types control pool | Round foreign seals | 8 | 0.911 | <5e-5 | unchanged |

A percentile of 0.5 means a foreign text is as predictable as a typical Indus-valley seal text of the same length. At 0.916, six of the eight round seals are less predictable than more than 93% of matched native seal texts.

Power checks used the same lengths and threshold. Simulated pseudo-writing (random signs drawn at Indus frequencies) was detected in 100% of 200 simulations. Shuffled order was detected in 98.5%.

## Training and controls
The bigram model was trained on 1,936 Indus-valley text types. Every text, foreign or control, was scored by a model trained without that text and without any text one edit away from it. Controls are 1,078 in-region square-seal text types. Inputs, code and per-text values are in results.json.

## Independent critic pass (separate agent; scripts in critic/)
- The rerun of `foreign_context.py` in a copy produced a byte-identical results.json.
- The neighbourhood exclusion matched a brute-force check on 68 texts with 0 mismatches.
- Direction: reversing the two L/R foreign texts, or reading all of them in the best-scoring direction, leaves the result at 0.91–0.92.
- Control pools:

  | Control pool | Mean percentile |
  |---|---:|
  | All seals | 0.915 |
  | SEAL:R | 0.920 |
  | Non-seal texts | 0.908 |
  | Poor-condition seals | 0.900 |

  Poor-condition native seals score 0.515 against the square-seal pool, so wear alone does not create the effect.
- Leave-one-out within the foreign group gives 0.904–0.943. The five Bahrain seals alone score 0.880 (p=4e-4).
- Strongest attenuation: comparing only against native texts that are themselves novel (nearest corpus relative at least 3 edits away) gives 0.764, p=0.004. That still meets the SUPPORT threshold.
- Removing sign-frequency effects (bigram minus unigram bits): all 8 foreign texts are positive, against 30% of controls, giving 0.904. The anomaly is in sign-to-sign transitions, not only in rare signs.
- No two foreign round seals are within 3 edits of each other. None has a one-edit relative in the Indus corpus.

## Post-hoc observations (exploratory; I had seen the texts before designing these)
1. **Seal format accounts for only part of the effect.** The six eligible round and cylinder seals from inside the Indus region score 0.663 (p=0.086). They are somewhat atypical, but well short of 0.916.
2. **The "twins" sign (ICIT 091, two joined human figures).**
   - It begins 3 of the 8 foreign round seals in reading order and appears in a 4th. A single-sign 091 round seal from Kalba (UAE) also exists but has no direction field, so it is ineligible.
   - It appears in only 2 of 1,078 eligible Indus-valley square-seal types.
   - Sharing of first signs within the foreign group exceeds a pooled-token reshuffle (4 pairs vs 0.78 expected, p=0.013).
   - This independently matches Laursen 2010 (p. 117): a prefixed "twins" sign is "the only rule-like regularity so far attested in this 'western written language'".
   - The anomaly does not depend on 091. Treating it as unknown gives 0.974. The four foreign seals without it score 0.976.
3. **Frequent stroke numerals and the "man" signs.** Signs 031–033 (one to three strokes), 093 ("man" variant) and 055 appear often. This fits Vidale's suggestion of personal-name or patronymic formulas, but that is not tested here.

## What this establishes
Round seals of the Gulf type, found at Ur, in Bahrain and in Luristan, carry Indus-sign sequences whose transitions are measurably unlike Indus-valley usage. The test used held-out, length-matched controls with leakage and near-duplicate controls. The effect is not explained by sign rarity, reading direction, wear, text length, near-duplication or the choice of control pool.

**Correction (round 33).** This is NOT the first quantitative test. Rao et al. 2009 already quantified that West Asian seals follow different rules, and Bourdeau's `gulf.py` (cyphersolver) measures it too: 47% of adjacent pairs are familiar against 70% at home, and endings are missing. Round 30's added value is the held-out, length-matched, leave-neighbourhood-out design; the circular-versus-square split; and the transcription sensitivity in round 31.

## What it does not establish
It cannot distinguish:
- a non-Indus language written in Indus signs (Parpola, Vidale),
- personal names or titles following foreign conventions,
- pseudo-script made by non-literate seal cutters (the British Museum notes this possibility for U.17649; Laursen treats one Karzakan seal as pseudo-script),
- systematic misreading of worn foreign seals by modern editors.

The internal regularity (the 091 prefix) argues somewhat against purely random pseudo-writing. With n=8 it is not decisive. The square-seal "normal abroad" contrast is underpowered (n=5).

Transcriptions were not checked against photographs. Most of these eight seals are published only in drawings or small photos.

## Why this matters for decipherment
If these seals record foreign (Dilmun or Mesopotamian) personal names, they are the one place where an Indus sign sequence could be matched to a name written in cuneiform. Dilmun and Meluhha personal names from about 2100–1900 BCE are attested in readable records. That is the only route in this project that can, even in principle, yield a sound value.

## Reproduce
From the folder containing `indus-lab`:
1. `python3 indus-lab/round30/foreign_context.py` (about 50 s).
2. `python3 indus-lab/round30/critic_checks.py`.

The critic's scripts are in `round30/critic/`. Standard library only, plus Pillow for `signs.png`.
