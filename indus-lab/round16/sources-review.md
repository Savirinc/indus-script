# Round 16: source and copper-tablet audit

Reviewed 2026-10-10. This is an evidence/provenance audit, not an endorsement of a decipherment. The website and cloned repository can represent different snapshots; preserve the root agent's commit hash when combining findings.

## Actual reading coverage

| Source | Coverage in this audit |
|---|---|
| Bourdeau, https://dbourdeau.github.io/cyphersolver/indus.html | Entire rendered text inspected; sections 4, 12–15 examined closely. Web refs turn139view0, turn140view0. |
| Parpola 2005, https://old.harappa.com/script/indusscript.pdf | Complete 39-page PDF obtained; text read, including references, printed pp.28–66. Fig.4 printed58 rendered and visually inspected. Local working copy /tmp/parpola2005-audit.pdf. Web refs turn141view0, turn143view0, turn145view0. |
| Parpola 1994, *Deciphering the Indus Script*, Fig.7.14 pp.111–112 | NOT directly inspected in this audit. Its purported content is represented in the project's hand-entered TSV; that is a derivative, not an independent check. |
| https://github.com/mayig/indus-valley-script-corpus | README read in full, including conventions, limitations and feature-vector definitions. Full corpus not independently retranscribed. Web ref turn147view2. |
| CISI 1, Joshi–Parpola 1987 | Website's M-414 image/caption located; no fresh object-by-object copper-photo audit completed here. Earlier rounds' inspected CISI pages must not be counted as inspection of these different copper objects. |
| Fuls 2022/2023/2024; Mahadevan 1977/2014; Lüders1912; DHARMA; Mahadevan2003 | Bibliographic entries on webpage read. These complete works were NOT read anew for this audit. Do not infer verification from citation presence. |
| DAMOS, ORACC, Monier-Williams, ePSD2, CLICS4, Dravidian Database, WALS, Grambank, JMnedict, Turkish names | Identified as listed comparator/control inputs; source-specific versions, extraction and representativeness remain outside this audit. |
| Prize announcement and Tamil Nadu2025/2026 volumes | Follow-up link auditor read the prize article; source auditor subsequently read the reachable Tamil Digital Library homepage. Specific volumes remain unread; no finding made about their contents. |

The webpage's section15 contains a mixture of direct hyperlinks and plain bibliographic mentions. A mention is not evidence that a source has been checked.

## What the complete 2005 paper supports

Parpola's Fig.4 (p.58) is a schematic drawing, not photographs. B19/C6 pair the same drawn inscription with a horned archer (14 examples) and a fig/crab ligature (7). The next page makes the further inference that the sign names a deity, then develops a Dravidian and religious interpretation. Those are separate inferential steps. The paper does not enumerate all seven equations claimed on Bourdeau's page.

Fig.1 (p.51; note35) points to M-478A/M-479A as an offering-scene analogy for the U/V sign. A visual resemblance supports a pictorial hypothesis, not an established phonetic reading. On p.50 Parpola explicitly distinguishes pictorial meaning, intended meaning and sound.

The paper identifies missing bilinguals, short texts, uncertain segmentation and uncertain language as obstacles (pp.44–46). It also proposes a concrete material examination: microscopy of the interior of sealing M-426 / ASI63.10.201 to assess possible writing on a wooden support (p.39 n.14). That is an acquisition/inspection lead, not proof of lost manuscripts.

## Code and manual-input audit

Files inspected directly:

- `/tmp/indus-cyphersolver-audit/targets/indus/copper.py`
- `/tmp/indus-cyphersolver-audit/targets/indus/rebus/copper_tablets.tsv`
- `/tmp/indus-cyphersolver-audit/targets/indus/results/copper.md`

The TSV attributes its groups to Parpola1994 Fig.7.14. It describes `link` as a manually recorded relationship between groups and labels drawing-to-ICIT conversions approximate. The result reports 46 prototype groups,217 copies,28 ICIT-matched texts,15 drawing transcriptions,3 untranscribed texts.

**T1 prints preassigned links; it does not discover the equations.** It resolves the `link` field, deduplicates a pair of group labels, and prints whichever inscription is available. It does not assert that both groups have identical transcriptions, check photographs, or test semantic equivalence. This is useful tabulation of prior scholarship, not independent confirmation of meanings.

The generated table contains ten rows: separate a/b variants and an elephant/horned-tiger image-to-image case occur alongside sign-to-image cases. A claim of seven equations therefore needs an explicit grouping/exclusion convention. In particular, the code allows a linked image to be printed in its nominal 'sign side' column.

| Candidate relationship | TSV group linkage | Photograph acquisition target supplied in TSV |
|---|---|---|
| goat /749 | A2–C4a,b | M-504; M-597,M-1550 |
| rhinoceros /341 | B5–A11 | M-516,M-517 reverse; B5 object identification still insufficient (`sealid, motif Rhin`) |
| hare /753 | B7–C2 | M-534…542,M-1491…1494; M-1547 reverse |
| archer /777 | B19–C6 | M-582,M-583,M-585…588,M-1535,M-1536,M-1540,M-2050; sign-side list shared with C5 |
| goat /777 or778 | B9–C5a,b | M-547…549; M-603,M-604,M-1555…1558, with C5/C6 attribution unresolved in that field |
| long-horned bull /lens sign | B1–C1 | M-519,M-520; C1 lacks object identifiers |
| spotted bull /short text | B10–A7 | M-511,M-512; B10 lacks object identifiers |

These are leads from the derivative TSV, **not independently verified catalogue assignments**. Ellipses in its object lists must be resolved to explicit IDs, not expanded blindly.

## Image and corpus provenance

https://dbourdeau.github.io/cyphersolver/indus_tablets.jpg is captioned as the project's font-based rendering; it cannot independently verify cuts, damage, face pairing or motifs. https://dbourdeau.github.io/cyphersolver/indus_m414.jpg is attributed to CISI1p100 M-414a. Its presence does not verify unrelated copper equations.

The mayig repository explicitly calls itself work in progress. Its author transcribes seal impressions, records graphemes left-to-right, uses Parpola groupings with extra features, and adds a Wells crosswalk. Uncertainty is annotator-judged. It should be treated as a third transcription of overlapping physical evidence, not a third independent archaeological sample.

## Required next evidence, and admissible conclusions

1. Inspect lawful scans of Parpola1994 Fig.7.14 and its accompanying explanation. Record whether links denote full equality, shared subsequences, or reconstructed relationships.
2. Acquire paired-face photographs and catalogue entries for both sides of every linked group; record museum/excavation IDs, completeness, mirror orientation, variants, and whether multiple catalogues depict the same physical object.
3. Independently annotate inscription equality and image category with the proposed language/meaning hidden. Retain uncertain animal identification rather than forcing one species.
4. Encode the supported observation as `same inscription / alternate reverse representation`. Separately score hypotheses such as animal name, deity, office, issuing institution, or ritual association. None follows automatically from the observation.
5. Test whether the relationship predicts newly annotated objects or independent groups. Repeated copies of one prototype corroborate its existence but are not independent discoveries of the semantic rule.

Our recommendation: prioritize this bounded photographic audit over adding the copper signs as fixed semantic training labels. The distinction can materially change any subsequent language-scoring benchmark.
