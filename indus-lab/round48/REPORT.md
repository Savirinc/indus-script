# Round 48 — Shape resemblance of Indus signs to Brahmi: **METHOD-FAIL**

Pre-registered in `PROTOCOL.md` (commit c083016), amended once before the second run (Amendment 1, commit b6c3529). Verdict word per protocol: **METHOD-FAIL**. No conclusion about Indus–Brahmi shape affinity is drawn, in either direction.

## What was tested
Whether the 581 corpus-attested Indus signs (glyphs from the lipi font, pinned) pick Brahmi letters as nearest shapes more often than Brahmi's share of a 1,061-letter pool from 25 scripts predicts, under a complexity-stratified label-permutation null, with dihedral freedom given to every script equally. The method had to prove itself first on scripts whose relationships are known.

## Positive controls: all four descriptors fail
A query passes if its top-ranked script is a known relative and at least two known relatives reach p < 0.05 (Amendment 1). A descriptor passes with 3 of 4 queries.

| Descriptor | Phoenician | Greek capitals | Old Italic | Imperial Aramaic | Passes |
|---|---|---|---|---|---:|
| A skeleton chamfer 40×40 | top Old North Arabian ✓, 1 sig | top Lycian ✓, 1 sig | top Old Turkic ✗ | top Kharoshthi ✓, 1 sig | 0/4 |
| B uniform-stroke chamfer 64×64 | top Imperial Aramaic ✓, 0 sig | top Lycian ✓, 2 sig | top Lydian ✗ | top Kharoshthi ✓, 1 sig | 1/4 |
| C shape context | top Lycian ✗ | top Lycian ✓, 2 sig | top Lycian ✗ | top Phoenician ✓, 0 sig | 1/4 |
| D = B + C | top Lycian ✗ | top Lycian ✓, 1 sig | top Lydian ✗ | top Meroitic ✗ | 0/4 |

The matcher is not blind: it repeatedly finds genuine relatives at the top (Old North Arabian for Phoenician, Lycian and Carian for Greek, Kharoshthi for Aramaic, Imperial Aramaic for Phoenician under B). But with 22 to 32 query letters the nearest-neighbour count has too little power to make two relatives significant at once, and typographic style (rounded Noto Brahmi and Aramaic versus angular Phoenician, Lycian and Indus strokes) competes with descent. Negative queries behaved: Brahmi was never enriched for Old Hungarian or Linear A (all p > 0.6). Full numbers in `selection.json`, `select.log`.

## What the v1 Indus run showed (seen before Amendment 1; carries no weight)
With descriptor A, Brahmi received 9 nearest-neighbour hits against 25.7 expected (E = 0.35, rank 20 of 25, stratified p = 0.94). Old South Arabian (E = 5.0) and Old Hungarian (E = 2.7) topped the table, which is the angular-stroke style effect. Kharoshthi was also depleted (E = 0.44). Identity-only transforms: Brahmi E = 0.62. Files in `v1/`.

**Table 7 diagnostic (v1).** Of the 20 author-specified sign–letter pairs with glyphs on both sides, the author's Brahmi letter was the sign's single nearest shape in the whole pool for 3 pairs (signs 890, 625, 392). For the other 17 the author's letter ranked at a median of 594th of 1,061 letters, i.e. in the farther half. Under a descriptor that fails its controls this is a description of the matcher, not of Table 7.

## What this means
- The shape leg of the Brahmi lead cannot be tested with modern typographic glyphs and a nearest-neighbour statistic at these inventory sizes. The same instrument cannot see Phoenician → Aramaic or Greek → Gothic, relationships nobody disputes.
- The symmetric consequence: published look-alike tables are not evidence either. If an instrument sensitive enough to detect known descent does not exist at this resolution, eyeballed resemblance between 47 simple letters and 700 signs is at best unquantified and at worst the chance rate.
- Round 47 (sound values: NULL) is unaffected. The Brahmi lead now has one leg rejected and one leg untestable.

## Reopen criteria
1. Epigraphic glyph sets instead of fonts: traced Ashokan Brahmi letter forms and traced Indus sign forms from published sign lists, under compatible licences.
2. A higher-powered statistic pre-registered from scratch: per query letter, the percentile rank of its best match in each candidate script among all pool letters, aggregated with a permutation test, instead of argmin counts. The v1 Indus numbers above must be declared in that protocol as previously seen.
3. The same controls: it must find Phoenician → Aramaic and Greek → Gothic before being pointed at Indus.

## Reproduce
```
bash fetch_fonts.sh                                   # pinned Noto fonts + lipi Indus font into ext/fonts, hashes in SHA256SUMS
../../ext/venv/bin/python run48.py select             # Amendment 1 selection on controls only, 20 s → selection.json
../../ext/venv/bin/python v1/run48_v1.py              # the original v1 run (controls + Indus), 8 s
```
Environment: `python3 -m venv ext/venv && ext/venv/bin/pip install pillow fonttools brotli numpy scipy`.
