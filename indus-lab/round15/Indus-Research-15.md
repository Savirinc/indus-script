# Indus research 15 — removing meanings and hiding sounds

10 October 2026. Two executed computational benchmarks. These use known Dravidian wordlists and artificial encryption, not Indus inscriptions. No ancient language identification is established.

## 1. Searching without supplied meanings

The program searched the entire eligible vocabulary of each other language using only normalized edit distance between supplied sound segments. Concept and cognacy labels were consulted afterwards for evaluation, not used to restrict the search.

It scored 1,869,766 cross-language form pairs and evaluated 37,734 queries across 380 ordered language pairs. It gave fractional credit for tied best matches, rather than selecting the most convenient tied answer.

| Top-one retrieval criterion | Observed | Uniform candidate baseline |
|---|---:|---:|
| Same documented meaning | 12.93% | 1.01% |
| Same meaning and cognacy annotation | 11.69% | 0.37% |
| Cognate retrieval, restricted to queries where one exists | 33.78% | 1.08% |

Twenty shuffled target-label controls averaged 1.014% for meaning and 0.363% for cognacy. No significance claim is made: these are artificial-label controls, not a model of historical language evolution. All languages are related; rejecting unrelated languages remains untested. Sounds and word segmentation remain known. These retrieval percentages are not directly comparable to round14's within-concept AUC.

## 2. A synthetic unknown alphabet

We replaced eligible Tamil sound segments with arbitrary tokens using a random one-to-one substitution. A concept-grouped split yielded 106 distinct training words and 27 held-out words; one overlapping test wordstring was removed. The solver received anonymous cipher words and an unaligned reference vocabulary. It received no meanings, cognacy labels, true key, plaintext target words or held-out cipher words during fitting.

The model fitted sound-sequence probabilities from the reference language and searched substitution keys with simulated annealing. Settings were fixed before fitting: six starts and 15,000 swap proposals per start for each of two reference conditions, for 180,000 proposals overall. Search selected keys by training likelihood, not by hidden-answer accuracy. Evaluation followed both fits. The saved run took approximately three seconds, excluding preparation and review.

| Reference and method | Held-out words decoded exactly | Sound segments correct |
|---|---:|---:|
| Malayalam, optimized key | 12 / 27 (44.4%) | 113 / 134 (84.3%) |
| Malayalam, frequency matching | 0 / 27 | 44 / 134 (32.8%) |
| Tamil, optimized positive control | 25 / 27 (92.6%) | 132 / 134 (98.5%) |
| Tamil, frequency matching | 1 / 27 | 66 / 134 (49.3%) |

The Malayalam run recovered 28 of 47 training-observed symbol values exactly. Its higher token accuracy reflects greater success on frequent symbols. The Tamil control recovered all 47 training-observed values. Its two erroneous test tokens used a symbol type absent from training.

Unselected random mappings averaged 1.55% held-out token accuracy in the Malayalam run and 2.33% in the Tamil run. The highest-training-score map among 100 random candidates decoded no held-out word exactly in either condition.

## What the result means

The code demonstrates a small, reproducible example of recovering an artificial cipher using a related language's sound patterns without aligned word meanings. This is a stronger engineering result than within-concept sound comparison. It supports developing the method further; it does not show that Indus was Tamil, Dravidian or even a phoneme substitution system.

The experiment deliberately supplies substantial advantages:

- Word boundaries and sound-segment units are known.
- The reference language is preselected, not discovered.
- The candidate sound inventory is the union of Tamil and Malayalam inventories, exposing the correct target inventory as an oracle simplification.
- The full reference dictionaries contain held-out concepts; the Tamil control includes the held-out plaintext words themselves as unaligned vocabulary. This is held-out cipher recovery, not prediction of previously unseen lexical items.
- The encryption is a single bijection. Unknown syllabic signs, word signs, allographs, multiple signs for one sound, damage and missing boundaries are not represented.
- This is one fixed split and key, not a general performance estimate. Both conditions use the same dataset and are not independent historical confirmations.

The split labels are available to the preprocessing harness. The true key is available only to encryption/evaluation. The solver's function arguments contain cipher training words, an unaligned reference, alphabet size and random seed. Lead review found no direct key or meaning access within the solver. The disclosed reference and inventory advantages remain important.

An initial serialization error involving NumPy integer values was repaired and the same seeds/settings rerun. No model changes or result-based tuning were made.

## Decision

Continue developing this computational route. The next necessary experiment is reference-language competition with unrelated controls, repeated fixed seeds, and a score that selects a candidate before hidden answers are opened. It must be able to reject a wrong language. After that, remove further advantages, including known sound inventory and word boundaries. The current success does not justify assigning Indus sign values.

## Reproduction

Preserve the bundle directory structure.

1. `python3 indus-lab/round15/retrieval/run.py` — standard-library retrieval benchmark.
2. `python3 indus-lab/round15/cipher/benchmark.py` — cipher benchmark; requires NumPy.

The bundle includes the DravLex source snapshot, license and provenance; both protocols and scripts; query-level retrieval results; control scores; cipher solver inputs; separately labelled evaluation answers; recovered mappings and review notes. The input is the same snapshot used in round14.

Source: Kolipakam et al., DravLex, Lexibank conversion, CC BY 4.0, https://github.com/lexibank/dravlex , commit 37578075e5ccb09c43022f7f1282125e748de84d.
