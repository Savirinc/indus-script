# Post-result robustness check

Specified after viewing the first results and independent methods review, before running these additional controls. No tuning of the original model.

Remove test strings within one insertion, deletion or substitution of any source-city string. Exact duplicates were already excluded. Preserve the fixed models and all four conditions.

Generate 200 source controls by grouping inscriptions by exact length, then independently permuting each position's signs across texts of that length. This preserves exact length-conditional position frequencies, lengths, vocabulary, source unigram and boundary distributions. It breaks cross-position association where the data permit; single-record length groups remain unchanged. These controls address positional-template confounding more directly than within-text shuffling. Refit the same bigram and evaluate on the further-filtered test set. No claimed independence, new language identification or grammar inference. Report first-position failure as well as internal success.
