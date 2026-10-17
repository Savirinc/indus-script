# Round14 bounded phonetic baseline

Prespecified before computing outcomes. This is a benchmark on known Dravidian lexical forms, not Indus data, decipherment, or language-family identification.

Include forms whose Loan field is explicitly false and whose whitespace-tokenized Segments and Cognacy are nonempty. Compare every pair from different languages within the same Parameter_ID (known meaning/concept). Multiple forms remain as supplied. Positive label means exact equality of the supplied nonempty Cognacy strings. No proposed sound correspondences, model training, threshold selection, or tuning.

Similarity is1 minus token-level Levenshtein distance divided by the larger segment count. Primary score: pooled ROC AUC with half credit for ties. Also report equal-weight macro AUC over concepts having both positive and negative pairs, since pooling can over-weight larger concepts.

Negative control:100 permutations with seed14026. Shuffle cognacy labels among eligible forms within each concept, retaining concept membership, label multiplicities, observed forms and languages. Recompute pair labels after each shuffle, preserving pair dependence from shared forms. Do not shuffle individual pair labels. Use this as a descriptive artificial-label control; cognacy exchangeability across languages is not a historical null, so do not report inferential p-values.

Known semantic equivalence is an oracle unavailable for unread Indus inscriptions. The dataset contains a related language family and annotated cognacy, so high AUC cannot identify an unknown language as Dravidian. Possible circularity of expert cognacy labels and phonetic resemblance, loans misclassified as inherited forms, related-language clustering and multiple lexical forms limit interpretation. No independent holdout is claimed; this fixed baseline has no trained parameters.
