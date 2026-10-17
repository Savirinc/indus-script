# Indus research 09 — a cross-city prediction test

**Concrete result:** sign presence did not improve on inscription length when predicting catalogue seals versus tablets across Harappa and Mohenjo-daro. This is a limit of this particular model and sample, not evidence that the script has no structure.

## What was done

Rules were written before fitting in `round09/protocol.md`. We used the existing 5,679-row transcription corpus, retaining complete seal/tablet rows with at least three signs and no unknown/boundary codes. Three object-type corrections from photographed CISI headings were applied. No proposed translations, Sanskrit readings, semantic notes, or upstream `class` labels entered the model.

2,173 rows were eligible. Shared ID stems, CISI IDs, site-specific excavation IDs, or identical unordered sign multisets connected rows into 1,578 groups. We excluded 22 groups with contradictory labels and 15 additional groups spanning sites; 1,541 remained. This deliberately conservative grouping can merge distinct objects. One deterministic representative row per group was used; these are not verified counts of physical objects, and other object faces are not all retained.

The two-city experiment used 447 Harappa groups (198 seals, 249 tablets) and 866 Mohenjo-daro groups (791 seals, 75 tablets). Other sites lacked 30 groups of each class under the frozen rule. Cross-site matching groups were excluded, so the experiment concerns distinct site-specific material, not the whole surviving corpus.

Each model learned from one city and predicted labels in the other. The sign model used binary sign presence plus log inscription length; the baseline used only log length. Both used class-balanced logistic regression, fixed C=1, threshold 0.5, and no tuning. Training data alone defined the sign vocabulary and length scaling.

## Results

Balanced accuracy gives seal detection and tablet detection equal weight; always guessing one class gives 50%.

| Learn from → test on | Length only | Signs + length | Gain and bootstrap 95% interval |
|---|---:|---:|---:|
| Harappa → Mohenjo-daro | 55.4% | 52.3% | −3.2 points [−8.9, +2.5] |
| Mohenjo-daro → Harappa | 68.2% | 59.6% | −8.6 points [−13.8, −3.1] |

ROC AUC similarly declined: 0.544 to 0.543 in the first transfer and 0.747 to 0.685 in the reverse transfer. Thus the negative conclusion is not solely an artifact of the 0.5 threshold. Intervals use 2,000 stratified bootstrap resamples of test groups, conditional on each fitted model; they do not cover catalogue errors or sampling bias.

## What independent review revealed

No train/test vocabulary or scaling leakage was found in the code review. But the tablet samples differ substantially:

| Catalogue subtype | Harappa tablets | Mohenjo-daro tablets |
|---|---:|---:|
| TAB:B | 163 | 29 |
| TAB:I | 85 | 0 |
| TAB:C | 0 | 46 |
| Reviewed correction from raw SEAL:R | 1 | 0 |

Those codes are retained literally until their definitions and object metadata are verified. A broad tablet label combines materially different collections. Subtype, chronology, recording convention, and preservation may contribute to the failed transfer. This inspection is post-result diagnosis, not proof of its cause.

An illustrative exploratory lead: sign 400 appears in 94/249 Harappa tablet groups (37.8%) versus 7/198 seal groups (3.5%). At Mohenjo-daro it appears in 7/75 tablet groups (9.3%) versus 44/791 seal groups (5.6%). A strong local association weakens substantially elsewhere. This does not mean sign 400 says 'tablet', and its earlier terminal-position preference remains a separate structural observation.

## The concrete next step

Compare like objects and establish metadata from photographs/catalogue entries before making a semantic inference. Start with common catalogue subtype TAB:B and a single seal subtype, matched by text length and checked for date and recording differences. The current Mohenjo-daro sample has only 29 TAB:B groups, below the existing 30-per-class gate: do not quietly lower that gate or call a revised model an independent replication. Recover and validate further examples or explicitly preregister a small-sample exploratory study with appropriate uncertainty.

Build a photo-backed audit queue for sign 400 in matched object types, including both occurrences and absences. Keep individual sign decomposition, positional structure, and animal-image association as distinct research tracks. The animal-image model has not been run in this round. No sound values, translations, or semantic anchors were established.

Both cities were test data in one direction and training data in the other. They are no longer an untouched final validation set for future revised models. Future confirmation requires additional held-out evidence.

## Reproducibility

`round09/analyze.py` regenerates grouping, models, predictions and results using numpy and scikit-learn. `groups.json` records retained and excluded memberships; `predictions-*.json` contains individual test predictions; `diagnostics.json` contains post-run subtype/sign summaries. `clarifications.md` records protocol wording limitations without changing the original protocol.

Corpus SHA256: `c22d39c3c2bda869c67fb01e7f2b4cdc64cc424405eafe89550d1702216b3429`.
Frozen protocol SHA256: `2e539b0c0169ece009b4ccac78d70255b794f5a36a45099190539473411d0f4c`.
Source: https://raw.githubusercontent.com/field-cady/indus_valley_script_corpus/main/inscriptions.csv

These are new computations on an existing public transcription, not a new archaeological discovery. Original photographs remain essential for validating the labels and sign readings.
