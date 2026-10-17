# Joint-constraint control: inconclusive

11 October 2026. This is a limitation check on round27, not a new decipherment result.

## Executed test

For each of the four existing cross-city splits, ten random-walk chains attempted 40,000 local swaps each. After 20,000 proposals, ten samples were collected every 2,000 proposals. The 400 sampled controls across the four conditions preserve every source inscription's exact sign multiset and each exact-length position's sign counts simultaneously. Invariants were asserted for every sample. The source model and one-edit-excluded test sets were unchanged.

| Training → testing | Subset | Controls at least as good / 100 | Mean changed sign positions | Mean changed inscriptions |
|---|---|---:|---:|---:|
| Harappa → Mohenjo-daro | all | 46 | 1.61% | 3.17% |
| Mohenjo-daro → Harappa | all | 29 | 0.43% | 1.02% |
| Harappa → Mohenjo-daro | SEAL:S | 100 | 0.43% | 1.02% |
| Mohenjo-daro → Harappa | SEAL:S | 51 | 0.51% | 1.20% |

The score comparison concerns internal signs. First/end scores remain identical by construction and were checked. Counts include ties and are descriptive, not p-values. Samples within chains are correlated.

## Interpretation

The observed ordering is not separated decisively from these sampled controls. But they leave 98.4–99.6% of positions unchanged on average, accepting only 4–28 moves per 40,000 proposals in the reported chains. Therefore this test also does not demonstrate that a freely rearranged composition-and-position model explains the observations. The sampler may be trapped in a small connected component, and no convergence or uniform sampling guarantee is available.

Round27 remains a verified engineering result: source-city sign-order models beat unigram baselines on target-city text types after removing exact and one-edit copies. Its weaker shuffled controls did not jointly preserve text composition and positional patterns. Round28 does not justify promoting that result to grammar, language identification, or phonetic decipherment.

## Decision

Mark the combined composition/position explanation UNRESOLVED. Do not claim it has been ruled out, and do not interpret 100/100 controls in one condition as proof of equivalence or a rejection of linguistic writing. A successful stronger sampler would need to explore substantially more admissible arrangements and establish what distribution it samples. More proposals of the same ineffective move alone are not a justified next step.

The project should now require external linguistic or archaeological evidence for any sound/meaning claim. This stage supplies a benchmark and its demonstrated limits. No sign-to-sound assignment or ancient-language identity is inferred.

## Reproduce

Run `python indus-lab/round28/joint_control.py` from the archive root. The archive includes round27 code, its frozen robustness split/predictions, the unchanged source CSV and provenance, and every control score/acceptance diagnostic. Standard library only.
