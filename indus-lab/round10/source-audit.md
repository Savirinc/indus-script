# Round 10 source audit — 2026-10-10

## Verified object-code meanings

Andreas Fuls, *Corpus of Indus Inscriptions* (2022), section 1.1, printed p.5, expressly defines:

| Code | Definition |
|---|---|
| TAB:B | bas-relief tablets |
| TAB:I | incised tablets |
| TAB:C | copper tablets (source text misspells copper as “cooper”) |
| TAG | clay objects carrying impressions of intaglio seals |

These describe objects/manufacturing categories, not deciphered functions. TAB:B is not a synonym for a sealing, and B does not mean baked. Source: https://www.researchgate.net/publication/373522666_Corpus_of_Indus_Inscriptions ; retrieved web refs turn69view1/turn70view0, lines606–635. This establishes what the code scheme means; individual mirrored records still need comparison with catalogue objects.

## Sign 400 mapping status

The acquired glyph table maps ICIT/Wells 400 to private-use font character U+E24A; population-script.sql independently contains the same pair. Our acquired `icit_m77_map.tsv` associates400 with Mahadevan MSg176 (93 aligned pairs, share0.98, ICIT count303). This is an empirical crosswalk, not an authoritative one-to-one mapping. The separate acquired CISI sign-description table maps Parpola P098 to Mahadevan M176 and describes a vertical line with small strokes projecting from one side throughout its height. Chaining these supports a candidate 400≈M176≈P98, which must remain provisional until comparing the published concordance and glyphs.

Fuls2023 *A Catalog of Indus Signs* explicitly includes concordances with Mahadevan at printedp37 and Parpola atp45. Its publicly parsed preview did not expose the400 entry or those tables; no direct verified exact equivalence claimed.
Source: https://www.researchgate.net/publication/373522673_A_Catalog_of_Indus_Signs (turn77view0). An unrelated modern webpage's ICIT176 is NOT Mahadevan176; do not confuse namespaces.

## Requested object records and photo access

All five requested object IDs are TAB:B in the acquired inscriptions.csv. Text is stored in physical left-to-right display order; R/L direction must be applied separately. Dates/materials below are source-record metadata, not independent verification.

| CISI object | ICIT text ID | Material | Stored string | Raw `time` | Raw `period` | Raw `phase` | Photo source |
|---|---|---|---|---|---|---|---|
| H-172 |1207.1|Steatite|+712-840-400-740-440+|-|-|-|CISI1 printedp207, scanpage243 (`cisi1-page243.png`); Parpola2011 Fig51 p41|
| H-174 |1208.1|Clay|+400-740-017-503+|Period 3C-3|-|Stratum II|CISI1 printedp207, scanpage243 (`cisi1-page243.png`); Parpola2011 Fig41 p35|
| M-470 |2955.2|Faience|+400-158-806-473+|Period 3C-2|Intermediate|I|CISI1 printedp113, scanpage149 (`cisi1-page149.png`)|
| M-478 |2962.1|Clay|+400-097-700-004+|Period 4|Late|I|CISI1 printedp115, scanpage151 (`cisi1-page151.png`)|
| M-482 |2966.1|Clay|+400-740-803+|-|-|-|Parpola2011 Fig44 p36, credited toCISI3.1 p387|

The three chronology columns reproduce the CSV fields literally; they are not reconciled chronological dates. A dash is the source's missing-value marker. M-478's four-token record must not be assumed to represent the entire photographed inscription: the plate shows more detail and a potential segment/whole-inscription mismatch is under photographic review.

M-470 has a separate other-side text2955.1 consisting of+540+. Counting its two sides as two independent objects would be wrong.

Accessible author-supplied photographic reproductions:
https://www.harappa.com/sites/default/files/pdf/Parpola_Asko_2011._Crocodile_in_the_Indu.pdf
Asko Parpola2011, *Crocodile in the Indus Civilization and later South Asian traditions*.
The cover is PDF page0 and numbered article page1 is PDF page1, so zero-based screenshot pages35,36,41 carry the figures described. Screenshots retrieved as turn76view0/1/2. Figure51 specifically creditsCISI1 p207; Figure44 creditsCISI3.1 p387. This is photographic reproduction after original catalogue, not a new independent photograph.

Parpola expressly identifies H-174 as having many duplicates. His semantic readings (including religion, sacrifice and Proto-Dravidian rebus proposals) are hypotheses and must not be imported as labels. Use photographs, object identification and clearly separated visual description only.

CISI1 original volume online: https://ignca.gov.in/Asi_data/76884.pdf . Search-engine indexed plate label confirms H-170–175, tablets in bas-relief, printedp207 (turn68search33). Direct webopen failed initially; the local primary PDF download subsequently completed, and the coordinator supplied the verified scan/printed-page locators listed above. Alternate archive source already recorded in project manifest.

## Prior art relevant to this project

Fuls2010 official ICIT documentation groups817,861,820 on printedp3 using adjacent-sign distributions. Our earlier cluster is replication of a known structural pattern, not a newly discovered grouping. Documentation also discusses eliminating duplicate-text “TAB-effect,” graphic labels that are not meanings, and site/time/type controls.
https://www.epigraphica.de/indus/help_onlinedatabase.pdf (turn69view0).

## Concrete next step

Audit photographed surfaces for400 presence/absence, line orientation and adjacent iconography, including matched no-400 controls. Keep text-side, physical object and mould-family identities distinct. TAB:B comparisons control manufacture more closely than poolingTAB:B/TAB:I/TAB:C, but not chronology/material/provenance. Do not treat photo availability as random, nor the resulting small convenience sample as independent statistical replication.
