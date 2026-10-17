# Audit of dbourdeau/cyphersolver `targets/indus` (commit 843165c): scripts, reproducibility, methods

Read-only audit. The clone was not modified. All runs used a copy at `bourdeau_review/run/repo`, with original results kept in `run/results_orig`. Inputs: the bundled `data/`, `keys/` and `rebus/` folders, our ICIT export (`indus-lab/raw/inscriptions.csv`, passed as argv or `ICIT_FULL`), the SK webfont (`INDUS_FONT`), and Dravidian DB v1.1. Python 3.13, numpy 2.5, scipy 1.18, PIL 12.3. File opens were logged with an audit hook. The full per-script table is in `bourdeau_review/scripts_runnability.tsv` (430 rows), with logs in `bourdeau_review/logs/`.

Note: the clone is shallow (one commit, 2026-10-10). The repo claims every prediction set was "registered and committed before the script", but that order cannot be checked from this clone.

## 1. Inventory by purpose

The repo has 430 `.py` files: 350 `predict_test*.py` (sets 1-350) and 80 others. It has 414 result files: 349 `predict_test*.md` with 3,069 verdicts (1,576 hold, 1,493 fail), plus 65 others. The `.md` files include `lit_check.md`, which is a hand-written literature review with no script behind it.

| Group | Key scripts | Inputs | Headline (from results/*.md) |
|---|---|---|---|
| A. Corpus build and loaders | `build_corpus.py`, `icit_full.py`, `signs.py`, `rtools.py`, `damaged.py`, `merge_m77.py`, `align_m77.py`, `cisi.py`, `build_fairservis.py`, `descfam.py` | Bundled outputs. Rebuilding needs the indus-website SQL (we have it), the M77 csv or the CISI repo (external). | 2,543 objects and 10,253 tokens in lines of 3+ signs; 1,664 M77-only texts used as "held out". |
| B. Structure on the bundled corpus | `structure.py`, `slots.py`, `sixth.py`, `seventh.py`, `segment.py`, `numerals.py`, `noun_class.py`, `name_classes.py`, `parpola_checks.py`, `tablets.py`, `readable.py`, `leads.py`, `sign_list.py`, `allographs.py` (font) | Bundled data only | Endings are fixed per name: 5 of 881 names take both, against 46 by chance. 520 marks a closed class (fish-final names make up 61%). Two stroke series (JS 0.59 bits). 6+fish is enriched 4.8 times (p = 4e-5). Merging look-alike signs takes the 223 common signs to 180. |
| C. Fuller-ICIT analyses | `gulf.py`, `periods.py`, `anchors_full.py`, `replicate_full.py`, `grammar_model.py`, `describe18.py`, `robust13/17.py`, `predict_test2-36` (argv), `predict_test37+` (via `rtools.load_all`) | ICIT csv | West Asian texts end in 740/520 in 2 of 18 lines, against 43% at home (p = 0.007). Grammar signs are stable across periods (z 0.0) while numerals change (z 3.7). |
| D. Picture = sign anchors | `copper.py`, `anchors.py`, `motif_checks.py`, `referents.py`, `predict_test94/96/200-203/233-254/287-350` | Bundled data, plus ICIT for `rtools` | 7 copper "equations". Provisional anchors: 347 for the multi-headed animal, 460 for the tree. Tier 1 "referent fixed by picture" 4.57% (set 348). Picture vault 46 of 165 against a shuffle median of 5 (set 341). |
| E. Key bench and decipherment controls | `bench.py`, `anchors_bench.py`, `sanskrit_key_test.py`, `equation_rebus.py`, `rebus_checks.py`, `sound_tests.py`, `lang_control.py`, `linb_control.py`, `elamite(_control).py`, `pe_formula.py`, `fit_holdout.py`, `matched_holdout.py`, `substrate.py`, `lmkey.py`, `keyfit.py`, `predict_test179-181/205-207` | Monier-Williams `mw.txt`, ePSD2 `sux_gloss.tsv`, DEDR, JAMBU/Tamil/Burushaski "scout" lists, DAMOS, Elamicon, Yajnadevam (almost all external) | No published key beats its own shuffles in its claimed language. Fitted keys "read" 79-94% of held-out text in any language. |
| F. Language comparison and typology | `typology.py`, `lbench.py`, `lang_names.py`, `tamil_brahmi.py`, `tamil_stars.py`, `fish_star_world.py`, `graffiti.py`, `predict_test171-175/195-198/204/220` | WALS and Grambank profiles (bundled). The rest is external (CLICS4, ORACC, DHARMA, Lüders, Tamil-Brahmi). | "Only Dravidian passes both" grammar tests (conditional). L world excludes 85.1% of genera. Tamil star numbers are *not* enriched before the fish (p = 1.0). |
| G. Outside-world anchors | `meluhha.py`, `meluhha_oracc.py`, `ur3_seals.py`, `weights.py`, `wells_test.py`, `m77_checks.py`, `replicate_m77.py` | Mostly external (ORACC, weights CSVs, M77) | See §3. |
| H. "Decipherment loops": S/G/SIGN/WORD metrics | `progress.py`, `prizebench.py`, `famlm.py`, `grammar.py`, `restore.py`, `nnlm.py`, `predict_test176-199`, `208-232`, `248-286`, `317-320` | Bundled data plus ICIT (`nnlm` needs torch) | S 4.635 bits/sign. SIGN top-1 39.7% (frequency baseline 9.6%). WORD top-1 0%. G margin 49.6 / 37.4. P (sound values) 0. |

## 2. Can each script run on bundled data + our ICIT csv + font + DEDR?

| Status | n |
|---|---|
| Ran to completion; output identical to the published .md (3 of them differ only in line order) | 116 |
| Ran to completion; output differs (86 of the 89 read the ICIT csv) | 89 |
| Inputs load and the run starts, but it did not finish in the 12-60 s sweep budget (N = 10,000 permutations; no missing-file failure, and no external-data calls found in the source) | 149 |
| Library modules with no .md output | 13 |
| Not runnable | 62 |
| Not run (`build_fairservis.py`, which writes `keys/`) | 1 |

**Not runnable, by missing input:**

- **Monier-Williams and ePSD2:** `bench.py`, `anchors_bench.py`, `fit_holdout.py`, `matched_holdout.py`, `equation_rebus.py`, `lang_control.py`, `export_bench.py`, `replicate_m77.py`, `substrate.py`, `predict_test198/206`.
- **`LANG_DATA` name lists and lexicons:** `predict_test171-175`, `180`, `197`, `204`.
- **Linear B (DAMOS/Tiripode):** `linb_control.py`, `lang_names.py`, `sound_shortlist.py`, `predict_test11/16/22/152/160/163/166/169/179/205/207/234/235/287/290/310`. Linear B is therefore missing for every positive-control gate.
- **M77 csv:** `align_m77.py`, `merge_m77.py`, `m77_checks.py`, `m77_gaps.py`, `rebus_checks.py`, `wells_test.py`, `predict_test168/284/314`.
- **CLICS4:** `fish_star_world.py`, `predict_test181`.
- **Other external data:**
  - ORACC: `meluhha_oracc.py`, `ur3_seals.py`.
  - Elamite: `elamite_control.py`, `elamite.py`, `pe_formula.py`.
  - Other: `sanskrit_key_test.py` (Yajnadevam xlits), `tamil_brahmi.py`, `weights.py`, `cisi.py`.
- **Environment:**
  - `nnlm.py` needs torch.
  - `render_glyphs.py` and `render_texts.py` hard-code the Windows `arial.ttf`.
- **Code rot:** `predict_test188.py` raises `KeyError: 'trik'` because `progress.MODEL` was later changed to include `trik` (set 211). This older set no longer runs with the current shared code.

The Dravidian DB alone unlocks only `sound_tests.py` (reproduced identically). Every DEDR-using bench script also needs MW and ePSD2.

**Priority sample (10-minute timeout each):**

| Script | Result |
|---|---|
| copper.py | Reproduced; the content is identical, but T4/T5 lines come out in a different order. The order depends on Python's hash seed (set iteration). |
| anchors.py (with font) | Identical |
| numerals.py, noun_class.py, name_classes.py, allographs.py, parpola_checks.py, meluhha.py | Identical |
| periods.py, describe18.py (ICIT) | Identical |
| gulf.py (ICIT) | Differs. Our export lacks the Dilmun seal (`415 803 1 717 354`): 19 West Asian objects instead of 20, 2 of 17 instead of 2 of 18, Fisher p = 0.012 instead of 0.007, familiar pairs 47% instead of 45%. |
| anchors_full.py (ICIT) | Differs by one seal text: 1,555 instead of 1,556; 619 tests instead of 621. Same single hit: 700 with Bult, p 6e-05. |
| grammar.py | Module; ran with no output |
| anchors_bench.py, fish_star_world.py, meluhha_oracc.py, linb_control.py, fit_holdout.py, matched_holdout.py, bench.py, elamite_control.py | Failed: missing MW/ePSD2, CLICS4, ORACC csv, DAMOS or Elamicon |
| build_corpus.py (SQL dump) | `corpus.tsv` and `glyphs.tsv` regenerate byte-identical except CRLF line endings |
| predict_test341.py | Identical: 46 of 165 against a median of 5 |

Of the 89 differing outputs, only 2 of the 773 verdicts in them flip:

- **set 114 SR20:** p moves from 0.0450 to 0.0509 with the same Jaccard of 0.108.
- **set 227 CS4:** the gap moves from 9.9 to 10.3 points.

Most other differences are small count shifts from our slightly smaller ICIT export (4,234 against 4,235 objects in `replicate_full`). Set 349 moves more than that (199 of 3,948 becomes 235 of 4,117 held-out matches; its shuffle median goes from 91 to 120). That run is deterministic under three hash seeds, so the change comes from the data export.

## 3. Summaries of the requested results files

**copper.md**
- 46 prototype groups and 217 tablets (Parpola 1994 Fig. 7.14). 28 texts come from ICIT, 15 were read off the drawing ("approximate"), and 3 are not transcribed.
- T1 lists 10 linked rows (7 distinct equations): 341 rhino, 749 goat, 753 hare, 777 archer/goat, 778 goat, the lens sign for the long-horned bull, and the elephant/tiger pair.
- These equations are *input* (the `link` column of `rebus/copper_tablets.tsv`). The script prints them and computes nothing.
- T5 tests the "names" on 1,181 pictured seals: every p is between 0.14 and 1.0, so none carries over to seals.
- `sign_list.md` and set 32 CT5 ("anchor-in-own-picture count 0, p = 1.0") record that the equations were *withdrawn as text anchors*. The DOSSIER still calls them "Firm".

**anchors.md**
- 1,621 pictured objects form 1,360 (text, picture) units.
- A1, with Bonferroni over 949 tests, finds only sign 400 with gharial (10/108, p 3e-6) and with the multi-headed animal (p 3e-5).
- A2 lists 18 texts always written with one picture; nearly all are moulded copies of one text (hare ×12, gharial ×11, archer ×10).
- A1b lists p-values with no correction. Candidates 347 (one text on 8 copies) and 460 (4 of 5 tablet texts with a tree, p = 0.0005) are "candidate anchors".

**anchors_bench.md**
- Published keys against the provisional anchors (200 shuffles).
- 460 = tree: no key gets it.
- Anchor texts naming their picture:
  - Yajnadevam: 5 of 10 (shuffle mean 4.73; 129 of 200 shuffles as good).
  - Fairservis: 7 of 10 (162 and 190 of 200).
  - Mahadevan: 6 of 10 (32 of 200).
  - Parpola: 3 of 10.
  - Kak: 0 of 10.
- No key beats its shuffles.

**anchors_full.md**
- Seals of the fuller corpus. S1 (sign × animal): 1,556 texts, 621 tests, alpha 8.1e-5; one hit, 700 with the short-horned bull (3 of 17, p 6e-5).
- S2 (sign × standard/trough): 1,070 tests, no hits.
- On seals, signs do not track the animal.

**linb_control.md**
- 4,988 DAMOS lines, 36,407 tokens, 136,872 Greek forms.
- Ventris's *true* key against 100 shuffles:
  - consonant-only: 32.7% against a 29.4% median; 11 of 100 shuffles as good.
  - vowels kept: 40.7% against 38.9%; 27 of 100 as good.
  - Linear B spelling, consonant-only: 33.5%; 12 of 100.
  - Linear B spelling, vowels kept: 41.4%; 41 of 100.
- The bench's scoring fails its own positive control on Linear B.

**fit_holdout.md**
- 2,088 training lines; 975 held-out M77-only lines; 250-sign keys over 47 values; 20,000 hill-climbing steps.
- Held-out scores: DEDR 91.6% (shuffle median 90.3%, 1 of 100 as good), Sanskrit 93.6% (0 of 100), Sumerian 85.0%, Munda 79.8%, Old Tamil 76.3%, Burushaski 78.8%.
- With sign-shuffled training, the Dravidian fit still scores 91.6% held out (99 of 100 shuffles as good).
- A planted synthetic key gives 95.3% against 93.3%.
- Every language "generalises", so the metric is near its ceiling.

**matched_holdout.md**
- Lexicons matched to 2,405 skeletons; 5 draws; 50 shuffles.
- Positive control (synthetic Dravidian from DEDR): Old Tamil z 8.81 wins 4 of 5 draws. DEDR, the source lexicon itself, comes **last** (z 2.02). The control fails.
- Indus: Burushaski 6.24, Sumerian 6.12, Sanskrit 5.98, DEDR 5.22, Old Tamil 5.06, Munda 4.97. Inconclusive by the author's own reading.

**meluhha.md**
- 1,148 one-line square seals.
- Name slot of 1-3 signs: 595 of them (52%).
- Slots opening with a doubled sign: 23 of 1,051 (2.2%), against doubled adjacent signs anywhere in the slot at 60 of 3,161 (1.9%).
- Descriptive only: no test, and no baseline for the 52%. It says nothing about Nanaza or Samar.

**meluhha_oracc.md**
- 161 Meluhha attestations in 121 texts: Ur III 77, Old Babylonian 36; administrative 91, lexical 48.
- People: "son of Meluhha" in 5 + 4 texts.
- Na-na-za / Sa₆-ma-ar appear on 3 Irisagrig oil-allotment tablets from Šu-Suen year 6 (Nisaba 15 0371, CUSAS 40 1354 and 1582).
- Goods: abba wood 20, carnelian 14, copper 10.
- A clean data extraction with no inferential claim.

**lit_check.md**
- A manual check of 10-11 findings (F1-F11) against Parpola 1994/2008/2015, Mahadevan 1970-1998, Wells 2006, Rao et al. 2009/2010 and others.
- Most findings are "partly" published.
- What it calls new:
  - counts and baselines, such as 5 of 881 against ~46;
  - the noun-class-suffix test;
  - the opener's dependence on site and object type;
  - the 6+fish enrichment test;
  - the shuffled-key test validated on Linear Elamite.
- Notable conflicts:
  - Wells 2006 eliminated Dravidian, which contradicts F3.
  - Rao et al. 2009 had already shown the West Asian texts are anomalous (F8).
  - Grammar-based restoration has prior art at about 74% (F10).
- Wells 2011/2015 chapters and all of Fuls were unread.

**bench.md**
- 2,088 lines. Lexicon skeletons: MW 67,795, DEDR 8,257, ePSD2 3,830.
- Yajnadevam (681 signs keyed, 93% of tokens):
  - Sanskrit 75.3% against 75.1%, with 87 of 200 shuffles as good.
  - In the vowel-aware version, DEDR reads his key *better* than Sanskrit: 70.4%, 0 of 100 shuffles as good.
- Fairservis: DEDR 87.7%, 63 of 200 as good. Vowel-aware 92.7% against a 97.4% median, so the real key is *worse* than its shuffles.
- Kak and Mahadevan keys are too small to test.
- B4: Yajnadevam's numerals are never read as their number words.
- No key passes.

**elamite_control.md**
- Linear Elamite: 168 lines, 2,520 tokens; 61 sound values cover 60% of tokens.
- Consonant-only, the real key scores 60.7% against a 62.4% median (156 of 200 shuffles as good), so the bench cannot see a correct key.
- Vowel-aware (E1v): 25.7% against 19.6%, 1 of 200 as good. The bench adopted this version because it passes here.
- The same vowel-aware scoring fails on Linear B (27 and 41 of 100 shuffles as good, above).

## 4. Bugs, leakage and methodological weaknesses

1. **The copper "equations" are asserted, not tested, and they stand on single text families.**
   - `copper.py` T1 prints Parpola's links from the tsv. Each equation is one obverse text shared by two batches, for example `235 705 33 845 407 321 407` on 14 hare tablets and 2 tablets with sign 753. That makes 7 independent observations at most, with no statistic.
   - `predict_test94` CU1 ("545 same-text pairs share a motif, p = 0.0001"), CU2 (MI 2.59 bits, p = 0.0001), CU8 and CU19 count every tablet as independent. Their nulls shuffle pictures across objects, so the 12 hare and 10 archer copies drive the result. This is pseudo-replication: the null should permute at the level of text families.
2. **copper.py T4 artefact.** 7 of the 12 "names":
   - composite: `905 32 597`, `32 597 142`, `597 142 615`;
   - knot: `415 220 845`, `220 845 407`;
   - rhinoceros: `235 233 222`, `233 222 740`.

   These count as "in two or more different texts" only because a two-line text (for example `495 460 365 2 4 407 / 905 32 597 142 615 615`) contains the other group's one-line text verbatim. N-grams are taken per line, but distinct texts are counted per whole string.
3. **Picture vault: the excess over shuffles is mostly a coverage effect.** I reproduced set 341 exactly: 46 of 165 correct against a shuffle median of 5. On the same 165 predicted items, always guessing the pool's most common picture (Bult for hand-made tablets, Mult for moulded) gets **39 correct**. The method's real gain is about +7, not +41. The shuffle null rarely produces qualifying units, so it makes almost no predictions. Score precision against a majority/base-rate predictor, not raw hits against shuffles. (Excluding near-duplicate training texts, meaning substring or one-edit neighbours, changes little: 45 of 162, median 6. Near-duplicate leakage is *not* the problem here.)
4. **The M77 "held-out" sample is not independent.**
   - In `fit_holdout.py`, which matched_holdout inherits, only exact repeats are removed.
   - Of the 975 held-out lines, **395 (41%) are substrings or one-edit variants of a training line**, and 158 (16%) have every trigram seen in training.
   - Duplicates are not collapsed: 2,088 training lines are only 1,651 distinct, and 975 held-out lines only 800.
   - The DOSSIER's "replicated on an independent sample (M77)" claims carry the same caveat.
5. **The bench fails its positive controls, and the scoring version was chosen after seeing results.**
   - Consonant-only scoring fails on both Linear Elamite (156 of 200) and Linear B (11 of 100).
   - The vowel-aware version was adopted because it passes Elamite (1 of 200), yet it fails Linear B (27 and 41 of 100).
   - So every "key X does not beat its shuffles" verdict has unknown power.
   - `fit_holdout` H3 shows the score saturates: sign-shuffled training reads held-out text as well as real training does (99 of 100 shuffles as good).
6. **Unadjusted multiplicity.**
   - Across 349 sets, 3,069 verdicts mostly use a threshold of p < 0.05 with no family-wise or FDR control. 1,576 "hold".
   - `anchors.py` A1b reports 460-tree (p = 0.0005) as the best new anchor. Its own test family has 396 tablet tests (Bonferroni alpha 1.3e-4), which it misses.
   - The 460 texts are also near-duplicates: `354 460 798 740` and `15 460 798 740` differ in one sign, and `495 460 740 400` and `415 240 495 460 752 740` share `495 460`. That is roughly 2-3 families, not 4 independent texts.
   - A1 (sign 400 with gharial and multi-headed animal) is confounded with object type: 400 is a tablet suffix and these pictures occur only on moulded tablets. The base rate is not stratified. Later sets fixed this by stratifying base rates by site and object class (sets 333-335).
7. **Fragile verdicts.** Two verdicts flip with a one-object change in the ICIT export (SR20 at p 0.045 → 0.051; CS4). Many verdicts sit at the 0.05 edge with only 1,000 permutations.
8. **Non-determinism.**
   - `copper.py` and `tablets.py` output depends on `PYTHONHASHSEED`. The `tablets.py` shuffle range came out 22-42 in the original, 24-44 in the sweep, and 21-40 / 22-42 under hash seeds 1 and 2. The cause is random draws over lists built from `set`s.
   - `leads.py` p moves from 0.428 to 0.430 on identical bundled data.
9. **Stale results and code rot.**
   - The published `sign_list.md` text does not match what `sign_list.py` now prints.
   - `predict_test188` crashes under the current `progress.MODEL`.
   - Shared modules (`progress`, `famlm`, `grammar`, `rtools`) change over time. Old sets therefore silently depend on newer code, and their published .md may not be what today's code produces.
10. **Unsafe failure modes.**
    - `cisi.py` given a bad path **overwrote `data/cisi_mayig.tsv` and `data/cisi_signs.tsv` with empty files** (this happened in my copy; I restored it).
    - `elamite.py` given a bad path exits 0 and writes "0 entries; permutations as large 500 of 500".
    - `predict_test174` and `pe_formula` divide by zero instead of reporting the missing data.
    - No script checks that its inputs exist.
11. **Leakage the authors acknowledged and kept.** The S metric conditions on line length, so the end token is almost free (PROGRESS.md audit after set 223). The 'first' component was withdrawn for conditioning on itself. The absolute S of 4.635 is optimistic.
12. **Weak controls elsewhere.**
    - `meluhha.md` has no null for its 52% figure.
    - The gulf result rests on 18 lines; removing one Dilmun seal moves p from 0.007 to 0.012.
    - The Linear B referent control has 95% held-out precision against 5% for Indus. It is a much easier domain, because ideograms sit next to their words, so passing it says little about the Indus pools.
