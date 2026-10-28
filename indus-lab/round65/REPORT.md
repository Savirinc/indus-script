# Round 65: Can the fit tell the right language from wrong ones? ONLY WITH THE TEXT'S OWN WORDS

28 October 2026. Protocol and script locked at 33a9556 before any fit. 120 fits at 600k steps, 8 processes. No amendments, and no robustness draws were triggered. The first launch failed before any fit ran (wrong relative path to Python in the background shell); it produced no output and was relaunched with absolute paths.

## Verdict: ONLY WITH THE TEXT'S OWN WORDS

| Check | Bar | Result |
|---|---|---|
| Solver control: G-same accuracy on the real cipher | median ≥ 0.70 | **0.855**, pass |
| G-same (plaintext's own words) first among itself + 9 wrong languages | ≥ 4 of 5 | **4 of 5** (lost layout 65005 to Persian, 0.575 against 0.569) |
| **G-IDS (independent Ancient Greek word list) first among itself + 9 wrong** | ≥ 4 of 5 | **1 of 5** |

R = order gain on the real cipher over the shuffled decoy ÷ the language's own order gain. Medians over 5 layouts:

| Lexicon | R (median) | Range | Raw LL on cipher | Sound accuracy (truth, descriptive) |
|---|---:|---|---:|---:|
| **G-same** | **0.596** | 0.57–0.61 | −3.83 | **0.86** |
| **G-IDS** | **0.293** | 0.28–0.40 | −4.11 | **0.12** (0.03–0.26) |
| G-mod (descriptive) | 0.253 | 0.18–0.32 | −4.21 | 0.14 |
| Persian | 0.394 | 0.19–0.58 | −4.39 | 0.07 |
| Latin | 0.335 | 0.27–0.39 | −4.22 | 0.04 |
| Basque | 0.271 | 0.24–0.30 | −4.19 | 0.02 |
| Spanish | 0.255 | 0.15–0.33 | −4.32 | 0.13 |
| Hungarian | 0.231 | 0.12–0.32 | −4.55 | 0.03 |
| Maori | 0.203 | 0.12–0.30 | −3.67 | 0.01 |
| Hawaiian | 0.199 | 0.14–0.31 | −3.61 | 0.00 |
| Sanskrit | 0.195 | 0.08–0.31 | −3.63 | 0.09 |
| Finnish | 0.159 | 0.00–0.26 | −4.05 | 0.00 |

G-IDS ranks by layout: 4th, 2nd, **1st**, 5th, 3rd of 10.

## What it means
1. **With the inscriptions' own words, the right language stands out from the inside.** G-same scores about twice the order gain of any wrong language (0.60 against at most 0.39 by median) in 4 of 5 layouts.
2. **With an independent word list of the same language, it does not.** The Ancient Greek IDS list ranks in the middle of the wrong languages. Accuracy against the truth explains why: **the solver does not decode the cipher with it at all** (median 0.12, against 0.86 with the plaintext's words). The bottleneck is not only the statistic. Knowing the right language, but not its words, is not enough to decode a corpus this small.
3. **The round 45 trap reappears.** By raw fit, Hawaiian (−3.61), Sanskrit (−3.63) and Maori (−3.67) beat even the true lexicon (−3.83). They are open-syllable languages whose bigrams suit a CV syllabary. Any claim that "language X fits the Indus signs best" by raw likelihood is uninformative.
4. **Descriptively**, by the unnormalised gain D, G-IDS is first in 3 of 5 layouts (lost to Latin and Spanish). This was not the pre-registered statistic, so the verdict stays.

## Bearing on Indus
Every candidate lexicon for Indus is a G-IDS, not a G-same:
- a dictionary of reconstructed Proto-Dravidian;
- Vedic Sanskrit;
- Munda.

None of these is the inscriptions' own vocabulary, which is probably largely names and titles. In this simulation, kinder than Indus (the right language is among the candidates, word signs are separable, the sound inventory is known), such a lexicon neither decodes the text nor can be picked out from wrong languages. **The missing ingredient is not corpus size (round 64). It is lexical overlap with the actual texts.** That points to the external routes:
- bilingual or anchored texts;
- names known from Mesopotamian records (the Meluhhan names, the Gulf seals of rounds 30–35 and 50–51);
- a much larger and more text-like candidate corpus.

## Limits
- **Linear B words are mostly names and commodities, as Indus words probably are.** An IDS concept list misses names in any language, so this test is hard on G-IDS by design. A Greek list of names would be a different, fairer right-language lexicon, and is the obvious follow-up.
- Each candidate has only about 1,500 words, spelled by one fixed rule. Ancient Greek through that rule is not identical to round 32's Greek→Linear B rule (λ→r and voiced→voiceless agree; aspirates and some clusters differ slightly).
- There are 5 layouts. The R values of small lexicons (Persian 865 words, own gain 0.50) vary most.

## Ledger
Measurement, cluster K3, no factor. Adds fact C24.

## Reproduce
`cd indus-lab/round65 && ../../ext/venv/bin/python run65.py` (about 20 minutes on 8 processes). It needs numpy (`ext/venv`), NeuroDecipher data and lexibank IDS.
