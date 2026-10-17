# Indus research 11 — fixed text, variable stroke field

**The strongest result of this round is a concrete cross-face contrast:** the same three-sign face is paired with a U-shaped sign and different stroke groups on another face. H-315, H-316 and H-317 provide specific catalogue examples. This is a structural constraint consistent with a quantity field, not a translation or a claimed new archaeological discovery.

## The three-object comparison

| Catalogue object | Face A, transcribed in stored order | Face B, transcribed in stored order | Literal form of stroke group |
|---|---|---|---|
| H-315 |400–740–176|700–032|Two long strokes|
| H-316 |400–740–176|700–033|Three long strokes|
| H-317 |400–740–176|700–034|Four long strokes|

Here700 labels the U-shaped sign, while740 is a different sign on faceA. Numbers such as032 are modern identifiers, not ancient written decimal numbers. The interpretation of032 as a two-stroke shape comes from the graphic form, not arithmetic on the label.

Coordinator and independent photographic checks find two, three, and four separate strokes respectively beside the U; the outermost fourth stroke on H-317 is less clear. Face A matches at the level of three broad glyph structures; fine epigraphic details remain unverified.

The original catalogue plates are CISI1 printed225/PDF261 forH-315, and printed226/PDF262 forH-316/H-317. All three are in the incised-tablet sections. Their excavation identifiers differ:10185c,2480,3025. The page renderings and an independent photographic review are included in the evidence package. Mirrored impressions and alternative exposures are views of the same object, not additional objects.

The narrow working model is **a stable text field paired with a variable stroke field**. A quantity or count is plausible; a category or rank remains an alternative. The fixed text might concern a commodity, person, institution, activity, or something else. Neither the variable field nor the fixed text currently tells us a spoken word, a language, a unit of measure, or whether an exchange actually occurred.

## How broadly the pattern appears in this dataset

We joined the supplied text rows by ID stem, preserving which texts belong to the same catalogue group. We searched for simple complete two-token rows containing700 and a member of the long-stroke series031–038, paired with an otherwise identical set of recorded texts on the other face(s).

The extraction finds27variable families, all fromHarappa, comprising120selected face rows and119ID stems. These are families selected because they vary, not a rate among all contexts. Requiring every supplied row of a stem to be complete and readable leaves the same result. This cannot certify unrecorded faces or object identities.

The largest family has the other-face text400–740–176, with032/033/034variants. It contains33selected rows but32ID stems: H-355 has two identical quantity-candidate faces. An independent audit also found H-316 andH-1304 share excavation identifier2480 and identical texts—a possible catalogue alias. The three chosen examplesH-315/H-316/H-317 are not linked to each other by that issue. Deduplicating repeated text configurations leaves the two/three/four contrast intact.

All contributing stems have internally consistent site, catalogue ID, excavation ID, material, type and side-count metadata; their row counts equal reported sides. This supports the dataset join, not proof of119distinct archaeological objects. The larger family spans different raw object types; only the illustrated trio is asserted to share the incised-tablet catalogue classification.

## Why this changes our research approach

Earlier classifier experiments required at least three signs per row and selected only one representative row per duplicate group. Those rules were appropriate to their declared prediction task, but could omit two-sign faces and lose the relation between the two sides. A whole-object representation exposes a relationship those experiments were not designed to test.

This is a useful methodological lesson: a tablet is an object with linked faces, text, pictures and archaeological context. Flattening it into one line can discard precisely the relationship we are trying to understand. Future models should keep faces linked, while separately controlling copied texts, molds, and catalogue aliases.

## M-478: a corrected concern

Our earlier warning that the photograph looked too long for its four-token transcription was too strong. Rendering the exact four glyph references made a plausible central alignment visible: comb → human-like figure with flanking uprights → U-shaped unit → grouped short strokes. The flanking motifs need not be text tokens, and one encoded sign can contain several strokes. An independent reviewer reached the same revised assessment forM-478 and its parallelsM-479/M-480.

This supports a plausible alignment, not an exact count of every comb arm or a complete epigraphic reading. The earlier four-token mismatch should no longer be used as evidence that the record is incorrect. Parpola2011discusses the four-stroke/U pairing, but itsFigure49caption saysM-474 while its prose saysM-478; the originalCISI1printed115plate labelsM-478. This citation discrepancy is preserved.

## Quantity hypothesis and prior research

The stroke-plus-U direction is established scholarly territory. Rao2018discusses a group of miniatureHarappa tablets and explores a ration-token interpretation using comparisons with proto-Elamite/proto-cuneiform material. Parpola2011proposes a vessel/offering interpretation forM-478. These are hypotheses and comparative arguments, not bilingual translations. Our calculation reproduces a tractable structural pattern and adds an auditable object/face comparison; no novelty claim is made.

The first targeted extraction used short-stroke codes001–007:13eligible rows and6unique strings contained adjacency to700. Inspection then revealed a distinct long-stroke series031–038; an explicitly post-hoc extension finds428rows but only32unique strings,393rows being two-token texts. Repeated copies andHarappa dominate the raw counts. We preserve both analyses rather than silently redefining the original test. The two stroke series are not assumed semantically equivalent.

## A route that did not hold up

The sign400/animal-label follow-up was inconclusive. Harappa has6/9Gavi-labelled tablet representatives containing400 versus12/43with other specific labels, but the length-adjusted interval is wide and includes no association. Mohenjo-daro has noGavi-labelled representatives in the selected sample, so there is no within-city replication. Its positive examples are labelledMult orNone, neither of which safely proves a particular motif absent. Photographically verified multiple-motif labels are needed before fitting a semantic model to imagery.

## Next discriminating evidence

Keep this three-object contrast as an inspected reference set. For other families, check original face pairings and stroke counts without assuming the numerical interpretation; retain contrary and unclear cases. Test the alternatives—quantity, category, workshop convention—against excavation context, mold relations, materials and independently established numerical series. A quantity hypothesis must eventually explain more than repeated tally-like shapes, including which values occur where and why. Do not assign a commodity or language merely because the pattern resembles accounting.

## Reproduction and sources

The evidence package includes quantity_audit.py, long_stroke_audit.py, crossface_audit.py, crossface_strict_audit.py, JSON results with all supporting IDs, independent code and image reviews, and the original-page renderings. The cross-face search is exploratory and was motivated after inspecting adjacency results; no selection-adjusted significance or prospective validation is claimed.

Corpus SHA256:c22d39c3c2bda869c67fb01e7f2b4cdc64cc424405eafe89550d1702216b3429.

- Original CISI1: https://ignca.gov.in/Asi_data/76884.pdf — printed225–226and115.
- Rao2018, *The Indus Script and Economics*: https://www.harappa.com/sites/default/files/pdf/The-Indus-Script.pdf
- Parpola2011: https://www.harappa.com/sites/default/files/pdf/Parpola_Asko_2011._Crocodile_in_the_Indu.pdf — printed40–41.
- Raw transcription: https://raw.githubusercontent.com/field-cady/indus_valley_script_corpus/main/inscriptions.csv
