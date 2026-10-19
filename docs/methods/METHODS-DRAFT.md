# No published key to the Indus script survives a shuffle test that the Linear B key passes: a pre-registered, controlled audit of decipherment claims and of the structural statistics used to support them

**Draft 0.2, 19 October 2026. Complete draft for the owner's review; not for circulation. Author: Arham Partap Jain (Savir Platforms Private Limited, India). Analyses were designed and run with an AI assistant (Claude, Anthropic); every protocol, script, seed and result is in the public repository `Savirinc/indus-script`, and Section 8 states what the assistant did.**

Text licence: CC BY 4.0. Code licence: MIT. Third-party data retain their own licences (see `THIRD_PARTY_NOTICES.md` in the repository).

## Abstract

Claims to have deciphered the Indus script appear every few years, most recently a cryptanalytic Sanskrit reading (Yajnadevam 2024) that reports every inscription as readable. We ask a question that any proposed key can be made to answer: do the readings it produces look more like its claimed language than the readings produced by random re-assignments of the same values to the same signs? We build a scorer (character trigram language models on a common 21-letter alphabet), show that it recognises the true Linear B key against its own shuffles by 6 to 13 standard deviations even when Linear B is degraded to the Indus corpus's sparsity of about 15 tokens per sign, and then apply it, unchanged, to every published Indus key available in machine-readable form: Yajnadevam 2024 (Sanskrit, 714 codes), Fairservis 1992 (Dravidian, 95 signs), Rao 1982 (Indo-Aryan, 56 signs transcribed from his figures), Parpola 1994, Kak 1988 and Mahadevan 2014. No key separates from its shuffles (|z| < 1 for the three large keys); impossible languages (Finnish, Basque) fit the same labels as well or better; and a sixty-thousand-step refit of each author's own labels produces "readings" far more language-like than the author's assignment, in whichever language is requested. Three further pre-registered tests close adjacent routes: a Dravidian rebus-anchor result that had reached p = 0.07 is reproduced by Finnish anchors at p = 0.016; a shape-resemblance test of the Indus–Brahmi hypothesis fails its positive controls (it cannot recover Phoenician → Aramaic from fonts), so look-alike tables carry no evidential weight either way; and the words Mesopotamian scribes used for Meluhhan goods, the only Harappan-era vocabulary in a readable script, show no family signal although the same instrument recovers the Mitanni Indo-Aryan words from an 11-word sample. We then turn the same discipline on the structural statistics that have been used to argue about the script's type without sounds. Against twelve real corpora cut to Indus size and text length (Greek, Hebrew, Cherokee, Ur III Sumerian, Old Babylonian and Old Assyrian letters, cuneiform seal legends, Egyptian, Shang oracle bone, Uruk IV and III proto-cuneiform, proto-Elamite, the Shijing), five pre-registered instruments fail their positive controls: inventory and entropy statistics cannot separate phonetic scripts from archaic non-phonetic accounting (the Rao et al. 2009 statistic does not discriminate on real controls); two unsupervised word segmenters cannot tell a one-sign-per-word corpus from a multi-sign-word corpus at 8,726 tokens; and combinatorial freedom does not pick out syllabograms where they are known. Two findings survive every control: the Indus corpus is not alphabet- or syllabary-like at matched size and is nearest the oracle-bone inscriptions by a factor of four to five, and only 3.5% of Indus texts repeat a sign, against 13–34% for every phonetic corpus except oracle bone. We relate all of this to Shannon's unicity distance: with 582 signs, texts averaging 4.5 signs that are mostly unique, and no bilingual, the corpus sits below the effective unicity distance of every decipherment method yet proposed. The practical conclusion is a checklist. A decipherment claim should be accompanied by (1) a frozen, automated reading pipeline, (2) its own shuffle null, (3) impossible-language controls given identical freedom, and (4) a positive control on a known script at matched sparsity. None of the published claims meets any of the four, and the controls assembled here are released as a reusable bench.

## 1. Introduction

The Indus script is attested on about 4,000 objects from 2600–1900 BCE, mostly stamp seals, sealings and small tablets, with inscriptions averaging five signs and never exceeding seventeen on a single face. It has been "deciphered" dozens of times since Waddell (1925): as Sumerian, as Dravidian (Heras 1953; the Soviet group under Knorozov 1965; the Finnish group under Parpola 1994; Fairservis 1992; Mahadevan 2014), as Indo-Aryan or Sanskrit (Rao 1982; Kak 1988; Bonta 2023; Yajnadevam 2024), as Munda, as Egyptian, and as not language at all (Farmer, Sproat and Witzel 2004). Possehl (1996b) catalogued the first sixty years of proposals; none is accepted, and the newest are not accepted either. The reason is not that the field is unreasonable. It is that every reading has been argued the same way: a key is assigned, the inscriptions are read, the readings are "meaningful", and the meaningfulness is presented as the proof.

That form of argument has a known failure mode. Given a short corpus, a large inventory of signs, and a dictionary, almost any assignment of sounds yields strings that can be glossed. Ventris did not persuade the field by producing Greek words; he persuaded it because Kober's grid had been built from the texts' own structure before any sound was assigned, because the sound values then predicted the readings of tablets not used in building the grid, and because the Pylos tripod tablet matched its own pictograms (Kober 1948; Ventris and Chadwick 1953). The decipherment was a prediction that could have failed, and did not. No Indus decipherment has been offered in that form.

This paper does two things. First, it asks of each published key the simplest question that could say no: are its readings more like its language than the readings produced by shuffling its own values among its own signs? The question requires no bilingual, no theory of the language, and no judgement about what a reading means; it only requires that a real key be distinguishable from a wrong one, which we verify on Linear B before applying it to the Indus material. Second, it applies the same discipline, a pre-registered protocol with a positive control on known scripts and a negative control with impossible languages, to the structural statistics (inventory size, entropy, segmentation, combinatorial freedom) that have been used to argue about the script's nature without sounds. Most of those instruments fail their controls, and the failures are reported in full, because an instrument that has never been seen to fail has never been tested.

What the paper does not do should be stated as plainly. It proposes no sign value. It does not decide whether the Harappan language was Dravidian, Indo-Aryan, Munda or something unattested; its evidence bears on whether anyone has demonstrated sign values, and the answer is no. It does not decide whether the signs encode language; it shows that the statistics commonly cited for and against that proposition cannot decide it either.

All of the work was carried out in public under a fixed set of rules (Section 7): the hypothesis, statistic, null, controls, thresholds, seeds and stopping rule of each round were committed to a public repository before the code was written, and every round ended in the verdict word its own protocol defined, including the five rounds whose verdict was that the method had failed.

## 2. Data

### 2.1 Indus corpus
The Indus Website export in Bourdeau's lineage (ICIT catalogue numbering via the `lipi` repository; GPL-3), 5,679 records. We keep core-region seals and tablets with known reading direction and no damaged sign, deduplicate exact repeats (a seal and its impressions are one text), and obtain 1,936 text types, 8,726 sign tokens and 582 sign types: 15.0 tokens per sign, median 2 tokens per sign; 340 of 582 signs occur three times or fewer; 15% of texts are two signs long; the longest is 13 signs. Rounds 47 and 49 drop two texts whose signs the Yajnadevam key does not label (1,934 texts, 8,720 tokens, 581 signs). The SHA-256 of the input file is recorded in the repository. Sign IDs are catalogue identifiers and carry no values. The upstream export includes one author's Sanskrit readings as columns; they are never used.

### 2.2 Keys
Yajnadevam 2024 (`lipi` repository, commit fc8813a5, 714 codes and the author's `xlitize()` inherent-vowel rule); Fairservis 1992 Appendix A, Parpola 1994 Fig. 15.2, Kak 1988 Table 4, Mahadevan 1998/2014, as transcribed by Bourdeau (`cyphersolver`, commit 04457698) with his confidence tiers; Rao 1982 Figs 4, 4A and 8–13C, transcribed here from the public scan with figure references and confidence labels. Bonta 2023 (second edition) could not be obtained in machine-readable or open form and is untested, not refuted.

### 2.3 Lexicons
Monier-Williams Sanskrit (SLP1); Tamil forms from the Dravidian Etymological Dictionary database and the Dravidian Database v1.1 (Merriam and Fuls 2026, CC BY 4.0; Proto-Dravidian reconstructions after Krishnamurti 2003); Finnish (Kotus word list); Basque (Xuxen); Greek (NeuroDecipher Linear B–Greek cognate file, Luo, Cao and Barzilay 2019); Old Indo-Aryan (CDIAL, Turner 1966, via JAMBU); Munda (JAMBU); Burushaski (Berger); concept-aligned Finnish and Basque from the Intercontinental Dictionary Series; Sumerian lemmas with guide words (ePSD2, Oracc, CC0). All are pinned by commit or hash.

### 2.4 Control corpora for the structural rounds (52–54)
Twelve corpora of known type, each reduced to a sequence of sign tokens by rules fixed before the Indus corpus was scored, each sampled into "Indus-shaped" subsets (windows drawn from the control's own units so as to reproduce the Indus text-length distribution and total of 8,726 tokens; a window never crosses a unit boundary):

| Code | Corpus | Type | Source (pinned) | Licence |
|---|---|---|---|---|
| GRK | Homer, Iliad and Odyssey, letters | alphabet | Perseus | CC BY-SA 4.0 |
| HEB | Pentateuch, Westminster Leningrad Codex, letters | abjad | openscriptures/morphhb | public domain |
| CHR | Cherokee New Testament, syllabary characters | syllabary | christos-c/bible-corpus | CC0 |
| SUX | Ur III administrative texts, cuneiform signs | logosyllabic | CDLI (cdli-gh/data) via Oracc sign list | CC BY / CC0 |
| OBL | Old Babylonian letters, cuneiform signs | logosyllabic | CDLI | CC BY |
| OAL | Old Assyrian letters, cuneiform signs | logosyllabic | CDLI | CC BY |
| SEAL | Ur III–Old Babylonian cylinder-seal legends | logosyllabic, seal genre | CDLI | CC BY |
| EGY | Egyptian tomb inscriptions, Gardiner codes | logo-consonantal | AES (Schweitzer) | CC BY-SA 4.0 |
| OBI | Shang oracle-bone inscriptions, graphs | logographic with rebus | OBIMD (KLOBIP) | CC BY 4.0 |
| U4, U3 | Uruk IV and Uruk III proto-cuneiform, ZATU signs | archaic accounting | CDLI | CC BY |
| PE | Proto-Elamite, Dahl signs | archaic accounting | CDLI | CC BY |
| CHN | Shijing, characters | one sign per word (reference) | chinese-poetry | MIT |

Cuneiform transliterations were mapped from ATF values to sign names through the Oracc Global Sign List, so that homophonous values of one sign are one token and determinatives and logograms count as the signs they are. Word boundaries for the segmentation rounds (53, 53b) are the ATF spacing; syllabic versus logographic flags for round 54 follow ATF case and marking conventions. No openly licensed corpus of running Linear B tablet text exists (DĀMOS and LiBER are non-commercial or no-export), so Linear B serves as the positive control only in the key-scoring rounds, where the NeuroDecipher word list suffices.

### 2.5 Glyphs for the shape test
Noto Sans fonts for 25 scripts (OFL, google/fonts commit 47d54ca1) and the `lipi` Indus sign font (codepoint = U+E000 + catalogue code).

## 3. Methods

### 3.1 The reading-fit statistic
A key K maps sign IDs to labels. A text is read by concatenating labels in reading order (for Yajnadevam, additionally with the author's own inherent-vowel rule, so that the strings scored are the author's own display strings). Labels and lexicons are reduced to one 21-letter alphabet (vowels a i u e o; consonants k g c j t d n p b m y r l v s), which removes diacritics, aspiration and length and so favours every key by making its output look more like every language. For each candidate language L a character trigram model with add-0.1 smoothing is trained on a random draw of the lexicon matched in size to the smallest lexicon in the comparison (five draws, averaged); the statistic S_L(K) is the mean bits per character of the readings under that model. Lower is more language-like. The implementation is standard-library Python.

### 3.2 The null: structure-preserving shuffles
Sign IDs are ranked by corpus frequency and grouped into bins of 20 consecutive signs (10 for partial keys). The key's labels are permuted among the signs within each bin, 1,000 times. This preserves the key's label multiset, the frequency profile of the output (how often each label appears), and every positional property of the texts; it destroys only the author's specific assignment of label to sign. z = (mean_null − S_real) / sd_null; the percentile is the share of shuffles with S ≥ S_real. A genuine key must sit far in the tail of its own shuffles. An unrestricted permutation null is also reported.

### 3.3 Positive control: Linear B degraded to Indus conditions
Linear B words from the NeuroDecipher cognate file are re-encoded with homophonic sign IDs so that tokens per sign ID match the Indus corpus (130 IDs, 1,737 tokens, 13.4 tokens per sign; and a 365-ID, 4.8 tokens-per-sign version), grouped into pseudo-texts of 1–3 words without dividers, and scored with the true key against Greek and four wrong languages, the Greek model being trained on words held out from the cipher. For partial keys the control is degraded further by dropping sign IDs until token coverage matches the key under test (0.28, 0.39, 0.57, 0.60, 0.78), three random subsets per level, with readings taken over covered runs of at least two signs. Pass criteria are fixed in advance: percentile ≥ 0.99, z ≥ 3, and a margin of at least 2 standard deviations over every wrong language, on at least two of three subsets.

### 3.4 Negative controls
Impossible languages (Finnish, Basque) and a cross-family language (Sanskrit for Dravidian keys, Tamil for Sanskrit keys) are scored on the same readings against the same null. Matched-budget fitted controls: the author's own label multiset is re-assigned to the same signs by simulated annealing (60,000 swap moves, temperature 3.0 → 0.05, three chains) to maximise each language in turn, and the fitted key is scored against the same shuffle null. The budget is seconds of computation, far less than any author spent, so it favours the author.

### 3.5 Verdict rules, pre-registered per round
METHOD-FAIL if the positive control fails; NOT TESTABLE if the key has fewer than 25 attested signs or its coverage level fails the control; NULL if the home-language percentile is below 0.95; ARTEFACT if an impossible language also passes or the margin over it is under 2 sd; SUPPORT if percentile ≥ 0.99, z ≥ 3 and margin ≥ 2 sd over every other language, with the control passing; MIXED otherwise.

### 3.6 Anchor-rebus test and its decoy (rounds 41–45)
A different route to the same question. Instead of a full key, a small set of signs is fixed to Proto-Dravidian words by the rebus arguments in the literature (fish = *mīn, man = *āḷ, arrow = *ampu, the numerals), the remaining signs are fitted on 80% of the inscriptions under a Proto-Dravidian trigram model by simulated annealing, and the fitted key is scored by its log-likelihood on the held-out 20%, with near-duplicate texts removed. The null is the same procedure with the anchor values shuffled among the anchor signs (15, then 60 shuffles), the positive control is Linear B with 17 true values under the same procedure, and the design is replicated on ten fresh splits with 24 anchors. The decoy round (45) repeats the 24-anchor, ten-split design with the anchor signs fixed to Finnish and to Basque words of the same meanings, under the rule that a pooled p ≤ 0.15 for either decoy makes the Dravidian result an ARTEFACT.

### 3.7 Shape-resemblance test (round 48)
Every corpus-attested Indus sign glyph and 1,061 letters of 25 scripts are rendered from fonts, skeletonised and compared under four descriptors (chamfer distance on skeletons at two resolutions, shape context, and their sum) with the dihedral group of flips and rotations allowed for every script equally. The statistic is the enrichment of a script among the nearest neighbours of the query glyphs relative to its share of the pool, under a complexity-stratified label-permutation null. The method had first to recover known descent: Phoenician → Aramaic and Old North Arabian, Greek → Lycian, Carian and Old Italic, Old Italic → its Italic relatives, Imperial Aramaic → Kharoshthi and Brahmi. A descriptor passes if three of four queries rank a known relative first with at least two relatives at p < 0.05. The Indus run was executed once before the control criterion was tightened; those numbers are reported as previously seen and carry no weight.

### 3.8 Loanword attribution (round 51)
For each target word with a gloss, the best normalised-Levenshtein match among lexicon words of related meaning in each family (Proto-Dravidian, Old Indo-Aryan, Munda, Burushaski; Finnish and Basque as decoys) is found, and the mean similarity of five shape-matched Sumerian background words (ePSD2 lemmas) is subtracted; the family score A is the mean gain over the background, bootstrapped over targets. Two gates must pass before the Meluhhan words are scored: the Mitanni Indo-Aryan words preserved in cuneiform must attribute to Indo-Aryan, and Turner's Dravidian loans in Sanskrit must attribute to Dravidian. A family is attributable if it ranks first and beats both decoys in 95% of resamples. The candidate set (eleven words proposed as Meluhhan by Parpola, Southworth, Witzel and others: abba, mesu, magilum, sinda/sindu, zaza, haluppu, gisimmar, ili/ellu/ulu) was frozen before scoring.

### 3.9 Structural instruments without sounds (rounds 52–54)
All five rounds share the Indus-shaped sampling of Section 2.4 (300, 100, 30 or 50 samples per control corpus), a seed, and a positive control on which the Indus verdict is conditional.

**Writing-system signature (52, 52b).** Eight features invariant under relabelling of signs: inventory V, hapax share, share of tokens in the ten commonest signs, unigram entropy H1, the ratio of within-text conditional entropy to unigram entropy H2/H1, Heaps' slope, the share of texts in which some sign repeats, and the share of adjacent doubled signs. Round 52 placed each held-out corpus in a 99% Mahalanobis region of its class; round 52b replaced that with nearest-corpus assignment standardised by the between-corpus spread, in three classes with at least three corpora each (small-inventory: GRK, HEB, CHR; large-inventory phonetic: SUX, OBL, OAL, SEAL, EGY, OBI; archaic accounting: U4, U3, PE). Positive control: leave-one-corpus-out classification, every corpus at least 50% correct, or no Indus verdict.

**Word segmentation (53, 53b).** Can texts be cut into recurrent multi-sign words, and does the one-sign-per-word Shijing separate from the multi-sign-word Akkadian letters on the result? Round 53 used a pointwise-mutual-information boundary rule with its threshold calibrated on the four cuneiform corpora that have gold word boundaries; round 53b used a Dirichlet-process unigram word model (Goldwater, Griffiths and Johnson 2009; Gibbs sampling over boundaries, α = 20, p# = 0.5, 150 annealed sweeps). Positive control: boundary F1 at least 0.15 above random boundaries placed at the same rate, on three of four gold corpora. Statistics: mean segment length S and share of units containing a multi-sign segment M; verdict words MULTI-SIGN-WORDS, SINGLE-SIGN-WORDS, BETWEEN.

**Syllabic core by combinatorial freedom (54).** The premise of the Kober method for a logosyllabic script: syllabograms combine freely, word-signs sit in slots. For each sign with at least ten tokens, F = the number of distinct left and right neighbours observed, divided by its mean under 30 within-text permutations. Positive control: F must separate syllabograms from logograms in the Old Babylonian and Old Assyrian letters, where the ATF marks which is which, with AUC ≥ 0.75. Negative control: the share of signs above a freedom threshold ("core share") must be at least 0.20 higher in Akkadian than in the Shijing and the oracle-bone corpus, which have no syllabic core.

## 4. Results

### 4.1 The scorer sees a real key at Indus sparsity (round 47)
| Control | Sign IDs | Tokens/ID | Greek z | Best wrong-language z | Pass |
|---|---:|---:|---:|---:|---|
| Linear B, bijective | 70 | 24.8 | 6.0 | 1.7 (Basque) | yes |
| Linear B at Indus density | 130 | 13.4 | 11.5 | 5.7 (Basque) | yes |
| Linear B at round-32 geometry | 365 | 4.8 | 13.5 | 6.1 (Basque) | yes |

The true key also beats its shuffles under wrong languages, because open-syllable strings are language-like in general; that is why the rules demand a cross-language margin and not merely "beats shuffles".

### 4.2 Published keys (rounds 47, 49)
| Key | Language | Signs | Coverage | Home z | Percentile | Best decoy z | Verdict |
|---|---|---:|---:|---:|---:|---:|---|
| Yajnadevam 2024, author's vowel rule | Sanskrit | 581 | 1.00 | −0.35 | 0.29 | Finnish −0.34 | NULL |
| Fairservis 1992 (sure, likely) | Tamil | 95 | 0.60 | 0.20 | 0.61 | Finnish 0.84 | NULL |
| Rao 1982 (sure, likely) | Sanskrit | 56 | 0.57 | −0.70 | 0.26 | Finnish 2.06 | NULL |
| Parpola 1994 | Tamil | 27 | 0.28 | – | – | – | NOT TESTABLE (control fails at this coverage) |
| Kak 1988 | Sanskrit | 7 | 0.16 | – | – | – | NOT TESTABLE (< 25 signs) |
| Mahadevan 2014 | Tamil | 5 | 0.14 | – | – | – | NOT TESTABLE (< 25 signs) |

For the three testable keys, no analysis variant (consonant skeleton, full lexicons, unrestricted null) puts the home language above the 61st percentile. Where anything moves it is Finnish: Rao's key reads more like Finnish (percentile 0.985) than like Sanskrit. The Linear B control at each key's coverage: 0.57 and 0.60 pass (3 of 3 and 2 of 3 subsets); 0.28 and 0.39 fail (1 of 3), so keys covering a quarter of the tokens cannot be judged by this method at this corpus size, a statement about power and not about those authors.

A diagnostic makes the numbers concrete. The inscription M-304, which Yajnadevam reads as a prayer, is under his own rule the string `aaasasanmaanaa`: 6.26 bits per character as Sanskrit, 3.61 as Finnish. Fairservis's commonest covered readings are *ancippu*, *tunkunelailmarupirar*, *nerakuticembalaan*; Rao's are *aea*, *aa*, *as*, *sss*. Kak's seven values read the commonest runs as *sata*, *para*, *rasa*, *vasa*; Mahadevan's five as *markol*, *maranru*. Four- or five-letter strings in a 21-letter alphabet are words in most languages, and no statistic can separate a correct five-sign key from a wrong one on this corpus.

### 4.3 Refits of the authors' own labels (z of the refit under the same null)
| Key | → Sanskrit | → Tamil | → Finnish | → Basque |
|---|---:|---:|---:|---:|
| Yajnadevam's 581 labels | 5.5 | 10.5 (Proto-Dravidian 5.7) | 5.4 | 9.8 |
| Fairservis's 95 values | 6.8 | 4.7 | 3.2 | 4.4 |
| Rao's 56 values | 4.8 | 5.4 | 3.6 | 4.8 |

Fifteen seconds of annealing over each author's own inventory of values produces a key that reads six standard deviations more like Sanskrit than Yajnadevam's assignment does, and does the same for Finnish and Basque. Whatever selected the published assignments, it was not the phonotactics of the claimed language. A refit of Yajnadevam's labels to Sanskrit reaches 2.87 bits per character, below the 2.99 bits per character of held-out real Sanskrit under the same model: a wrong key outscores real language, which is the operational definition of a corpus below the unicity distance (Section 5.1).

### 4.4 Dravidian anchors and the Finnish decoy (rounds 41–45)
| Anchor set (24 signs, 10 splits, 60 shuffles) | Mean percentile | Pooled p |
|---|---:|---:|
| Proto-Dravidian rebus anchors (round 43) | 0.95 | 0.066 |
| Finnish words as anchors (round 45) | 0.97 | 0.016 |
| Basque words as anchors (round 45) | 0.31 | 0.72 |

The Linear B control passed in every round (true values beat all 20 shuffles on all 10 splits). The Dravidian anchors sat in the top 8% of their own reassignments on every split, which rounds 41–43 had reported as suggestive. Finnish anchors did better. By the pre-registered rule the result is an ARTEFACT: the method rewards some property of the anchor words, plausibly word shape, that has nothing to do with being the right language. Basque's failure shows the artefact is not universal, and the mechanism was not identified.

### 4.5 Shape resemblance (round 48)
| Descriptor | Phoenician | Greek | Old Italic | Imperial Aramaic | Passes |
|---|---|---|---|---|---:|
| Skeleton chamfer 40×40 | relative first, 1 sig. | relative first, 1 sig. | fail | relative first, 1 sig. | 0/4 |
| Uniform-stroke chamfer 64×64 | relative first, 0 sig. | relative first, 2 sig. | fail | relative first, 1 sig. | 1/4 |
| Shape context | fail | relative first, 2 sig. | fail | relative first, 0 sig. | 1/4 |
| Sum | fail | relative first, 1 sig. | fail | fail | 0/4 |

METHOD-FAIL. The matcher is not blind (it repeatedly finds Old North Arabian for Phoenician, Lycian for Greek, Kharoshthi for Aramaic) but with 22–32 query letters it lacks the power to make two relatives significant at once, and typographic style competes with descent. The symmetric consequence is the result: an instrument that cannot see Phoenician → Aramaic in fonts cannot see Indus → Brahmi either, and eyeballed look-alike tables between 47 simple letters and 700 signs are unquantified at best. Descriptively, in the run seen before the criterion was fixed, Brahmi ranked 20th of 25 scripts as nearest shape to the Indus signs, and for 17 of the 20 sign–letter pairs in Yajnadevam's Table 7 the author's letter ranked at a median of 594th of 1,061 pool letters.

### 4.6 Meluhhan vocabulary (round 51)
Both gates pass: the Mitanni Indo-Aryan words attribute to Indo-Aryan in 100% of resamples (A = +0.39), Turner's Dravidian loans to Proto-Dravidian in 99% (A = +0.15). So an 11-word sample suffices to see a clear signal.

| Family | A | 95% CI | P(rank 1) | P(beats both decoys) |
|---|---:|---|---:|---:|
| Finnish (decoy) | +0.28 | +0.19 to +0.38 | 0.70 | – |
| Proto-Dravidian | +0.23 | +0.15 to +0.31 | 0.21 | 0.24 |
| Basque (decoy) | +0.22 | +0.16 to +0.28 | 0.03 | – |
| Old Indo-Aryan | +0.19 | +0.10 to +0.28 | 0.07 | 0.09 |
| Burushaski, Munda | ≈ 0 | | 0.00 | 0.00 |

NO FAMILY ATTRIBUTABLE. The only meaningful Dravidian hit is the sesame etymon (*ellu* ~ Proto-Dravidian *el*), counted three times at modest similarity, which Bedigian (1985), Southworth (2005) and Witzel (1999) already debated. Possehl's (1996a) catalogue, obtained after the first run, turned out to contain no loanword list at all but Sumerian and Akkadian terms qualified "of Meluhha"; four of the eleven frozen candidates are native Mesopotamian words that no source actually derives from Meluhha. The one word an ancient lexical list itself calls Meluhhan, *šamru* "thorn tree" (Glassner 1996), comes from a first-millennium source when Meluhha usually meant Nubia; it matches Sanskrit *śamī* and Proto-Dravidian "thorn" equally at 0.60, a similarity one random Sumerian plant word in five achieves against each lexicon. The entire Harappan-era vocabulary in a readable script that anyone has called Meluhhan is six or seven short words, and they decide nothing.

### 4.7 The structural instruments and their controls (rounds 52–54)

**Writing-system signature.** Round 52 recovered the alphabet class perfectly when held out (Greek and Hebrew 300 of 300) and failed completely on the large-inventory split (Sumerian and Egyptian called logographic, oracle bone called logosyllabic, 0 of 300 each): METHOD-FAIL, with the lesson that a class region estimated from resampling one corpus has no between-system variance in it. Round 52b, with three classes of at least three corpora and a nearest-corpus rule, passed nine of twelve leave-one-out tests at 100% and failed three (Cherokee → large-inventory; oracle bone → archaic, 7% correct; Old Assyrian 73%): METHOD-FAIL again. The feature table explains why.

| Corpus | V | hapax | top10 | H1 | H2/H1 | Heaps | repeat | double |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Indus** | **582** | **0.368** | **0.332** | **6.92** | **0.494** | **0.457** | **0.035** | **0.001** |
| GRK | 24 | 0 | 0.741 | 4.09 | 0.851 | 0.011 | 0.340 | 0.016 |
| HEB | 22 | 0 | 0.757 | 4.08 | 0.926 | 0.001 | 0.338 | 0.025 |
| CHR | 81 | 0.017 | 0.410 | 5.62 | 0.734 | 0.053 | 0.139 | 0.007 |
| SUX | 423 | 0.220 | 0.241 | 7.31 | 0.477 | 0.290 | 0.139 | 0.010 |
| OBL | 250 | 0.250 | 0.327 | 6.43 | 0.634 | 0.266 | 0.134 | 0.006 |
| OAL | 174 | 0.144 | 0.400 | 6.04 | 0.685 | 0.186 | 0.177 | 0.011 |
| SEAL | 304 | 0.206 | 0.448 | 6.27 | 0.508 | 0.279 | 0.139 | 0.020 |
| EGY | 411 | 0.277 | 0.436 | 6.39 | 0.562 | 0.379 | 0.276 | 0.047 |
| OBI | 669 | 0.368 | 0.323 | 7.23 | 0.461 | 0.448 | 0.030 | 0.001 |
| U4 | 726 | 0.253 | 0.312 | 7.57 | 0.505 | 0.413 | 0.240 | 0.005 |
| U3 | 857 | 0.361 | 0.276 | 7.82 | 0.512 | 0.456 | 0.178 | 0.009 |
| PE | 905 | 0.358 | 0.317 | 7.53 | 0.469 | 0.508 | 0.224 | 0.004 |
| CHN | 1,621 | 0.372 | 0.179 | 9.18 | 0.313 | 0.549 | 0.189 | 0.024 |

Means over 300 Indus-shaped samples per corpus (8,726 tokens, Indus text lengths). Three things are robust because they do not depend on the failed distinction. (i) The Indus corpus is far from every small-inventory script on every feature (standardised distances 4.4–7.1, against 0.4–2.7 to large-inventory corpora; inside the small-inventory range on 0 of 8 features). This is the inventory-size argument of Parpola and Mahadevan stated with corpus size and text length held equal, on every feature and not only on V, and it holds on the five features that do not depend on how allographs are split. (ii) The Indus corpus is nearest the Shang oracle-bone inscriptions (distance 0.44) by a factor of four to five over the next corpus (Uruk III 2.05, Ur III 2.11), stable under every leave-one-out; the resemblance is specific (inventory 582 against 669, hapax 0.368 against 0.368, H2/H1 0.494 against 0.461, repetition 0.035 against 0.030). (iii) The within-text repetition rate is the Indus signature: 3.5% of Indus texts and 3.0% of oracle-bone texts repeat a sign, against 13–34% for every other corpus; random texts with the same signs and lengths would repeat one in 17% of cases. Merging the seventeen stroke numerals into one sign raises the Indus rate to 17.7%: about one text in seven carries two different stroke numerals, so the strokes form a sub-system of their own.

What the failure teaches is the paper's second result. The ratio H2/H1 is 0.477 for Ur III Sumerian, 0.508 for seal legends, 0.562 for Egyptian; and 0.512 for Uruk III proto-cuneiform, 0.505 for Uruk IV, 0.469 for proto-Elamite. At matched size and text length the phonetic scripts and the largely non-phonetic accounting systems overlap completely on conditional entropy, on unigram entropy and on Heaps' slope. Rao et al. (2009) argued from conditional entropy that the Indus signs encode language; Sproat (2014) objected that the statistic had not been shown to separate language from non-language on real systems. Tested against the real systems it should have been tested against, it does not separate them. The question of whether the signs encode language cannot be settled by this family of statistics, in either direction.

**Word segmentation.**

| Gold corpus | PMI margin over random (53) | Dirichlet-process margin (53b) |
|---|---:|---:|
| Seal legends | 0.180 pass | 0.196 pass |
| Ur III lines | 0.047 | 0.089 |
| Old Babylonian letters | 0.072 | 0.149 (0.0009 short) |
| Old Assyrian letters | 0.027 | 0.149 (0.0007 short) |

Both METHOD-FAIL under the pre-registered rule (three of four at 0.15); the second by less than a thousandth on two corpora, which was reported as the distance and not corrected by moving the bar or re-running with other seeds. The deeper finding is that the verdict rule could not have worked even with a passing control: the Shijing, where nearly every character is a word, segments to a mean length of 1.495 under the lexicon model and 1.50 under PMI, while the Akkadian letters, whose words average 2.5–2.9 signs, segment to 1.48 and 1.19–1.28. Two different segmenters recover recurrence and formula, which a literary text has more of than a letter, and not word structure. At 8,726 tokens, unsupervised segmentation cannot tell a one-sign-per-word corpus from a multi-sign-word corpus. Descriptively, the Indus corpus segments to S = 1.42 with 73% of texts containing a multi-sign segment; shuffling sign order within texts collapses this to 1.07 and 24%, so the cohesion is real sign order; and the induced lexicon is the set of frequent sequences already known from bigram work (861-002, 817-002, 820-002, sign-plus-jar endings, the 920-060-741 formula). The model rediscovers the formulae and reveals nothing behind them.

**Combinatorial freedom.** The AUC separating known syllabograms from known logograms is 0.455 on the Old Babylonian letters and 0.651 on the Old Assyrian; the Shijing's one-sign-per-word characters combine more freely (core share 0.855) than Akkadian syllabograms (0.768, 0.791). METHOD-FAIL on both controls. The intuition is wrong on real data for an identifiable reason: syllabograms are constrained inside words by the phonotactics and morphology of the language, so their neighbour sets are far from random, while a word-sign in a monosyllabic language is followed by whatever word comes next. Freedom measures where in the hierarchy a sign sits, inside a word or between words, not whether it is phonetic. The Indus value (core share 0.594, between oracle bone 0.340 and Egyptian 0.654) is uninterpretable for the question asked; the per-sign table is kept as the input for a distributional grid, since slot restriction is what it does measure, and the most restricted signs (817, 090 "man", 520 "arrow", 400, 861, 820) are the known terminal and near-terminal signs.

## 5. Discussion

### 5.1 Why every key reads, and why that proves nothing
Shannon (1949) defined the unicity distance of a cipher as the length of ciphertext at which the correct key becomes the only one consistent with the plaintext's redundancy: U ≈ H(K) / D, where H(K) is the key's information in bits and D the redundancy per symbol of the language. Below U, many keys fit, and the true one cannot be identified from the text alone. The Indus problem is worse than a cipher in three ways. The key is large: a bijection of 582 signs onto even a fixed inventory of values carries log2(582!) ≈ 4,500 bits before any freedom in the values themselves is counted, against a ciphertext of 8,726 symbols. The redundancy is low: the texts are, on every structural statistic, short records of names and titles, and names are the least redundant text a language produces, as anyone who has tried to guess a surname from its first three letters knows. And the decipherer has freedoms a cryptanalyst lacks: the alphabet is chosen by the decipherer, allographs are split or merged by the decipherer, and a dictionary of 186,000 Sanskrit headwords or a Tamil pun on fish and star stands ready to turn any short string into something.

Section 4.3 is the operational demonstration. A 15-second refit of Yajnadevam's own labels produces strings that score as more Sanskrit than real Sanskrit; refits to Finnish and Basque produce strings as Finnish and Basque as his are Sanskrit. When a wrong key outscores real language, the text is below U by definition. Round 32 showed the same thing from the other direction: at Indus sparsity a solver given the true Linear B lexicon, the true inventory of values and a purely phonetic script recovers under 10% of tokens, and a wrong key outscores the true one. Roughly 40 externally fixed sign values, or a corpus two or three times larger, would bring the problem across the threshold under those kind assumptions.

The manual glossing stage completes the mechanism. Our test scores a key plus a mechanical reading rule, and that is what makes it a test: the same strings are produced for Finnish as for Sanskrit. Every published decipherment adds a stage after the key, in which the reader segments, applies sandhi, permits regex alternatives and chooses among dictionary senses. Round 47 shows that the Sanskrit in Yajnadevam's readings must enter at that stage, because it is not in the key's output. The same inscription has been glossed as a Shiva epithet by one author and as a priestly calendar title by another from the same signs. That is not two readings of one text; it is two demonstrations that the stage after the key will produce meaning from anything.

### 5.2 What the corpus does support
A test that says no to every key is only useful if it would say yes to something, and the structural rounds show what. Sign order is real: a bigram model trained on Harappa predicts Mohenjo-daro texts not in its training set, and the reverse, beating 200 of 200 position-preserving shuffles in every condition (round 27), and shuffling sign order within texts collapses every cohesion statistic in rounds 52–53b. Round seals of Gulf type found at Ur, in Bahrain and in Luristan are foreign in sign order (mean percentile 0.916 against length-matched native seals, p < 5 × 10⁻⁵; rounds 30–31), robust to every disputed reading and to removal of the one likely pseudo-inscription, which is what seals cut abroad for foreign names or by imitators would look like. The system is not an alphabet or a syllabary, by a control that passed, and its statistics sit with short formulaic records in large-inventory systems, closest to the oracle-bone divination records. Texts almost never use a sign twice, which any key that assigns syllables or letters must explain, and which a key assigning word-signs (names, titles) does not have to. The jar sign ends 28% of texts and is fixed per text, behaving as a suffix (round 34 audit). None of this fixes a sound or a meaning, and all of it is what a real key would have to reproduce.

### 5.3 What would change the picture
Anchors. On the order of 40 independently fixed values is round 32's estimate of what statistics would need to carry the rest; today there are none. The routes to an anchor have been checked. A near-bilingual, an Indus-sign seal impressed on a dated cuneiform tablet, does not exist in any published catalogue (Gadd 1932; Hallo and Buchanan 1965; Collon 1996; the full CDLI dump): the three Gulf-seal impressions on tablets are of the textless Dilmun type (round 50). The Meluhhan loanword route is closed on the published record (Section 4.6). Attested Dilmun and Meluhhan personal names are too few (27) to anchor the Gulf seals (round 35). What remains is new material: a text over 20 signs from Ganweriwala, Rakhigarhi or Dholavira; new Meluhhan names from Irisagrig or Girsu tablets; the unread chapters on Ur sealings in Mitchell (1986) and Laursen and Steinkeller (2017). The corpus itself can be made more tractable without new text by rigorous allograph merging, which raises tokens per sign; that is a palaeographic task and it is checkable.

### 5.4 What the failed instruments teach
Five pre-registered structural rounds, five instrument failures on real controls. Each failure is a finding about the instrument. Inventory and entropy statistics measure record type and inventory size, not system type: a corpus of short formulaic records in a large inventory looks the same whether it is phonetic (oracle bone) or accounting (Uruk III), and arguments from H2/H1 in either direction (Rao et al. 2009; Farmer, Sproat and Witzel 2004) should be retired. Unsupervised segmentation at this corpus size recovers recurrence, which is a property of genre and formula as much as of word structure, so "the Indus texts segment into words" is not evidence that they contain words. Combinatorial freedom measures slot position, not sign function. And thresholds set in advance can fall on a knife edge, as 53b's did by 0.001; the right response is to report the distance and not to move the bar, since a bar moved after the fact is no bar. A replication with other seeds is legitimate only as a new round that says in advance that it is a replication.

The controls themselves are the reusable product. Twelve corpora of known type, reduced to sign tokens by fixed rules, with gold word boundaries and syllabic/logographic flags where the writing system supplies them, sampled to Indus size and text length, are released with the repository. Any future structural claim about the Indus script, from any direction, can be run against them in an afternoon; if the claim's statistic does not separate the controls, the claim is not about the Indus script.

### 5.5 A checklist for future claims
1. Freeze the reading pipeline, as code, before looking at results. No manual glossing stage between key and claim; if segmentation, sandhi or dictionary choice is part of the method, it is part of the code and Finnish gets the same freedom.
2. Report the key's position in its own structure-preserving shuffle distribution.
3. Give an impossible language identical freedom, and report it.
4. Pass a known-script positive control at matched tokens per sign and matched coverage.
5. Reproduce the corpus's structural signature: a text almost never repeats a sign; the numerals are a sub-system; the jar sign is a suffix.
6. Publish the key as a machine-readable table against a named sign catalogue.

None of the published claims meets the first four. The repository provides the harness for the second, third and fourth, and the instructions for running a new key through it take twenty minutes.

## 6. Limitations
Character trigram models underuse a language's redundancy; a stronger scorer (lexical, morphological) would raise the discrimination available to a genuine key and should be tried, but would need its own controls, and the Linear B results show the present scorer already has large margins to spare. Partial keys are scored only where they apply and only above 57% coverage; Parpola's and Mahadevan's values are untested, not refuted. Fonts stand in for epigraphic shapes in round 48; the test should be rerun with traced Ashokan Brahmi and traced Indus signs under a rank-based statistic, and the previously seen numbers declared. The control corpora are transliterations and modern editions, mapped to signs by rules that themselves embody editorial decisions (Oracc sign names, Gardiner codes, OBIMD graph identities); the Cherokee corpus is printed, not excavated; the Shijing is a received text; Linear B could not be used as a structural control for want of an open corpus. Bonta 2023 awaits a copy. Nothing here bears on which language the Indus people spoke; it bears on whether anyone has demonstrated sign values, and on which statistics can and cannot speak to the script's nature at this corpus size.

## 7. Reproducibility
Every round has a `PROTOCOL.md` committed before its code, with hypothesis, statistic, null, positive and negative controls, thresholds, seeds, trial counts and stopping rule; amendments are dated, reasoned and precede results; and a `REPORT.md` ends in the protocol's verdict word. Inputs are pinned by commit or SHA-256, and `MANIFEST.json` lists the hash of every tracked file. Rounds 47, 49, 52–54 run on standard-library Python (8 min, 20 min, and 1–6 min each); round 48 needs Pillow, numpy and scipy; round 51 needs numpy and rapidfuzz. The twelve control corpora are regenerated from their pinned sources by `fetch_controls.sh` and the extractors in rounds 52–54; extracts under open licences are committed. The history of the repository is the audit trail: the commit that registered each protocol precedes the commit that ran it.

## 8. Declaration of AI assistance
The analyses in rounds 27–54 were designed and executed with an AI assistant (Claude, Anthropic) operating under written rules in the repository: pre-register before code, positive control first, impossible-language negative control, report failures, and no agreement between models counted as evidence. The assistant wrote protocols, code and reports at the author's direction; the author set the questions, chose the keys and corpora, approved each protocol before its run, and reviewed each verdict. Every artefact the assistant produced is committed, with its seeds, so that the reader can check what was done rather than take either party's word for it. Where the assistant proposed a statistic that then failed its control, the failure is reported under the protocol's verdict word (rounds 36–38, 48, 52–54).

## Acknowledgements and data sources
Bourdeau's Indus Website export and `cyphersolver` transcriptions of published keys; Yajnadevam's `lipi` repository, from which the corpus export and sign font derive; Tejesh Raut's explorer; the Dravidian Database (Merriam and Fuls 2026) and DravLex (Kolipakam et al. 2018); the Intercontinental Dictionary Series (lexibank); JAMBU for CDIAL and Munda data; Kotus; Xuxen; NeuroDecipher (Luo, Cao and Barzilay 2019); ePSD2 and the Oracc Global Sign List; the Cuneiform Digital Library Initiative; the Ancient Egyptian Sentences corpus (Schweitzer); the Oracle Bone Inscription Multimodal Dataset (KLOBIP); Perseus; openscriptures; the Cherokee New Testament corpus; the chinese-poetry project; Noto fonts; and the public scans on the Internet Archive that made Rao 1982, Possehl 1996, Collon 1996 and Glassner 1996 readable. Copyrighted scans were used for reading only and are not redistributed.

## References
Bedigian, D. 1985. Is še-giš-ì sesame or flax? *Bulletin on Sumerian Agriculture* 2: 159–178.

Bonta, S. 2023. *[second edition of the author's Indus decipherment, Academia.edu id 120435855; not obtained]*.

Collon, D. 1996. Mesopotamia and the Indus: the evidence of the seals. In J. Reade (ed.), *The Indian Ocean in Antiquity*, 209–225. London: Kegan Paul / British Museum.

Fairservis, W. A. 1992. *The Harappan Civilization and Its Writing: A Model for the Decipherment of the Indus Script*. Leiden: Brill.

Farmer, S., Sproat, R. and Witzel, M. 2004. The collapse of the Indus-script thesis: the myth of a literate Harappan civilization. *Electronic Journal of Vedic Studies* 11(2): 19–57.

Gadd, C. J. 1932. Seals of ancient Indian style found at Ur. *Proceedings of the British Academy* 18: 191–210.

Glassner, J.-J. 1996. Dilmun, Magan and Meluhha: some observations on language, toponymy, anthroponymy and theonymy. In J. Reade (ed.), *The Indian Ocean in Antiquity*, 235–248. London: Kegan Paul / British Museum.

Goldwater, S., Griffiths, T. L. and Johnson, M. 2009. A Bayesian framework for word segmentation: exploring the effects of context. *Cognition* 112(1): 21–54.

Hallo, W. W. and Buchanan, B. 1965. A "Persian Gulf" seal on an Old Babylonian mercantile agreement. In *Studies in Honor of Benno Landsberger* (Assyriological Studies 16), 199–209. Chicago: Oriental Institute.

Heras, H. 1953. *Studies in Proto-Indo-Mediterranean Culture*, vol. 1. Bombay: Indian Historical Research Institute.

Kak, S. 1988. A frequency analysis of the Indus script. *Cryptologia* 12(3): 129–143.

Knorozov, Y. V. (ed.) 1965. *Predvaritel'noe soobshchenie ob issledovanii protoindiyskikh tekstov*. Moscow: Institute of Ethnography.

Kober, A. E. 1948. The Minoan scripts: fact and theory. *American Journal of Archaeology* 52(1): 82–103.

Kolipakam, V., Jordan, F. M., Dunn, M., Greenhill, S. J., Bouckaert, R., Gray, R. D. and Verkerk, A. 2018. A Bayesian phylogenetic study of the Dravidian language family. *Royal Society Open Science* 5: 171504.

Krishnamurti, B. 2003. *The Dravidian Languages*. Cambridge: Cambridge University Press.

Kuiper, F. B. J. 1991. *Aryans in the Rigveda*. Amsterdam: Rodopi.

Laursen, S. T. 2010. The westward transmission of Indus Valley sealing technology: origin and development of the "Gulf Type" seal and other administrative technologies in Early Dilmun, c. 2100–2000 BC. *Arabian Archaeology and Epigraphy* 21(2): 96–134.

Laursen, S. T. and Steinkeller, P. 2017. *Babylonia, the Gulf Region, and the Indus: Archaeological and Textual Evidence for Contact in the Third and Early Second Millennia BC*. Winona Lake: Eisenbrauns.

Luo, J., Cao, Y. and Barzilay, R. 2019. Neural decipherment via minimum-cost flow: from Ugaritic to Linear B. *Proceedings of ACL 2019*, 3146–3155.

Mahadevan, I. 1977. *The Indus Script: Texts, Concordance and Tables*. Memoirs of the Archaeological Survey of India 77. New Delhi.

Mahadevan, I. 2014. Dravidian proof of the Indus script via the Rig Veda: a case study. *Bulletin of the Indus Research Centre* 4. Chennai: Roja Muthiah Research Library.

Merriam, N. and Fuls, A. 2026. Dravidian Database v1.1. Zenodo, doi:10.5281/zenodo.22215802.

Mitchell, T. C. 1986. Indus and Gulf type seals from Ur. In S. H. A. Al Khalifa and M. Rice (eds), *Bahrain through the Ages: the Archaeology*, 278–285. London: KPI.

Parpola, A. 1994. *Deciphering the Indus Script*. Cambridge: Cambridge University Press.

Possehl, G. L. 1996a. Meluhha. In J. Reade (ed.), *The Indian Ocean in Antiquity*, 133–208. London: Kegan Paul / British Museum.

Possehl, G. L. 1996b. *Indus Age: The Writing System*. Philadelphia: University of Pennsylvania Press.

Rao, R. P. N., Yadav, N., Vahia, M. N., Joglekar, H., Adhikari, R. and Mahadevan, I. 2009. Entropic evidence for linguistic structure in the Indus script. *Science* 324(5931): 1165.

Rao, S. R. 1982. *The Decipherment of the Indus Script*. Bombay: Asia Publishing House.

Shannon, C. E. 1949. Communication theory of secrecy systems. *Bell System Technical Journal* 28(4): 656–715.

Southworth, F. C. 2005. *Linguistic Archaeology of South Asia*. London: RoutledgeCurzon.

Sproat, R. 2014. A statistical comparison of written language and nonlinguistic symbol systems. *Language* 90(2): 457–481.

Turner, R. L. 1966. *A Comparative Dictionary of the Indo-Aryan Languages*. London: Oxford University Press.

Ventris, M. and Chadwick, J. 1953. Evidence for Greek dialect in the Mycenaean archives. *Journal of Hellenic Studies* 73: 84–103.

Waddell, L. A. 1925. *The Indo-Sumerian Seals Deciphered*. London: Luzac.

Wells, B. K. 2011. *Epigraphic Approaches to Indus Writing*. Oxford: Oxbow.

Witzel, M. 1999. Substrate languages in Old Indo-Aryan (Rgvedic, Middle and Late Vedic). *Electronic Journal of Vedic Studies* 5(1): 1–67.

Yajnadevam (Bharath Rao). 2024. A cryptanalytic decipherment of the Indus script. Preprint, 13 November 2024; key and corpus in the `lipi` repository, commit fc8813a5.
