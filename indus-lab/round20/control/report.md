# Tamil sequence-order control: completed

The existing solver recovered substantially more of the artificial Tamil cipher using the original Tamil reference than using any of five references whose segments were shuffled inside each word. **This is an engineering control, not an Indus language test.**

| Reference | Exact held-out words /27 | Correct held-out segments /134 | Correct training-seen key entries /47 |
|---|---:|---:|---:|
| Original Tamil | 25 | 132 | 47 |
| Within-word shuffle 20001 | 0 | 24 | 4 |
| Within-word shuffle 20002 | 0 | 20 | 4 |
| Within-word shuffle 20003 | 3 | 80 | 13 |
| Within-word shuffle 20004 | 0 | 41 | 5 |
| Within-word shuffle 20005 | 2 | 63 | 11 |

All six conditions used the original encrypted training input, the same disclosed 50-segment candidate inventory, solver seed15104, and unchanged six-chain, 15,000-proposal-per-chain budget. The 540,000 proposals finished in **10.30 seconds**, below the fixed 180-second cap. The original Tamil evaluation exactly reproduced round15's saved positive-control evaluation. No settings were tuned and no runs discarded.

Each shuffled reference preserves all 133 word lengths and the global segment counts exactly. The original reference contains all27 held-out plaintext strings; the five shuffled references contain respectively2,1,0,0,1. Respectively8,6,8,11,13 reference words stayed unchanged by chance. These checks were made after all fits and were not used to select a control. This disruption changes both word forms and local sequence statistics, so the result does not isolate syntax, grammar or dictionary coverage individually.

The experiment shows that sequence information in the original reference aids this particular favorable recovery task beyond the preserved lengths and segment frequencies. Some shuffled references still recover many common tokens (up to80/134) while recovering only13/47 key entries: token accuracy can overstate alphabet recovery. Five shuffles, one encryption key and one split are coarse descriptive checks; no p-value or general performance estimate is claimed.

Word boundaries, phonemic segmentation, bijective substitution and the target's known phonemic inventory remain supplied. The full Tamil reference deliberately includes test vocabulary. The solver had no hidden key, target alignments, concepts, held-out cipher text or evaluation answers: `evaluation_answers.json` was first opened only after all six fits finished. The original Tamil reference is nevertheless an intentionally generous unaligned oracle lexicon, not unknown-language evidence.

Files: `protocol.md` was saved before fitting; `run.py` imports the unchanged round15 solver; `solver-inputs.json` preserves the concrete six references and source hashes; `results.json` contains all conditions, traces, evaluation counts and mappings. No Indus sign was assigned a sound or meaning. This extends an already completed benchmark and should not be presented as a new decipherment method.

Run: `OPENBLAS_NUM_THREADS=1 python indus-lab/round20/control/run.py` (NumPy required).
