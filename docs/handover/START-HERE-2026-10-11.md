# Indus research handoff — 11 October 2026

## Purpose and honest status
Portable working snapshot for an independent Claude/Claude Code audit and continued collaboration. No Indus sign has been assigned a sound or meaning that this project has independently established. No accepted translation has been produced. This is a research record, not a decipherment.

Read CLAUDE-PROMPT.md, CURRENT-STATUS.md and EXTERNAL-EVIDENCE.md first. Then inspect the actual experiment reports, protocols and scripts. Earlier READMEs describe earlier stages and are not the current status. Corrections in later rounds supersede stronger earlier interpretations. This handoff does not contain the entire chat or every external book or repository.

## Contents
The supplied indus-lab tree preserves existing code, source snapshots, reports, result files, source ledgers and selected photographic extracts. Round numbers are historical stages, not a claim that every numbered directory exists or that every file was independently reviewed. MANIFEST.json fingerprints every included file; EXCLUDED.json records omitted local files. Full PDFs, caches and git internals are excluded; relevant original-document URLs are retained in project provenance and EXTERNAL-EVIDENCE.md. No source file is overwritten by this handoff.

## Inputs and their limits
- Main later snapshot: indus-lab/raw/inscriptions.csv, 5,679 rows; SHA256 c22d39c3c2bda869c67fb01e7f2b4cdc64cc424405eafe89550d1702216b3429.
- This is a modern transcription/catalogue export, NOT untouched ancient evidence. Rows need not correspond one-to-one to physical objects.
- It contains upstream Sanskrit/translation fields. Preserve for provenance but NEVER use them as truth labels, training targets or confirmation of a reading.
- Earlier corpus.tsv has 2,543 selected rows. Do not silently mix it with the later CSV.
- Sources ultimately include Bourdeau, ICIT/indus-website, Lipi and Mayig. Their coverage, editorial dependence and sign mappings require scrutiny. Identical transcriptions copied between repositories are not independent evidence.
- Published comparative Dravidian data are under round14/dravlex; comparative ledgers under round21. Cognate group labels are scholarly inputs, not predictions made by our model.
- Licence/attribution files stay with the materials. Do not assume all photographs or book extracts are public domain or republishable.

## Run safely
Use a copy of the extracted folder: scripts may regenerate their output files. Python 3 standard library suffices for rounds 27–28. Earlier image/statistical scripts can require numpy, scipy, Pillow, fontTools or PyMuPDF; inspect imports and per-round documentation. Some source-download scripts require network access or paths not bundled here. No claim that every historical script was rerun during packaging.

From the folder containing indus-lab:

    python3 indus-lab/round27/cross_city.py
    python3 indus-lab/round27/robustness.py
    python3 indus-lab/round28/joint_control.py

Round28 attempts 1.6 million moves; do not mistake the sampled checkpoints for independent replicates. To verify file integrity without running research scripts:

    python3 verify_manifest.py

## Recommended next action
Independently audit the strongest existing evidence before adding tests. Select one genuinely discriminating experiment, specify the competing hypotheses and stopping rule before execution, and produce a result with reproducible inputs. If only exploratory material is available, label it exploratory. Do not keep returning with another unbounded literature lookup.
