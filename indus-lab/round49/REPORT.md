# Round 49 — Tournament of published Indus sign keys: **Fairservis NULL; Parpola, Kak, Mahadevan NOT TESTABLE**

Pre-registered in `PROTOCOL.md` (commit 4663b7e) before any key was scored; harness committed before the run. No amendments.

## Verdicts
| Key | Home language | Signs | Coverage | Verdict |
|---|---|---:|---:|---|
| Fairservis 1992 (sure/likely) | Dravidian / Tamil | 95 | 0.60 | **NULL** |
| Fairservis 1992 incl. unsure | Dravidian / Tamil | 166 | 0.78 | NULL (secondary) |
| Parpola 1994 rebus values | Dravidian | 27 | 0.28 | **NOT TESTABLE**: Linear B control fails at this coverage (1 of 3 subsets) |
| Kak 1988 | Sanskrit via Brahmi | 7 | 0.16 | NOT TESTABLE: fewer than 25 signs |
| Mahadevan 1998/2014 | Dravidian | 5 | 0.14 | NOT TESTABLE: fewer than 25 signs |
| Yajnadevam 2024 (reference, plain concatenation) | Sanskrit | 581 | 1.00 | NULL (reference; round 47 is the verdict) |
| Rao 1982, Bonta 2023, Siddiqui | Indo-Aryan / Indo-Iranian | – | – | **pending input** (see below) |

## Positive control: the instrument works at Fairservis's coverage, not at Parpola's
Linear B at Indus density (130 sign IDs, 227 texts, 1,737 tokens), degraded by dropping sign IDs until token coverage matched each key, read as covered runs of ≥ 2 signs, scored against Greek and four wrong languages.

| Coverage level | Subsets passing | Greek z (3 subsets) | Best wrong-language z |
|---|---|---|---|
| 0.28 (Parpola) | 1 of 3 | 3.9, 3.2, 4.9 | 2.7, 2.2, 1.4 |
| 0.60 (Fairservis) | 2 of 3 | 4.9, 6.0, 6.9 | 3.0, 2.2, 2.8 |
| 0.78 (Fairservis wide) | 3 of 3 | 8.2, 9.5, 8.8 | 3.9, 4.8, 4.2 |

At 28% coverage the Greek key is still above its shuffles but the margin over wrong languages is not reliable, so a key that covers only a quarter of the tokens cannot be judged by this method at this corpus size. That is a statement about power, not about Parpola.

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

## Keys too small to test
Kak's seven values read the commonest covered runs as *sata*, *para*, *rasa*, *vasa*. Mahadevan's five read *markol*, *maranru*, *markolpatanru*. Four- or five-letter strings in a 21-letter alphabet are words in most languages; there is no statistic that can separate a correct five-sign key from a wrong one on this corpus. Bourdeau reached the same conclusion.

## Pending inputs
- **Bonta 2023, 2nd edition** (~60 signs, early Indo-Aryan): the PDF is behind Academia.edu's login (HTTP 403 for automated fetch). Arham to download https://www.academia.edu/120435855/ and place it in `data/sources/`; the sign table will be transcribed to the three-column key format with page references, committed, and scored with this exact harness, unchanged.
- **Rao 1982**: the phonetic-value table of *The Decipherment of the Indus Script* is not online; the NBU thesis that reproduces it as a figure was unreachable (HTTP 502, twice). Same procedure once a scan is supplied.
- **Siddiqui**: no public sign table found; nothing to test.
- **Mukhopadhyay**: two logographic identifications, not a phonetic key; outside this instrument.

## What this means
Every published phonetic key that can be tested on this corpus (Yajnadevam, Fairservis) is indistinguishable from its own shuffles. Every other published key is too small to test, which cuts both ways: it cannot be refuted, and it cannot be evidence. Nothing here bears on whether the language was Dravidian or Indo-Aryan. It bears on whether anyone has shown sign values, and the answer remains no.

## Reproduce
```
cd indus-lab/round47 && bash fetch_lexicons.sh      # pinned lexicons
# keys: ext/cyphersolver_keys/ from dbourdeau/cyphersolver@04457698 targets/indus/keys/ (hashes in SHA256SUMS)
cd ../round49 && python3 run49.py                    # 20 min, stdlib only; writes results.json
```
