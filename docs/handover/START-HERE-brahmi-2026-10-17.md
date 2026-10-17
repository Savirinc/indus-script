# Indus research: Claude Code handover
Prepared 17 October 2026 for Arham Partap Jain.

## Start
Open this extracted directory as your Claude Code project. Paste:

> Read CLAUDE-CODE-PROMPT.md and carry out its instructions. Begin by verifying the package and reproducing the current audit. Then independently assess the mapping and run the strongest feasible discriminating test. Work through to a written result; do not stop at a plan.

Offline reproduction requires Python 3, standard library only:

```sh
python3 verify_package.py
python3 reproduce_current.py
```

The second command runs in a temporary copy and does not overwrite the evidence snapshot.

## Read in this order
1. CLAUDE-CODE-PROMPT.md — scope, method, deliverables and stopping criteria.
2. CURRENT-STATE.md — latest measured results and unresolved issues.
3. current-audit/REPORT.md and its actual scripts/data.
4. prior-project/CURRENT-STATUS.md and EXTERNAL-EVIDENCE.md — earlier experiments and corrections.

## Contents
- current-audit/: runnable Round 29 code, author mappings, explorer data, source snapshots and per-record results.
- prior-project/: earlier working handover through Round 28, including data, code, reports and selected images.
- Indus-Brahmi-Full-Mapping-Atlas.pdf: visual reference for the proposed values. It is not a verified decipherment key.
- PACKAGE-MANIFEST.json: hashes for this package; verify_package.py checks them.

This is a portable research snapshot, not the entire chat, full CISI books or all original artifact photographs. Full source repositories and the original scholarly PDFs are not all bundled. Some historical scripts require additional dependencies/network access. Only the current reproduction commands have been rechecked for this handover.

The package includes third-party material for research with original attribution retained. It does not grant new publication or redistribution rights. Existing reports contain evolving hypotheses; later corrections supersede earlier confident statements.
