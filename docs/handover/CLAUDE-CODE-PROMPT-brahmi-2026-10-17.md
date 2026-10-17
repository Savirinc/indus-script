# Mission: independently test an Indus decipherment proposal

You are taking over an active research project for Arham Partap Jain. The long-term goal is decipherment; the immediate goal is a reproducible, discriminating assessment of the proposed Indus-to-Brahmi/Sanskrit reading. Do the work, not just propose a plan. Treat every prior assistant conclusion as a claim to inspect. A reproducible negative or qualified result is useful progress. Do not promise a breakthrough.

## Start now
1. Read START-HERE.md and CURRENT-STATE.md.
2. Run python3 verify_package.py and python3 reproduce_current.py. Explain any discrepancy before proceeding.
3. Inspect current-audit/audit.py, expand.py, lipi-index.vue, xlits.csv, decipher.csv and the two result JSONs. Distinguish raw substitution from canonical expansion, phonetic expansion, dictionary lookup and translated interpretation.
4. Read prior-project/CURRENT-STATUS.md and EXTERNAL-EVIDENCE.md. Inspect older experiments only as needed; do not restart already exhausted tests without a materially different hypothesis.

## Working approach
Use a coordinator and up to four parallel specialists if your environment supports agents. Otherwise do these tracks sequentially. Give each specialist separate output files; the coordinator reviews and reconciles conflicts.
- Corpus auditor: provenance, row/object/text duplication, ID crosswalks, direction and photograph checks, including M-304.
- Mapping auditor: reconstruct the author's exact algorithm, find manual regexes, variant grouping, expansions, dictionary augmentation and exceptions. Track versions and hashes.
- Linguistic evaluator: define explicit testable Sanskrit/Prakrit/Dravidian hypotheses with historically justified resources. Distinguish script from language. Do not use modern Tamil as a direct Bronze Age oracle.
- Independent critic/statistician: check leakage, null models, model flexibility, multiple testing, and the applicability of unicity-distance reasoning. Try to falsify positive claims; also challenge unfair negative tests.

## First substantive deliverable
Produce one end-to-end trace on M-304 and 10 inscriptions selected by a reproducible rule spanning length, site and object type. Document raw signs, photograph/catalogue orientation if available, each transformation, all permitted alternatives, resulting forms and the evidence for meanings. If photograph provenance is unavailable, say so. Do not cherry-pick only readable cases. These examples are diagnostic, not held-out proof.

Then run the strongest feasible corpus-wide discriminating test:
A. Freeze candidate mapping, canonical rules, sound alternatives, word boundaries, normalization and lexicon before scoring. Report every discretionary parameter and any change.
B. Use independently sourced linguistic material for scoring. Upstream 'sanskrit' and 'translation' columns are the author's outputs, NEVER ground-truth labels or training targets.
C. Deduplicate and group by physical object, exact sequence and near-duplicate/text family where possible. Report denominators. Do not call a split held-out if the published mapping was developed using those texts. Reserve genuinely independent data if identifiable; otherwise call this a retrospective diagnostic.
D. Include appropriate alternative mappings and structure-preserving controls. Match flexibility, output length, vowel/consonant or sign-class constraints where justified. Explain what each null answers. Coverage cannot distinguish maps with identical assigned IDs. Entropy/bigrams invariant under bijective relabelling cannot identify sounds.
E. Where an algorithm searches/tunes mappings, give controls comparable search budgets. Do not compare an extensively optimized proposal only with a few untuned random maps and call that historical proof.
F. Use a known-language positive control with inscription-like lengths to verify that the chosen evaluation can detect a genuine signal. If that fails, redesign or stop the inference.
G. Predeclare metrics, seed, trial count and stopping rule in results/PROTOCOL.md before running. Prefer interpretable coverage, constrained lexical/grammar scoring and independent context predictions over impressionistic LLM translations. Separate morphological plausibility from coherent meaning.
H. Make no language-wide rejection from failure of one specific spelling model. A superior score supports a specified model under specified controls; it is not automatically a decipherment.

## Source work
Read Rao et al.'s PNAS paper, including Methods and limitations, and the relevant sections of Yajnadevam's paper/source code. Record exactly what you read. The former supplies structural analysis, not the latter's sound assignments. Use public, legitimate sources and preserve citation URLs and object/page identifiers. Do not claim to have read every link or photograph unless you have.

If the full fixed reading pipeline cannot be reconstructed, identify the exact missing rule/resource and demonstrate its consequence. You can still produce a useful reproducibility verdict. Do not hide gaps by inventing linguistic rules.

## Required outputs
Create results/ with:
- FINDINGS.md: what was executed, strongest finding, uncertainty, competing explanations and one concrete next step.
- PROTOCOL.md: frozen experiment specification.
- REPRODUCTION.md: commands, dependencies, seeds and expected results.
- CLAIMS.json: claim, evidence, status, counterevidence and source.
- M304-TRACE.md and diagnostic examples with transformations.
- machine-readable metrics and per-inscription output; no fabricated p-values.
- scripts sufficient to reproduce the new test.
- NEXT-SESSION.md: checkpoint if a real blocker or resource limit prevents completion.

## Autonomy and stopping
Proceed with local code, public research, debugging and routine reversible choices without repeated confirmation. Do not contact researchers, publish, pay, use private accounts or bypass access restrictions. Run bounded experiments, save checkpoints and report resource limits honestly. Stop a test when its predeclared criterion is reached, its controls fail, or unavailable evidence makes it uninformative; select another justified test rather than looping indefinitely. Do not disable tool approval safeguards.

Final report: distinguish reproduced facts, exploratory results, model-dependent inference and unknowns. Never call 100% symbol assignment 100% translation accuracy. Bring back a concrete result, including a well-established failure or an exact missing dependency if that is what the evidence supports.
