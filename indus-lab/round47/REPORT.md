# Round 47 — Yajnadevam's Indus→Brahmi/Sanskrit key is not Sanskrit-specific

17 October 2026. Pre-registered in `PROTOCOL.md` (committed c5bc1b1, amendment eee5b06) before `run47.py` ran. One run, 8 minutes, stdlib Python. Outputs: `results.json`, `per_text.tsv`, `run47.log`.

## Verdict (rule 2 of the protocol): **NULL**

The key's readings are **not more Sanskrit-like than structure-preserving shuffles of the same key.** Percentile 0.29, z = −0.35: the real key sits in the middle of its own null, slightly on the wrong side. Every control that was supposed to catch a genuine signal worked; the signal is absent.

## Positive controls: the method can recognise a true key

Linear B with the Ventris key, held-out Greek lexicon (719 types), same statistic, same 1,000-shuffle null:

| Control | Sign IDs | Tokens/sign | z Greek | best other z | pass |
|---|---:|---:|---:|---:|---|
| PC1 bijective | 70 | 24.8 | **6.01** | 1.65 (Basque) | yes |
| PC2 Indus density | 130 | 13.4 | **11.53** | 5.70 (Basque) | yes |
| PC2b round-32 geometry | 365 | 4.8 | **13.48** | 6.12 (Basque) | yes |

Greek is identified at every density, with the required ≥ 2 margin over four wrong languages. Note that the true key also beats shuffles under *wrong* languages (open-syllable structure is language-like in general); that is why the protocol demands a cross-language margin, not just "beats shuffles".

## Indus result

Corpus: 1,934 of 1,936 core text types (2 dropped for unlabelled signs), 8,720 tokens, 581 sign types, 15.0 tokens/sign. Key: 714-code expanded lipi map. Lexicons size-matched to the smallest (Proto-Dravidian, 1,765 types), 5 draws.

| Analysis | Sanskrit z (pct) | Finnish | Basque | Proto-Dravidian |
|---|---:|---:|---:|---:|
| **Primary**: author's vowel rule, matched lexicons, stratified null | **−0.35 (0.29)** | −0.34 (0.38) | −0.36 (0.33) | 0.00 (0.50) |
| Consonant skeleton (Bourdeau's mode) | −0.73 (0.23) | 1.71 (0.96) | 0.88 (0.80) | −0.85 (0.21) |
| Full lexicons (Sanskrit 185,776 headwords) | −0.57 (0.24) | −0.11 (0.46) | −0.43 (0.33) | 0.00 (0.50) |
| Unrestricted permutation null | 0.26 (0.56) | 1.40 (0.94) | 0.06 (0.51) | 0.65 (0.73) |

No analysis puts Sanskrit above the 60th percentile. Where anything moves, it is Finnish (consonant skeleton, percentile 0.96), which is exactly the round 45 pattern and is not evidence for Finnish either.

## Matched-budget fitted controls: how much does 60,000 steps buy?

Keeping the author's own 714 labels and only re-permuting them over signs, a small annealing run (3 chains × 60k swaps, about 15 s each) makes the corpus "read" any language:

| Fitted to | z under its own language | z under Sanskrit |
|---|---:|---:|
| Finnish | **5.41** | 0.99 |
| Basque | **9.83** | 1.53 |
| Proto-Dravidian | **5.68** | 0.61 |
| Sanskrit (refit) | **5.49** | — |
| *Author's key as published* | — | **−0.35** |

Two things follow. A key fitted to an impossible language in seconds looks far more language-like than the published key does for Sanskrit. And the published key is far from optimal even under a Sanskrit phonotactic criterion: a 15-second refit of the author's own label inventory beats it by six standard deviations. Whatever selected the published assignments, it was not Sanskrit phonotactics.

## Diagnostics

**M-304** (ICIT 2823.1): signs 090-550-534-742-220-740-090, labels `a as as an m an a`, author's display string `aaasasanmaanaa`, consonant skeleton `ssnmn`. 6.26 bits/char under Sanskrit, 3.61 under Finnish. This is the inscription the author reads as a prayer. Mechanically it is a string of vowels and nasals/sibilants.

Ten texts by fixed rule (every 190th), author's vowel rule applied: `aajatasan`, `satadaaasvananaara`, `tadasmaaasi`, `amanmna`, `vajanraamavatas`, `maansavaraan`, `kamamaaan`, `asmaanjaaaan`, `raaaska`, `ravasman`, `damaananraan`. Eight of the ten are cheaper to encode as Finnish than as Sanskrit. Full list with bits per language in `results.json` and `per_text.tsv`.

**Table 7 subset** (exploratory): 33 texts with ≥ 50% of signs among the 18 Brahmi-shape-anchored IDs: Sanskrit z = 0.09, percentile 0.53. The shape-anchored part of the key carries no detectable signal either, at low power.

## What this does and does not show

- It shows that the published key, applied with the author's own vowel rule, produces strings with no Sanskrit-specific phonotactic structure beyond chance, at a test resolution that recognises the Linear B key at Indus density by 6–13 standard deviations.
- Combined with round 46: the key *covers* the corpus completely and *means* nothing by that fact. Any key with the same label inventory covers it; a randomly re-permuted one is as Sanskrit-like.
- It does **not** score the author's full pipeline. His readings pass through manual word segmentation, regex-permitted alternatives, sandhi and dictionary glossing (`glossing.csv`, `words.csv`). This round shows that the Sanskrit in the output must enter at that human stage, since it is not in the key's output. A test of that stage would need the glossing to be frozen and the same freedom granted to Finnish; it cannot be run on a key alone.
- It does not refute an Indo-Aryan or any other language for the Indus script. It refutes one key and one argument ("100% assignment").
- The Brahmi-descent claim (Table 7) was not separately testable here beyond the low-power subset; it stands or falls on palaeography and chronology, not on this test.

## Decision

**Brahmi/Sanskrit key lead: PARKED.** Reopen only with (a) a fully automated reading pipeline, frozen in advance, that is granted identical freedom for Finnish and Basque and still prefers Sanskrit by the protocol's margins; or (b) externally anchored sign values (bilingual, names) that agree with the key's assignments.

Recommended next: the methods write-up now has its third leg. Round 32 (statistics cannot recover sounds at 15 tokens/sign), round 45 (Dravidian anchors beaten by Finnish) and round 47 (the Sanskrit key beaten by a 15-second Finnish refit) make one argument with code. The other live lead, external anchors from Gulf seal publications, needs PDFs from Arham.

## Reproduce
```
bash fetch_lexicons.sh        # ~55 MB into ../../ext/lexicons, hashes printed
python3 run47.py              # 8 min; prints VERDICT NULL
```
Inputs and hashes: `fetch_lexicons.sh`, `../../ext/lexicons/SHA256SUMS`, `results.json["lexicon_sizes"]`. Seeds in `PROTOCOL.md`.
