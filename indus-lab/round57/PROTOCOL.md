# Round 57 — Bhaty 2024: do Indus seals read as Bronze Age place names under her key?

Pre-registered 22 October 2026, before any code for this round was written. No Indus reading under the modified key has been computed. The three gazetteer files in this folder are frozen with this commit.

## Claim under test
Rupa Bhaty, "Tracing Magan and Its People via Indus Seals", *Pratnakīrti* 5(2), 2024, pp. 1–14 (and the 2025 ResearchGate paper and 2026 book that extend it). She takes Yajnadevam's 2024 Brahmi/Sanskrit sign values as given, changes one value, and reads recurring sign groups as place and ruler names of the Bronze Age Gulf, Mesopotamia, Anatolia and India: Moka/Mokan/Mokani = Makran/Magan, Hattusa, Umma, Susa, Isin, Nuzi, Hamazi, Daman, Revakhanda, Beroea, Manium, Maništušu. She does not claim to read every seal; she reinterprets a subset (48 "Moka" entries, 63 "Mana" entries) of Yajnadevam's readings.

**The one change, identified before this protocol.** Her Table 1 rereads the glyph Yajnadevam calls Brahmi *o* but uses as *ā*. Checked against her listed seals (H-278/281/871–873, M-369, H-12, H-20, K-10, H-1938) in `raw/inscriptions.csv`, her "m-(o)-ka-an" is the sequence 255-435-690-740 (reading order), so the glyph is **435** (allograph **436**), labelled `a` in `round46-brahmi-coverage/expanded-map.json`. The Bhaty key **K_B** = that map with 435 and 436 set to `o`. The cluster 255-435/436-690 occurs in 24 distinct core text types (her 48 counts repeated objects).

## Hypotheses
- **H1 (her claim):** under K_B, Indus texts contain Bronze Age place names more often than a wrong key with the same values would produce.
- **H0:** they contain them as often as structure-preserving shuffles of K_B do; the place names are what any similar key finds with her matching freedom.

## Data
- Corpus: `round47/run47.py:load_corpus()`, texts with every sign labelled in the map (expected 1,934 types, 8,720 tokens), reading order.
- **Real gazetteer G_BA:** (a) every ePSD2 lemma tagged GN (geographic name) or SN (settlement name) in `../round51/epsd2_lemmas.tsv` (Oracc ePSD2, CC0; the Sumerian/Akkadian record of places known to Mesopotamia, including Magan, Meluhha, Dilmun, Umma, Susa, Isin); plus (b) every name in `bhaty_places.tsv` (her own reported hits and the Gulf names her argument rests on). Including (b) favours her claim; it is done deliberately.
- **Decoy gazetteer G_SCR (primary decoy):** each skeleton of G_BA with its consonants randomly permuted (seed 57501; a permutation identical to the original is redrawn up to 20 times). Exactly matched in count, length and letter frequency; no place names.
- **Decoy gazetteer G_FIN (secondary):** `finnish_places.txt`, 116 Finnish municipality names. An impossible region.
- **Positive-control gazetteer G_LB:** `linearb_places.tsv`, 41 place names attested in Linear B, in Linear B spelling.

## Matching rule (the freedom granted, identical for every key and gazetteer)
1. Collapse every name and every reading to lower-case ASCII: strip diacritics; š ś ṣ z x → s; ŋ → g; ḫ h → k; ṭ θ → t; f → p; w → v; q → k; y → j; drop digits and hyphens.
2. Consonant skeleton: delete vowels a e i o u.
3. Merge voicing and liquids, as Bhaty's own equations require (Magan = Makran = Moka; Hattusa = Hattum): g → k, d → t, b → p, j → c, l → r; then collapse runs of the same consonant to one (Umma → m, Hattusa → ts).
4. Only names whose merged skeleton has **at least 3 consonants** are scored (primary). 2-consonant skeletons are reported as a secondary count; they match too much by chance to carry a verdict.
5. A name matches a text if its merged skeleton is a contiguous substring of the text's merged reading skeleton. Reading skeleton for Indus: `run47.read_c` (labels concatenated, `an`→`n`, `as`→`s`, vowels dropped) then step 3. For Linear B: the true syllable values concatenated, then steps 2–3.

This is more generous than exact spelling and less generous than her practice (she also crosses language boundaries, permits Prakrit and pidgin forms and non-contiguous readings). Vowels play no role, so her one change (435 → o) does not alter any skeleton; the test is of the consonant key she adopted plus her toponym-matching.

## Statistic
**T(K, G)** = number of distinct (text, name-skeleton) pairs in which the skeleton matches, over all texts, using the unique skeletons of G with ≥ 3 consonants.

## Null
1,000 structure-preserving shuffles of the key's labels within frequency bins of 20 signs (`run47.freq_bins`, `run47.shuffle_key`), seeds 57201–58200. Reported as p_upper = (1 + #{T_shuf ≥ T_real}) / 1001 and pct = #{T_shuf < T_real} / 1000. z = (T_real − mean) / sd.

## Positive control (must pass or the Indus verdict is METHOD-FAIL)
Linear B at Indus density, built exactly as round 47's PC2 (`run47.lb_build` on the held-out half `halfB`, seed 47301 split, target sign IDs = tokens ÷ Indus tokens-per-sign, 1–3 words per pseudo-text, homophones), with the true key. Pass if, for G_LB: pct ≥ 0.99 and z ≥ 3; and for the scrambled G_LB (same construction, seed 57502): pct < 0.95. If the control's own texts contain fewer than 10 G_LB matches under the true key, the control is uninformative and the verdict is METHOD-FAIL.

## Negative controls
G_SCR and G_FIN scored under K_B and the same 1,000 shuffles.

## Decision rules (Indus, applied only if the positive control passes)
- **SUPPORT:** G_BA pct ≥ 0.99 and z ≥ 3; G_SCR pct < 0.95; G_FIN pct < 0.95; and T_real(G_BA) per name exceeds T_real(G_SCR) per name.
- **ARTEFACT:** G_BA pct ≥ 0.95 but G_SCR or G_FIN also ≥ 0.95, or G_BA per-name rate ≤ G_SCR per-name rate.
- **NULL:** G_BA pct < 0.95.
- **MIXED:** anything else.

## Secondary analyses (reported, not verdict-bearing)
1. Round 47's language test on K_B unchanged: trigram LMs (Sanskrit, Finnish, Basque, Proto-Dravidian; matched lexicon draws 47101–47105), Bhaty vowel rule = `run47.read_v` with `o` treated as a vowel, 1,000 shuffles seeds 57201–58200. Reported with round 47's verdict words for comparison with Yajnadevam's −0.35.
2. Her specific names: for each name in `bhaty_places.tsv` with ≥ 3 skeleton consonants, the number of texts matched under K_B and the share of shuffles that match at least as many.
3. 2-consonant skeletons (Moka = mk, Umma = m excluded, Susa = s excluded): same statistic, for description.
4. The Moka cluster 255-435-690: count under K_B; for each shuffle, the count of texts whose skeleton contains `mk` (how often a wrong key yields "Moka/Maka" somewhere).

## Stopping rule
One run with the seeds above. No change to gazetteers, matching rule or thresholds after any Indus number is seen; any change before results goes in an Amendment below with its reason. Runtime estimate: a few minutes (gazetteer test) plus ~8 minutes (secondary LM test), stdlib Python.
