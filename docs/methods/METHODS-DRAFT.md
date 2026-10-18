# No published key to the Indus script survives a shuffle test that the Linear B key passes: a pre-registered, controlled audit of decipherment claims

**Draft 0.1, 18 October 2026. Not for circulation. Author: Arham Partap Jain (Savir Platforms). Analyses were designed and run with an AI assistant (Claude); every protocol, script, seed and result is in the public repository `Savirinc/indus-script`.**

Text licence: CC BY 4.0. Code licence: MIT. Third-party data retain their own licences (see `THIRD_PARTY_NOTICES.md`).

## Abstract

Claims to have deciphered the Indus script appear every few years, most recently a cryptanalytic Sanskrit reading (2024) that reports all inscriptions as readable. We ask a question that any proposed key can be made to answer: do the readings it produces look more like its claimed language than the readings produced by random re-assignments of the same values to the same signs? We build a scorer (character trigram language models on a common alphabet), show that it recognises the true Linear B key against its own shuffles by 6 to 11 standard deviations even when Linear B is degraded to the Indus corpus's sparsity of about 15 tokens per sign, and then apply it, unchanged, to every published Indus key available in machine-readable form: Yajnadevam 2024 (Sanskrit, 714 codes), Fairservis 1992 (Dravidian, 95 signs), Rao 1982 (Indo-Aryan, 56 signs transcribed from his figures), Parpola 1994, Kak 1988 and Mahadevan 2014. No key separates from its shuffles (|z| < 1 for the three large keys); impossible languages (Finnish, Basque) fit the same labels as well or better; and a sixty-thousand-step refit of each author's own labels produces "readings" far more language-like than the author's assignment, in whichever language is requested. Three further pre-registered tests close adjacent routes: a Dravidian rebus-anchor result that had reached p = 0.06 is reproduced by Finnish anchors at p = 0.016; a shape-resemblance test of the Indus–Brahmi hypothesis fails its positive controls (it cannot recover Phoenician→Aramaic from fonts), so look-alike tables carry no evidential weight either way; and the words Mesopotamian scribes used for Meluhhan goods, the only Harappan-era vocabulary in a readable script, show no family signal although the same instrument recovers the Mitanni Indo-Aryan words from an 11-word sample. We relate all of this to Shannon's unicity distance: with 582 signs, texts averaging 4.5 signs that are mostly unique, and no bilingual, the corpus sits below the effective unicity distance of every decipherment method yet proposed. The practical conclusion is a checklist. A decipherment claim should be accompanied by (1) a frozen, automated reading pipeline, (2) its own shuffle null, (3) impossible-language controls given identical freedom, and (4) a positive control on a known script at matched sparsity. None of the published claims meets any of the four.

## 1. Introduction

[To write. Points: history of claims (Heras, Soviet team, Parpola/Finnish, Fairservis, Rao, Kak, Mahadevan, Yajnadevam, Bonta); Possehl 1996 counted dozens; Farmer–Sproat–Witzel 2004 and the response; why "it reads" is not evidence; Ventris's grid and the Pylos tripod tablet as the standard of proof; what this paper does and does not claim (no sign value is proposed; Dravidian vs Indo-Aryan is not decided).]

## 2. Data

- **Indus corpus.** Indus Website export (Bourdeau lineage, GPL-3), 5,679 records; core-region seals and tablets with known direction, no damaged sign, deduplicated to **1,934 text types, 8,720 sign tokens, 582 sign types**, 15.0 tokens per sign, median 2 tokens per sign; 340 of 582 signs occur three times or fewer; 15% of texts are two signs long. SHA-256 of the input file is recorded.
- **Keys.** Yajnadevam 2024 (`lipi` repository, commit fc8813a5, 714 codes and the author's `xlitize()` vowel rule); Fairservis 1992 Appendix A, Parpola 1994 Fig. 15.2, Kak 1988 Table 4, Mahadevan 1998/2014 (transcriptions by Bourdeau, `cyphersolver` commit 04457698); Rao 1982 Figs 4, 4A, 8–13C, transcribed here with figure references and confidence labels. Bonta 2023 could not be obtained.
- **Lexicons.** Monier-Williams Sanskrit (SLP1), Tamil forms from the Dravidian Etymological Dictionary database (CC BY 4.0), Proto-Dravidian reconstructions (Dravidian DB v1.1), Finnish (Kotus word list), Basque (Xuxen), Greek (NeuroDecipher Linear B–Greek cognate file), Old Indo-Aryan (CDIAL via JAMBU), Munda (JAMBU), Burushaski (Berger), IDS concept-aligned Finnish and Basque, Sumerian lemmas with guide words (ePSD2, CC0). All pinned by commit or hash.
- **Scripts for the shape test.** Noto Sans fonts for 25 scripts (OFL, google/fonts commit 47d54ca1); the lipi Indus sign font (codepoint = U+E000 + catalogue code).

## 3. Methods

### 3.1 The reading-fit statistic
A key K maps sign IDs to labels. A text is read by concatenating labels in reading order (for Yajnadevam, additionally with the author's own inherent-vowel rule). Labels and lexicons are reduced to one 21-letter alphabet. For each candidate language L a character trigram model with add-0.1 smoothing is trained on a matched-size random draw of the lexicon (five draws, averaged); the statistic S_L(K) is bits per character of the readings. Lower is more language-like.

### 3.2 The null: structure-preserving shuffles
Sign IDs are ranked by corpus frequency and grouped into bins of 20 (10 for partial keys). The key's labels are permuted within bins, 1,000 times. This preserves the key's label multiset, the signs' frequency profile and all positional structure of the texts; it destroys only the author's specific assignment. z = (mean_null − S_real)/sd_null; the percentile is the share of shuffles with S ≥ S_real. A genuine key must sit far in the tail of its own shuffles.

### 3.3 Positive control: Linear B degraded to Indus conditions
Following round 32's benchmark, Linear B words (NeuroDecipher cognate file) are re-encoded with homophonic sign IDs so that tokens per sign ID match the Indus corpus (130 IDs, 1,737 tokens) and grouped into pseudo-texts of 1–3 words; the true key is scored against Greek and against four wrong languages. For partial keys the control is degraded further by dropping sign IDs until token coverage matches the key (0.28, 0.39, 0.57, 0.60, 0.78), three subsets per level. Pass criteria are fixed in advance (percentile ≥ 0.99, z ≥ 3, margin ≥ 2 over every wrong language).

### 3.4 Negative controls
Impossible languages (Finnish, Basque) and a cross-family language (Sanskrit for Dravidian keys, Tamil for Sanskrit keys) are scored on the same readings. Matched-budget fitted controls: the author's own label multiset is re-assigned to the same signs by simulated annealing (60,000 swap moves, T 3.0→0.05, three chains) to maximise each language in turn, and the result is scored against the same null.

### 3.5 Verdict rules (pre-registered per round)
METHOD-FAIL if the positive control fails; NOT TESTABLE if the key has fewer than 25 attested signs or its coverage level fails the control; NULL if home-language percentile < 0.95; ARTEFACT if an impossible language also passes or the margin is < 2 sd; SUPPORT if percentile ≥ 0.99, z ≥ 3 and margin ≥ 2 over every other language; MIXED otherwise.

### 3.6 Anchor-rebus test and its decoy (rounds 41–45)
[Summarise: 17 then 24 Dravidian rebus anchors predicting held-out inscriptions vs 100 shuffled anchor sets; 10 fresh splits; then the same with Finnish and Basque words as anchors.]

### 3.7 Shape-resemblance test (round 48)
Every Indus sign glyph and 1,061 letters of 25 scripts rendered, skeletonised, compared by chamfer distance (and three other descriptors) with dihedral freedom; statistic = enrichment of a script among nearest neighbours relative to its pool share, complexity-stratified label-permutation null; positive controls Phoenician, Greek, Old Italic, Imperial Aramaic with their known relatives.

### 3.8 Loanword attribution (round 51)
Round 39's sound-and-meaning instrument: for each target word with gloss, best normalised-Levenshtein match among lexicon words of related meaning in each family, minus the mean of five shape-matched background words (Sumerian lemmas); bootstrap over targets; gates on Mitanni Indo-Aryan words (must attribute to Indo-Aryan) and on Turner's Dravidian loans in Sanskrit (must attribute to Dravidian).

## 4. Results

### 4.1 The scorer sees a real key at Indus sparsity
| Control | IDs | tokens/ID | Greek z | best wrong-language z |
|---|---:|---:|---:|---:|
| Linear B, bijective | 70 | 25 | 6.0 | 1.7 |
| Linear B at Indus density | 130 | 13 | 11.5 | 5.7 |
| Linear B at 60% coverage (3 subsets) | ~82 | – | 4.9 / 6.0 / 6.9 | 3.0 / 2.2 / 2.8 |
| Linear B at 28% coverage (3 subsets) | ~42 | – | 3.9 / 3.2 / 4.9 | 2.7 / 2.2 / 1.4 (fails margin) |

### 4.2 Published keys
| Key | Language | Signs | Coverage | Home z | Percentile | Best decoy z | Verdict |
|---|---|---:|---:|---:|---:|---:|---|
| Yajnadevam 2024, author's vowel rule | Sanskrit | 581 | 1.00 | −0.35 | 0.29 | Finnish −0.34 | NULL |
| Fairservis 1992 | Tamil | 95 | 0.60 | 0.20 | 0.61 | Finnish 0.84 | NULL |
| Rao 1982 | Sanskrit | 56 | 0.57 | −0.70 | 0.26 | Finnish 2.06 | NULL |
| Parpola 1994 | Tamil | 27 | 0.28 | – | – | – | NOT TESTABLE (control fails) |
| Kak 1988 | Sanskrit | 7 | 0.16 | – | – | – | NOT TESTABLE |
| Mahadevan 2014 | Tamil | 5 | 0.14 | – | – | – | NOT TESTABLE |

### 4.3 Refits of the authors' own labels (z of the refit, same null)
| Key | → Sanskrit | → Tamil | → Finnish | → Basque |
|---|---:|---:|---:|---:|
| Yajnadevam's 581 labels | 5.5 (6.1 plain) | 10.5 | 5.4 (4.4) | 9.8 (7.4) |
| Fairservis's 95 values | 6.8 | 4.7 | 3.2 | 4.4 |
| Rao's 56 values | 4.8 | 5.4 | 3.6 | 4.8 |

A refit of Yajnadevam's labels to Sanskrit reaches 2.87 bits per character, below the 2.99 bits per character of held-out real Sanskrit under the same model: by Shannon's criterion the corpus is below the unicity distance of this class of key.

### 4.4 Dravidian anchors and the Finnish decoy (rounds 41–45)
| Anchor set | Pooled p over 10 splits |
|---|---:|
| 24 Dravidian rebus anchors | 0.066 |
| Finnish words as anchors | 0.016 |
| Basque words as anchors | 0.72 |

### 4.5 Shape resemblance (round 48)
Four descriptors; best passes 1 of 4 positive-control queries. METHOD-FAIL. Descriptive: Brahmi ranked 20th of 25 scripts as nearest shape to Indus signs.

### 4.6 Meluhhan vocabulary (round 51)
Gates pass (Mitanni words → Indo-Aryan in 100% of resamples; Turner's Dravidian loans → Proto-Dravidian in 99%). Eleven candidate words: no family attributable; Finnish ranks first in 70% of resamples. Possehl's 1996 catalogue, obtained afterwards, contains Sumerian terms qualified "of Meluhha", not loanwords; the one word an ancient list labels Meluhhan (šamru, "thorn tree") comes from a first-millennium source when Meluhha meant Nubia.

## 5. Discussion

### 5.1 Why every key reads, and why that proves nothing
[Shannon unicity distance: key information vs redundancy per sign; letters/prose vs syllables or words/names; the table of three cases; median two tokens per sign; the role of the human glossing stage; the same strings glossed as a Shiva epithet and as a priestly calendar title.]

### 5.2 What the corpus can support
[Structural results that survive controls: order transfers between cities (27, 29); Gulf round seals foreign in order (30–31); fixed endings per text; the unicorn as emblem with 892 distinct texts in 1,005. Profile of names and titles.]

### 5.3 What would change the picture
[Anchors: ~40 externally fixed sign values (round 32 estimate); a bilingual; the sealed-tablet route now checked and empty (round 50); the loanword route closed on the published record; the Dilmun name route non-informative at 27 names (round 35).]

### 5.4 A checklist for future claims
1. Freeze the reading pipeline before looking at results; no manual glossing stage between key and claim.
2. Report the key's position in its own structure-preserving shuffle distribution.
3. Give an impossible language identical freedom and report it.
4. Pass a known-script positive control at matched tokens per sign and matched coverage.
5. Publish the key as a machine-readable table with the sign catalogue it uses.

## 6. Limitations
Trigram models underuse a language's redundancy; a stronger scorer (word segmentation, morphology) would raise discrimination for genuine keys and should be tried, but it would also need its own controls. Fonts stand in for epigraphic shapes in round 48. Partial keys are scored only where they apply. Nothing here bears on whether the Indus people spoke Dravidian, Indo-Aryan or something else; it bears on whether anyone has demonstrated sign values.

## 7. Reproducibility
All rounds have a committed `PROTOCOL.md` preceding the code, fixed seeds, pinned inputs with hashes, and a `REPORT.md` with the protocol's verdict word. Commands: see repository README. Round 47 runs in 8 minutes on stdlib Python; round 49 in 20 minutes; round 48 needs Pillow, numpy and scipy; round 51 needs numpy and rapidfuzz.

## Acknowledgements and data sources
[Bourdeau's Indus Website export and cyphersolver transcriptions; Yajnadevam's lipi repository; Tejesh Raut's explorer; Dravidian Database; lexibank IDS; JAMBU; Kotus; Xuxen; NeuroDecipher; ePSD2; Noto fonts; archive.org scans used for reading only.]

## References
[To compile: Fairservis 1992; Rao 1982; Kak 1988; Mahadevan 1998, 2014; Parpola 1994; Yajnadevam 2024; Bonta 2023; Farmer, Sproat & Witzel 2004; Rao et al. 2009; Possehl 1996; Witzel 1999; Southworth 2005; Glassner 1996; Collon 1996; Hallo & Buchanan 1965; Gadd 1932; Laursen 2010; Laursen & Steinkeller 2017; Shannon 1949; Luo, Cao & Barzilay 2019 (NeuroDecipher); Bedigian 1985.]
