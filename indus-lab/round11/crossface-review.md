# Independent review: cross-face stroke variants

Reviewed crossface_audit.py, crossface_strict_audit.py, both output files, and the underlying raw rows. No p values were calculated. No original photographs were independently inspected in this review; photographic confirmation remains the coordinator's separate check.

## What the implementation actually establishes

The script groups rows by the integer part of the supplied ID. It identifies complete, simple two-token rows containing 700 plus one code 031–038, then groups these by site and the set of all other qualifying row text strings from the same ID stem. It retains only families with multiple stroke-code variants. Therefore the output concerns repeated **non-selected-face text sets**, not necessarily identical whole objects, image programs, manufacture, or every feature of the other faces.

The strict version rejects an entire stem if any supplied row is incomplete, contains000/999, or is not a simple full text. Its output is exactly equal to the first version. Thus silent exclusion of an incomplete/non-simple supplied face does not create the reported families. This says nothing about unrecorded faces or mistakes in the source.

There are 27 reported families, all at Harappa, comprising 120 selected rows and 119 distinct ID stems. These families were selected for showing variation; 27 is not a rate of variation among all possible contexts. No generalization to all sites follows.

## ID-stem grouping audit

All 119 contributing stems are internally consistent in site, CISI identifier, excavation identifier, object type, material, and reported side count. For every contributing stem, the number of raw rows also equals its reported `sides` value. Raw full IDs are unique across all 5679 rows. This supports using the stem as the dataset's face-grouping key for this calculation.

It does not prove that distinct stems are distinct archaeological objects. There is at least one concrete alias risk: H-316 (stem1338) and H-1304 (stem5470) both have excavation identifier 2480 and the same pair of texts. Preserve both source records, flag the possible duplicate, and do not present them as independently verified objects.

## Largest family and duplicate influence

The largest family has non-selected-face text `+400-740-176+` and codes032,033,034 paired with 700 on another supplied face.

| Code | Selected face rows | Distinct ID stems |
|---|---:|---:|
| 032 | 2 | 2 |
| 033 | 22 | 21 |
| 034 | 9 | 9 |
| Total | 33 | 32 |

H-355/stem1374 has three supplied rows: the 400-740-176 text plus two identical700-033 face texts. It contributes two selected rows but only one stem. The H-316/H-1304 possible alias contributes another non-independent033 pair. Merging only that possible alias would reduce the largest family to 31 candidate object groups, without removing any of the three code variants. This is a sensitivity count, not proof that there are 31 physical objects.

The chosen examples H-315, H-316, H-317 are distinct stems, each with two rows and a single constant-context face. Their excavation identifiers are 10185c,2480,3025 respectively. No dataset-level alias links those three to one another. Their encoded pairs are 700-032,700-033,700-034. Original publication images should confirm both the face pairing and the target stroke groups.

Most repetitions are copies of a small number of text patterns. Counting each copy as a separate independent instance would exaggerate evidential strength. The structural contrast survives deduplicating complete encoded text patterns: the three stroke variants still exist. The largest family contains five exact full-object text multisets because one034 instance reverses stored pair order, and H-355 repeats the033 pair on a third face. If order and multiplicity are ignored, it reduces to three variable-code configurations.

## Context and orientation limitations

- `sorted(set(other))` intentionally discards ordering and multiplicity of non-selected face texts. No contributing stem in these outputs actually repeats its non-selected text, so the multiplicity collapse is not responsible for this result. Still, the future representation should preserve face IDs and full face lists.
- All selected 700/stroke faces are excluded from `other`, so their number and placement are not held constant. H-355 is the observed example of this distinction.
- The two-token target accepts either order. H-933/stem1813 has `+034-700+`; the others in the largest family use 700 first. Say "700 paired with code032/033/034," not that the script establishes a universal reading order.
- The non-selected strings are matched in stored order; reading direction and mirrored impressions are not normalized. This is conservative for finding identical stored strings but can miss equivalent contexts.
- Grouping does not hold object type, material, date, iconography, or excavation context constant across stems. The largest family contains raw TAB:I, TAB:B, and SEAL:R labels; some raw types may need publication review. Do not describe all 32 stems as verified identical tablet types.
- Calling an internal list `quantity` does not establish that the marks encode quantity. Catalogue numbers are identifiers; stroke appearance, grouping, and the relation to counts require separate evidence. Font-template inspection is not inspection of each artefact.

## Defensible claim

**Within this transcription dataset, a repeated Harappa face text 400-740-176 is paired on another recorded face with 700 plus different members of the 031–038 stroke-code series, specifically 032,033,034. This contrast survives strict inclusion of all supplied faces and removal of obvious within-object repeated rows.**

If photographs confirm H-315/316/317, those examples support a limited physical-artifact claim: the same three-sign face coexists with systematically different stroke groups alongside the same other sign. That constrains a future reading to explain a stable component and a variable component. It is compatible with numerical or classificatory interpretations, but does not identify units, commodities, people, grammatical roles, sound values, or a unique language. It is not by itself a new decipherment or proof of a transaction.

Next concrete step: retain a photographed face-by-face record for H-315/316/317, mark the H-316/H-1304 alias, and test whether the same visible variation occurs in additional preselected families. Do not choose only families that visually confirm the transcription.
