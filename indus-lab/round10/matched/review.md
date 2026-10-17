# Exploratory matched-subtype follow-up: sign 400

Question: Is the previously selected sign 400 more frequent on catalogue subtype `TAB:B` than `SEAL:S`, within both major sites and after controlling exact inscription length?

This analysis is exploratory. Sign 400 was selected from earlier results, including access to both sites. The nominal p values and intervals below do not correct for that selection. This is not prospective independent replication or a decipherment result.

## Data and units

Use the fixed retained representative groups from round09, restricting the raw subtype to `TAB:B` or `SEAL:S`. The three reviewed `SEAL:R` corrections do not enter this contrast. We preserve round09 completeness, minimum-three-sign, duplicate, and conflicting-label exclusions. Each unit is one representative row from a conservative connected component, not a verified physical object; other faces can be absent. Because exact unordered sign multisets were joined in round09, no multiset pattern is repeated among the retained representatives. Near-duplicate formula families can remain.

| Site | TAB:B with sign 400 | SEAL:S with sign 400 | Length-conditioned common odds ratio (exact 95% interval) | Exact conditional nominal p |
|---|---:|---:|---:|---:|
| Harappa | 64/163 (39.3%) | 5/148 (3.4%) | 16.37 (5.65–65.14) | 1.13e-10 |
| Mohenjo-daro | 7/29 (24.1%) | 35/671 (5.2%) | 5.15 (1.68–14.21) | .00219 |

Mantel–Haenszel descriptive odds ratios are 16.75 and 5.43 respectively. Do not interpret odds ratios as ratios of probabilities. Each site's sign 400 association remains positive after conditioning on exact length; this rules out length alone as an explanation under the conditional sampling assumptions. It does not rule out catalogue errors, time/material/workshop differences, formula dependence, or selection effects.

## Method

For every site × exact-length stratum, fix the number of tablets and number of inscriptions with sign 400. Under no conditional association, tablet/sign overlap is hypergeometric. Convolve these distributions to obtain an exact null distribution for total overlap. The two-sided p value sums outcomes at least as far from the null expectation as observed. This differs from Fisher's probability-ordering definition for a single table; unadjusted Fisher tests are also supplied in results.json.

Estimate a common conditional odds ratio by exponential tilting of the stratum hypergeometric distributions; invert exact one-sided tails for an equal-tail 95% confidence interval. Common-odds estimates assume a common effect across included lengths and are descriptive here. Do not claim actual exchangeability or independence merely because duplicate checks passed.

A separate 200,000-draw conditional simulation for Mohenjo-daro produced p=.00204, consistent with the exact .00219 calculation at Monte Carlo precision.

## Sensitivities

- Delete each representative group/exact multiset pattern in turn: all nominal p values remain below .05. Worst Harappa p=1.74e-10; worst Mohenjo-daro p=.00868 (delete M-488).
- Delete an entire same-length, one-sign-variable multiset family: Harappa's 14 eligible families all retain strong association; worst p=2.11e-10. Mohenjo-daro has one such family containing at least two sign400 tablets: M-470 and M-1419 share the unordered core {158,400,806} and vary by sign 473 versus 467. Removing both gives OR(MH)=3.88, p=.0241. This is one limited family definition, not comprehensive control of formula dependence.
- Delete every four-sign inscription: Mohenjo-daro's nominal p rises to .118 (OR(MH)=3.11). Four of its seven sign400 tablets have length four. Thus its result is not robust to dropping that entire length class. Harappa remains nominally associated after deleting any one shared length class.
- The Mohenjo-daro tablet sample is only 29 representative groups. No classifier replication was run with a silently reduced threshold; this is a separately declared exploratory association analysis.

## Defensible conclusion and next action

Sign 400 is a concrete candidate for a relationship with catalogue object subtype: the association appears in both sites and survives exact-length adjustment and deletion of any one representative. This does not assign it a word, number, grammatical function, or sound. It does not contradict round09's failed full-model transfer: one selected feature can show a narrower association while a many-feature model generalizes poorly.

Photographically verify all seven Mohenjo-daro positive tablet representatives, subtype labels, and the sign400 identification before using this as a semantic anchor: M-470, M-478, M-482, M-488, M-1390, M-1408, M-1419. Include matched sign-absent tablets and sign-present square seals to avoid inspecting only supporting examples. Check molds/copies and excavation contexts, especially M-470/M-1419. Then freeze a rule and test on newly verified evidence not used to select sign400.

Reproduce: `python3 indus-lab/round10/matched/analyze.py` then `python3 indus-lab/round10/matched/family_sensitivity.py` (NumPy and SciPy required). Previous rounds are unmodified.

## Requested alternative sampling sensitivity

A final sensitivity starts again from all raw complete Y records with at least three signs, no000/999, and raw subtype TAB:B or SEAL:S. It deduplicates exact unordered sign multisets **within each city**, excludes within-city multiset groups with conflicting subtype labels, and chooses a deterministic representative. Patterns shared between cities are retained. This also changes physical-object/excavation grouping, so it is an alternative sampling check, not a controlled isolation of cross-site exclusion and not independent replication.

| Site | TAB:B sign400 | SEAL:S sign400 | Length-conditioned common odds ratio (95% interval) | Nominal p |
|---|---:|---:|---:|---:|
| Harappa | 78/213 | 5/158 | 17.19 (6.09–67.17) | 3.62e-12 |
| Mohenjo-daro | 10/40 | 36/694 | 6.26 (2.46–15.05) | 7.84e-5 |

The positive association persists under this alternative sampling. It therefore does not require round09's full combination of global cross-site exclusions and ID/excavation merging. This does not establish which exclusion rule mattered or remove selection effects.

Material remains a substantial unresolved difference. In the alternative sample, Harappa TAB:B comprises faience129, clay41, steatite7, unspecified36; square seals are steatite134, clay1, unspecified23. Mohenjo-daro TAB:B comprises clay18, faience9, paste1, unspecified12; square seals are steatite628, faience12, silver2, clay1, unspecified51. These counts are catalogue labels. There is inadequate balanced overlap to interpret the association as object purpose independent of material using this check. No additional feature scans were performed.

Reproduce this sensitivity with `python3 indus-lab/round10/matched/alternative_sampling.py`; results and selected rows are saved separately.
