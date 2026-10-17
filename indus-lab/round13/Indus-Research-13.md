# Indus research 13 — testing the vessel hypothesis

10 October 2026. Status: photographic and data acquisition audit; no capacity fit and no decipherment.

## Concrete progress

We located and inspected original catalogue photographs of the three calibration vessels: CISI Volume 1, printed pages 233–234 (PDF pages 269–270). A separate reader examined the plates without consulting the transcription first. We also searched the entire supplied transcription dataset for complete, simple pottery inscriptions consisting of sign 700 plus one long-stroke code 031–038.

| Object | Supplied transcription | Catalogue stroke interpretation | Physical capacity available here? |
|---|---|---|---|
| H-370 | 037 | Seven strokes; no 700 | No |
| H-371 | 700–036 | Six strokes plus 700 | No |
| H-372 | 700–033 | Three strokes plus 700 | No |

H-370's seven separate long marks are clear. H-372 has three separate near-parallel marks and a distinct angular form. H-371 requires segmentation of the rightmost marks: the catalogue interprets six strokes followed by an angular sign. The initial blind reader saw seven near-upright traces and a separate oblique feature. That discrepancy concerns whether two traces are arms of one sign, not automatically an erroneous catalogue count. It must not be resolved by selecting the segmentation that gives the best capacity fit. Final independent adjudication: six standalone strokes are clear; the remaining two traces could be arms of one angular sign, but their lower junction is not definite in this scan. The segmentation remains unresolved. No raw transcription was changed.

## What a numerical hypothesis must predict

If the same unit applies to all three, their capacities should be proportional to 7:6:3, within independently justified manufacturing and measurement uncertainty. But including H-370 adds the assumption that strokes without 700 express the same unit. A strict same-form comparison initially has only H-371 and H-372: the predicted ratio is 2:1 under the catalogue segmentation. Neither prediction has been tested against independently verified capacities in this round.

These ratios are conditional mathematical consequences of the proposed rule, not measured ratios or a reading of the script. An unresolved mark must remain an alternative segmentation before any fit.

## Search for additional test objects

The reproducible extraction returned six records. Two are the calibration vessels H-371/H-372; four are acquisition candidates:

| Record | Catalogue ID | Excavation reference as supplied | Catalogue stroke count |
|---|---|---|---|
| 701.1 | H-2272 | H95-2831 | 3 |
| 717.1 | Not supplied | H95-4614-53Figure 40.01 | 3 |
| 3810.1 | M-1588 | Not supplied | 1 |
| 3912.1 | H-1550 | H90-2975 | 1 |

All six records have zero in the three dimension fields. Those zeros are unusable/missing data, not measurements of zero size. A complete inscription does not establish a complete pot: some candidates may be sherds whose original capacity cannot be recovered. No candidate is yet an independent capacity-validation case. Catalogue records and photographs must establish object identity, preservation and measurement availability first.

## Acquisition result and decision

Wells 2015's published method approximates vessel volume with an ellipsoid and adjusts dimensions for walls and the mouth. We retrieved that methodological prose, but not the numeric cells of Table 4.1. The official sample omits them; JSTOR reports no access; an exposed 2018 volume upload contains frontmatter rather than the relevant chapter. No access restrictions were bypassed. Kalibangan K-090 cannot serve as independent confirmation if its photograph's scale is inferred from the proposed reading itself.

The precise missing source is an authorized copy of Wells 2015, printed pages 60–62, especially Table 4.1 and its correction instructions. Even after obtaining it, the calculated capacities need a geometry audit; agreement with the same selected vessels used to choose a unit is calibration, not new confirmation.

Next priority: acquire that table, independently resolve H-371's sign boundaries, and determine whether the four additional candidate records preserve measurable vessels. Do not run a regression against invented dimensions or infer scale from the hypothesis.

## Reproduction and sources

- Primary photographs: Joshi and Parpola, CISI Volume 1, printed pp.233–234: https://ignca.gov.in/Asi_data/76884.pdf
- Publisher sample and table locations: https://www.archaeopress.com/Archaeopress/DMS/3608E8E0F92C4920AE82709E2A32643F/9781784910464-sample.pdf
- Publicly indexed Wells chapter prose (secondary hosting of the author's text): https://ru.scribd.com/document/1007007442/The-Archaeology-and-Epigraphy-of-Indus-Writing-Bryan-K-Wells-Andreas-Fuls-Archaeopress-Publishing-Ltd-Oxford-2015-Archaeopress-Publishing
- Access status: https://www.jstor.org/stable/j.ctvr43jmf
- Supplied transcription data: https://github.com/field-cady/indus_valley_script_corpus

Run `python3 indus-lab/round13/extract_candidates.py`. The bundle contains the input CSV, extraction code, six candidate records, contract and two catalogue page renders. These are derived records and catalogue reproductions, not untouched original objects. All currently studied material is exposed; no untouched validation is claimed.
