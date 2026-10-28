# Round 65b: How many of the texts' own names must be known? NOT CLOSED AT 50%

28 October 2026. Protocol and script locked at 7c51f74 before any fit. 425 fits at 600k steps, 8 processes. No amendments, and no robustness draws were triggered. The first launch did not start (the background shell ignored `cd`, so the script was not found). It produced no fits and was relaunched with the absolute script path. The G-same control reproduces round 65's five accuracies exactly (determinism check passed).

## Verdict: NOT CLOSED AT 50%

| Names known (of 455 name words) | G-IDS + names first by R (of 5) | G-IDS + names accuracy, median (range) | Names alone, accuracy (range) |
|---|---:|---:|---:|
| 0 (round 65) | 1 | 0.12 (0.03–0.26) | n/a |
| 5% (23 words) | 2 | 0.18 (0.05–0.27) | 0.10 (0.00–0.21) |
| 10% (46) | 0 | 0.11 (0.04–0.24) | 0.09 (0.00–0.11) |
| 25% (114) | 0 | 0.12 (0.07–0.15) | 0.09 (0.05–0.26) |
| **50% (228)** | **1** | **0.20** (0.02–0.24) | **0.28** (0.08–0.57) |
| Bar | ≥ 4 | ≥ 0.50 | descriptive |

The solver control passed: G-same median 0.855.

The wrong languages, given the same names, decode 0.00–0.15 (medians). Their R values overlap G-IDS's at every fraction. Latin, Persian and Hungarian lead at different fractions.

## What it means
1. **Knowing half of the texts' names, spelled exactly as the texts spell them, does not make an independent word list of the right language decode the text** (0.20 against 0.86 with the full plaintext vocabulary). Nor does it make that list stand out from wrong languages given the same names.
2. **The names alone start to work only at 50%**, and unevenly: 0.57 in one layout, 0.08 in another.
3. **So in this setting the solver needs nearly the texts' whole vocabulary.** Rounds 63b–65 had been treating "the right language" as one thing. Here it is clear that this instrument needs "the right *words*".

## Why, and the limit that matters most
The solver scores a decoding only through a **syllable-bigram model** built from the lexicon. A known name adds a few bigrams to a model of about 1,500 words. It does not tell the solver *where* in the texts that name stands.

A solver that matched whole known words against sign sequences would use names very differently. Each match would fix several signs at once, which is the anchor route: round 32 needed about 40 anchored signs.

So this result bounds **this instrument** (bigram-model fitting, which is also what most published Indus "fits" amount to). It does not bound decipherment by name-matching. That route is untested here.

## Bearing on Indus
- For Indus, only a handful of Meluhhan personal names are proposed from cuneiform, none tied to a seal. That is far below even the 5% level tested here, and these were exact spellings known to be in the texts.
- **Fitting a candidate language's dictionary to the Indus signs cannot work on this corpus, with or without the known names.** That goes for Dravidian, Sanskrit, Munda or any other.
- What is left is anchoring. External evidence would tie particular sign sequences to particular names or words:
  - a seal of a known person;
  - a bilingual;
  - a Gulf seal with a cuneiform caption.

## Limits
- **Kinder than Indus:**
  - names spelled exactly as in the texts;
  - the right language present;
  - word signs single-use;
  - the sound inventory known.
- **Names that became word signs in a layout cannot help that layout,** since about 42% of words are word signs. That is part of the measurement.
- Nested name samples from one shuffle: a different draw of names could do somewhat better or worse. There are 5 layouts per fraction.

## Ledger
Measurement, cluster K3, no factor. Adds fact C25.

## Reproduce
`../../ext/venv/bin/python run65b.py` from this folder (about 35 minutes on 8 processes). It needs numpy (`ext/venv`), NeuroDecipher data and lexibank IDS.
