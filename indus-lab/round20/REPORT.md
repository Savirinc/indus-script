# Tamil candidate tests — 11 October 2026

Three experiments were executed. None establishes an Indus sound value or identifies its language. Tamil remains a hypothesis. This is a bounded analysis of available inputs, not an exhaustive test of all Tamil or Proto-Dravidian readings, and not a direct comparison of modern Tamil letter shapes with ancient signs.

## 1. Direct Indus-to-Tamil repetition-pattern screen

The local CSV contains 5,679 parsed data records. The website reports 5,680 records for its full export; that discrepancy is not resolved here and the reported total is not silently substituted for our measured count. A strict clean-text filter retains 3,677 records yielding 3,759 lines, or 2,276 distinct sequences. The other 2,002 records remain in the source but are excluded from this test. Exclusions reflect formatting, boundaries and unknown signs, not necessarily physical damage alone.

The model assumes one inscription line is one word and a bijective correspondence between signs and phonemic segments. This is an unverified simplifying assumption. A 133-word Tamil reference gives compatible repetition patterns for 2,065/2,276 lines (90.73%). Two hundred within-word shuffled Tamil references average 2,073.59 matches (91.11%), ranging from 2,064 to 2,084. Reversing each Indus line gives 2,067 matches against real Tamil; this is a sensitivity check, not a direction determination.

Of the 2,065 matches, 2,048 contain no repeated sign. Such a line can fit any same-length word with no repeated segment. The 246 lines with exactly one candidate in this tiny dictionary are not translations: another lexicon can supply other candidates and no globally consistent sign key was solved. All 20 available Dravidian language inventories were also screened; their unequal vocabulary coverage makes a ranking unsuitable for language identification. There is no unrelated-language control in this particular experiment.

Conclusion: this simple matching method supplies no distinctive evidence for Tamil. It does not disprove Tamil, a syllabic model, a mixed writing system, multiple words per inscription or an ancestral language. Dictionary coverage is limited, and DravLex is not an exhaustive Old Tamil corpus.

## 2. Can the solver recover deliberately encrypted Tamil?

The frozen earlier benchmark was rerun with original Tamil and five references shuffled within words. Each condition received the same 90,000 search proposals. Real Tamil recovered 25/27 held-out words and 132/134 segments. Shuffled conditions recovered 0, 0, 3, 0 and 2 words, respectively, and 24, 20, 80, 41 and 63 segments. No hidden answer was supplied to the solver.

This favorable control supplies word boundaries, segment units and the candidate alphabet. The unaligned original reference contains the held-out words themselves. Shuffling changes lexical coverage as well as order. Thus this demonstrates limited engineering capability, not identification of an unknown language or an isolated test of grammar. Full conditions, limitations, inputs, traces and evaluations are in control/.

## 3. Reproduction of Bourdeau's Tamil star-number test

The live repository was checked at commit 843165c369a9c35658b1a7656860e06abd7a5de3. The original tamil_stars.py ran unchanged and reproduced its committed output exactly. Its four comparisons did not show the predicted enrichment of the selected star-name numbers before fish signs. These test results constrain that particular reading proposal; they do not estimate the probability that Indus is Tamil. See bourdeau_reproduction.md for exact counts, assumptions, commands and dependency inventory.

The project also explicitly withdrew a language-narrowing result after a genre-controlled Japanese comparison scored better. Other scripts use pooled Dravidian forms rather than Tamil alone. We did not claim these were Tamil-only tests or rerun their missing external datasets.

## Consequence for the investigation

Keep Tamil/Dravidian candidates open, but require one consistent mapping across inscriptions, explicit writing-unit assumptions, held-out archaeological constraints, and comparison with alternatives. Do not allow a different free substitution for each inscription. Before fitting larger Tamil models, obtain versioned historically appropriate references and test script models (phonemic, syllabic, mixed) separately. Neither word resemblance nor modern glyph resemblance supplies the missing sound values.

## Reproduce

From the extracted archive root:

```sh
python indus-lab/round20/pattern_test.py
OPENBLAS_NUM_THREADS=1 python indus-lab/round20/control/run.py
cd bourdeau-tamil-reproduction
python tamil_stars.py
```

The first and third scripts use Python's standard library; the control requires NumPy. Protocols, complete results, independent review and the exact data subsets used are included. Source hashes are in the output JSON. Imported translation/Sanskrit/cult fields were not used. Upstream licences accompany their respective source material.

Sources: https://dbourdeau.github.io/cyphersolver/indus.html ; https://github.com/dbourdeau/cyphersolver/tree/843165c369a9c35658b1a7656860e06abd7a5de3/targets/indus ; DravLex provenance and licence included in the data folder.
