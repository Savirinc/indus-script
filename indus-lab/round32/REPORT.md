# Round 32 — Decipherability benchmark: the Indus corpus sits below the threshold for statistical decoding

11 October 2026. A real deciphered script (Linear B, 919 words, known Greek) was degraded step by step toward Indus conditions.

## Pre-registered result (PROTOCOL.md): INFEASIBLE

| Condition | Sign IDs | Token accuracy | Notes |
|---|---:|---:|---|
| A: exact vocabulary (oracle) | 70 | **100%** | Solver works |
| B: related-language lexicon (Greek forms + guessed spelling rules), one sign per value | 70 | **83%** | Recoverable |
| B0: same lexicon, syllables shuffled within words | 70 | 7% | Control: sequence content drives recovery |
| C: as B, but ~370 sign IDs (several signs per value) | 373 | 8–9% | Fails |
| D: as C, 1–3 words per text, no dividers | 373 | 4–6% | Fails |
| E: family phonotactics only (no shared words), one sign per value | 70 | 55% | Partial |
| F: as E with ~370 signs and no dividers (closest Indus analogue) | 368 | 4–7% | Fails |

**Deviation, disclosed.** The pre-registered solver lacked the standard homophonic-cipher emission term, which made its many-to-one search degenerate. The term was added as v2 (it has no effect on the one-sign-per-value conditions) and C, D and F were rerun. The verdict is unchanged. The v1 code is kept as `benchmark_v1_prereg.py`; v1 results are in `results_*.json` and v2 results in `results_v2_*.json`.

## Exploratory (post hoc): where is the threshold?
Same corpus and related-language lexicon, varying only the number of sign IDs (v2 solver):

| Sign IDs | Tokens per sign | Token accuracy | Does a wrong key outscore the true key? |
|---:|---:|---:|---|
| 115 | 30 | 84% | — |
| 173 | 20 | 83% | — |
| 239 | 14 | 18% (150k steps); 30% (600k steps) | Yes, at 600k steps |
| 373 | 9 | 8% | Yes |

The Indus core corpus has 582 sign types and 8,726 deduplicated sign tokens: **15 tokens per sign**, and 302 signs seen at most twice. That is just below the collapse point, and this is under conditions far kinder than the real Indus case:
- the language is known exactly;
- the set of possible sound values is supplied;
- the script is purely phonetic, with no logograms;
- the texts are ordinary words rather than names.

## Exploratory: how many independently known signs would rescue it?
At Indus-matched density (239 sign IDs), the k most frequent signs were given their true values (simulating anchors from a bilingual or from matched names):

| Anchored signs | Share of tokens anchored | Accuracy on the remaining tokens |
|---:|---:|---:|
| 0 | 0% | 18–30% |
| 5 | 4% | 41% |
| 10 | 7% | 48% |
| 20 | 13% | 61% |
| 40 | 24% | 72% |

Even with 40 anchors, a wrong key still outscores the true key, so the lexicon model is overfitting. The gains come from the anchors constraining the search.

## What this means for the mission
1. **Statistical decoding from the Indus corpus alone is not feasible**, even granting a correct related-language lexicon. Every past proposal that "fits" (Dravidian, Indo-Aryan or otherwise) is expected to fit. Fit is not evidence at this corpus size. This explains the null results of rounds 20–23 and why competing published decipherments cannot be told apart.
2. Decoding becomes plausible only by moving the corpus across the threshold:
   - **Anchors.** On the order of 10–40 independently fixed sign values are needed for a majority of the rest to follow, under kind assumptions. Today the project has zero secure anchors; the Gulf-seal "twins" sign is a candidate structural anchor, not a sound value.
   - **More text.** Roughly 1.5–2× the current deduplicated sign tokens per sign would be needed to reach the ~20–30 tokens/sign zone. New excavations (e.g. Rakhigarhi, Dholavira, Gulf sites) and full digitisation of CISI volumes 3.1–3.3 bear directly on this.
   - **Fewer free signs.** Rigorous allograph merging (Indus sign lists range from about 400 to over 600 signs) raises tokens per sign without new text. This is a palaeographic task and is checkable.
3. The best-supported decoding route is therefore the **name-anchor route** (rounds 30–31), combined with sign-list consolidation. It is not further language-model fitting.

## Limitations
- One script, one corpus, one key/homophone draw, and two to four annealing chains per condition. The thresholds are approximate.
- Homophones were assigned at random per token; real allography is structured, which may help.
- The Greek-to-Linear B spelling rules reproduce 48% of spellings exactly. A better lexicon could shift the threshold. For Indus no attested contemporaneous lexicon exists, which shifts it the other way.

## Reproduce
- `python3 indus-lab/round32/benchmark.py <neurodecipher>/data/linear_b-greek.cog [A B B0 C D E F]`
- `sweep_exploratory.py` and `anchors_exploratory.py` take the same data path plus sign-ID targets or anchor counts.
- Optional environment variables: `R32_STEPS` and `R32_CHAINS`.

Data: NeuroDecipher (Luo, Cao & Barzilay 2019) commit 480bad2. Requires numpy.
