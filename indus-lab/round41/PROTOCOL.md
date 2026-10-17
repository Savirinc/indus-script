# Round 41 — Do Dravidian rebus anchors predict unseen Indus inscriptions? (pre-registered)

Written 12 October 2026 before any fitting. Working hypothesis (user-directed, round 40 "premise holds"): the Harappan language was Dravidian.

## Anchors (fixed in advance; from round 36 blind tags + Proto-Dravidian words)
- **Pictographs** take their PDr word, from `round36/data/lang_pdr.tsv` (first/primary form):
  - 740 jar/pot
  - 220 fish
  - 090 man
  - 520 arrow
  - 269 bird
  - 803/806 leaf
- **Numerals** take PDr number words, same file: 001/031 one; 002/032 two; 003/013/033 three; 004/014/034 four; 005/015/035 five; 016/036 six; 017 seven; 018 eight.
- Values are the normalised strings (round 37 `norm`).

## Model
- Each sign carries a sound string. The decoded text = the concatenation of its signs' strings.
- **Language model:** character trigram (add-0.1) over the normalised PDr reconstructions (Dravidian Database `pdr_04.csv`), with word boundaries; texts are scored as ^decoded$.
- **Free signs** (all non-anchors) take values from an inventory: the 150 most frequent CV/CVC chunks of PDr forms. Many signs may share a value (homophones); a homophonic emission term (round 32 v2) is included.
- **Fit:** simulated annealing on TRAIN texts only; anchors fixed. 60,000 proposals, temperature 3→0.05.

## Split
- Indus core text types (1,936), random 80/20 TRAIN/TEST, seed 41001.
- TEST texts that are exact or one-edit near-duplicates of a TRAIN text are dropped.

## Test
- **Statistic:** mean per-text log-likelihood of TEST texts decoded with the fitted key (no refitting on TEST).
- **Real anchors:** the Dravidian values above.
- **Null:** 15 keys with the anchor values permuted (numerals among numerals, pictographs among pictographs; seeds 41100–41114), each refitted identically.
- **p** = (1 + #null ≥ real) / 16.

## Positive control (gate, runs first)
- Same pipeline on Linear B (round 32 data): texts = 919 words.
- Anchors = the 24 most frequent sign IDs with their TRUE values; LM = the round-32 Greek "cognate" lexicon in Linear B spelling, as characters.
- Null = the same 24 values permuted.
- **PASS** if the true-anchor held-out log-likelihood beats all 15 permutations (p = 1/16).
- If the control fails, the Indus result is uninformative.

## Decision
- **SUPPORTED:** control passes AND Indus p ≤ 1/16 (beats all 15).
- **WEAK SUPPORT:** p ≤ 3/16.
- Otherwise NOT SUPPORTED.

Support would mean the Dravidian values for these 24 signs fit the inscriptions' sound sequences better than the same values misassigned. It would not be a reading. Step 3 (the copper-tablet picture test) proceeds only on SUPPORTED.

## Amendment (before any fitting)
Inspecting the "primary" PDr rows showed wrong or non-standard picks: bird = *peṇṭṭi 'female of animal'; jar, leaf and four are Starostin forms. Objective rule adopted: use only Krishnamurti 2003 reconstructions whose meaning matches the concept; drop the others.

Final anchors (17 signs):

| Sign(s) | Concept | PDr |
|---|---|---|
| 220 | fish | *mīn |
| 090 | man | *āḷ |
| 520 | arrow | *ampu |
| 001, 031 | one | *okk- |
| 002, 032 | two | *īr/*ir- |
| 003, 013, 033 | three | *mū-nṯu |
| 005, 015, 035 | five | *cay-m-tu |
| 016, 036 | six | *cāṯ-u |
| 017 | seven | *ēẓ |
| 018 | eight | *eṇ-ṭṭu |

Dropped: 740 jar, 803/806 leaf, 269 bird, 004/014/034 four. The Linear B control likewise uses the 17 most frequent sign IDs.
