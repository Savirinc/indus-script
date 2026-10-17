# Digest: Bourdeau / Claude Indus project (targets/indus @ 843165c)

Files read in full: PROGRESS.md, PAPER_DRAFT.md, NOTES.md. A few facts in sections 3 come from `results/` files and are marked [results]. Citations use "N:pass" for NOTES (e.g. N:P10 = tenth pass), "N:set k" for the per-set entries in the decipherment loops, "PR" for PROGRESS.md and "PD:§" for PAPER_DRAFT.md. Status of the notes file: "in progress". It runs 23-25 Sept 2026: about 350 registered prediction sets and three runs of a "decipherment loop" (loops 1-174).

## 1. Work streams, in order, with final status

| # | Stream (NOTES pass/set) | Script → result | Final status |
|---|---|---|---|
| 1 | Parpola 2005 lecture counts C1-C16 (P1) | `parpola_checks.py`, `m77_checks.py` → `results/parpola_checks.md`, `m77_checks.md` | **Established** (counts mostly confirmed). 7+fish rests on 1 seal (H-9); fig+fish rests on 2 (M-172, M-414) |
| 2 | ICIT↔M77 sign map (P1) | `align_m77.py` → `data/icit_m77_map.tsv` | Established: 991 lines, 96% single counterpart |
| 3 | Rebus chance baseline R4; Parpola 1994 readings R1-R3 (P2) | `rebus_checks.py` → `rebus_checks.md` | Established negative: an arbitrary picture gives a Tamil star name 15-68% of the time. Parpola's numeral restriction "does not hold" |
| 4 | Signs vs seal motifs (P2, P17, set 67) | `motif_checks.py`, `anchors_full.py` | Established negative: "Seal texts do not name or qualify the animal" |
| 5 | Structural layer (numeral systems, endings, 845(61)407 formula) (P3) | `structure.py` → `structure.md` | Established (grade A). Readings of it are grade C |
| 6 | Copper tablets as bilinguals (P4) | `copper.py`, `rebus/copper_tablets.tsv` → `copper.md` | 7 equations proposed. **3 of them withdrawn as text anchors in set 32** (see §2) |
| 7 | Slot classes; numerals vs Harappan weights (P4, P10) | `slots.py`, `numerals.py`, `weights.py` | Established: the numerals are "not weight units" |
| 8 | Sanskrit/Sumerian controls on the fish=star pun (P4); CLICS world base rate (P6) | `lang_control.py`, `fish_star_world.py` | Established: the pun is Dravidian-only among South Asian families (basic vocabulary) |
| 9 | Ending proposals vs structure (P4) | `sound_tests.py` | Mixed. 520 = Tamil *utu*/-*otu* is "grade C, a candidate, not a reading" |
| 10 | Tablet equations as rebuses (P5) | `equation_rebus.py` | Failed for every language: ranks 19/23/12/23 (Dravidian) against chance ~13 |
| 11 | Yajnadevam key, consonant mode (P5, P8) | `sanskrit_key_test.py`, `bench.py` | Failed (63 of 200 shuffles as good) |
| 12 | Proto-Elamite parallel (P5, P6) | `elamite.py`, `pe_formula.py` | Established as a structural parallel |
| 13 | Ending grid, opener formula (P6) | `sixth.py` | Grid established. The opener site effect was **withdrawn** in P17 (it was a Lothal sealing artefact) |
| 14 | Tamil star names; 12+fish/1+fish (P7, P8) | `tamil_stars.py` | Only 6+fish is enriched. 12+fish and 1+fish are "artifacts" (Lothal sealings, opener stroke) |
| 15 | Meluhhan names (P7, P10, P13) | `meluhha.py`, `meluhha_oracc.py` | 2 names only (§3) |
| 16 | Decipherment bench B1-B5 (P8-P10, P17) | `bench.py`, `keys/`, `elamite_control.py`, `linb_control.py` | **Downgraded**: "cannot reliably recognise a correct decipherment" (Linear B fails, §4) |
| 17 | M77 replication, segmentation, allographs (P9) | `merge_m77.py`, `replicate_m77.py`, `segment.py`, `allographs.py` | Established |
| 18 | Fairservis key (P9) | `build_fairservis.py` | Failed (below its shuffles) |
| 19 | Noun-class test; new anchors 347/460 (P11) | `noun_class.py`, `anchors.py` | Class test established (conditional). Anchors provisional |
| 20 | Word order + combined language test (P12) | `typology.py`, `anchors_bench.py` | "Only Dravidian passes both outright", conditional. **Weakened later** (§6, contradiction C5) |
| 21 | Fitted keys on unseen texts (P13) | `fit_holdout.py`, `matched_holdout.py` | Established negative (§4) |
| 22 | Tamil-Brahmi names; first registered predictions (P14) | `tamil_brahmi.py`, `predict_test.py` | The Dravidian-model predictions P1 and P3 failed |
| 23 | Restoration, periods, Gulf control, Witzel (P15) | `restore.py`, `periods.py`, `gulf.py`, `substrate.py` | Restoration and Gulf established. Witzel test "not possible" |
| 24 | Wells 2006 Munda test (P17) | `wells_test.py` | Wells's arguments "do not survive the data" |
| 25 | Registered-prediction loops, sets 4-135 (P18-P149) | `predict_test4..135.py` | Structure only. Tally 1045 held / 986 failed at loop end. "Saturation of internal hypothesis testing" (N: Loop end) |
| 26 | External-direction sets 136-175 (West Asian, glyph shapes, CISI, capture-recapture, Ur III, name lists) | `predict_test136+.py`, `cisi.py`, `ur3_seals.py`, `lang_names.py` | Mostly structural. Language "stays undecided" (sets 185-189) |
| 27 | Decipherment loops 1-174 (sets 176-349), metric in `progress.py` → `results/progress_log.tsv` | `grammar.py`, `famlm.py`, `lmkey.py`, `nnlm.py`, `predict_test176-349.py` | P (sound values) = 0 throughout. Stopping rule met twice (loops 102 and 149). Third run ends at loop 174 with streak 1 and no closing note |

## 2. Every claim of a fixed meaning or sound for a sign

**Sound values: none.** PR tier 3: "0 (no sound value has passed)". PD abstract: "No sound value is established." Component P = 0 in every loop.

| Sign (ICIT) | Claimed value | Evidence | Status / retraction |
|---|---|---|---|
| strokes 1-7 (short), 13-19 tiered (16=6, 17=7), 31-36 long, 55=12, one sign = 24 | counts | stroke count; M = 16.6% of tokens | Taken as established ("their sense is the count", PR tier 1). Short and long strokes are two systems (JSD 0.59-0.77) |
| 740 'jar' | name ending, person/"rational" class | fixed per name (5/881 against 46), stem-final, segmenter binds it | Function established; value only a proposal (C: Parpola genitive). Sound proposals tested: Mahadevan -(a)nru, Yajnadevam -an, Kak *sa*, Parpola possessive *-a* via *a* 'cow'. None validated. Kak's key "passes only via 740 = sa at line ends" (set 206) |
| 520 'arrow' | ending of fish-headed names | fish heads 154/254. "Class is lexical, per head" (set 121) | Function established. N2's "520 counted like a noun" was **corrected**: '33 520' / '705/706 33 520' is a fixed formula (sets 16, 17, 82). Tamil *utu* = sociative *-otu*: grade C only (N:P4 §5) |
| 90 'man' | head noun after 740 ('X-740 man') | follows 740 in 112 of 178 | Structural. Word-order half credited to Parpola 1994 (N:P14 §3) |
| 400, 151 | second-slot suffixes (400 = Harappa tablet suffix) | sets 82-83 | Structural |
| 817/820/861 + 2/60/1 | one heading formula | P6, sets 89, 104 | Structural |
| 700 'pot' | counted container / capacity measure | 4+pot beside a pot-offering scene on M-478/479 (Parpola 2005 Fig. 1); 45 of 51 tablet numerals before 700 are long strokes | Picture anchor "B". Later: "a count sign only (values 2-4 in 98%)" (set 63) |
| 783/785 'fig' (three-leaf) | pipal | 4+fig+jar on H-289, H-290 and one unnumbered tablet, all with a pipal reverse | "The sign means 'fig'" (N:P3 §5, grade B). Never formally revisited |
| 777 (fig+crab) | markhor goat **and** horned archer | Parpola 1994 Fig. 7.14 linked groups | In M (copper equations). See retraction below |
| 749 | markhor goat | same | **Withdrawn as a text anchor** (set 32) |
| 341 | rhinoceros (a logogram by shape) | same | **Withdrawn as a text anchor** (set 32) |
| 753 | hare | same | **Withdrawn as a text anchor** (set 32) |
| lens sign; "3 700 900 165" | long-horned bull; bull with heart-shaped spots | same | Not revisited separately |
| *Retraction, set 32 (N:P46):* | | "the 'firm' copper equations ... (341 rhino, 749 / 778 goat, 753 hare) never occur in the copper labels of their own picture in the ICIT texts (CT5: 0); they came from Parpola's reverse drawings and are withdrawn as text anchors." Set 33: "8 of his 10 linked groups pair an image reverse with a single-sign reverse." | |
| 347 | multi-headed animal | 8 of 9 objects, but one text on 8 moulded tablets | **Provisional.** Untestable on new objects (0 cases; set 177) |
| 460 (three cones) | tree/plant | 4 of 5 distinct tablet texts, p = 0.0005 | **Provisional**, "best supported" new candidate. Untestable on new objects (2 cases; set 177). No key gives it a word for tree |
| 645, 318 | cross; gharial | one text each | "weak" |
| 6+fish (16 220 etc.) | Pleiades (Parpola) | enriched 4.8× (ICIT), 11.5× (M77-only), 4.7× (fuller) | "The only star name the numerals support" (N:P8). **But** see contradiction C4: 2+fish dominates, and Parpola's own CISI M-1..M-184 has no 6+fish |
| 7+fish; fig+fish | Ursa Major; North Star | 1 seal; 2 seals | Unsupported (single attestations). 7+fish depleted (0.2×) |
| fish 220 series | 'star' (*min*) | the pun is Dravidian-only among South Asian families (CLICS4) | First step "distinctive". The compound check is weak |
| referent units (tier 1) | e.g. 923 elephant, 790 goat, 4 pipal, 17/318/440/503 gharial (set 303); 806 158 tree; 706 33 923 740 elephant | text-picture association on tablets, FDR-calibrated | **Referent, "not read"**: "local labels; they do not transfer between tablet types (1 of 40)". Not pictographs (set 315: 1/24; "923 is a 'right parenthesis'"). Coverage has moved 0.38% → 2.29% → 23.5% → **1.09% (copy-counting flaw, set 337)** → 4.57% (set 348). Held-out precision 5%, "twice chance" |
| 741/742/745 et al. | phonetic-sign shortlist | freedom score | **Failed** SL1-SL3 (set 12). N4 "withdrawn as evidence of sound spelling" (set 16, Linear B control) |
| stroke signs in foreign names | possibly phonetic | West Asian lines contain numerals in 14 of 18 (set 136) | "supports, weakly" |

## 3. West Asia, Meluhha, cuneiform, 'twins', 415-803-1, bilinguals, anchors

- **West Asian seals, first pass (N:P1 C5/C6).** The jar is doubled only on the round, unprovenanced seal ICIT 3889 = M77 9901 (467 550 1 740 740). Round and cylinder seals sit at the 95th surprisal percentile. The Kish square seal is typical; the Salut (Oman) square seal is atypical.
- **N:P5 §7.** 11 seals. 2 end in an ending (South Asia 55%, p = 0.016), 0 open with the heading (p = 0.075), 9 carry a numeral.
- **N:P15 §3 / PD §4.7 (`gulf.py`).** 20 intact objects. Endings on 11% of lines against 43% at home (Fisher p = 0.007). Heading 0/20. 84% of tokens are common home signs. 45% of sign pairs are attested at home (home texts 70%, shuffled 22%). The two West Asian texts ending in 740 are square seals from Kish and Gonur. [results/gulf.md] lists the sites: Karzakan 3, Ur 2, Altyn Depe, Hajar, Kish, Luristan, Qala'at al-Bahrain, Ra's al-Junayz, Shortughai, Susa, Tell Umma, Gonur, Salut, Saar, Janabiyah, Kalba, Dilmun. Commonest signs: 220, **91**, 55, 1, 2 (5 each).
- **Set 8 (Y).** Y1 bound pairs 5.6% against 12.7% (p = 0.06, fails). Y2 freer signs (p = 0.03, holds). Set 11 replicates with M77 freedom (p = 0.001). Set 12: SL1 fails (30% against 32%). Set 136: WA1 17% against 57%; WA6 6.52 bits/sign against ~5.4; WA7 reversed (numerals in 14 of 18). Set 168: "5 of 16 foreign stroke runs precede signs never counted at home". Set 170: foreign lines use rare signs 3×.
- **Laursen 2010 (N:P14 §4, P16 §4).** 29 Indus-inscribed Gulf-type seals; "only three carry sequences known in the Indus Valley". "the 'twins' sign begins 4 Bahrain texts: non-Indus names in Indus signs, a test bed rather than a key." **Not transcribed**: the seals are "given only as drawings (his Fig. 11)". *No sign ID is given for 'twins' in the three files.* In the corpus, ICIT **91** opens Luristan 91 840 413 831, Karzakan 91 31 455 220 and 91 32 1 33, and Kalba (91 alone), and sits inside Saar 55 220 91 1 93 31 [results/gulf.md]. That 91 is the 'twins' sign is my inference, not his statement.
- **415-803-1 sequences** [results/gulf.md, predict_test8.md]. Two West Asian cylinder seals: Ur "415 803 1 328 4 2" and Dilmun "415 803 1 717 354". Altyn Depe has "415 390". In set 291 (loop 116), "415 803", "415 803 1" and "803 1" came out as seal referent units for the **gaur**, but with FDR 43% they were not adopted. 803 is a leaf-in-oval sign (fish-class name slot, N:P4 §2). Fairservis keys 415 = *kiṟ-a* 'below/south' and 803 = *paṭu-nel(r)* 'setting sun, west'. The NOTES/PROGRESS/PAPER files themselves never discuss the 415 803 1 pair.
- **Meluhhan names.** Na-na-za (also na-na-sa3) and Sab-ma-ar / Samar appear on three Irisagrig/Urusagrig tablets of Šu-Suen 6 (Nisaba 15 371, CUSAS 40 1354 and 1582), "oil allotment of the men of Meluhha ... shepherds of bezoars". Source: Laursen and Steinkeller 2017: 83-84.
  - ORACC search (`meluhha_oracc.py`): 161 attestations in 121 texts. Everyone else is Sumerian/Akkadian-named (Ur-Lamma son of Meluhha, Ur-Igalim, Lu-sunzida, Ili-ahi, Elum-Meluh, envoy Utu-illat).
  - CDLI search (cdli.earth, transliteration 'me-luh', ATF export): 223 texts, 149 not in ORACC. The only people named are Šu-ilišu "translator of Meluhha" (seal CDLI 014339, Akkadian) and Dadi, "soldier of the Meluhha boat" (BIN 8 298).
  - Result: "Nanaza and Samar remain the only direct evidence." The 2-3 syllable length fits the 1-3-sign name slot (52% of 1,148 seals); with two names "this rules nothing in or out" (N:P7 §5).
- **Bilinguals.** "No partial bilingual exists: no object carries both Indus signs and a readable text (Ur U.7683 has cuneiform and no Indus signs; Šu-ilišu's seal is Akkadian)" (N:P14 §4). The only "language-free bilingual evidence" is text plus picture on the same tablet. Parpola's "pictorial bilingual" holds for 3 images (hare 12/12, archer 10/10, elephant 11/11; N:P2 §4).
- **Anchors.** Copper equations (§2) and their set-32 withdrawal. 347/460 provisional. The bench's B3 anchors (341, 749, 753, 777/778 plus 8 texts) score no key above chance: Yajnadevam 4/8 (shuffles 2.6), Parpola 2/8 (2.3), Fairservis 5/8 (5.4). On the 460-anchor texts every key is at chance. Yajnadevam's readings name the pictured animal 0 of 11 times.

## 4. Feasibility benchmarks (numbers)

- **Planted key (synthetic).** 96.5-98.7% against shuffles 85.9-89.5% (P8).
- **Fitted key by hill-climbing.** Reads 94.0% (Sanskrit), 93.1% (Dravidian) and 93.1% (Sumerian) of the real corpus (P8), so "a reading rate alone is no evidence".
- **Linear Elamite control** (`elamite_control.py`, P10). 168 lines, 2,520 signs, 246 variants keyed with 61 values; Hallock's Achaemenid lexicon (OCR).
  - Consonants only: 60.7% against 62.4% (156 of 200 shuffles as good).
  - Vowels kept: 25.7% against 19.6% (2 of 100) in the first check; rerun 25.7% against 19.2% (4/100), with consonants-only at 80/100.
- **Linear B control** (`linb_control.py`, P17). DAMOS, 4,988 lines; LSJ + Homeric, 136,872 forms.
  - Consonants: 32.7% against 29.4% (11/100). Vowels: 40.7% against 38.9% (27/100). With the Greek list adjusted to Linear B spelling: 12 and 41/100.
  - Verdict: the bench "cannot reliably recognise a correct decipherment".
- **Published keys, vowels kept** (P10).
  - Yajnadevam: Sanskrit 53.0% against 44.8% (10/100); Dravidian 70.4% against 61.2% (0/100). This is read as a CV-syllable artefact. Without his ending values: Sanskrit 42.6% against 43.9% (29/50), Dravidian 57.6% against 52.5% (2/50).
  - Fairservis: Dravidian 92.7% against 97.4% (97/100).
  - Parpola: 77.3% against 92.5% (100/100).
- **Character-LM key scorer** (`lmkey.py`, set 205). Ventris's key beats 100/100 shuffles on held-out lines with a Greek model; with a Sanskrit model, 9/100.
  - Published keys through this scorer (set 206): Fairservis 12/100, Yajnadevam 7/100, Parpola and Mahadevan worse than their shuffles, Kak only via 740 = *sa* (254/1000 without it).
- **Blind key fitting on Linear B** (set 207). Sanskrit fits best; Greek comes last (seed 1) or third (seed 2); 0 of 30 Ventris values recovered.
- **Substitution-phonetics** (set 179). Linear B p = 0.001. Fairservis and Yajnadevam pass on sample A only.
- **Rebus search over 503 CLICS languages** (set 181). No signal; Dravidian and Indo-Aryan both at the 44th percentile.
- **Fitted-key holdout** (`fit_holdout.py`, P13). 2,088 ICIT lines, 250 signs, 47 values, 20,000 steps; tested on 975 M77-only lines.
  - Held-out margins: DEDR 91.6/90.3 (1/100), Sanskrit 93.6/91.7 (0), Sumerian 85.0/81.5 (0), Munda 79.8/77.2 (2), Old Tamil 76.3/64.6 (0), Burushaski 78.8/69.7 (0).
  - A key fitted to shuffled training lines does not generalise (99/100). A planted Dravidian key does (95.3 against 93.3).
  - Margins track lexicon density.
- **Matched lexicons** (`matched_holdout.py`). 2,405 skeletons, 5 draws.
  - Synthetic Dravidian control: Old Tamil z 8.8 (wins 4/5), DEDR last (2.0).
  - Indus: Burushaski 6.2, Sumerian 6.1, Sanskrit 6.0, DEDR 5.2, Old Tamil 5.1, Munda 5.0. "Inconclusive."
- **Referent method controls.**
  - Linear B: 143 words qualify against a null of 2; recovers a-mo-ta ROTA and ko-wa MUL (sets 234-235).
  - Held-out precision: Linear B 95-96% against Indus 28-44% (set 310), later 5% (sets 340, 349).
  - Picture-vault control: 710 of 1,716 against a shuffle maximum of 22.
- **Power notes.**
  - Set 23 (Z): same-text tablets share a level 25% against 21% over 3,470 pairs. The 36- and 71-pair seal test "could not have seen it", so V's failure is "uninformative".
  - Set 57: "low power: 740 dominates".
  - Set 168: only 14 long names recur.
  - Baayen's P "underpowered (91 hapax heads)".
  - R4 rebus baseline: 15% strict to 68% loose.
  - Fish=star pun: 3 of 2,895 languages.
  - Restoration against M77 readings (sets 283-285, 314): 21/49 against a context baseline of 19; overall 29/75 against 23 ("narrowly").
  - SIGN task 39.7%/61.8%; WORD task 0%/3.4% (frequency baseline 0/1.3).
- **Prize target table (PR).** A winning entry needs 80-95% of tokens read as sense, about 70 common signs valued, and frozen values tested on new texts. Current: V 0.008%, U 0, P 0.

## 5. Data sources (for reproduction)

- **Lecture PDF**: old.harappa.com/script/indusscript.pdf. Cloudflare blocks plain curl; a browser user agent works. Not committed.
- **Corpus A**: github.com/yajnadevam/indus-website `population-script.sql` (GPL-3.0) → `build_corpus.py` → `data/corpus.tsv` (2,543 objects). The motif column comes from its ICONOGRAPHY table.
- **Corpus B (M77)**: github.com/joyboseroy/indus_decipher `data/m77_indusscript_real_corpus.csv` (MIT; a logged-in export of indusscript.in). Not copied into the repo. The additions are in `data/corpus_m77_added.tsv`.
- **Corpus F (fuller)**: "built into the JavaScript of indusscript.net". 4,578 objects (later 5,680 records); local only; `icit_full.py`. Use LINES_REVERSED = True (set 24).
- **CISI digitisation**: github.com/mayig/indus-valley-script-corpus (M-1..M-184) → `cisi.py`, `data/cisi_mayig.tsv`.
- **Books and scans**:
  - CISI vol. 1 scan (user-supplied, library no. 76884).
  - Parpola 1994 on archive.org, `decipheringtheindusscriptaskoparpolabookmarked_300_F`.
  - Fairservis 1992 Appendix A (archive.org page images) → `keys/fairservis1992*.tsv`.
  - Mahadevan 2003 *Early Tamil Epigraphy* (archive.org OCR, then page scans; `scratchpad/lang/ete_personal_names.tsv`).
  - Lüders 1912 (Internet Archive OCR).
  - Campbell's Santali dictionary (archive.org cu31924096339464); Hoffmann 1903, Bodding 1929, Phillips 1873 (archive.org).
  - Hemmy (Marshall 1931, Mackay 1938) and Vats 1940 weight tables, typed by hand.
- **Lexicons**:
  - Dravidian Database v1.1 (Zenodo 10.5281/zenodo.22215802).
  - Monier-Williams (Cologne csl-orig).
  - ORACC ePSD2 (CC0).
  - JAMBU (github.com/moli-mandala/data; Munda, plus Berger and Yoshioka for Burushaski).
  - Tamil Lexicon on DSAL.
  - Hallock 1969 (archive.org OCR).
  - Elamicon/OCLEI Linear Elamite corpus and sign table.
  - CLICS4; WALS; Grambank (`data/wals_profile.tsv`, `grambank_profile.tsv`).
- **Other comparison corpora**:
  - Proto-Elamite: SFU remap of the CDLI corpus.
  - DAMOS Linear B; LSJ + Homeric forms.
  - ORACC Ur III → `ur3_seals.py` → `data/ur3_seals.tsv`.
  - DHARMA tfa-* (CC BY 4.0).
  - Rajan and Sivanantham 2026 (Tamil Nadu graffiti).
  - Witzel 1999 (EJVS).
  - Kenoyer and Meadow 2010 (CISI 3.1).
  - Fuls 2022/2023 previews (user-supplied).
- **Keys**: Yajnadevam github.com/yajnadevam/lipi `xlits.csv` (not bundled: no licence). Parpola, Mahadevan and Kak keys are in `keys/`.
- **Caveat**: many inputs are "read from the scratchpad, not copied" or "not committed". Corpora B and F, the lexicons and the scans are not in the repo.

## 6. Open leads, and what he did not do

**Leads he names:**
- Outside evidence is the only way forward: "a bilingual, a secure cognate language, or archaeological context" (Loop end).
- Stroke signs used phonetically in foreign names (set 136).
- Freedom scores as a way to find phonetic signs (set 8). The shortlist built from them later failed.
- Better images for restoration and for the M-603/604 side A: CISI vol. 2/3 plates or museum photographs (set 255).
- CISI vol. 2 for H-396, H-568, H-598 and H-602.
- About 4,000 unused signs in the damaged texts (Correction 25 Sept).
- Parpola 1997/2003 readings.
- Better glyph data for compound analysis (set 137).

**What he did not do:**
- Did not transcribe Laursen's 29 Gulf seals.
- Did not build a graffiti-to-Indus sign mapping ("would be this project's guess").
- Did not test Witzel's substrate words (positive control failed).
- No Prakrit genitive list (EIAD unusable).
- Keys not usable or not online: Hunter 1934, the Soviet keys, Rao 1982, Jha and Rajaram 2000.
- Not read in full: Wells 2011/2015, Fuls 2013-2020, Mahadevan 1970/1986, Parpola 2008/2015. Mahadevan 2014 was read later (set 145).
- Not in either corpus: 4MSR/Binjor, Kotada Bhadli, Sanauli, newer Rakhigarhi seals.
- "rebus search not run" in the gate list (PR tier 2).
- In set 115, the published authors' views were "summarised from memory".
- profile.json was not updated for passes 6-8.
- The site page and the in-browser bench are withheld.

## Contradictions and stale statements across files

- **C1.** PD abstract and §7 give "197 predictions ... 73 held and 124 failed". That is the tally at set 21. NOTES ends at 1581 held / 1492 failed.
- **C2.** PD §4.9 says the copper-tablet equations "stand", and PR tier 1 still counts "4 copper-tablet signs" (V 0.008%). NOTES set 32 withdrew 341, 749/778 and 753 as text anchors. NOTES "Next steps" §2 still calls them "the firmest meaning anchors".
- **C3.** PD §4.8: "27% at the first guess (55% within five)" mixes two models from N:P15: neighbour-at-edge is 27%/41%, commonest-neighbour 24%/55%.
- **C4.** PD §4.9 and §7 present 6+fish as the one enriched star name. Sets 138, 139 and 182 find '2+fish' commonest in ICIT, M77 and Parpola's own CISI transcription, where "'6 + fish' does not occur" (M-1..M-184). Set 115: the six/seven-fish pattern "does not appear". (Enrichment over base rate and raw frequency are different measures, but the paper does not reconcile them.)
- **C5.** PD §5 and the abstract: "only Dravidian passes both grammar tests". Later, sets 185-189, 197-198 and 141 find name structure nearer Prakrit on some measures, "does not discriminate languages", and order typology "not separating" Dravidian from Indo-Aryan. PR keeps L at 4 families open, with "no candidate beats the decoys".
- **C6.** The PD bench section never mentions the char-LM scorer that passes the Linear B gate (set 205), or the published keys' failure through it (set 206).
- **C7.** Tier 2 counts drift: "3 of 6" (PR table), "1 of 3 methods" (PR target table), "C 2 of 4" (loop 30), "2 of 5 methods" (loop 32).
- **C8.** PD §2 and §8 treat the fuller corpus as 4,578 objects whose provenance must be cleared, and N:P2 §5 / Next steps §1 say the full ICIT needs Fuls's account. The final NOTES Correction says F (5,680 records) "matches or exceeds" Fuls 2022, and the earlier notes "are withdrawn".
- **C9.** The tier-1 referent figure has been revised many times; the PR cell carries the full history. The figure most often quoted elsewhere (2.28%/2.29%) is superseded: the inflated 13.64% fell to 1.09% after the mould-copy counting flaw (set 337), and the line now stands at 4.57%.
- **C10.** West Asian sample sizes differ across passes: 11 seals (P5), 20 objects or 18 lines (P15, sets 8 and 136). The ending rates also differ: 11% against 43% (740/520 only) versus 17% against 57% (with the closers included).
