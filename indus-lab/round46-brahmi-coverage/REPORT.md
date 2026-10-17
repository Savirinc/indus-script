# Indus–Brahmi mapping: first executable audit

This is a coverage and crosswalk audit, not a decipherment or a linguistic validation.

## What was actually run

Downloaded the data behind Tejesh Raut's explorer and applied the explicit `xlit` fields from Yajnadevam's repository to every parseable three-digit sign code. The first pass performs no dictionary matching, Sanskrit word completion, sound expansion, schwa insertion/deletion, canonical decomposition, regex processing, or semantic translation. The second pass adds ONLY the author’s ordered canonical substitution/decomposition step; it does not implement dictionary matching or translate meanings. Blank values and damage placeholders remain unknown. The candidate strings are program outputs, not ancient readings.

The full repository mapping is a separate experiment from the screenshot's Table 7; it contains many additional assumptions and signs. It must not be represented as a direct application of Table 7 alone.

## Main result after checking the application code

The application's `mkregex` function fills blank xlit fields through canonical sign substitutions and decompositions. Reproducing its single ordered pass yields 714 non-placeholder assignments. ALL 2,477 conservative complete single-line records now receive proposed values. Across the full 5,445 records, 3,497 have nonempty sequences without unresolved tokens; the rest include empty records or damage placeholders. This establishes executability and coverage, not correctness. The earlier 77.8% figure below describes direct fields BEFORE this required processing, and is not a failure rate of the author's application.

The remaining unknown codes after expansion are 000 and 999. This is a concrete resolution of the initial blanks. Applying the full rules is materially different from applying the 38-entry screenshot alone.

## Initial direct-field results (before canonical processing)

- Explorer records: 5,445; 902 contain no parseable sign sequence. These are not translation failures.
- Records with sequences: 4,543; all sign tokens have nonblank proposed values in 2,857 (62.9%). This includes uncertain directions and damaged records; it is only a lookup-coverage count.
- Conservative comparison subset: 2,477 complete, single-line records with R/L or L/R direction, no damaged edge notation and no 000/999 placeholders.
- Full proposed lookup covers every token in 1,927 of these 2,477 records (77.8%). The other 550 have at least one blank proposed value.
- Across all records: 16,531 sign-code occurrences; 14,172 assigned. Damage/unknown placeholders are included in this denominator; this is not a readability rate.
- Full mapping file: 716 rows; 681 nonblank, non-placeholder assignments.

Counts are records, not independent artifacts or unique texts. No deduplication or blind linguistic evaluation was performed. The mapping was developed using Indus material, so this corpus is not an independent validation set.

## M-304 worked example

Explorer stored transcription: `+090-740-220-742-534-550-090+`.
Recorded direction: R/L. Reading-order code sequence: `090 550 534 742 220 740 090`.
Literal proposed lookup output: `a | as | as | an | m | an | a`.
This does not by itself yield a translated prayer. Reaching a word or sentence requires further spelling and linguistic rules, which have not been applied here. This observation does not refute those further rules; it identifies what direct substitution does and does not establish.

## Screenshot Table 7

The November 13, 2024 paper's Table 7 has 38 sound-labelled entries and 32 distinct extracted Indus font codepoints. Repeated glyphs include g/gh, c/ch, d/ḍ, n/ṇ, p/ph and ṣ/h. The table is not a one-to-one alphabet.

Using an existing old-font-to-catalogue crosswalk, 21 entries resolve uniquely to 18 distinct catalogue IDs; 3 entries have multiple candidates and 14 remain unresolved. These are provisional font crosswalks, not independent image adjudications. Their 24 fully covered records are a lower bound on this partial implementation, NOT the coverage ceiling of Table 7. Unresolved mappings must not be filled from desired Sanskrit words.

| Proposed sound | PDF font codepoint | Candidate catalogue IDs | Status |
|---|---|---|---|
| a | E06C | 090 | unique font crosswalk |
| i | E261 | — | unresolved |
| u | E53B | 513 | unique font crosswalk |
| e | E3B3 | — | unresolved |
| o | E402 | 436 | unique font crosswalk |
| k | E4C7 | 645 | unique font crosswalk |
| kh | E275 | 370 | unique font crosswalk |
| g | E3EA | 066 | unique font crosswalk |
| gh | E3EA | 066 | unique font crosswalk |
| ṅ | E56B | — | unresolved |
| c | E210 | 350, 351 | multiple catalogue candidates |
| ch | E210 | 350, 351 | multiple catalogue candidates |
| j | E322 | — | unresolved |
| jh | E365 | 906 | unique font crosswalk |
| ñ | E427 | — | unresolved |
| ṭ | E34F | 899 | unique font crosswalk |
| ṭh | E6D3 | 812, 816 | multiple catalogue candidates |
| ḍ | E346 | 920 | unique font crosswalk |
| ḍh | E353 | 921 | unique font crosswalk |
| ṇ | E538 | — | unresolved |
| t | E443 | — | unresolved |
| th | E6C3 | — | unresolved |
| d | E346 | 920 | unique font crosswalk |
| dh | E37D | 890 | unique font crosswalk |
| n | E538 | — | unresolved |
| p | E566 | — | unresolved |
| ph | E566 | — | unresolved |
| b | E503 | 625 | unique font crosswalk |
| bh | E577 | — | unresolved |
| m | E10A | 220 | unique font crosswalk |
| y | E59C | 420 | unique font crosswalk |
| r | E1FF | 392 | unique font crosswalk |
| l | E405 | 452 | unique font crosswalk |
| v | E559 | — | unresolved |
| ś | E304 | — | unresolved |
| ṣ | E190 | 175 | unique font crosswalk |
| s | E19B | 176 | unique font crosswalk |
| h | E190 | 175 | unique font crosswalk |

## Why some lookup fields are blank

The most frequent non-placeholder unassigned codes are 240, 235, 233 and 231. Checking the application resolved these blanks through canonical sign substitutions: for example 240 and 233 map to 220, while 235 decomposes into 220-900. This audit deliberately does not silently turn those blanks into omitted text.

## Files and reproduction

Run `python3 audit.py` then `python3 expand.py` in this directory (Python standard library only).
- `candidate-readings.json`: all 5,445 records, explicit unresolved tokens and direction status.
- `table7-crosswalk.json`: every Table 7 entry, including unresolved entries.
- `results.json`: initial direct-field counts and missing-ID frequencies.
- `canonical-results.json`, `expanded-map.json`, `expand.py`: second pass, after canonical processing.
- `lipi-index.vue`: exact application source used to identify and reproduce canonical processing.
- `xlits.csv`, `decipher.csv`: author's proposed mappings, not established values.
- `texts.js`, `signs.js`, `icit.js`, `app.js`, `explorer.html`: downloaded explorer inputs/source.
- `glyphs.tsv`: existing older font crosswalk; its codepoints must not be confused with the newer repository font encoding.
- `manifest.json`: input/output byte hashes.

## Sources and scope

Retrieved 2026-10-17.
- Explorer: https://tejesh-raut.github.io/indus-valley-script/#signs
- Explorer data: https://tejesh-raut.github.io/indus-valley-script/data/texts.js
- Proposed mapping commit: fc8813a52e183d19c441631dc26c33a4dccbea39
- Mapping: https://github.com/yajnadevam/lipi/blob/fc8813a52e183d19c441631dc26c33a4dccbea39/src/assets/data/xlits.csv
- Compact mapping: https://github.com/yajnadevam/lipi/blob/fc8813a52e183d19c441631dc26c33a4dccbea39/src/assets/data/decipher.csv
- Table 7, PDF page 23: https://rarebooksocietyofindia.org/book_archive/A_cryptanalytic_decipherment_of_the_Indu.pdf
- Older font crosswalk: https://raw.githubusercontent.com/dbourdeau/cyphersolver/main/targets/indus/data/glyphs.tsv

This is a reproducibility snapshot for research, not a claim of ownership or a grant of new redistribution rights over third-party data.

## Next discriminating test

Finish the 17 unresolved/ambiguous Table 7 entries by image review and freeze that map. Then specify the author's complete orthographic rules separately and test linguistic predictions against matched alternative mappings. Coverage alone cannot distinguish a correct mapping from a wrong one with the same set of assigned IDs.
