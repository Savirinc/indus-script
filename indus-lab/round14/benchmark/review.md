# Executed known-language phonetic baseline

The fixed score was computed on1,986 explicitly nonloan forms spanning20 languages and100 annotated concepts. There are18,990 cross-language within-concept pairs:6,913 with equal cognacy annotations and12,077 with different annotations.

- Pooled ROC AUC:0.81844.
- Equal-concept macro AUC:0.86799 across95 concepts having both pair classes.
-100 within-concept form-label permutations: macro AUC mean0.49915, range0.47383–0.52482.
- Permuted pooled AUC mean0.58528, range0.56831–0.60132. Pooled scores mix concepts with different cognacy prevalence and intrinsic phonetic similarity, so the appropriate shuffled baseline is not automatically0.5. The within-concept macro result is easier to interpret.

AUC measures ranking discrimination, not percentage correctly translated or classified. The score distinguishes annotated cognate pairs better than artificially relabelled controls when the matching meanings are already supplied. Expert cognacy judgements themselves incorporate historical sound evidence, so this is a useful implementation benchmark rather than independent proof of that evidence.

All languages are Dravidian; there is no outside-family negative set. Meaning labels are known, unlike Indus inscriptions. No result identifies Indus as Dravidian, recovers Indus sounds, or translates anything. No significance p-value or independent holdout is claimed.

Validation: exact input hash stored, deterministic seed and100-draw cap retained; embedded checks verify perfect/reversed/tied AUC and a basic segment-edit distance. All pairs preserve concept membership and exclude same-language pairs. Permutations move labels among forms, then rebuild pair labels, preserving dependencies created by shared forms.
