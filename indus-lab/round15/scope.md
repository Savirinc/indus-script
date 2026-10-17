# Round15 scope fixed before results

Two tests remove advantages of round14. They test methods on a contemporary comparative wordlist, not ancient inscriptions.

1. Meaning-free retrieval retains known pronunciations but no longer restricts candidate matches to a shared concept. Each query searches all eligible forms in another language. Labels are used only to evaluate answers. Report all-query accuracy and conditional accuracy when an annotated cognate exists separately.
2. A synthetic substitution test conceals Tamil phonemic segments behind arbitrary tokens. Malayalam is a preselected known comparison language. A same-language reference control may diagnose solver limits. Word boundaries and language choice remain given. Artificial phoneme substitution does not model an unknown logo-syllabic writing system.

Metrics must not be compared directly with round14 AUC. A ranking score within a known meaning is a different task from finding a word in a full vocabulary, or recovering a substitution key.

The two agents run separate experiments. Neither result selects the best language hypothesis for Indus. Solver inputs must not expose concept labels, cognacy labels or the true substitution key. Preprocessing and evaluation may use those fields and must be separable from search. No tuning on held-out scores. Preserve failures and state computational budgets.
