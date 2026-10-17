# Round 12 — evidence contract and validation reset

Audit date: 2026-10-10. Scope: local reports 10 and 11, their independent reviews and extraction code, `expand.py`, raw corpus headers and examples, and the lab README. No fresh archaeological or web verification was performed for this audit. Earlier files are unchanged.

## Assessment

The bottleneck is not insufficient numbers of agents or correlations. It is lack of an independently observed bridge from graphic structure to reference, function, sound and language. Many semantic interpretations can fit the same short formula. Better prediction of a missing catalogue ID cannot by itself resolve those interpretations.

The strongest current physical observation is the broad repeated A-face arrangement and differing B-face stroke groups on H-315/H-316/H-317. It supports a stable/variable field contrast. Quantity, category, rank and production convention are still distinguishable hypotheses, not conclusions. The photographs were checked with the expected counts disclosed, so this is independent inspection but not blinded validation. Sign400's object-type association is exploratory, selected after corpus inspection, and partially photographically supported. Neither supplies a word or sound.

## Highest-impact failure modes

1. **Observational underdetermination.** A small integer-looking stroke series alongside a stable sign is compatible with several purposes. Neither animal pictures nor modern naming of shapes fixes their intended referent. A narrative explaining already-seen examples is weaker than predictions that competitors fail.
2. **Unit mismatch.** Raw rows can be faces; ID stems are source group keys, not verified physical objects; catalogue IDs can be aliases; photographs can be impressions or alternate views; exact strings and mould families are different units. H-355 supplies two identical selected faces; H-316/H-1304 may be aliases. Counts over these units answer different questions.
3. **Inherited transcription and segmentation.** Font templates implement editorial categories. Component extraction can rediscover how a font was constructed, rather than ancient sign composition. Code IDs, boundaries, orientation and compound-sign decisions require image-linked alternatives. The M-478 correction illustrates that a multi-stroke form may be one encoded sign; counting marks cannot independently establish the number of signs.
4. **Confounded labels.** Medium, manufacture, object category, site, chronology and workshop are not randomized. Report10's length matching leaves these unresolved. A classifier may recognize a catalogue convention or manufacturing practice rather than ancient meaning.
5. **Selection history.** Candidate400, the long-stroke extension, and variable cross-face families were chosen after looking at related results. Report11's 27 variable families were selected precisely for variation; the number is not the proportion of all families that vary. Thresholds, exclusions and outcomes cannot be rewritten as prospective after this history.
6. **Confirmation by shared source.** Agents reading the same font, transcript, paper or suggested count share its possible mistakes. A second transcription of the same object checks transcription robustness; it is not an independently excavated object. Several agreeing agents do not make specialist authentication.
7. **Missing evidence misread as negative evidence.** An unrecorded motif, missing face, undated layer or absent image is unknown. Treating it as absent creates apparently clean semantic associations.
8. **Invalid validation target.** A successful algorithm that distinguishes object types or fills missing signs does not establish that its latent groups are nouns, suffixes, commodities or numbers. Benchmarks must distinguish the exact claim being tested.

## Evidence contract

Every claim must point to a versioned packet with the following fields. Unavailable fields remain explicitly unknown; no guessed value may silently become a label.

| Layer | Required record | Permitted conclusion |
|---|---|---|
| Source | Author/publication, original URL or file, hash, page, figure, acquisition date, upstream lineage | Where an assertion or image came from |
| Object | Museum/excavation/catalogue IDs; candidate alias edges and grounds; site/context confidence | A proposed physical entity, with unresolved identities preserved |
| Surface/view | Face label, photograph versus ancient/modern impression versus tracing; crop box; transformation history | Which surface is being observed and how |
| Mark | Pixel/region coordinates, literal visual description, damage/occlusion, alternative segmentation, reviewer and information disclosed to reviewer | Observed form at stated resolution |
| Transcription | Sign scheme/version, alternatives, line boundaries, stored order and reading-direction confidence | An editorial encoding, not a translated word |
| Context | Material/type/motif/phase with individual source and confidence; multi-label motif descriptions | Independently supported archaeological associations |
| Test | Exact question, population, unit, exclusions, denominator, split graph, frozen code/hash, alternatives, outcome and stopping rule | A reproducible result within its scope |
| Interpretation | Explicit rival explanations, distinguishing prediction, evidence level and disconfirming observations | A bounded hypothesis; no promotion to sound/meaning without separate support |

Keep original raw inputs immutable. Corrections are overlays with author, date, evidence and previous value. Separate literal annotations from catalogue transcription and proposed semantics. Preserve face order and multiplicity even if a particular analysis deliberately ignores them.

### Evidence levels

- **E0 — supplied label:** raw metadata, font or transcription claim.
- **E1 — image-supported form:** source-linked visible feature; uncertain details retained.
- **E2 — replicated structural relation:** survives independent objects/families, plausible coding alternatives and suitable controls.
- **E3 — externally constrained function/reference:** predicts independently measured context better than specified competitors. A quantity interpretation requires evidence beyond the count-like appearance itself.
- **E4 — reading:** a fixed sound/meaning proposal makes coherent, discriminating predictions on genuinely new evidence and has independent specialist reproduction.

These are claim-specific statuses, not a cumulative score or percent deciphered. The same object can support E1 stroke counts while its supposed commodity remains E0 speculation.

## Columns and units that are not ground truth

- `sanskrit`, `translation`, `class`, and interpretive `notes`: exclude from model targets/features and semantic validation. `expand.py` already removes these fields; future ingestion must keep this prohibition explicit. Raw labels such as PN/SC are not independently established linguistic categories.
- `text`, `signs`, `text length`, `dir.`, `complete`, `preservation`, `condition`: supplied readings/editorial assessments, subject to image review. Completeness flag Y cannot certify every face or every fine stroke. Stored order is not automatically reading order.
- `symbol`/motif and `cult`: editorial iconographic labels. `None` and `Mult` cannot establish absence of a target animal. Descriptive animal identification and religious interpretation require separate fields.
- `type`, `shape`, `material`, dimensions: potentially useful measurements/classifications, not validated just because internally consistent. Report10/11 already show subtype and medium issues; transcription and publication classifications may differ.
- `time`, `period`, `phase`, `depth`: require excavation-context sourcing, provenance and dating uncertainty. A depth value alone is not an absolute date or reliable cross-site sequence.
- `id`, `cisi`, ID stem, `excavation-idno`, `sides`: identity clues and source grouping fields, not independent-object guarantees. Shared excavation number flags an alias hypothesis; it does not settle it without source verification.
- Font connected components, component sums, visual similarity and catalogue-number arithmetic: graphic descriptors only, not ancient graphemes, phonemes or meanings.
- Exact-text groups, sign multisets, inferred mould groups and variable families: analytic units with different dependencies. Exact-text deduplication is not physical deduplication; a multiset discards order; a family selected for variation cannot measure prevalence.

## Held-out policy after corpus-wide exposure

There is no honest way to make a fresh random split of this same corpus an untouched discovery confirmation. The team has seen global summaries, selected candidates and adjusted analyses; its ideas inherit that exposure. Do not call new seeds, site splits or withheld rows "unseen" without specifying who saw what and when.

Use three separate evaluation tracks:

1. **Retrospective robustness:** existing corpus, leave-site/family/object-group-out analyses, alternative transcriptions and alias policies. Report as reuse of exposed evidence. Nested fitting prevents within-run leakage but cannot erase historical hypothesis selection.
2. **Prospective measurement validation on known material:** freeze annotation instructions and predictions before obtaining new photographs or independently recoding uninspected views. Blind annotators to expected count, catalogue ID where feasible, text context and hypothesis. Because the source objects/transcriptions were already selected, this validates measurement and specified predictions, not an untouched population discovery. Preserve all failures and unscorable cases.
3. **External prospective confirmation:** a documented acquisition not used to form the hypothesis, with eligibility and evaluation frozen before access. It can be newly excavated material or independently sourced/annotated material absent from model development, but a later corpus export containing the same known objects is not automatically new evidence. State remaining inherited selection explicitly.

Before splitting, construct a dependency graph linking confirmed/possible aliases, original/impression views, multiple faces, known mould/copy families and closely related text templates. Use conservative connected groups for the primary split; report sensitivity where uncertain edges overmerge. Grouping on template similarity is a dependence control, not a claim of archaeological identity. Never scatter different faces or photographs of one object across train/test.

A custodian records a test manifest/hash and denies hypothesis-generating agents its labels/results until evaluation. All agents and shared files are part of the exposure log. A successful test set becomes development evidence after release; subsequent refinements need a new test set. If the same lockbox must support several planned tests, freeze all tests at once and adjust multiplicity/allocate error in advance. Do not run repeated agent loops until a threshold passes. Preserve a fixed stopping rule and a result category of unresolved.

Freeze evaluation metrics and competitors, not only a verbal hypothesis. Known-script positive controls establish whether the particular method can recover a known relation under comparable short-text, sample-size and noise conditions. A method failing those controls cannot identify language from Indus fit. Passing them is necessary method evidence, not proof of an Indus reading.

## First concrete deliverable

Build a prospective measurement packet for the variable stroke-field hypothesis. The already inspected H-315/316/317 trio is a training/reference set. Before further viewing, select a declared sample from additional families plus constant-field and ambiguous controls, record all eligibility decisions, and freeze literal stroke-count/face-pairing questions. Independent annotators see source crops without predictions; report disagreement rather than majority-vote certainty. Reconcile aliases and mould relationships separately.

The first decision is whether the broad fixed-face/variable-stroke relation survives image recoding beyond the reference trio. The next semantic experiment must specify an external feature on which quantity versus category/workshop hypotheses predict different outcomes. If that feature is unavailable, record that bottleneck and acquire it; another correlation scan cannot substitute for it. In particular, correlating a presumed value with physical tablet size would require an independently justified relationship, since token size need not encode the quantity it represents.

## Local evidence inspected

- `Indus-Research-10.md`, `Indus-Research-11.md` and corresponding round files.
- `round10/matched/analyze.py` and its declared retained-row sampling scope.
- `round11/quantity-protocol.md`, `quantity_audit.py`, `long_stroke_audit.py`, `crossface_audit.py`, `crossface_strict_audit.py`.
- `round11/crossface-review.md`, `round11/crossface-photo-review.md`.
- `expand.py`, `README.md`, `raw/README.md`, headers/examples from `raw/inscriptions.csv` and `raw/corpus.tsv`.

No claim here re-runs all historical calculations or freshly authenticates the archaeological images. This audit defines what their existing results can and cannot establish.
