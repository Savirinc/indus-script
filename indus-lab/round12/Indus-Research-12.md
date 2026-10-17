# Indus research 12 — independent experimental design

10 October 2026

The research has moved from collecting more patterns to selecting observations that can distinguish competing explanations. Three agent reviews covered prior literature, evidence integrity and experimental design. We built a complete object/face evidence model and executed one bounded structural test. No decipherment or semantic breakthrough is established.

## Completed work

| Deliverable | Result |
|---|---|
| Object/face model | All 5,679 source rows preserved within 4,694 provisional ID-stem groups |
| Provenance | Raw CSV SHA-256 retained; raw sign strings and token spans preserved |
| Identity audit | 20 possible site/excavation-ID alias groups; six have equal complete text multisets; none automatically merged |
| Interpretation isolation | Proposed translation, Sanskrit, class, cult and notes columns excluded from analytical labels; untouched CSV retained |
| Evidence database | JSON and SQLite objects, faces and alias candidates |
| Reviewed corrections | Three prior object-type corrections retained separately; none overlaps the new test's eligible objects |
| Claim ledger | Structure, physical-function hypotheses and readings explicitly separated |

These are catalogue coverage counts, not a claim that we possess every Indus inscription or that 4,694 distinct physical objects have been verified. The model preserves every recorded face; it does not imply every physical face is known.

## Executed experiment

Question: when one recorded face contains sign 700 with one of the long-stroke codes 031–038, does its stroke code concentrate in particular complete remaining-face contexts?

The protocol screened all 4,694 stems, not just previously selected variable families. It required complete simple inscriptions, exactly one target face, at least one other face, known consistent site/material/type and a recorded face count matching the supplied sides field. It retained 278 stems, seven strata and 189 contexts.

Of 530 same-context pairs, 338 also shared the target code. In 999 within-stratum shuffles, this count ranged from 165 to 273, averaging 195.52. The numerical upper-tail reference is 0.001, but it is not a calibrated claim of independent archaeological replication: copies and production families are not known independent units.

The adversarial check is decisive. Collapsing repeated context/code configurations leaves 209 configurations. Same-context/same-code pairs then become impossible by construction. A valid control respecting those unique configurations always scores zero. A naive shuffle would manufacture duplicate configurations. We therefore withhold a sensitivity p-value and stop escalating this statistic.

What survives: structured repetition in the supplied records. What does not follow: quantity, category, sound, word meaning or independent replication. This is exploratory analysis of already exposed data.

## Chosen next route: inscriptions versus physical measurements

Quantity and arbitrary category labels can explain the same distribution of sign strings. More text-only computation cannot distinguish those unrestricted explanations. Physical evidence could constrain a narrower hypothesis.

Wells's 2015 book identifies a study of inscribed vessels: Figure 4.6 on printed page 60, Table 4.1 of measurements and volume calculations on page 61, and Table 4.2 of estimated units on page 62. The official publisher sample verifies these references. The acquisition targets are H-370, H-371 and H-372. Actual measurement-table cells have not yet been independently retrieved and verified in this round, so no capacity fit was performed.

The test will separate measured dimensions from calculated volume. Three dimensions do not uniquely determine the interior capacity of a bulging pot. A model needs direct capacities or defensible geometric uncertainty. Under the narrow hypothesis V = k*u, capacity-per-stroke intervals must share a common unit u. Failure rejects that rule; agreement only supports compatibility. An additional independently measured vessel, evaluated after freezing the rule, would be more informative than further fitting these selected examples.

## How research decisions are now made

Evidence curator → literature review → competing predictions → fixed protocol → implementation → adversarial review → acquire evidence or reject/refine the hypothesis.

Agents do not vote a meaning into existence. The lead selects methods without asking the user to supply technical direction. Every claim carries provenance, rivals, evidence grade and a stopping condition. More computation is justified only when it can resolve a live uncertainty. The present corpus has no untouched validation set.

Priority is obtaining and auditing the vessel measurements and photographs. The blocked acquisition is documented, not replaced with guessed numbers. Linguistic sound values remain downstream of stronger constraints.

## Sources and reproducibility

- Raw transcription source: https://github.com/field-cady/indus_valley_script_corpus — a derived transcription dataset, not untouched archaeological evidence.
- Official Wells 2015 sample: https://www.archaeopress.com/Archaeopress/DMS/3608E8E0F92C4920AE82709E2A32643F/9781784910464-sample.pdf
- Primary plate source for earlier photo checks: CISI Volume 1, https://ignca.gov.in/Asi_data/76884.pdf
- Prior research comparison: Rao 2018, https://www.harappa.com/sites/default/files/pdf/The-Indus-Script.pdf ; Fuls 2010, https://www.epigraphica.de/indus/help_onlinedatabase.pdf

The accompanying bundle includes the source CSV, full model, SQLite database, scripts, inclusion ledger, shuffle results, agent reviews, correction overlay and operating protocol. Run `python3 indus-lab/round12/build_evidence.py` to rebuild the evidence model and `python3 indus-lab/round12/null-test/run.py` to reproduce the bounded test. The latter uses only the Python standard library. Preserve the archive directory structure.
