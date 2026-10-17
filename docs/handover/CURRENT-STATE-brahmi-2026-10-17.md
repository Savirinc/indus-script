# Current state: separate observations from interpretations

## What we measured
Latest source: Tejesh Raut's explorer, downloaded 17 October 2026.
- 5,445 records; 902 contain no parseable three-digit sign sequence.
- 4,543 records with sequences. These are catalogue records, not deduplicated objects/texts.
- 2,477 records pass our conservative filter: complete Y/YES, single line, known R/L or L/R direction, no damaged edges and no 000/999 placeholders.
- Direct xlit fields cover every sign in 1,927 of these records.
- Applying the author's ordered canonical expansion covers all 2,477.
- Expanded map: 714 non-placeholder codes with proposed values. Unresolved placeholders: 000 and 999.
- Across all records, 3,497 contain nonempty sequences with every code assigned after expansion.

Meaning: the full proposed mapping is executable and provides assignments across the filtered subset. It establishes neither phonetic truth nor Sanskrit grammar nor historical Brahmi descent. No independent linguistic validation or fair language comparison has been run in Round 29.

## Mapping provenance
Bharath Rao, known as Yajnadevam, proposes the Sanskrit reading. He is distinct from Rajesh P. N. Rao at the University of Washington, who studies statistical structure.
- Mapping/source commit: fc8813a52e183d19c441631dc26c33a4dccbea39 in yajnadevam/lipi.
- xlits.csv gives explicit proposed values, canonical codes and regex fields.
- expand.py reproduces the single ordered canonical pass relevant to coverage. It does NOT implement the full application, dictionary matching, schwa handling, sandhi, or translation.
- lipi-index.vue preserves the inspected source. Independently check parser types, pass order and any omitted behavior.

## M-304 example and caveat
Explorer stored transcription: +090-740-220-742-534-550-090+.
Recorded direction: R/L. Our reading-order raw lookup: a | as | as | an | m | an | a.
This is a mechanical output, not a prayer translation. Before interpreting it, independently verify the record against the photograph, seal/impression orientation and catalogue convention. Do not infer direction merely from English display order or blindly trust our reversal.

## Screenshot and atlas
The screenshot is Table 7, 'Indus signs standardized into Brahmi', in Yajnadevam's paper dated November 13, 2024, printed page 23 / zero-based PDF page 22.
- 38 sound-labelled entries; 32 distinct extracted Indus font codepoints.
- Provisional older-font crosswalk: 21 entries uniquely resolve to 18 catalogue IDs; 3 have multiple candidates; 14 unresolved.
- This incomplete Table 7 crosswalk must NOT be conflated with the full 714-code map.
- Atlas: 714 assignments. Its downloaded font has 713 glyphs; 941 has a proposed value but no available drawing.
- Atlas Brahmi strings are separated character-name displays of raw labels, not fully orthographic Brahmi words or independent historical evidence. The full mapping has been projected into Brahmi for display; shape resemblance was not independently established for all 714 signs.
- Older PDF font private codepoints differ from the newer repository font's E000 + code convention. Never mix them without a verified crosswalk.

## Three corpora, not one
1. Prior main export: 5,679 CSV rows; upstream site sometimes reports 5,680. Discrepancy unresolved.
2. Current explorer: 5,445 records; do not silently pool with (1).
3. Rao et al.'s PNAS paper: EBUDS, 1,548 deduplicated lines, approximately 7,000 signs, Mahadevan's 417-sign inventory. Not our ID system or dataset.

## Important earlier results
Consult prior-project/CURRENT-STATUS.md and original outputs before relying on exact figures.
- Tamil repetition-pattern test did not outperform shuffled controls.
- Cross-city sign-order prediction improved on unigram baselines; this does not identify sounds or language.
- Joint position/composition control was inconclusive because its sampler barely moved.
- Copper-tablet motif correlations weaken under text-family holdout; there are no seven established sign=image translations.
- External Meluhha-associated names and the Ur seal were not joined into a bilingual key.
- Linear B demonstrates a bilingual is not logically required. More constraints can in principle identify a reading, but no generic length threshold proves this candidate without its model assumptions.

## Primary links
https://homes.cs.washington.edu/~rao/indus.html
https://homes.cs.washington.edu/~rao/PNASIndus.pdf
https://tejesh-raut.github.io/indus-valley-script/#signs
https://github.com/yajnadevam/lipi
https://github.com/yajnadevam/ScriptDerivation
https://rarebooksocietyofindia.org/book_archive/A_cryptanalytic_decipherment_of_the_Indu.pdf
https://dbourdeau.github.io/cyphersolver/indus.html

The snapshot is evidence of what was downloaded, not assurance every upstream source is independently correct or that every linked work has been fully read.
