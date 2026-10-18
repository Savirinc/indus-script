# Round 48 — Does the Indus sign inventory resemble Brahmi more than scripts that cannot be related to it?

Pre-registered 2026-10-18, before any distance was computed. Changes after this commit go in an "Amendments" section with the reason.

## Question
The Brahmi lead has two legs. Leg 1, the sound values of the 714-code key, was tested in round 47 and is not Sanskrit-specific (NULL). Leg 2, the claim that Indus signs *look like* Brahmi letters, has never been tested against a null. Thirty-eight published look-alike pairs (Table 7, Yajnadevam 2024) feel compelling, but Brahmi has 47 letters built from a few strokes, and the Indus catalogue has 700 signs. Crosses, forks, cups and ladders occur in every script. The question is whether Brahmi wins more nearest-shape matches than its inventory size predicts, and whether it beats scripts that are geographically and chronologically impossible ancestors or descendants of Indus.

## Hypotheses
- **H1** Indus signs resemble Brahmi letters beyond chance, and more than they resemble unrelated scripts.
- **H0** Brahmi's share of nearest-neighbour matches equals what its share of the letter pool predicts, once letter complexity is controlled.

## Frozen inputs
| Input | Source | Pin |
|---|---|---|
| Indus glyphs | yajnadevam/lipi `src/assets/fonts/indus-font.woff2`, codepoint = U+E000 + catalogue code | commit fc8813a5; sha256 b2758032… (SHA256SUMS) |
| 25 comparison scripts | Noto Sans fonts, google/fonts `ofl/` | commit 47d54ca1; hashes in SHA256SUMS |
| Indus query set Q1 | every sign code attested in the round 47 core corpus (`load_corpus`, 1,934 text types, 582 codes) that has a glyph | round47/run47.py |
| Query set Q2 | the 100 most frequent codes of Q1 by token count | same |
| Query set Q3 (diagnostic only) | the 18 catalogue codes uniquely crosswalked from Table 7 | round46 `table7-crosswalk.json` |

Letter inventories (consonant and independent-vowel letters only; no vowel signs, digits, punctuation, ideograms). Counts are renderable glyphs in the stated ranges.

| Script | Range(s) | n | Relation to Phoenician / Greek (for controls) |
|---|---|---:|---|
| Brahmi | 11005–11033 | 47 | target |
| Kharoshthi | 10A00, 10A10–13, 10A15–17, 10A19–35 | 37 | Aramaic-derived, contemporary with Brahmi |
| Phoenician | 10900–10915 | 22 | PC1 query |
| Imperial Aramaic | 10840–10855 | 22 | Phoenician descendant |
| Samaritan | 0800–0815 | 22 | Phoenician descendant |
| Greek capitals | 0391–03A1, 03A3–03A9 | 24 | Phoenician descendant; PC2 query |
| Old Italic | 10300–1031F | 32 | Greek descendant |
| Lycian | 10280–1029C | 29 | Greek-derived |
| Carian | 102A0–102D0 | 49 | Greek-related |
| Lydian | 10920–10939 | 26 | Greek-related |
| Old South Arabian | 10A60–10A7C | 29 | Semitic sibling |
| Old North Arabian | 10A80–10A9C | 29 | Semitic sibling |
| Gothic | 10330–1034A | 27 | Greek-derived |
| Runic | 16A0–16EA | 75 | distant (via Old Italic) |
| Old Turkic | 10C00–10C48 | 73 | distant (via Aramaic/Sogdian) |
| Old Hungarian | 10C80–10CB2 | 51 | distant; NC1 query |
| Glagolitic | 2C00–2C2E | 47 | invented, Greek-influenced |
| Old Permic | 10350–10375 | 38 | invented, Cyrillic/Greek-influenced |
| Elbasan | 10500–10527 | 40 | invented |
| Osage | 104B0–104D3 | 36 | invented 2006, Latin-based |
| Tifinagh | 2D30–2D67 | 56 | Libyco-Berber |
| N'Ko | 07CA–07EA | 33 | invented 1949 |
| Meroitic cursive | 109A0–109B7 | 24 | Egyptian-derived |
| Linear A | 10600–1065F | 96 | Cretan, 1800–1450 BCE, unrelated; NC2 query |
| Cypro-Minoan | 12F90–12FF0 | 97 | Cypriot, 1550–1050 BCE, unrelated |
| **Pool total** | | **1,061** | |

Wedge scripts (Ugaritic, Old Persian) and Ogham are excluded on purpose: their texture is so different that they would be far from everything and inflate every other script's enrichment.

## Rendering and distance
1. Render each glyph with Pillow at 200 px em, crop to the ink bounding box, pad to a square preserving aspect ratio, resize to 40×40 with antialiasing, threshold at 0.5.
2. Thin to a one-pixel skeleton (Zhang–Suen). Glyphs whose ink box is under 4 px in either dimension are dropped and listed.
3. Distance d(A,B) = ½·[mean over skeleton pixels of A of the Euclidean distance transform of B + the same with A and B swapped], in units of grid pixels / 40.
4. Transform freedom: d is minimised over the 8 dihedral transforms of A (rotations by multiples of 90° and reflections). The same freedom applies to every script. Identity-only distances are a secondary analysis.

## Statistic
For each query glyph find its nearest pool letter. For script X, with n_X letters in a pool of N:

E_X = (number of query glyphs whose nearest neighbour is in X) ÷ (N_q · n_X / N).

Primary statistic: E_Brahmi on Q1. Also reported: Brahmi's rank among 25 scripts by E_X, and E_X for every X.

## Null
10,000 random permutations of script labels over the pool letters, preserving inventory sizes; p = share of permutations with E ≥ E_real; z = (E_real − mean)/sd. **Primary null is complexity-stratified:** labels are permuted only within deciles of skeleton pixel count, so a script cannot win merely by being as simple as Indus signs. Unstratified null reported too. Seed 48001 (Q1), 48002 (Q2), 48003 (Q3), 48101+ (controls).

## Controls
- **PC1** Query = Phoenician (22); pool = the other 24 scripts. Passes if Imperial Aramaic and Samaritan each have stratified p < 0.05 **and** the top-ranked script by E is Phoenician-descended (Imperial Aramaic, Samaritan, Greek capitals, Old Italic, Lycian, Carian, Lydian, Gothic, Old South Arabian, Old North Arabian, Kharoshthi).
- **PC2** Query = Greek capitals (24). Passes if at least two of {Phoenician, Old Italic, Lycian, Carian, Lydian, Gothic} have stratified p < 0.05 and the top-ranked script is in that set.
- **NC1** Query = Old Hungarian (51). **NC2** Query = Linear A (96). Neither can be related to Brahmi. Brahmi's E and p for these queries measure how much Brahmi is enriched for any angular or geometric inventory. Expected: p ≥ 0.05.

## Verdict rules (fixed now)
- **METHOD-FAIL** if PC1 or PC2 fails. Nothing about Indus is then concluded.
- **SUPPORT** if Q1 stratified p < 0.01, Brahmi ranks 1st of 25 on Q1, Q2 stratified p < 0.05, and E_Brahmi(Indus Q1) exceeds E_Brahmi for both NC1 and NC2.
- **NULL** if Q1 stratified p ≥ 0.05.
- **ARTEFACT** if Q1 p < 0.05 but Brahmi is also enriched (p < 0.05) for NC1 or NC2, or an unrelated script (any of Runic, Old Turkic, Old Hungarian, Glagolitic, Old Permic, Elbasan, Osage, Tifinagh, N'Ko, Linear A, Cypro-Minoan) ranks above Brahmi on Q1.
- **MIXED** otherwise; then say exactly which clause failed.

## Secondary analyses (reported, not verdict-bearing)
- Rarefied mean nearest distance: every script subsampled to 22 letters, 200 draws; mean over Q1 of the nearest distance; rank table. Removes size dependence a different way.
- Kharoshthi vs Brahmi: both Indian, same century; if Indus matches one but not the other, that is informative either way.
- Table 7 diagnostic: for the 18 uniquely crosswalked pairs, the distance from the Indus sign to the author's chosen Brahmi letter, and whether that letter is the sign's global nearest neighbour in the whole pool. Report the fraction. This is his own selection, so it cannot support H1; it can show how far his matches are from the best available.
- Identity-only transform version of the primary statistic.

## What a result would and would not mean
- SUPPORT: Indus signs share shape vocabulary with Brahmi beyond chance and beyond unrelated scripts. That is shape affinity, not descent and not sound values; round 47 stands.
- NULL or ARTEFACT: the published resemblances are what 47 simple letters and 582 signs produce by chance. The Brahmi lead is then closed on both legs, pending epigraphic (not typographic) glyph sets.

## Limits stated in advance
Modern typographic forms (Noto, and a modern normalised Indus font) stand in for epigraphic shapes; Noto Brahmi follows Ashokan forms. A 40×40 skeleton loses stroke-order and stroke-width information. Compound Indus signs are included; the stratified null controls complexity, not compositionality. Dihedral freedom is generous to every script equally. Fonts are external inputs that upstream could change; hashes are recorded.

## Amendment 1 (2026-10-18, after the v1 run; reason stated)
**What happened.** Descriptor v1 (40×40 skeleton chamfer, dihedral freedom) ran as written. PC1 failed: for Phoenician, the top script was Old North Arabian (a genuine Semitic sibling, p=0.021) but Imperial Aramaic (p=0.47) and Samaritan (p=0.39) were not recognised. PC2 failed: Lycian was recognised (p=0.001) but no second Greek-derived script was. Verdict for v1: **METHOD-FAIL**, recorded in `v1/`. The Indus analysis also ran in that script, so its v1 numbers were seen (Brahmi E=0.35, rank 20 of 25, i.e. depleted, not enriched). They are reported as the v1 outcome and carry no weight either way.

**Diagnosis.** A skeleton chamfer at 40×40 is dominated by typographic style (rounded Noto Brahmi and Aramaic versus angular Phoenician and Indus strokes). Two of the three pre-specified PC1 targets are also the most evolved forms (Imperial Aramaic is 5th-century BCE cursive; Samaritan is later still), which made PC1 harder than the Indus question itself.

**Change 1: descriptor selection on controls only.** Four candidate descriptors are fixed here and evaluated on controls alone:
- **A** v1 as above.
- **B** uniform-stroke chamfer: 64×64 grid, skeleton dilated to a 3-pixel stroke, symmetric chamfer on the dilated masks, dihedral min.
- **C** shape context: 64×64 skeleton, log-polar histogram around the centroid (5 radial × 12 angular bins, radii normalised by the glyph's RMS radius), chi-square distance, dihedral min.
- **D** B and C combined: each distance divided by its median over all pairs, then summed.

**Change 2: positive-control queries and related sets** (standard palaeography; fixed before any candidate other than A is run):
| Query | Related set |
|---|---|
| Phoenician | Old North Arabian, Old South Arabian (siblings); Imperial Aramaic, Samaritan, Greek capitals (descendants) |
| Greek capitals | Phoenician; Old Italic, Gothic, Lycian, Carian, Lydian |
| Old Italic | Greek capitals, Runic |
| Imperial Aramaic | Phoenician, Samaritan, Kharoshthi |

A query **passes** if its top-ranked script by E is in its related set **and** at least two related scripts have stratified p < 0.05. A descriptor **passes** if at least 3 of the 4 queries pass. Negative queries stay Old Hungarian and Linear A. Under this rule descriptor A still fails (Phoenician: one related script significant; Greek: one), so the rule is not a relaxation that rescues v1.

**Change 3: selection and Indus run.** Among passing descriptors, choose the one with the most query passes, ties broken by the mean stratified z of related scripts across the four queries. Run the Indus analysis **once** with that descriptor. If no descriptor passes, the round ends METHOD-FAIL and the shape question is declared untestable with typographic glyphs. Verdict rules of the original protocol apply unchanged to the selected descriptor's Indus run. Seeds: 48201+ for selection, 48001–48006 for Indus as before.
