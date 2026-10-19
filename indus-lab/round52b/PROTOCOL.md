# Round 52b — Writing-system signature with enough corpora per class (pre-registered)

Written 19 October 2026 after round 52's METHOD-FAIL, before `extract52b.py` or `run52b.py` exist and before any feature has been computed on any new corpus. The Indus feature vector and the seven round-52 corpora are already known (round 52 `results.json`); every corpus added here is new and unseen. Committed before code.

## What round 52 taught
Two things broke it: one or two corpora per class, so leave-one-out had nothing to generalise from; and class regions built from resampling variance, which is tiny and says nothing about how systems differ from each other. Round 52b fixes both and, because the CDLI dump turns out to hold the archaic administrative corpora, asks a sharper question.

## Question
With corpus size and text length held at Indus conditions, is the Indus corpus statistically nearest to (a) small-inventory phonetic scripts, (b) large-inventory phonetic scripts (logosyllabic, logo-consonantal, logographic with rebus), or (c) the archaic administrative systems of the late fourth millennium (proto-cuneiform, proto-Elamite), which are largely non-phonetic sign-and-number records? Class (c) is the first real-data control the project has had for the Farmer–Sproat–Witzel position (conjecture A1): if the Indus corpus sits with the archaic accounting systems rather than with the phonetic scripts, A1 is weakened; if it sits with the phonetic scripts, A1 is strengthened and A3 is narrowed. A result in neither direction is possible and would be reported as such.

Genre confound, stated now: the Indus texts are mostly seal legends; the archaic corpora are accounts; the Old Babylonian and Old Assyrian corpora are letters; Ur III is accounts. A seal-legend corpus in a phonetic script (CDLI seal inscriptions, Ur III and Old Babylonian, Sumerian and Akkadian) is added so that one phonetic corpus matches the Indus genre.

## Corpora
Round 52 corpora unchanged (`round52/controls/*.txt`, hashes in `round52/SHA256SUMS`). New corpora all come from the same pinned CDLI dump (commit d66b12b0, CC BY) and the same tokeniser as round 52 (Amendment 1 rules), selected by catalogue period and genre and by the `#atf: lang` line:

| Code | Class | Selection | Expected size |
|---|---|---|---|
| GRK, HEB, CHR | SMALL (phonetic, small inventory) | round 52 | — |
| SUX | LARGE-PHON | round 52 (Ur III administrative, Sumerian) | 5.1 M tokens |
| OBL | LARGE-PHON | Old Babylonian, genre Letter, lang akk | ~50 k lines |
| OAL | LARGE-PHON | Old Assyrian, genre Letter, lang akk | ~26 k lines |
| SEAL | LARGE-PHON | texts whose designation begins `CDLI Seals`, lang sux or akk, period Ur III or Old Babylonian or Early Old Babylonian, any genre; used only if the extract has ≥ 17,452 tokens (2 N) | unknown |
| EGY, OBI | LARGE-PHON | round 52 | — |
| U4 | ARCHAIC | Uruk IV, Administrative, lang qpc | ~6.7 k lines |
| U3 | ARCHAIC | Uruk III, Administrative, lang qpc | ~27 k lines |
| PE | ARCHAIC | Proto-Elamite, all genres, any lang line or none | ~11 k lines |
| CHN | reference only | round 52 (received text) | — |

Proto-cuneiform and proto-Elamite ATF already uses sign names (ZATU and Dahl numbers), so no sign-list mapping is applied; variant suffixes `~a`, `~b` are kept as distinct signs, as ICIT keeps Indus variants. Numerals such as `1(N01)` or `5(disz)` are one sign each in every corpus, as in round 52. Damaged lines are dropped by the round 52 rule.

U4 and U3 are two stages of one system; this is stated and the class has three corpora from two systems. If SEAL is too small it is dropped and LARGE-PHON has five corpora.

## Features and sampling
Exactly round 52: eight relabelling-invariant features; B = 300 Indus-shaped samples per corpus (window sampling from units, Indus length distribution, N = 8,726); seed 52101 + corpus index × 1000 + sample index. The round 52 `features()` and `indus_sample()` functions are imported unchanged.

## Standardisation and classifier
Each feature is standardised by the standard deviation of the **corpus means** across all classified corpora (between-corpus spread), not by resampling variance. A corpus is represented by its mean vector. The classifier is nearest corpus mean by Euclidean distance in the standardised space; the predicted class is that corpus's class. CHN is never a neighbour (reference only).

## Positive control
Leave-one-corpus-out: for each classified corpus, remove it, re-standardise, and classify each of its 300 samples by nearest remaining corpus mean. Required: every corpus assigns ≥ 80% of its samples to its own class.
- PASS: all corpora ≥ 80%.
- WEAK: all ≥ 50%, some below 80%; the verdict carries `(WEAK CONTROL)`.
- METHOD-FAIL: any corpus below 50%. Indus numbers reported as uninterpretable.
The three classes must each contain at least three corpora for the test to run; otherwise NOT RUN.

## Verdict for the Indus corpus
Nearest corpus and its class, with the full ordered distance list. Stability: repeat with each classified corpus removed in turn; if the nearest class is the same in every case the verdict is `NEAREST-<class> (STABLE)`, otherwise `NEAREST-<class> (UNSTABLE; flips when <corpus> removed)`. Also reported: for each class, the number of the eight features on which the Indus value lies within the range of that class's corpus means (range check, 0–8).

Pre-stated reading of outcomes:
- NEAREST-SMALL: would contradict round 52 and the inventory; treated as a method problem to investigate, not a result.
- NEAREST-LARGE-PHON (STABLE): A3 stays OPEN and narrows; A1 is unchanged or mildly strengthened.
- NEAREST-ARCHAIC (STABLE): A1 is weakened; the project's non-linguistic round (56) becomes urgent, and the genre confound must be examined by comparing SEAL and Ur III separately before anything is said in public.
- UNSTABLE either way: no conjecture status changes.

## Robustness (reported, not part of the verdict)
Same nearest-corpus analysis with the five features that do not depend on inventory splitting (top10, H1, H2/H1, repeat, double), and with Indus numerals (001–018, 031–036) merged into a single sign to see whether numeral handling drives any proximity to the archaic class.

## Pins and reproducibility
`extract52b.py` reads the round 52 download directory; `SHA256SUMS` lists the new extracts; `controls/` commits every new extract (all CC BY). `run52b.py`, standard library only. One run; code fixes before results are recorded as amendments.
