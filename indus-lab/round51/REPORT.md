# Round 51 — Proposed Meluhhan loanwords in Sumerian and Akkadian: **NO FAMILY ATTRIBUTABLE** (gates passed)

Pre-registered in `PROTOCOL.md` (commit 0dbdac8); candidate set frozen in `candidates.tsv` (commit 1aa4fc0) before scoring. No amendments. Decision by the pre-set rule: **NO FAMILY ATTRIBUTABLE**. The round is **INCOMPLETE** with respect to one source: Possehl 1996a, which holds the full "some 40 Indian words" list, is not available online; the candidate set is the subset that Witzel 1999/2000, Parpola 1994 and Southworth 2005 name explicitly.

## Gates (both passed)
| Gate | Target set | Result |
|---|---|---|
| G1 Indo-Aryan words in cuneiform (Mitanni) | 11 words | IA ranks first in 100% of resamples, A = +0.39, CI +0.17 to +0.57; no other family above 0.08 |
| G2 Dravidian loans in Sanskrit (round 39 set) | 41 words | PDR ranks first in 99%, A = +0.15, CI +0.09 to +0.21 |

G1 is the one that matters: the instrument recovers a known donor through cuneiform spelling from an 11-word sample, which is the size of the candidate set. So a null below is not for lack of power to see a clear signal of that strength.

## The candidate words
| Family | A (mean gain over baseline) | 95% CI | P(rank 1) | P(beats both decoys) |
|---|---:|---|---:|---:|
| FIN | +0.282 | +0.186 to +0.377 | 0.70 | 0.00 |
| PDR | +0.229 | +0.147 to +0.308 | 0.21 | 0.24 |
| EUS | +0.219 | +0.161 to +0.280 | 0.03 | 0.00 |
| IA | +0.192 | +0.098 to +0.275 | 0.07 | 0.09 |
| BUR | -0.005 | -0.014 to +0.000 | 0.00 | 0.00 |
| MUNDA | -0.006 | -0.018 to +0.000 | 0.00 | 0.00 |

Finnish, an impossible donor, ranks first in 70% of resamples. Proto-Dravidian is second with a positive interval but beats the decoys in only 24% of resamples; the rule requires 95%. Indo-Aryan is fourth. Nothing is attributable.

Per word, best sound-and-meaning match in each family (similarity 0 to 1):

| Target | PDR | IA | MUNDA | FIN | EUS |
|---|---|---|---|---|---|
| abba | dabb (0.50) | amra (0.50) | – (0.00) | puutavara (0.22) | bananace (0.25) |
| mesu | medi (0.50) | selu (0.50) | – (0.00) | metsa (0.60) | uku (0.25) |
| magilum | kalam (0.43) | vahitra (0.29) | – (0.00) | alus (0.43) | uci (0.14) |
| sinda | kinda (0.80) | sanda (0.80) | – (0.00) | metsa (0.20) | suhanodo (0.38) |
| sindu | sintc (0.60) | sindura (0.71) | – (0.00) | puu (0.20) | suhanodo (0.38) |
| sasa | sak (0.50) | raksana (0.43) | – (0.00) | karya (0.40) | kabale (0.33) |
| haluppu | uruppa (0.43) | haridru (0.43) | – (0.00) | palmu (0.43) | uku (0.29) |
| gisimmar | usir (0.38) | vistara (0.38) | – (0.00) | kammen (0.25) | suhan (0.25) |
| ili | isi (0.67) | tailika (0.43) | – (0.00) | olyu (0.25) | olio (0.50) |
| ellu | el (0.50) | kutu (0.25) | – (0.00) | olyu (0.50) | olio (0.25) |
| ulu | us (0.33) | kutu (0.50) | – (0.00) | olyu (0.50) | olio (0.25) |

The sesame words do what the literature says: *ili / ellu / ulu* find Dravidian *eḷ / eḷḷu* and nothing comparable in Indo-Aryan, which has *tila*. That is one etymon counted three times, and it is the only Dravidian hit of note. The wood, boat and cattle words scatter: every family finds something of similar quality, and Finnish finds as much as any, because a 21-sound alphabet and a 1,600-word meaning-matched lexicon produce look-alikes for any short CVCV word.

Toponyms (Meluhha, Magan), scored separately: Finnish first again; not verdict-bearing.

## What this means
- The only Harappan-era vocabulary recorded in a readable script carries no family signal detectable at this sample size, apart from the sesame etymon that Bedigian, Parpola, Southworth and Witzel already debated, and which Witzel himself reads as possibly Para-Munda via Vedic *jar-tila*.
- This is consistent with round 39/40 (Rigvedic substrate leans Dravidian but below the attribution bar) and does not strengthen it: the sesame word is one data point, not a lean.
- The sample is tiny. With Possehl's full 40-word list the test would have roughly four times the power. That list is the reopen condition.

## Reopen criteria
Possehl 1996a ("Meluhha", in Reade ed., *The Indian Ocean in Antiquity*, pp. 133-208) or any later compilation of the Mesopotamian "Indian" words with forms and meanings. Add rows to `candidates.tsv` with proposer and page; rerun `run51.py` unchanged.

## Reproduce
```
cd indus-lab/round51 && ../../ext/venv/bin/python run51.py    # ~1 min; needs numpy, rapidfuzz, ext/moli-mandala_data (data/munda, data/other materialised), ext/lexibank_ids
```
`epsd2_lemmas.tsv` is the Sumerian background: 14,817 citation forms with guide words extracted from ePSD2 `gloss-sux.json` (Oracc, CC0, 2023-01-19).
