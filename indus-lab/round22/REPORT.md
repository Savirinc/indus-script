# Held-out Dravidian initial-sound prediction

11 October 2026. This is a diagnostic of descendant-language correspondences, not a reconstruction or an Indus decipherment.

## Result

| Method | Correct / 782 | Accuracy |
|---|---:|---:|
| Learned conditional correspondences | 632 | 80.8% |
| Copy Tamil initial | 576 | 73.7% |
| Training-set modal target initial | 98 | 12.5% |
| Shuffled training associations, mean of 100 replicates | 223.23 | 28.5% |

There are 782 concept-language records spanning 86 distinct concepts and 19 target languages. Five folds hold out entire concepts. The model fixes 69 errors made by copying, but introduces 13 new errors, for a net gain of 56 correct predictions (7.16 percentage points). It beats copying in 11 language directions, ties in three, and loses in five. Shuffled-control correct counts range from 182 to 262. These descriptive results are not a statistical claim based on 782 independent samples.

## All directions

| Target language | Records | Model correct | Copy correct | Ambiguous concepts excluded |
|---|---:|---:|---:|---:|
| Badga | 51 | 42 | 39 | 3 |
| Betta_Kurumba | 51 | 43 | 38 | 2 |
| Brahui | 21 | 11 | 8 | 2 |
| Gondi | 33 | 27 | 28 | 1 |
| Kannada | 56 | 51 | 34 | 4 |
| Kodava | 59 | 49 | 45 | 2 |
| Kolami | 30 | 26 | 26 | 0 |
| Kota | 55 | 44 | 45 | 1 |
| Koya | 35 | 30 | 30 | 0 |
| Kurukh | 25 | 15 | 9 | 2 |
| Kuwi | 19 | 11 | 12 | 1 |
| Malayalam | 75 | 69 | 66 | 4 |
| Malto | 19 | 6 | 8 | 3 |
| Ollari_Gadba | 25 | 21 | 21 | 0 |
| Parji | 35 | 25 | 21 | 2 |
| Telugu | 39 | 29 | 30 | 5 |
| Toda | 49 | 40 | 36 | 1 |
| Tulu | 45 | 38 | 31 | 2 |
| Yeruva | 60 | 55 | 49 | 2 |

## What is and is not being tested

The input supplies cognacy classifications. Thus the algorithm is told which words are related before prediction. It tests only initial segments, conditional on those classifications and an unambiguous-initial filter. It does not discover relatives, predict full words, date changes, decide ancestral pronunciations, or assign Indus sign values.

Thirty-seven ambiguous concept-language cases were excluded before fitting. This includes Tamil/Kannada foot: shared groups provide both a:a and p:p initials. Therefore this run does not test the p:p foot exception highlighted in round21. All nine retained Tamil p / Kannada h concepts were predicted correctly in their held-out folds, but that must not be stated as an exceptionless historical law.

For 126 held-out records, the source initial did not occur in training; the program copied it. The baseline already scores highly because these are related languages and selected cognates. Some groups contain multiple roots, synonyms or morphology, which this initial-only model cannot resolve. The dataset had been inspected in earlier work, so this is computational withholding rather than a newly acquired external validation corpus.

## Consequence for our research

Keep the comparative route. Do not apply this table to the Indus script: it maps known modern phonetic segments to other known phonetic segments, while Indus phonetic values remain unknown. The next substantive stage is published ancestral reconstructions plus full segment alignment and conditioning, tested on whole held-out cognate sets. The current experiment provides a reproducible baseline against which that more demanding model can be assessed.

## Reproduce

From the archive root run `python indus-lab/round21/build_comparative.py`, then `python indus-lab/round22/test_initials.py`. Standard library only. Source data, license and provenance are included. Every held-out prediction is in predictions.json. Protocol wording was clarified after execution to correctly describe pooled concept-language weighting; code and results were not tuned.
