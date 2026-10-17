# Synthetic hidden-alphabet recovery: a completed engineering control

A fixed solver recovered part of a randomly encrypted Tamil wordlist using only an unaligned Malayalam reference list and phoneme-sequence statistics. This is a synthetic substitution benchmark, not an Indus decipherment result or evidence for a particular Indus language.

## Results

The held-out set contains 27 distinct Tamil word forms, comprising 134 segment tokens, from 19 held-out concepts. None of these exact wordstrings occurs in the encrypted training set. The reference lexicons deliberately have oracle coverage: they can include those concepts, and the Tamil positive control includes the held-out plaintext word forms themselves without alignments.

| Reference and solver | Exact held-out words | Correct held-out segments | Correct key entries among 47 training-observed cipher types |
|---|---:|---:|---:|
| Malayalam, optimized mapping | 12/27 (44.4%) | 113/134 (84.3%) | 28/47 (59.6%) |
| Malayalam, frequency-rank mapping | 0/27 | 44/134 (32.8%) | 8/47 |
| Malayalam, best training-score mapping among 100 random maps | 0/27 | 15/134 (11.2%) | 4/47 |
| Tamil positive control, optimized mapping | 25/27 (92.6%) | 132/134 (98.5%) | 47/47 (100%) |
| Tamil positive control, frequency-rank mapping | 1/27 | 66/134 (49.3%) | 11/47 |
| Tamil positive control, best training-score mapping among 100 random maps | 0/27 | 5/134 (3.7%) | 1/47 |

Mean segment accuracy across all 100 unselected random maps was 1.55% for the Malayalam-condition RNG and 2.33% for the Tamil-condition RNG. These baselines were not selected using hidden answers. The optimized Malayalam score is weighted toward common segment tokens; recovering 84.3% of held-out tokens is not recovering 84.3% of the alphabet.

The positive control decoded every held-out token whose cipher type had appeared in encrypted training: 132/132. Its two remaining errors are tokens of a training-unseen type. The solver cannot identify the mapping of unobserved cipher symbols from training evidence alone. Malayalam recovered 113/132 held-out tokens with training-seen types.

## Construction and solver boundaries

Eligibility followed round14: Loan=false, nonempty Segments, and nonempty Cognacy. Cognacy only gates eligibility; its values are not passed to the solver. The '+' structural delimiter was removed; other CLDF segment tokens, including long segments, were kept atomic. The eligible source has 134 Tamil forms and 109 Malayalam forms. Tamil's 94 concepts were split deterministically into 75 training and 19 test concepts. Deduplication left 106 encrypted training words and 27 test words; one held-out string identical to a training string was removed.

The artificial cipher is one fixed random permutation. Word boundaries and token segmentation remain known. A generous candidate output inventory is the 50-segment union of the eligible Tamil and Malayalam inventories, including target inventory information. Full reference dictionaries contain 109 distinct Malayalam words and 133 distinct Tamil words. These are substantial simplifications compared with an undeciphered archaeological script.

The `solve` function receives only anonymous encrypted training words, one unaligned reference wordlist, alphabet size, and an RNG seed. It receives no plaintext target forms, held-out cipher text, hidden key, meanings, concepts, cognate labels, IDs, or word alignments. The reference data are converted into smoothed interpolated unigram/bigram/trigram probabilities. A single substitution mapping is optimized against the encrypted training data's mapped trigram likelihood.

Each condition uses six fixed chains of 15,000 pair-swap proposals with a fixed decreasing temperature: one frequency-ranked initialization and five random starts. The best reference likelihood determines the returned mapping. No hidden-answer scores choose a chain. Both conditions finish before evaluation begins. All six Tamil-control chains reached the same best score. Malayalam chains reached different optima; this is a finite search, not a demonstrated global optimum.

## Runtime and reproducibility

The completed fixed experiment used 180,000 optimization proposals total and finished in approximately 3.03 seconds in this environment, below its three-minute CPU target. There was one earlier identical fit whose result serialization failed on NumPy integer types; only JSON serialization was repaired, and the exact fixed seeds/settings were rerun. No optimization setting was changed in response to results.

Run `python3 indus-lab/round15/cipher/benchmark.py`. Requires NumPy. protocol.md was finalized before fitting, and its hash plus the input data hash are in results.json. solver_inputs.json contains the anonymous training inputs and reference words. evaluation_answers.json is explicitly the separate synthetic scoring answer file, not solver input. results.json contains seeds, budgets, traces, mappings, and all reported metrics.

## Interpretation

This establishes that the implemented bounded search can recover an artificial substitution under unusually favorable assumptions, and that one close-language reference provides useful sequence constraints in this particular split. The same-language control helps distinguish a wholly broken search from limitations of cross-language similarity.

It does not establish performance on new languages, other random keys, other wordlists, an unknown symbol inventory, missing word boundaries, mixed writing systems, uncertain photographs, sign variants, or non-phonemic symbols. The target is known to be phonemic Tamil by construction. The inference is not that Indus is Tamil or that an Indus sign stands for a recovered Tamil sound. Incorrect literal Tamil-key entries under the Malayalam objective can also reflect language-specific substitutions or tokenization differences; this benchmark scores literal key recovery and does not evaluate whether such replacements are linguistically useful.

A future robustness test should change these simplifying conditions with a newly frozen protocol and independent evaluation, rather than tune this run until it looks better.
