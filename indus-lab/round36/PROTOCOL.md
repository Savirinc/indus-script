# Round 36 — Rebus tournament (pre-registered)

Written 12 October 2026, after the blind pictograph tags were frozen (`indus_pictograph_tags.tsv`) and before any scoring code was run. Two candidate word forms (Proto-Dravidian and Sanskrit "fish"/"man") were glimpsed while checking file formats, after the tags were frozen.

## Idea
- In pictorial scripts that acquired sound values (Egyptian, Sumerian, Chinese, Maya), a picture sign comes to carry the SOUND of its name in the scribes' language (the rebus principle).
- Each candidate language therefore determines a sound key for the tagged picture signs with ZERO fitted parameters: sign → that language's word for the pictured concept.
- If the script used rebus and language L is right, signs whose L-words sound alike should be used in similar contexts (homophones are interchangeable) more than chance predicts.

## Inputs (frozen)
- **Indus:**
  - corpus = 1,936 core text types (round 30 `F.TRAIN`; reading order; no 000);
  - tags = 24 signs (7 object signs: jar, fish, man, arrow, bird, leaf×2; 17 numeral signs, 1–8).
- **Languages** (`rebus_data/lang_*.tsv`; PRIMARY = first listed form per concept, column `form_ipa_or_simplified`):
  - pdr (Proto-Dravidian), san (Sanskrit), pmu (Proto-Munda), pkher (Proto-Kherwarian), sat (Santali), unr (Mundari), srb (Sora), khr (Kharia), bsk (Burushaski), elx (Elamite), sux (Sumerian);
  - controls: eus (Basque), fin (Finnish), jpn (Japanese);
  - Chinese: och (Old Chinese, for reference).
- **Chinese control:**
  - corpus = `chinese_corpus_trad.txt` (1,562 classical texts, one character = one sign);
  - TRUE language = the Middle Chinese reading (`mc_baxter_phonoml`, first value) of each tagged character itself.

## Score S1 (one primary score)
- **Pairs:** all pairs of tagged signs with different concepts, excluding numeral–numeral pairs.
- **Phonetic similarity** sim_L(a,b) = 1 − normalised Levenshtein distance between the simplified forms, lower-cased, non-letters removed.
- **Distributional similarity** D(a,b) = cosine similarity of [left-neighbour counts ‖ right-neighbour counts] over the corpus, with text boundaries as a neighbour symbol.
- **S1(L)** = Spearman ρ between sim_L and D over the pairs.
- **Null:** 2,000 permutations of L's words among the tagged concepts (numerals shuffled among numerals, objects among objects), seed 36000. Percentile = share of null ρ below the observed ρ.
- Signs whose concept has no word in L are dropped for that language. A language with fewer than 6 usable signs is reported but not ranked.

## Chinese control (runs FIRST; decides whether Indus runs)
- **C-full:** all Chinese pictographs available in `chinese_pictographs.tsv` that occur ≥5 times in the corpus, full corpus.
- **C-indus:** only the concepts in the Indus tag set (jar, fish, man, arrow, bird, leaf, numerals 1–8), with the corpus subsampled to Indus size (lines drawn at random, seed 36100, until ≥8,726 characters).
- **PASS** for a setting: the true Middle Chinese key has percentile ≥ 0.95 AND ranks first of all languages by percentile.

## Decision
- **C-indus passes →** run the Indus tournament with the identical code. A language "leads" if its percentile is ≥ 0.95, it ranks first, and every control language (eus, fin, jpn) is < 0.95. Otherwise: no language identified.
- **C-indus fails but C-full passes →** the method works in principle but has no power with as few identifiable pictures as the Indus script offers. Do NOT run Indus as evidence; report how many tagged signs were needed.
- **C-full fails →** S1 cannot detect rebus even in Chinese; the method is rejected.
