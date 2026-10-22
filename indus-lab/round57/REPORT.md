# Round 57 — Bhaty 2024 place names on Indus seals: **NULL** (positive control passed)

Pre-registered in `PROTOCOL.md` (commit 0766692) with the gazetteers frozen; Amendment 1 (one respelling, Maništušu) before any run. One run, seeds 57201–58200, 1,000 shuffles. Run time 71 s. Outputs `results.json`, `run57.log`.

## The claim
Rupa Bhaty (*Pratnakīrti* 5(2), 2024; ResearchGate 2025; book 2026, promoted on The Ranveer Show ep. 461) takes Yajnadevam's Brahmi/Sanskrit key, changes one glyph (sign 435/436, *ā* → *o*, identified from her own seal list), and reads recurring sequences as Bronze Age place and ruler names: Moka/Mokan/Mokani = Makran/Magan, Hattusa, Umma, Susa, Isin, Nuzi, Hamazi, Daman, Varan, Revakhanda, Beroea, Manium, Maništušu. She does not claim to read every seal; she reinterprets a subset of Yajnadevam's readings.

## Verdict: **NULL**
Under her key, Indus texts contain no more Bronze Age place names than structure-preserving shuffles of her own key produce.

| Gazetteer (skeletons ≥ 3 consonants) | Names | T real | Shuffle mean (sd) | z | Percentile |
|---|---:|---:|---:|---:|---:|
| **Bronze Age places**: ePSD2 GN/SN + all of Bhaty's names | 275 | 765 | 806 (163) | **−0.25** | **0.41** |
| Same skeletons with consonants scrambled (decoy) | 275 | 1,907 | 1,860 (261) | 0.18 | 0.53 |
| Finnish municipalities (decoy) | 71 | 309 | 208 (53) | 1.93 | 0.95 |

Matches per name: Bronze Age places 2.8, scrambled non-names 6.9, Finnish towns 4.4. Real ancient place names match the readings **less** often than random consonant strings of the same length and **less** than Finnish towns; Finnish comes closer to significance (0.949) than the claimed gazetteer does.

## Positive control: passed
Linear B at Indus density (round 47 PC2 geometry), true key, 41 place names attested in the tablets in Linear B spelling: T 54 against a shuffle mean of 32 (z 4.2, percentile 1.00); scrambled Linear B place names 0.25. The instrument finds real place names in a script that contains them, at Indus sparsity and under the same matching freedom (vowels ignored, voicing and l/r merged). Matched: Knossos, Kydonia, Pylos-area names, Lato, Metapa, Amnisos and others.

## Her named places, one by one (description, not verdict-bearing)
| Name (skeleton) | Texts matched under her key | Share of shuffles matching as many |
|---|---:|---:|
| Mokan / Magan (mkn) | 21 | 0.006 |
| Daman (tmn) | 65 | 0.000 |
| Varan (vrn) | 62 | 0.000 |
| Hamazi (kms) | 9 | 0.05 |
| Madra (mtr) | 31 | 0.18 |
| Manium (mnm) | 37 | 0.61 |
| Hattusa (kts) | 2 | 0.36 |
| Dilmun (trmn) | 2 | 0.52 |
| Makran, Meluhha, Revakhanda, Maništušu | 0 | – |
| Moka (mk, 2 consonants) | 31 | 0.33 |

A few of her names are frequent under her key: Mokan, Daman and Varan sit on common sign sequences that end in the jar sign 740 (*an*), so any skeleton ending in a frequent consonant plus *n* is guaranteed hits. That is why they were found; it is not a property of place names. She chose these names after reading the seals, which is exactly the selection the full-gazetteer test removes: when every Bronze Age place known to Mesopotamia is scored the same way, the total sits in the middle of the null. Makran and Meluhha, the names the Magan argument most needs, never occur; the "Moka" string itself (mk) occurs in 31 texts, no more than a wrong key yields (percentile 0.67). The 2-consonant gazetteer rises above shuffles (percentile 0.99) because two-letter skeletons such as *mn* and *sn* coincide with the commonest endings; Finnish 2-consonant names were not scored, and the protocol excluded 2-consonant matches from the verdict in advance for this reason.

## Secondary: round 47's language test on her key
| Language | z | Percentile |
|---|---:|---:|
| Sanskrit | −0.35 | 0.30 |
| Finnish | −0.43 | 0.33 |
| Basque | −0.47 | 0.30 |
| Proto-Dravidian | −0.02 | 0.49 |

Identical to Yajnadevam's key (round 47: −0.35). Changing one vowel does not change the result.

## What this means
- Her method finds place names because short consonant strings with free vowels, merged voicing and any language from Gujarat to Greece will always find some. The test that matters is whether real places beat non-places and wrong keys; they do not.
- The base key is still NULL (round 47); her one change cannot rescue it, and the place-name reading adds no signal on top.
- This bears on the readings, not on the history: Magan, Meluhha and Indus–Gulf trade are real; their names are not demonstrated on the seals.

## Reopen criteria
A key of her own that passes round 47's test, or a place-name list fixed **before** reading the seals whose matches beat shuffles and the scrambled and Finnish decoys under this protocol.

## Reproduce
```
cd indus-lab/round57 && python3 run57.py    # 71 s; needs ext/lexicons and ext/neurodecipher as for round 47
```
