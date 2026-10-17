# Indus research 10 — a tangible, bounded association

**Finding:** in the acquired transcription corpus, the comb-like sign labelled ICIT400 is much more frequent on bas-relief tablets than on square seals, in both Harappa and Mohenjo-daro. The association survives comparison at the same inscription length and a different duplicate-removal rule. It remains an exploratory object-category association, not a reading of the sign or a novel discovery claim.

## The matched comparison

The previous round pooled bas-relief, incised, and copper tablets. Fuls's original corpus defines these as TAB:B, TAB:I, and TAB:C. They are distinct categories, and the two cities have very different mixtures. This round restricts comparison to TAB:B versus SEAL:S (square seals).

| Site | Bas-relief tablets containing400 | Square seals containing400 | Length-adjusted odds ratio, nominal95% interval |
|---|---:|---:|---:|
| Harappa |64/163 —39.3%|5/148 —3.4%|16.37 [5.65,65.14]|
| Mohenjo-daro |7/29 —24.1%|35/671 —5.2%|5.15 [1.68,14.21]|

Counts refer to the earlier round's retained representative groups, not a verified physical-object census. Only complete rows with at least three signs, no000/999, and the existing duplicate/conflict exclusions enter. Separate faces are not all concatenated. Odds ratios are not probability ratios.

We condition on exact inscription length within each city. The test fixes both category counts and sign-presence counts at each length, then calculates the exact distribution of their overlap. Nominal two-sided p values are1.13e-10 and.00219. The sign and comparison were chosen after earlier exploration; these values and intervals do not account for that selection and cannot be presented as independent discovery confirmation. No classifier threshold was quietly lowered: this is an explicitly exploratory association study, not a rerun of the frozen classifier.

## Checks that strengthen—and limit—the finding

Removing any single representative leaves the nominal association in both cities. Removing the related Mohenjo-daro M-470/M-1419 pair also leaves a positive association (nominalp=.0241). But removing the entire four-sign length class weakens Mohenjo-daro to nominalp=.118. Its evidence rests on only seven positive tablet groups, and is not robust to every reasonable perturbation.

We also rebuilt the sample directly from raw eligible rows, deduplicating sign multisets separately within each city and retaining patterns shared between cities. Under that different sampling rule:

| Site | Bas-relief tablets | Square seals | Length-adjusted odds ratio |
|---|---:|---:|---:|
| Harappa |78/213 contain400|5/158 contain400|17.19|
| Mohenjo-daro |10/40 contain400|36/694 contain400|6.26|

This is sensitivity analysis on the same underlying corpus, not independent replication. It shows that the original global duplicate exclusions are not necessary for the observed positive association. Several grouping choices changed together; it does not isolate the effect of any one choice.

Material remains strongly confounded with category: square seals are predominantly steatite, whereas the tablets include clay and faience. Dating, workshops, mold families, image selection, catalogue errors and transcription conventions also remain potential explanations. Length adjustment alone cannot remove those differences.

## What the photographs establish

We located plate images for all seven Mohenjo-daro positive representatives: M-470, M-478, M-482, M-488, M-1390, M-1408 and M-1419. We also inspected H-172 and H-174. An independent agent reviewed five of these objects against the font reference without assigning meanings.

The broad comb-like shape is visible especially clearly on H-172, H-174 and M-478. Obtaining the higher-quality original CISI2 scan also resolved broad comb morphology on M-1390 and M-1419; M-1408 remains damaged/uncertain. The reference font has a stem with six lateral arms, but exact arm counts and boundaries cannot be verified consistently in all photographs. H-174 itself has two comb-like end forms coded differently in the transcription: resemblance alone is not an exact sign identification.

M-478's complex photographed band has not yet been aligned with its four-token database text. This may involve compound signs, segmentation or a record issue; it is not automatically proof that the transcription is wrong. M-470's database row suffix.2 must not be equated with photographic faceB: the relevant sign row is photographed as A.

Thus **the numerical result is still based on transcriptions, with partial photographic support—not a fully photo-validated frequency claim**. Complete positive and negative controls, exact sign alignment, and object/mold identities remain outstanding. Original and impression views of one object were not counted as separate observations.

## What this gives us

A practical constraint for future explanations: any proposal for sign400 must account for its distribution across object categories, cities, materials and text positions. Possible causes include a convention associated with a document type or activity, workshop practices, chronology, or transcription choices. None currently supplies a word, sound, quantity or grammatical function.

The earlier whole-model transfer failure remains valid. A selected single sign can show a narrow association while a many-sign model generalizes poorly. The new result neither overturns that test nor establishes why it failed.

Next decisive work is exact photo-to-token alignment for these cases and matched controls, especially M-478, followed by a rule frozen before testing newly verified material. Do not keep trying alternative analyses until a p value is small; retain the negative and fragile results alongside the positive ones.

## Correction to the novelty record

Fuls's2010 database documentation already groups817,861 and820 through neighboring-sign distributions. Our earlier finding is replication of published work. This is useful evidence that the machinery can recover known structure, but it must not be called our discovery. No novelty claim is made for the sign400 association without a broader prior-art review.

## Evidence and reproduction

- `matched/analyze.py`: exact length-conditional tests, intervals, leave-one-group checks.
- `matched/family_sensitivity.py`: limited formula-family deletion check.
- `matched/alternative_sampling.py`: second duplicate/sampling policy.
- JSON files preserve included IDs, counts, statistics and sensitivity outputs.
- `source-audit.md`, `photo-review-a.md`, and `photo-audit-coordinator.md` separate source definitions, independent image observations and unresolved matches.
- `photos/` contains unenhanced published page renderings and a clearly non-archaeological font reference.

The underlying corpus SHA256 remains c22d39c3c2bda869c67fb01e7f2b4cdc64cc424405eafe89550d1702216b3429.

Sources:
1. Fuls2022, *Corpus of Indus Inscriptions*, object definitions: https://www.researchgate.net/publication/373522666_Corpus_of_Indus_Inscriptions
2. CISI1 original catalogue: https://ignca.gov.in/Asi_data/76884.pdf — printed207,113,115,119.
3. CISI2: https://archive.org/download/corpus-vol-2_202409/CorpusVol2.pdf — printed184,189,191.
4. Parpola2011 photographic reproductions: https://www.harappa.com/sites/default/files/pdf/Parpola_Asko_2011._Crocodile_in_the_Indu.pdf — Fig44p36 and Fig51p41. Proposed semantic readings in that paper are not adopted.
5. Fuls2010 database documentation, p3: https://www.epigraphica.de/indus/help_onlinedatabase.pdf
6. Acquired transcription source: https://raw.githubusercontent.com/field-cady/indus_valley_script_corpus/main/inscriptions.csv
