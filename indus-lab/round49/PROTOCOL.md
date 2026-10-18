# Round 49 — Tournament of published Indus sign keys under one frozen test

Pre-registered 2026-10-18 before any key was scored. Changes after this commit go in an "Amendments" section with the reason.

## Question
Round 47 showed that one published key (Yajnadevam 2024, Sanskrit) reads no more like its home language than its own shuffles, and that impossible languages fit the same labels at least as well. Does any other published key do better? The same instrument, with the same positive control and the same impossible-language controls, is applied to every key whose values exist in machine-readable form, and will be applied unchanged to keys supplied later.

## Keys
| Key | Home language | Signs in corpus | Token coverage | Runs ≥ 2 signs | Status |
|---|---|---:|---:|---:|---|
| Fairservis 1992, Appendix A, sure/likely matches (`fairservis1992.tsv`) | Dravidian (Tamil-like morphemes) | 95 | 0.60 | 1,364 | **tested** |
| Fairservis 1992 incl. unsure matches (`fairservis1992_wide.tsv`) | Dravidian | 166 | 0.78 | 1,770 | tested, secondary |
| Parpola 1994, Fig. 15.2 rebus values (`parpola1994.tsv`) | Proto-Dravidian / Tamil | 27 | 0.28 | 374 | **tested** if PC passes at 0.28 |
| Kak 1988, Table 4 (`kak1988.tsv`) | Sanskrit via Brahmi shapes | 7 | 0.16 | 100 | **not testable** (< 25 signs) |
| Mahadevan 1998/2014 (`mahadevan2014.tsv`) | Dravidian | 5 | 0.14 | 54 | **not testable** |
| Yajnadevam 2024, 714 codes (round 46 `expanded-map.json`) | Sanskrit | 581 | 1.00 | all | reference row, plain concatenation |
| Rao 1982 | Indo-Aryan | ? | ? | ? | **pending input**: the book's phonetic-value table is not online; Arham to supply |
| Bonta 2023, 2nd ed. (~60 signs) | early Indo-Aryan | ? | ? | ? | **pending input**: Academia.edu is gated; Arham to download https://www.academia.edu/120435855/ |
| Siddiqui | Indo-Iranian | – | – | – | no public sign table found; not testable until one exists |
| Mukhopadhyay | Dravidian (two logographic words) | 2 | – | – | not a phonetic key; outside this test |

Key files: Bourdeau's transcriptions in dbourdeau/cyphersolver `targets/indus/keys/` at commit 04457698, fetched to `ext/cyphersolver_keys/` with hashes in `SHA256SUMS` (no licence stated upstream; used locally, not redistributed). Sign IDs are ICIT catalogue numbers, the same system as `inscriptions.csv` (round 33 verified compatibility). Fairservis values take the first alternative, as Bourdeau's `build_fairservis.py` does. Pending keys will be transcribed to the same three-column format and committed with provenance before scoring.

**Minimum for testability:** at least 25 signs attested in the corpus. Below that the shuffle null has too few distinct permutations and the run set is dominated by two or three signs.

## Frozen inputs
Corpus: round 47 `load_corpus` (1,934 text types, 8,720 tokens, 582 signs; sha256 c22d39c3…). Lexicons: Sanskrit MWS (round 47 pin), Finnish, Basque (round 47 pins), **Tamil** from `indus-lab/external/dravidian_db_v1.1/forms.csv` rows with `Language_ID = Tamil` (13,768 forms, CC BY 4.0), Proto-Dravidian `pdr_04.csv` via round 37 `norm` as a diagnostic only (1,765 words, too small to be matched). Greek from the Linear B cognate file (round 47 pin).

## Common alphabet
Every label and every lexicon word is reduced to one alphabet: vowels a i u e o (length dropped; ai, au kept as two letters), consonants k g c j t d n p b m y r l v s. Rules: Unicode diacritics stripped (ā→a, ṭ→t, ṉ ṅ ñ ṇ→n, ḷ ḻ→l, ṟ→r, ṣ ś→s); aspirates lose h; h→s; w→v; z→s; f→p; x q→k; everything else dropped. Sanskrit SLP1 goes through round 47 `col_san` first. This is harsher than round 47's 20-label alphabet but identical for all keys and languages.

## Reading procedure
A text is split into maximal runs of consecutive signs that the key covers. Runs of ≥ 2 signs are read by concatenating the collapsed labels in reading order; shorter runs are dropped. No vowel insertion, no sandhi, no segmentation: the test scores the key, not a glossing stage.

## Statistic, null, size matching
As round 47: character trigram LM (add-0.1), S = bits per character over all run readings; 5 lexicon draws matched to the smallest tested lexicon after cleaning (seeds 49101–49105), averaged. Null: 1,000 structure-preserving shuffles of the key's values among its in-corpus signs, permuting within bins of 10 signs by corpus frequency (seeds 49201+). Report S, null mean, sd, z, percentile for each (key, language).

## Positive control
Linear B at Indus density (round 47 PC2 geometry: 130 sign IDs, 1,737 tokens, seeds 32001–32003), degraded to each tested key's coverage: sign IDs are dropped at random until token coverage is within ±0.03 of the key's (0.60 for Fairservis, 0.28 for Parpola, 0.78 for Fairservis-wide), 3 subsets per level (seeds 49301+), then run through the identical pipeline. **Pass at a level** if, in at least 2 of 3 subsets, Greek has percentile ≥ 0.99, z ≥ 3, and a z margin ≥ 2 over each of Sanskrit, Tamil, Finnish, Basque. A key whose coverage level fails is **NOT TESTABLE** at this corpus, not NULL.

## Negative controls
Impossible languages Finnish and Basque for every key; cross-family language (Sanskrit for Dravidian keys, Tamil for Sanskrit keys). Matched-budget fitted controls: the key's own value multiset re-assigned among its in-corpus signs by simulated annealing (60,000 swap steps, T 3.0→0.05, 3 chains, seeds 49401+) to maximise each language in turn; reported as diagnostics (how much a key of this shape *could* score).

## Verdict rules per key (fixed now)
- **NOT TESTABLE**: fewer than 25 in-corpus signs, or the positive control fails at its coverage level.
- **NULL**: home-language percentile < 0.95.
- **ARTEFACT**: home-language percentile ≥ 0.95 but Finnish or Basque also ≥ 0.95 for the same key, or the home-language z margin over the best impossible language is < 2.
- **SUPPORT**: home-language percentile ≥ 0.99, z ≥ 3, and z margin ≥ 2 over every other language.
- **MIXED**: anything else, with the failing clause named.
Round verdict word: the list of per-key verdicts; a SUPPORT for any key triggers a pre-registered replication on fresh lexicon draws and the round 24 copper-tablet picture test before anything is claimed.

## Diagnostics (reported, not verdict-bearing)
Readings of the 15 most frequent texts under each key; Proto-Dravidian LM scores; Fairservis-wide; Yajnadevam plain-concatenation reference; the Kak and Mahadevan readings listed descriptively.

## Limits
Partial keys are scored only on the runs they cover, which favours them (their authors chose which signs to value). Morpheme values concatenated without morphology are a crude rendering of a Dravidian reading, but the same crudeness applies to the Linear B control, which must still pass. Tamil is attested 2,000 years after the seals; Proto-Dravidian is the right target but its lexicon is too small to train on, so it is a diagnostic. A NULL means the key's values carry no more Tamil-ness than their frequencies predict; it does not refute Dravidian as a hypothesis.
