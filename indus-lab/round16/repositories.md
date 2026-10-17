# Round16 — public repository audit

Audit date: 2026-10-10. Ten requested repositories inspected through primary GitHub pages plus REST README/LICENSE responses. No third-party algorithms were run in this audit. Source snapshots and blob hashes are in `repo-sources/`; compact records are in `repositories.json`. Metadata can change, so these are snapshot findings.

## Reuse decisions

### mayig/indus-valley-script-corpus

- **Role:** data + annotation tools.
- **Verified licence scope:** MIT root LICENSE; README also mentions MIT/Apache intentions; only MIT file verified.
- **Dependency:** CISI / Parpola, Wells crosswalk.
- **Priority:** High. Reuse per-face JSON and explicit damage/uncertainty/morphology features. Independent editorial representation of overlapping ancient objects, not a new excavation corpus.
- Primary: https://github.com/mayig/indus-valley-script-corpus

### joyboseroy/indus_decipher

- **Role:** statistical tools + multiple corpus exports.
- **Verified licence scope:** MIT root LICENSE; external corpus rights remain separate.
- **Dependency:** indus-website; mayig CISI; M77 via indusscript.in.
- **Priority:** High. Reuse falsification/control framework and M77 converter after schema audit. M77 portal extraction required authenticated access; third-party redistribution permission is not established by MIT software license.
- Primary: https://github.com/joyboseroy/indus_decipher

### yajnadevam/indus-website

- **Role:** database website + SQL export.
- **Verified licence scope:** GPL-3.0 root LICENSE text verified.
- **Dependency:** ICIT-derived source lineage in existing lab; README itself is setup instructions.
- **Priority:** Medium. Useful source snapshot/interface/font. Keep proposed readings excluded. Recheck field-level origin and licensing.
- Primary: https://github.com/yajnadevam/indus-website

### yajnadevam/lipi

- **Role:** translation website + corpus exports + claimed decipherment.
- **Verified licence scope:** No root license detected; GitHub API license endpoint404.
- **Dependency:** ICIT/M77-derived exports as reported by downstream README.
- **Priority:** Source tracing only. README asserts decipherment; do not accept translations as labels. Primary upstream for several mirrors; permissions need resolution before redistribution.
- Primary: https://github.com/yajnadevam/lipi

### field-cady/indus_valley_script_corpus

- **Role:** corpus mirror/fork + experimental mappings.
- **Verified licence scope:** MIT root LICENSE identical blob to mayig; upstream lipi CSV rights not settled.
- **Dependency:** mayig fork files plus lipi CSV import explicitly stated.
- **Priority:** Already used; low novelty. Our raw inscriptions.csv lineage. Do not count as independent from lipi/ICIT. Separate proposed Dravidian mappings from raw transcriptions.
- Primary: https://github.com/field-cady/indus_valley_script_corpus

### prabhatchanchal/IndusBench

- **Role:** benchmark tools + derived data + reading-model evaluation.
- **Verified licence scope:** No root license detected; README says same as lipi, whose license was not detected.
- **Dependency:** lipi inscriptions.csv and claimed phoneme mappings.
- **Priority:** Medium methods; low evidence independence. Reuse benchmark ideas only after audit/permissions. DCS is an author-defined composite, not a calibrated decipherment probability. Existing mappings may have seen full corpus before split.
- Primary: https://github.com/prabhatchanchal/IndusBench

### isramos/indus-script-sign-merging

- **Role:** sign-inventory sensitivity tools.
- **Verified licence scope:** GPL-3.0 root LICENSE; vendored mayig MIT; other data notices separate.
- **Dependency:** mayig merge decision set plus derived source corpora.
- **Priority:** Highest methodological priority. Run independent verifier and audit null calibration. Directly relevant to whether added strokes are allographs. Repository identifies itself as non-peer-reviewed draft and retains retractions.
- Primary: https://github.com/isramos/indus-script-sign-merging

### vatsalajha/indus

- **Role:** unsupervised structural tools; external data procedures.
- **Verified licence scope:** MIT CODE only per LICENSE note; README broader aggregate claim; use narrower scope.
- **Dependency:** mayig CISI, Fuls, M77, ICIT compilation.
- **Priority:** High methods. Useful extraction/checksum and sign-class controls. Data not shipped or covered by code license. Claimed replication on another transcription does not imply independent objects.
- Primary: https://github.com/vatsalajha/indus

### sriharideveloper/indus

- **Role:** structural workbench + pinned secondary corpus.
- **Verified licence scope:** MIT code/docs; claims upstream corpus MIT notice, not independently resolving upstream rights.
- **Dependency:** horus84/Computational_Linguistics at ac44f08c835de3b709875441eea9d60d1811e3cf; DATA_CARD inspected; ultimate mirror overlap not byte-verified.
- **Priority:** Medium methods; low data novelty. Reusable parsing, claims ledger and held-out benchmarks. Explicitly withdraws semantic meaning from English slot labels. No literal reading claimed.
- Primary: https://github.com/sriharideveloper/indus

### BitConcepts/glossa-lab

- **Role:** agentic platform + unverified Proto-Dravidian reading hypotheses.
- **Verified licence scope:** MIT software; root LICENSE separately assigns research/indus outputs CC BY4.0.
- **Dependency:** Holdat IVS; literature anchors and other sources need per-file audit.
- **Priority:** Platform ideas / adversarial test material. README retires old161-anchor90.96% headline after its own simulated-annealing falsification. Current strict94-candidate set is still a hypothesis, not verified readings; coverage is not decipherment confidence.
- Primary: https://github.com/BitConcepts/glossa-lab

## What is actually independent

Repository count is not evidence count. The lipi → field-cady/IndusBench chain shares underlying transcriptions. The older indus-website export and lipi also trace to ICIT-derived material in our existing source record; object-level matching, not repository names, determines overlap. The mayig JSON is a different editorial representation of CISI objects with useful feature annotations, but the ancient objects overlap ICIT and M77. M77 is valuable as another scholarly transcription system; crosswalk alignment and shared-object membership must be preserved. Sign-merging and structural workbenches mostly add methods, not new archaeological observations.

A repo-level MIT/GPL badge is not evidence that the maintainer can relicense imported photographs, books or third-party database material. Record each imported file separately. In particular, field-cady retains the same MIT licence blob as mayig while explicitly importing lipi CSVs; do not infer a clean rights chain from the fork licence. IndusBench delegates licence to lipi without a discovered root licence, so mark unresolved. Publicly readable is not automatically openly licensed.

## Next concrete reuse sequence

1. Compare mayig feature schema with our literal morphology/uncertainty contract and use its crosswalk as an alternative hypothesis, not identity truth.
2. Inspect/run isramos standalone numerical verifier and calibration on pinned inputs; then port only the independently understood controls into our sign-merging experiment.
3. Audit joyboseroy M77 line converter and corpus registry; preserve incomplete/uncertain marks and undecoded direction codes.
4. Compare sriharideveloper/vatsalajha controls with ours as code-level replications. Use dependency-aware splits rather than treating new repositories as new evidence.
5. Keep lipi and glossa-lab proposed sound values quarantined as candidate keys to falsify with frozen null/known-script controls. Do not train on their English/Sanskrit/Dravidian translations as ground truth.

## Methodological warnings

IndusBench DCS combines prediction, compression, entropy, grammar, context, reproducibility and simplicity with chosen weights. A score is not a probability of decipherment and a structural gain does not certify phoneme assignments. Normalizing variants can itself inject a mapping. Full-corpus-derived keys can contaminate nominal train/test evaluation even when test text hashes are locked.

Glossa-lab offers relevant agent orchestration and provenance machinery but its self-reported retractions show why autonomous loops require independent gates. We have not independently validated its current anchors, claimed replication, or preprint. Its original161/90.96% marketing description conflicts with the superseding README rebase; quote the current README carefully, if at all.

No repository reviewed here establishes a decipherment through this audit. Recommended reuse prioritizes provenance, morphology, known-script controls and falsification rather than reading coverage.

## Additional primary provenance checks

- isramos `data/derived/PROVENANCE.md` explicitly identifies its larger corpus as joyboseroy’s derivative of yajnadevam SQL, with pinned commit and SHA256; its three CISI granularities come from mayig via joyboseroy converters. These are not five independent corpora.
- sriharideveloper `data/DATA_CARD.md` pins the5679-row file to horus84, not directly field-cady. Its checksum differs from our current file; do not claim byte identity. It removes gap/damage codes during parsing; audit for invented adjacency across missing signs before reuse.
- joyboseroy `CORPUS_REGISTRY.md` distinguishes3573 M77 lines from2906 texts; WUCS is published aggregate statistics only, not downloaded raw data; EBUDS was not separately reconstructed. Those distinctions matter when claiming replication.
