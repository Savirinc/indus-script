# Round 49 — Tournament of published Indus sign keys: **Fairservis NULL; Rao NULL; Parpola, Kak, Mahadevan NOT TESTABLE**

Pre-registered in `PROTOCOL.md` (commit 4663b7e) before any key was scored; harness committed before the run. Addendum 1 (commit a0eef0d) added Rao 1982, transcribed from a public scan, without changing any rule; the whole run was then repeated (the control-subset seeds shift with the number of coverage levels, so the 0.60 and 0.78 control numbers differ slightly from the first run; both passed both times).

## Verdicts
| Key | Home language | Signs | Coverage | Verdict |
|---|---|---:|---:|---|
| Fairservis 1992 (sure/likely) | Dravidian / Tamil | 95 | 0.60 | **NULL** |
| Fairservis 1992 incl. unsure | Dravidian / Tamil | 166 | 0.78 | NULL (secondary) |
| Parpola 1994 rebus values | Dravidian | 27 | 0.28 | **NOT TESTABLE**: Linear B control fails at this coverage (1 of 3 subsets) |
| Kak 1988 | Sanskrit via Brahmi | 7 | 0.16 | NOT TESTABLE: fewer than 25 signs |
| Mahadevan 1998/2014 | Dravidian | 5 | 0.14 | NOT TESTABLE: fewer than 25 signs |
| Yajnadevam 2024 (reference, plain concatenation) | Sanskrit | 581 | 1.00 | NULL (reference; round 47 is the verdict) |
| **Rao 1982** (sure + likely matches, `keys/rao1982.tsv`) | old Indo-Aryan / Sanskrit | 56 | 0.57 | **NULL** |
| Rao 1982, sure matches only | Sanskrit | 33 | 0.39 | NOT TESTABLE: control fails at this coverage (secondary) |
| Bonta 2023, Siddiqui | Indo-Aryan / Indo-Iranian | – | – | pending / no table (see below) |

## Positive control: the instrument works at Fairservis's coverage, not at Parpola's
Linear B at Indus density (130 sign IDs, 227 texts, 1,737 tokens), degraded by dropping sign IDs until token coverage matched each key, read as covered runs of ≥ 2 signs, scored against Greek and four wrong languages.

| Coverage level | Subsets passing | Greek z (3 subsets) | Best wrong-language z | Level |
|---|---|---|---|---|
| 0.28 | 1 of 3 | 3.9, 3.2, 4.9 | 2.7, 2.2, 1.4 | FAIL |
| 0.39 | 1 of 3 | 4.6, 2.6, 4.0 | 2.5, 1.9, 2.5 | FAIL |
| 0.57 | 3 of 3 | 5.3, 8.0, 6.6 | 3.3, 3.9, 3.8 | PASS |
| 0.6 | 2 of 3 | 6.0, 6.4, 4.4 | 2.6, 3.4, 2.7 | PASS |
| 0.78 | 3 of 3 | 9.5, 9.5, 9.5 | 5.7, 5.2, 4.5 | PASS |

At 28% and 39% coverage the Greek key is still above its shuffles but the margin over wrong languages is not reliable, so a key that covers only a quarter of the tokens cannot be judged by this method at this corpus size. That is a statement about power, not about Parpola.

## Fairservis 1992: the main result
z against 1,000 structure-preserving shuffles of his own values, five matched lexicon draws (8,023 words each):

| Language | S bits/char | Shuffle mean | z | Percentile |
|---|---:|---:|---:|---:|
| **Tamil (home)** | 3.732 | 3.750 | **0.20** | **0.61** |
| Sanskrit | 4.341 | 4.344 | 0.03 | 0.53 |
| Finnish | 4.223 | 4.295 | 0.84 | 0.78 |
| Basque | 4.027 | 4.041 | 0.14 | 0.47 |
| Proto-Dravidian (diagnostic) | 4.004 | 4.007 | 0.07 | 0.52 |

His Dravidian values produce readings exactly as Tamil-like as random reassignments of the same values to the same signs. Finnish fits his key slightly better than Tamil does. A 60,000-step refit of his own value multiset reaches z 4.7 for Tamil, 6.8 for Sanskrit, 4.4 for Basque and 3.2 for Finnish: the key's shape allows strong "fits" to any language, and his actual assignment achieves none of them. This agrees with Bourdeau's independent finding (round 34) that the Fairservis key scored below its shuffles on a different instrument.

What the readings look like under his key, runs only, commonest texts: `176-740-400` → *ancippu*; `501-405-002-240-520` → *tunkunelailmarupirar*; `503-615-752-740` → *nerakuticembalaan*; `415-220-520` → *kirapirar*. The three commonest inscriptions (two-sign numeral-plus-jar texts) have no covered run.


## Rao 1982: the Indo-Aryan key
Rao's system (Figs. 8–10 of his book) gives about 24 basic signs alphabetic values by resemblance to Old North Semitic letters, treats short strokes as vowel marks, and analyses compounds into those basics. Fifty-six corpus signs could be crosswalked with confidence (`keys/rao1982.tsv`, each with its figure reference); they cover 57% of tokens, 1,275 runs.

| Language | S bits/char | Shuffle mean | z | Percentile |
|---|---:|---:|---:|---:|
| Sanskrit | 5.110 | 4.941 | -0.70 | 0.262 |
| Tamil | 4.951 | 5.179 | 1.73 | 0.970 |
| Finnish | 4.398 | 4.800 | 2.06 | 0.985 |
| Basque | 4.824 | 4.874 | 0.27 | 0.578 |
| PDr | 4.526 | 4.642 | 0.84 | 0.784 |

His key reads *less* like Sanskrit than random reassignments of his own values (z −0.70), and more like Finnish (z 2.06, percentile 0.985) and Tamil than like its home language. The Finnish figure is just under the 0.99 bar, so it is not an ARTEFACT verdict, but it is the pattern round 45 and round 47 found: a key built from look-alikes carries no language, and whichever language happens to like its vowel-heavy strings scores best. Refits of his own values: Sanskrit 4.8, Tamil 5.3, Finnish 3.6, Basque 4.8. Readings of the commonest covered texts: `033-700` → *aea*; `032-700` → *aa*; `176-740-400` → *as*; `700-033` → *aae*; `003-861` → *aepa*; `501-405-002-240-520` → *ats*; `700-032` → *aa*; `415-220-520` → *sss*; `806-845-061-407-850-900-740` → *ppa*; `235-705-033-845-407-321-407` → *aae*; `803-415-220-318-920-255-436-690-590-407-740` → *ss|tba*.

The sure-only variant (33 signs, 39% coverage) sits below the method's power limit and is not judged.

## Keys too small to test
Kak's seven values read the commonest covered runs as *sata*, *para*, *rasa*, *vasa*. Mahadevan's five read *markol*, *maranru*, *markolpatanru*. Four- or five-letter strings in a 21-letter alphabet are words in most languages; there is no statistic that can separate a correct five-sign key from a wrong one on this corpus. Bourdeau reached the same conclusion.

## Pending inputs
- **Bonta 2023, 2nd edition** (~60 signs, early Indo-Aryan): the PDF is behind Academia.edu's login (HTTP 403 for automated fetch). Arham to download https://www.academia.edu/120435855/ and place it in `data/sources/`; the sign table will be transcribed to the three-column key format with page references, committed, and scored with this exact harness, unchanged.
- **Rao 1982**: resolved by Addendum 1 (public scan on archive.org; transcription in `keys/rao1982.tsv`).
- **Siddiqui**: no public sign table found; nothing to test.
- **Mukhopadhyay**: two logographic identifications, not a phonetic key; outside this instrument.

## What this means
Every published phonetic key that can be tested on this corpus (Yajnadevam, Fairservis, Rao) is indistinguishable from its own shuffles or worse; two of the three (Yajnadevam under round 47's own vowel rule, Rao here) are liked more by Finnish than by their home language. Every other published key is too small to test, which cuts both ways: it cannot be refuted, and it cannot be evidence. Nothing here bears on whether the language was Dravidian or Indo-Aryan. It bears on whether anyone has shown sign values, and the answer remains no.

## Reproduce
```
cd indus-lab/round47 && bash fetch_lexicons.sh      # pinned lexicons
# keys: ext/cyphersolver_keys/ from dbourdeau/cyphersolver@04457698 targets/indus/keys/ (hashes in SHA256SUMS)
cd ../round49 && python3 run49.py                    # 20 min, stdlib only; writes results.json
```
