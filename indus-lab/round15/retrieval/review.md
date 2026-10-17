# Executed meaning-blind retrieval

All380 ordered language pairs were tested. Each query searched the entire nonloan target-language inventory using phonetic segment edit distance; meaning and cognacy labels were used only afterward for evaluation.1,869,766 unordered cross-language form pairs supplied37,734 retrieval queries.

| Evaluation | All queries | Uniform candidate baseline |
|---|---:|---:|
| Same concept top1, fractional ties |12.93%|1.01%|
| Same concept and cognacy top1, fractional ties |11.69%|0.37%|

For13,053 queries with a cognate candidate actually available, cognate retrieval was33.78% versus1.08% uniform baseline. Equal-weight language-pair macro success in that subset was29.11%; the difference reflects varying available-query counts by language pair. Availability was used for reporting only and did not restrict the candidate search.

18,920 queries had tied winners; mean top tie size was2.72 and the largest tie contained119 forms. Every tied winner received equal fractional credit; no label-informed tie breaking occurred.

Twenty artificial target-label shuffles yielded mean same-concept retrieval1.01% and same-concept+cognacy retrieval0.36%, broadly agreeing with uniform baselines. These shuffles jointly preserve each target form's concept/cognacy label pair while moving it within its language. Query labels remain original. No inferential p-value is reported.

The fixed phonetic score finds useful lexical resemblance without being told which meanings to match, but misses most correct answers. Known segmentation and known phonetic values remain substantial information. All languages belong to the same family; no outside-family negative set exists. This is not an Indus result or a demonstration of language-family identification.

Round14 measured within-known-meaning ranking AUC; round15 measures unrestricted target-vocabulary top1 retrieval. Their numeric percentages are different metrics and must not be described as a direct accuracy drop from one to the other.

Validation: exact rational comparison for edit-distance ties; input hash preserved; exactly1,986×19 queries; no same-language candidates; all evaluated rates bounded0–1. Source and result snapshots are retained with per-query winners and all language-pair summaries. There was no training, hyperparameter tuning, or genuinely unseen holdout.
