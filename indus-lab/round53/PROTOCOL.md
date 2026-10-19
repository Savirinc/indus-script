# Round 53 — Do Indus texts contain multi-sign words? (pre-registered)

Written 19 October 2026, before `extract53.py` or `run53.py` exist and before any cohesion statistic has been computed on any corpus. Committed before code.

## Question
Two readings survive rounds 52–52b. (a) A mixed logosyllabic or logo-consonantal system in which most texts are strings of **multi-sign words** (cuneiform seal legends: name, patronymic, title, each two to five signs). (b) A system in which **each sign is a word**, which is what "monosyllabic" claims amount to in practice: one-syllable roots written one sign each, as in Old Chinese. The two differ in adjacent-sign cohesion. In (a) some adjacent pairs recur far above chance (inside words) and others do not (between words); in (b) cohesion is weak and uniform, because word order is freer than sign order inside a word. This round asks which pattern the Indus corpus shows at its own size, using a fixed unsupervised segmenter calibrated on corpora with known word boundaries.

## Corpora and units
All from the round 52/52b downloads (pinned there). Units are whole texts, lines or clauses of 2 to 13 signs, the Indus range; longer units are dropped, not cut. Samples are built by drawing whole units until N = 8,726 tokens (last unit trimmed). Text length is therefore approximately rather than exactly matched; the mean unit length of every sample is reported.

| Code | Group | Corpus and gold boundaries |
|---|---|---|
| SEAL | MULTI (gold) | cuneiform seal legends, Ur III to Old Babylonian; words from ATF spacing, signs from hyphens; one unit per seal |
| SUX | MULTI (gold) | Ur III administrative lines, Sumerian; words from ATF spacing |
| OBL | MULTI (gold) | Old Babylonian letters, Akkadian, lines |
| OAL | MULTI (gold) | Old Assyrian letters, Akkadian, lines |
| CHN | SINGLE (approximate) | Shijing clauses split at punctuation; Old Chinese is predominantly one syllable per word, with a minority of two-character words, so its gold is "mostly single" rather than exact |
| OBI | unknown | oracle-bone sentences; no word boundaries in the data; reported, not used for calibration |
| Indus | test | `FC.TRAIN`, 1,936 texts |

Determinatives in cuneiform are attached to their word (inside it). Numeral tokens count as signs; a numeral followed by a commodity sign is two words in the ATF spacing.

## Segmenter (fixed)
For a sample, count within-unit adjacent pairs c(a,b), left totals c(a,·), right totals c(·,b), and T = total pairs. Cohesion of a pair is PMI(a,b) = log2( c(a,b) · T / ( c(a,·) · c(·,b) ) ); pairs with c(a,b) = 1 are assigned −∞ (a singleton pair is never evidence of a word). A boundary is placed between a and b when PMI(a,b) < τ. Segment length = number of signs between boundaries.

τ is chosen **once**, on the four MULTI corpora only, as the value in {−2, −1.75, …, 6} that maximises the mean boundary F1 (precision and recall of placed boundaries against gold internal boundaries) over 100 samples per corpus. Indus is not touched during calibration.

## Positive control
At τ*, boundary F1 on each MULTI corpus must exceed the F1 of random boundaries placed at the same rate (mean over 100 random placements per sample) by at least 0.15 on average, for at least three of the four MULTI corpora. Otherwise METHOD-FAIL: the segmenter cannot find words at this corpus size, and nothing is said about Indus.

## Statistic
S = mean segment length under the segmenter at τ*, and M = share of units that contain at least one multi-sign segment. Computed on 100 samples per control corpus (seed 53001 + corpus index × 1000 + sample index) and once on the Indus corpus.

## Verdict
Let S_multi be the smallest control mean S among the MULTI corpora that passed the positive control, and S_single the CHN mean S, with their sample standard deviations.
- `MULTI-SIGN-WORDS`: Indus S is within 2 sd of some passing MULTI corpus or above S_multi, and more than 2 sd above S_single.
- `SINGLE-SIGN-WORDS`: Indus S is within 2 sd of S_single or below it, and more than 2 sd below S_multi.
- `BETWEEN`: neither.
- `METHOD-FAIL`: positive control not met.
A second check, reported alongside: the same rule on M. If S and M disagree the verdict is BETWEEN.

## Confounds stated in advance
- Hapax-rich corpora produce more singleton pairs and so more boundaries. Indus (37% hapax types) is like OBI (37%) and CHN (37%) in this respect and unlike SEAL (21%). The controls are at the same N, so the effect is in the calibration, but a SINGLE result could partly reflect sparsity. The report will show S restricted to units whose every sign occurs ≥ 5 times in the sample, as a diagnostic.
- Unit length differs (Indus mean 4.5; seals longer). Reported, not corrected.
- CHN gold is approximate; it anchors the SINGLE end only loosely.

## Negative-control diagnostic
Indus with sign order shuffled within texts must give S near the CHN value or lower (cohesion destroyed). If it does not, the segmenter is reacting to frequency, not order, and the result is uninterpretable.

## Pins
`extract53.py` writes `controls/*.txt` with word boundaries marked by ` | ` (committed; all CC BY or MIT); `SHA256SUMS`; `run53.py` standard library only; `results.json`, `run53.log`, `REPORT.md`. One run; fixes before results go in amendments.
