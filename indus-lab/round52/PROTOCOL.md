# Round 52 — Which class of writing system does the Indus sign inventory behave like? (pre-registered)

Written 19 October 2026, before `run52.py` exists and before any statistic has been computed on any corpus. The only prior work was obtaining the control corpora and reading their file formats (recorded below). Committed before code.

## Question
Every decipherment claim presupposes a system type: Yajnadevam and Rao read the signs as an alphabet-like letter set; Parpola, Mahadevan and Fairservis as a logosyllabic system; Farmer, Sproat and Witzel as not writing at all. Sign-inventory size alone (582 types in the ICIT list; 417 in Mahadevan) is usually cited for "logosyllabic", but inventory depends on how allographs are split and on corpus size. This round asks, with corpus size and text length held equal, **which known class of writing system the Indus corpus is statistically nearest to, and whether it falls inside the normal range of any class at all.** Nothing here identifies sounds or language. Every statistic is invariant under relabelling of signs (CLAUDE.md rule), so this is Track 2 structure, not a reading.

## Classes and control corpora
Each control is a real text corpus in a known system, turned into sequences of sign tokens. Licence and source pinned in `fetch_controls.sh` and `SHA256SUMS`.

| Code | Class | Corpus | Sign token | Source, licence |
|---|---|---|---|---|
| GRK | alphabet | Homer, Iliad and Odyssey, Perseus `perseus-grc2` | letter, lower-cased, diacritics stripped, spaces and punctuation removed (scriptio continua, as inscriptions) | PerseusDL canonical-greekLit, CC BY-SA 4.0 |
| HEB | abjad | Westminster Leningrad Codex, Genesis–Deuteronomy | consonantal letter; points and cantillation stripped; final-letter forms merged with base letters; spaces removed | openscriptures/morphhb, public domain |
| CHR | syllabary | Cherokee New Testament | Cherokee syllabary character (U+13A0–13F5); spaces and punctuation removed | christos-c/bible-corpus, CC0 |
| SUX | logosyllabic | CDLI Ur III administrative texts in Sumerian (`#atf: lang sux`, catalogue period "Ur III", genre "Administrative") | ATF sign (hyphen-separated unit), mapped to its Oracc Global Sign List sign name where the value is listed, else kept as the value; determinatives in braces are signs; numeral tokens such as `5(disz)` are one sign each | cdli-gh/data dump (CC BY), oracc/ogsl |
| EGY | logo-consonantal | AES tomb inscriptions (`_aes_bbawgrabinschriften`) plus `_aes_smaek`, sentences whose every token carries an MdC encoding | Gardiner code from the `hiero` field, split on MdC operators `- : * & ( ) < >`; rotation and shading suffixes stripped | simondschweitzer/aes, CC BY-SA 4.0 |
| OBI | logographic | OBIMD oracle-bone inscriptions, groups whose category begins `InscriptionSentence`, characters in `OrderNumber` order, groups containing a placeholder (`SeatFont` ≠ 0) dropped | main-character UID (`Label`) | KLOBIP/OBIMD on Hugging Face, CC BY 4.0 |
| CHN | logographic (received text) | Shijing | character; punctuation removed | chinese-poetry/chinese-poetry, MIT |

Linear B, the usual positive control, has no openly licensed corpus of running tablet texts (DĀMOS is CC BY-NC-SA with no export; LiBER non-profit only; the repository's NeuroDecipher file is a word list). Cherokee therefore stands as the syllabary; it is modern and printed, which is stated as a limitation. Ugaritic (CC BY-NC) is not used.

Indus: `FC.TRAIN` from `round30/foreign_context.py` (core-region text types, deduplicated, reading order; 1,934 texts, 8,720 tokens, 582 types). Deduplication is kept because the controls are running texts without duplicates.

## Matching corpus conditions
An **Indus-shaped sample** of a control is built as follows. Let the Indus text-length multiset be L (lengths in signs of the 1,934 texts). Draw lengths from L with replacement until the token total reaches 8,720 (last text trimmed to hit the total exactly). For each drawn length ℓ, pick a random unit of the control (verse, line, sentence or group as listed above) with at least ℓ signs and take a random contiguous window of ℓ signs. Windows never cross a unit boundary. Because windows are not anchored at unit starts, no feature below depends on text-initial or text-final position.

B = 300 Indus-shaped samples per control corpus, seed 52001 + corpus index × 1000 + sample index.

## Features (computed identically on every sample and on the real Indus corpus)
1. **V**: number of distinct sign types.
2. **hapax**: share of types occurring once.
3. **top10**: share of tokens in the ten commonest types.
4. **H1**: unigram entropy, bits.
5. **H2/H1**: plug-in conditional entropy of the next sign given the previous one, over within-text adjacent pairs only, divided by H1.
6. **heaps**: slope of log V(n) against log n over the sample's tokens in random order, for n from 500 to 8,720.
7. **repeat**: share of texts of length ≥ 2 containing the same sign twice.
8. **double**: share of within-text adjacent pairs that are the same sign twice.

All eight are invariant under sign relabelling. V and hapax depend on how a sign list splits allographs; the Indus list is ICIT (Wells), the most split of the published lists, and this is a stated limitation. Each feature is standardised by the pooled within-corpus standard deviation across all control samples.

## Classification
Each class is modelled as a multivariate Gaussian on the eight standardised features, fitted to the samples of its corpora (alphabet: GRK and HEB pooled; syllabary: CHR; logosyllabic: SUX and EGY pooled; logographic: OBI and CHN pooled). Covariance is regularised by adding 0.05 to the diagonal. Distance is Mahalanobis; the 99% region is the chi-square(8) quantile 20.09.

## Positive control (must pass before the Indus result is read)
Leave-one-corpus-out at class level, for every corpus that has a partner in its class: fit the class models with that corpus removed, then classify each of its 300 samples by nearest class. Six tests: GRK, HEB, SUX, EGY, OBI, CHN. CHR has no partner; its within-corpus homogeneity is reported but is not a test.

- PASS: every one of the six tests assigns ≥ 80% of samples to the right class.
- WEAK: every test ≥ 50%, at least one below 80%. The Indus verdict is then reported with the suffix `(WEAK CONTROL)`.
- METHOD-FAIL: any test below 50%. The Indus numbers are reported as uninterpretable.

## Negative-control diagnostic
Two shuffled Indus corpora, reported but not part of the verdict: (a) sign order permuted within each text; (b) all 8,720 tokens permuted across texts, lengths kept. They show which features carry order information. A positive-control check of the diagnostic: the same two shuffles of one SUX sample must move H2/H1 towards 1.

## Verdict (the Indus corpus itself, one feature vector)
- `MATCH-<class>`: inside the 99% region of exactly one class.
- `AMBIGUOUS`: inside the 99% regions of two or more classes.
- `OUTSIDE-ALL, nearest <class>`: outside every region; the nearest class and all four distances are reported. This outcome cannot distinguish "a system unlike any control" from "an inventory-splitting artefact of the ICIT list", and the report must say so.
- `METHOD-FAIL` as above.

A verdict is a statement about the sign system's statistics at 8,720 tokens, not about language or meaning, and does not bear on whether the system encodes speech (round 56 addresses that).

## Robustness (reported, not part of the verdict)
Rerun the Indus vector with the five features that do not depend on inventory splitting (top10, H1, H2/H1, repeat, double) and report whether the nearest class changes.

## Pinned inputs and reproducibility
- `fetch_controls.sh` downloads every control at a pinned commit or revision; `SHA256SUMS` lists the downloaded files. Extracted token sequences are written to `controls/*.txt` (one unit per line, signs space-separated) and committed where the licence permits redistribution (all of the above do; CDLI and AES extracts are small subsets).
- `run52.py`, standard library only, writes `results.json` and `run52.log`.
- Seed 52001. B = 300. Stopping rule: one run; no reruns with other seeds unless the code is found to be wrong, in which case the fix and a rerun are recorded as an amendment before results.

## Amendment 1 (19 October 2026, after extraction, before any feature was computed)
Decisions forced by the file formats, recorded before `run52.py` is run:
1. Greek final sigma ς is merged with σ, as a positional allograph, by analogy with the Hebrew final-letter rule already stated.
2. Sumerian: the Oracc sign list spells the velar fricative `h`, so ATF `h` is kept as `h`; ATF `sz`, `s,`, `t,`, `j` become `š`, `ṣ`, `ṭ`, `ŋ`; ASCII index digits become subscripts. A value written `value(SIGN)` is mapped to SIGN. Editorial notes `($ ... $)` are removed before tokenising. Values not in the sign list keep the value as the sign token (prefixed `v:`), which splits a few signs by value; the mapped and unmapped token counts are logged.
3. Sumerian extract size: the Ur III administrative extract is 5.1 million tokens (27 MB). It is not committed; `SHA256SUMS` records its hash and `fetch_controls.sh` plus `extract52.py` regenerate it from the pinned dump. All other extracts are committed.
4. The CDLI catalogue is read from the round 50 download (same pinned dump, commit d66b12b0).

## Amendment 2 (19 October 2026, before results)
The protocol quoted the Indus corpus as 1,934 texts and 8,720 tokens from memory. `FC.TRAIN` actually holds 1,936 texts and 8,726 tokens (CLAUDE.md gives 1,936). The sample size N is therefore 8,726, set from the loaded corpus; nothing else changes.
