# Whole-word prediction: limited improvement

11 October 2026. This experiment tested modern cognate word prediction, not ancestral reconstruction or Indus decipherment.

## Main result

| Method | Exact words / 825 | Exact accuracy | Segment edits / 3539 target segments |
|---|---:|---:|---:|
| copy | 100 | 12.12% | 2197 / 3539 (62.08%) |
| segment | 105 | 12.73% | 2136 / 3539 (60.36%) |
| context | 105 | 12.73% | 2143 / 3539 (60.55%) |

The segment model fixes 31 whole-word failures of copying but breaks 26 previously exact copies. The contextual model fixes 33 but breaks 28. Both gain only five exact predictions overall (0.61 percentage points). Context changes only 30 predictions relative to the segment-only model; the fixed context support threshold and small training samples limit its reach. Context has seven more segment edits than segment-only mapping.

There are 825 language/cognate-group records covering 89 concepts. All groups of a concept are held out together. This is a different sample and a much harder scoring target than round22; the percentages are not directly interchangeable. The code uses known scholarly cognacy assignments and independently selects one form per language/group by lexical ordering of segment tuples. It does not choose the closest synonym to improve the score.

## All languages

| Target | Records | Copy exact | Segment exact | Context exact |
|---|---:|---:|---:|---:|
| Badga | 54 | 11 | 10 | 10 |
| Betta_Kurumba | 53 | 5 | 4 | 3 |
| Brahui | 23 | 0 | 0 | 0 |
| Gondi | 34 | 4 | 5 | 5 |
| Kannada | 61 | 7 | 12 | 12 |
| Kodava | 61 | 17 | 19 | 19 |
| Kolami | 30 | 0 | 1 | 1 |
| Kota | 56 | 10 | 9 | 9 |
| Koya | 36 | 2 | 3 | 3 |
| Kurukh | 27 | 1 | 2 | 2 |
| Kuwi | 20 | 0 | 0 | 0 |
| Malayalam | 82 | 19 | 16 | 16 |
| Malto | 22 | 0 | 0 | 0 |
| Ollari_Gadba | 25 | 1 | 0 | 0 |
| Parji | 37 | 0 | 1 | 1 |
| Telugu | 45 | 1 | 5 | 5 |
| Toda | 50 | 5 | 3 | 5 |
| Tulu | 47 | 4 | 3 | 3 |
| Yeruva | 62 | 13 | 12 | 11 |

## Interpretation and decision

The previous success with initial segments does not establish reliable full-word prediction. This simple whole-word model barely improves on copying in exact accuracy, though segment-only mapping reduces edit distance by 61 edits (2.78% relative reduction). Neither model is ready to supply ancestral lexical forms.

This result does not reject comparative reconstruction or a Dravidian hypothesis for Indus. The model is deliberately simple: unit-cost alignments do not encode phonetic similarity; insertion attachment is mechanical; no morphological segmentation, subgroup history or historical chronology is modelled. Multiple valid alternatives may exist, but only the fixed selected target is scored. The data are sparse, and language/group records are dependent.

Research decision: retain this frozen baseline and stop treating a short modern vocabulary list as sufficient for ancestral reconstruction. Before extending the Indus mapping, obtain a source-backed reconstruction table with subgroup level, attested historical reflexes, and explicit sound-change conditions. Test ancestral hypotheses against multiple descendants, retaining ambiguity rather than inventing a single proto-form. Future models must be assessed on genuinely separate material because this dataset has now been inspected repeatedly.

## Reproduce

Run `python indus-lab/round21/build_comparative.py`, then `python indus-lab/round23/test_words.py` from the archive root. Standard library only. The archive includes source data, license, provenance, all predictions, protocol and review. No Indus sign sound values were assigned.
