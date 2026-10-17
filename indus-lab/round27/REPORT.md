# Cross-city sign-order prediction

11 October 2026. Positive structural result; no phonetic or semantic decipherment.

## Result after removing exact and one-edit matches

| Training city → test city | Subset | Unseen text types | Frequency-only loss | Sign-order loss | Loss reduction |
|---|---|---:|---:|---:|---:|
| Harappa → Mohenjo-daro | all | 741 | 7.263 | 6.668 | 8.2% |
| Mohenjo-daro → Harappa | all | 428 | 7.297 | 7.071 | 3.1% |
| Harappa → Mohenjo-daro | SEAL:S | 615 | 6.869 | 6.332 | 7.8% |
| Mohenjo-daro → Harappa | SEAL:S | 123 | 7.010 | 6.228 | 11.2% |

Loss is mean bits per predicted internal sign token; lower is better. Internal excludes the first sign and the end marker. These are not percentages of words translated or signs correctly sounded. Text types are deduplicated within each city; longer inscriptions contribute more tokens to the loss. The four conditions overlap and must not be added as independent evidence.

The original source-city training sets contain 695/1022 text types for Harappa/Mohenjo-daro (all types) and 185/743 for SEAL:S. All parameters were fixed before first execution. Further removal of one-edit neighbours was a post-result robustness check, explicitly documented, with unchanged models. It removed 237,223,111,45 additional test types, respectively.

In all four conditions the observed internal loss is lower than all 200 source controls that independently shuffle each position within exact-length groups. The original evaluation also beat all 200 within-text order shuffles in each condition. Reported 0/200 counts are descriptive; they are not zero p-values or independence-adjusted significance claims.

## What this supports

In this dataset, local sign-order associations transfer across Harappa and Mohenjo-daro beyond exact text copying, one-edit copying, overall sign frequencies, and the separate tested null models for length-specific position distributions and within-text sign composition. The signal also appears in the common SEAL:S object class, so broad object-type mixture alone is insufficient to explain that restricted result.

This is an independently executed test of expected shared structure, not a claim to have discovered that the cities used a shared script for the first time. It supplies a reproducible evaluation, not a newly deciphered word.

## Failure and limits

First-sign prediction is worse than the frequency-only baseline in every original and robustness condition. Do not report this as universal predictive success. Position-preserving controls have identical first/end scores by construction.

The position controls preserve length/slot marginals but destroy individual inscription sign composition and mix possible genres/workshop templates. The within-text controls preserve composition but destroy position. Passing these separately does not exclude a joint composition-and-position explanation. Longer formula fragments, production relationships, site/period differences and common editorial conventions remain. Some unseen signs map to a single UNK bucket: successful bucket prediction does not recover their identities. Reading order is taken from database direction metadata, not newly established.

## How this constrains future work

Keep both cities as a transfer benchmark. Any learned structural rule should be tested across cities, with duplicate and near-duplicate exclusions. A phonetic proposal needs an additional external linguistic test: merely replacing sign IDs by letter labels preserves the same statistics and cannot establish a language. The current experiment does not distinguish Tamil/Dravidian from other language families or from a nonlinguistic structured notation.

For a real reading, fix the sign-to-sound mapping and independently sourced candidate language model before evaluating excluded inscriptions. Compare competing languages and equally flexible random mappings, and require archaeological compatibility. Do not infer words directly from the positive cross-city result.

## Reproduction

From the archive root run `python indus-lab/round27/cross_city.py`, then `python indus-lab/round27/robustness.py`. Standard Python library only. The unchanged source CSV and its provenance/license, both protocols, all splits, per-text losses, aggregate results and independent review are included. No Sanskrit or translation field is used by the scripts.
