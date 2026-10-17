# Lead review

Meaning-free retrieval scorer inspected: distance uses Segments only, with language IDs choosing the target vocabulary. Parameter_ID and Cognacy are consulted after rankings for evaluation. Exact rational comparisons preserve tied scores; fractional credit avoids choosing a convenient tie. Query count checks: 1,986 forms times 19 target languages = 37,734 queries. Each direction searches the entire eligible target vocabulary.

Primary interpretation is all-query top-one retrieval. Conditional accuracy when a cognate exists is useful but has easier coverage and must not replace the primary result. Same-concept is semantic matching; same-concept plus identical supplied Cognacy is the operational cognate target. Neither metric establishes historical ancestry independently.

Source eligibility excludes explicit loan labels and missing cognacy. This makes the sample curated, although labels do not select candidate matches in scoring. All 20 languages belong to the same family; unrelated-language rejection remains untested. Segments are supplied by the source, including its segmentation conventions. Artificial shuffled labels are descriptive controls, not historical null hypotheses.

Cipher review: lead and methods reviewer inspected the solver API, objective, split and evaluation. No blocking implementation bug or direct hidden-answer leakage found. Full reference coverage and target sound inventory remain disclosed oracle advantages. Evaluation is on held-out ciphertext words, not unseen lexical entries.
