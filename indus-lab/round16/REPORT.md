# Indus research 16 — source audit and a corrected research direction

Audit date: 10 October 2026. Prepared for Arham Partap Jain.

## What changed

Your criticism was correct. Daniel Bourdeau's page contains substantial prior work, explicit failures and constraints that should have shaped our earlier experiments. Our round 15 hidden-key exercise is a useful engineering baseline under easier assumptions; it is not a new decipherment route. This audit corrects that framing.

We read the complete Indus webpage, visually inspected all three embedded images, reviewed its direct-link inventory, read Parpola's complete 2005 paper, inspected selected underlying implementations and saved results, and audited ten additional public repositories. The accompanying reports identify exact coverage. This is not a claim to have independently verified every test, read every cited book, or audited every file in the repository. No third-party models were rerun during this audit.

Primary page: https://dbourdeau.github.io/cyphersolver/indus.html

Code: https://github.com/dbourdeau/cyphersolver/tree/main/targets/indus

Pinned checkout: `843165c369a9c35658b1a7656860e06abd7a5de3`. The page and repository are different snapshots: the page reports 247 sets / 2,727 hypotheses; current notes record completed results through 349, with 350 present as code/registration but no saved result. Never combine those counts as one simultaneous experiment.

## The page, section by section

These are summaries of Bourdeau's reported findings, followed by our audit implications. They are not independent reproductions.

| Section | What it covers | What we must carry forward |
|---|---|---|
| 1. Corpora/signs | ICIT-derived exports, M77, crosswalk and font sign IDs | Different transcriptions can describe the same objects. IDs are catalogue labels, not values or meanings. |
| 2. Lecture checks | Fish combinations and frequency claims in Parpola 2005 | Check counted objects, copies and variants before interpreting frequency. |
| 3. Tamil readings | Compound matching with chance baselines | Finding a plausible word is insufficient when many synonyms/readings were tried. |
| 4. Copper tablets | Proposed seven sign–image equations | Source links are manually supplied; photograph verification is still required for our use. Association does not uniquely fix a word. |
| 5. Language controls | Sanskrit/Sumerian alternatives and fish–star comparisons | Lexical coincidence and selective flexibility can produce attractive false readings. |
| 6. Registered tests | Hypothesis/result ledger and controls | Useful audit trail; this audit did not verify every registration's historical commit order. Repeated reuse of holdouts remains a concern. |
| 7. Structure | Ending slots, sign order, line breaks, numeral contexts | Keep observable positional facts separate from labels such as noun, suffix or name. |
| 8. Other transcriptions/keys | CISI comparison and known-script tests | A scorer recognizing a supplied key is a different task from recovering an unknown key. |
| 9. Names | Capture–recapture and Ur III comparison | The narrowed conclusion is individuality of compositions, not proven personal names. |
| 10. Place/time | Findspots, levels, variants, foreign seals | Archaeological metadata and object duplication require separate validation. |
| 11. Language order | Typology and name-list comparisons | Genre-matched Japanese decoys overturn an apparent South Asian language preference. Typological exclusions depend on unproved grammatical interpretations. |
| 12. Bench | Meaning, controls, unseen texts, structural predictions | Project-defined progress measures are not official decipherment criteria or probabilities. |
| 13. Open problems | No compelled sound values; language unknown | New independent evidence or a demonstrably better discriminating test is needed. The author's internal stopping point is not a proof of impossibility. |
| 14. Withdrawals | Sound-sign shortlist, numeral systems, office/name, convergence and picture claims | Preserve these corrections; do not resurrect superseded results from older files. |
| 15. Sources | Corpora, books, comparators, code, government volumes | Citation presence is not verification. Our source report lists unread works and unavailable material. |

The page calls early Brahmi donor inscriptions 'near' the Indus in time. Even 200 BCE is approximately 1,700 years after 1900 BCE. They can be genre comparators, but they are not contemporaneous Indus evidence or an established linguistic bridge.

## All three embedded pictures

1. `indus_signs.jpg` is a font-rendered sign grid with IDs and counts. It is useful for learning the transcription system, but cannot reveal original carving damage or stroke variation.
2. `indus_m414.jpg` is an artifact image attributed to CISI 1, p. 100, M-414a. The caption distinguishes impression orientation and an unclear sign. A proposed North Star reading is not established by seeing a fish-like sign.
3. `indus_tablets.jpg` is another font-generated chart. It contains sequences, counts, catalogue IDs and text labels for reverse motifs; it is not a photographic set of the animal reverses.

Thus all three were inspected, but this webpage alone is not the raw-image corpus we want.

## Three decisive code findings

**Known key versus unknown key.** In set 205, a character language model rates the supplied Ventris Linear B key above 100 shuffled keys under Greek. In set 207, freely fitting values instead selects Sanskrit in both reported seeds and recovers 0/30 common Greek values. We inspected code and saved outputs, not a fresh run. This rejects that procedure as a reliable language identifier. It does not establish that every possible approach must fail: inventory restrictions, many-to-one collapse, terminal rather than best-state return, limited seeds and weak split independence warrant review.

**Genre matters.** Set 198's genre-matched comparison makes Japanese nearest on its structural measures. That is not evidence that Indus was Japanese; it shows that the comparison cannot uniquely identify its language. Our future control pool must include plausible wrong answers matched in genre and statistical properties.

**Copper links are prior input.** `copper.py` reads manually assigned `link` fields in `rebus/copper_tablets.tsv`. It prints their associations; it does not discover them, check photographs or assert equality of both transcriptions. Its ten output rows include variants and an image/image pair, so the seven-equation summary requires a stated grouping convention. The source typology is Parpola 1994 Fig. 7.14, which we have not directly inspected in this audit. Parpola 2005 Fig. 4 is a schematic drawing and supports a narrower substitution observation. Deity identity, word meaning and sound are further hypotheses.

## What the later repository changes

The current progress notes repeatedly revise image associations after accounting for copies, source pools and object types. Their latest 4.57% referent-coverage figure is not 4.57% of the script translated; the associated held-out precision is about 5%. Restoration results can also look stronger against a frequency baseline than against a neighbour-context baseline. These are project-reported metrics with different denominators, and the detailed methods appendix records their scope.

An older `DOSSIER.md` still presents two numeral systems and stronger fixed-meaning/language interpretations. The webpage explicitly retracts two numeral systems. Therefore a repository search must follow the correction history rather than treat every Markdown statement as the current conclusion.

## Public repositories found and inspected

| Repository | Useful contribution | Reuse decision |
|---|---|---|
| [dbourdeau/cyphersolver](https://github.com/dbourdeau/cyphersolver/tree/main/targets/indus) | Broad test ledger, controls, failed approaches | Map our work to this prior work before adding tests. |
| [mayig/indus-valley-script-corpus](https://github.com/mayig/indus-valley-script-corpus) | Per-face transcription, features, uncertainty and crosswalk | High data-model priority; overlapping ancient objects. MIT root licence. |
| [joyboseroy/indus_decipher](https://github.com/joyboseroy/indus_decipher) | Corpus converters, registry, falsification framework | High methods priority; inspect data lineage and external rights separately. MIT code. |
| [isramos/indus-script-sign-merging](https://github.com/isramos/indus-script-sign-merging) | Tests of sensitivity to merging sign variants | Strong match for our sign-decomposition question. GPL-3.0; non-peer-reviewed working draft. |
| [vatsalajha/indus](https://github.com/vatsalajha/indus) | Structural controls and extraction procedures | Useful methods. MIT licence specifically covers code. |
| [sriharideveloper/indus](https://github.com/sriharideveloper/indus) | Structural workbench and claims ledger | Audit gap removal so missing signs do not create false adjacency. |
| [yajnadevam/indus-website](https://github.com/yajnadevam/indus-website) | Database/interface/font source | GPL-3.0 root licence; proposed readings excluded from ground truth. |
| [yajnadevam/lipi](https://github.com/yajnadevam/lipi) | Corpus exports and claimed decipherment | Source tracing; no root licence detected. Reading claims unverified. |
| [field-cady/indus_valley_script_corpus](https://github.com/field-cady/indus_valley_script_corpus) | Mirror including the lineage we already used | Additional repository, not independent evidence. MIT root does not settle imported CSV rights. |
| [prabhatchanchal/IndusBench](https://github.com/prabhatchanchal/IndusBench) | Evaluation ideas | Uses Lipi material; root licence unresolved; composite score is not decipherment probability. |
| [BitConcepts/glossa-lab](https://github.com/BitConcepts/glossa-lab) | Agent orchestration and hypothesis tracking | Platform ideas only. Earlier anchor headline was retired after its own controls; replacement readings unverified. |

The detailed repository appendix records licence scopes, upstream dependencies and source references. The deliverable omits bulk third-party source snapshots; URLs and hashes identify the inspected versions. Public accessibility alone does not establish permission to redistribute every imported photograph or database.

## The next concrete experiment, defined now

Priority is a bounded **copper-pair evidence audit**, because these observations are already being used as semantic anchors. Our source appendix lists candidate catalogue IDs for each relationship. Start with the hare pairing B7/C2: the derivative table lists M-534…542/M-1491…1494 and M-1547. These are acquisition leads, not verified assignments.

For every candidate pair, record: physical-object identifier; source and page; face; photo or drawing; mirror orientation; literal sign sequence; damage; reverse motif; copy/prototype membership; and whether equality is exact, partial or reconstructed. Have two annotations made without proposed language labels. Keep uncertain species and signs uncertain.

Admit only the observation supported by the evidence: for example, 'the same inscription occurs with these alternate reverse representations'. Test animal-name, institution, deity and ritual hypotheses separately. A failed image match removes a supposed anchor; a verified match gives us a defensible constraint. Neither result alone supplies pronunciation.

For computational work, the gate is now explicit: a changed method must recover a known script and reject genre-matched wrong languages under comparable freedom, using independent groups and a frozen evaluation set. More optimisation of the same unconstrained fitting score is not progress by itself.

## Files in the accompanying audit bundle

- `methods.md`: implementations, outputs, limitations and latest progress audit.
- `methods-files.json`: exact reviewed-file manifest and hashes.
- `sources-review.md`: complete 2005paper review and copper-photo acquisition targets.
- `repositories.md` / `repositories.json`: ten additional repositories, licences and dependencies.
- `link-coverage.md`: direct-link reading coverage and exclusions.
- `page-links.json`:54 page anchors and image inventory.
- `source-snapshot.json`: page hash, pinned repository and image classifications.

Attribution: webpage text and its research summaries by Daniel Bourdeau, September 2026, stated CC BY4.0. This report adds our independent code/source audit and explicitly separates unverified claims. Parpola 2005: https://old.harappa.com/script/indusscript.pdf. No claim of a decipherment is made.
