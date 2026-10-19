# Round 54 — Syllabic core by free combination: METHOD-FAIL on both controls (the intuition is wrong on real data)

Protocol `PROTOCOL.md` (committed 7dc203d before code). Code `extract54.py`, `run54.py`; `results.json`, `run54.log`. Seed 54001, B = 50 Indus-shaped samples per corpus, 30 within-text permutations per sample, types with ≥ 10 tokens scored.

## Verdict
**METHOD-FAIL**, twice over.

| Control | Requirement | Result |
|---|---|---|
| Positive: freedom F separates Akkadian syllabograms from logograms | AUC ≥ 0.75 on OBL and OAL | OBL **0.455**, OAL **0.651** (SEAL-akk 0.469) |
| Negative: Akkadian core share exceeds the logographic corpora by ≥ 0.20 | C_akk − C_logo ≥ 0.20 | OBL 0.768, OAL 0.791 against Shijing **0.855**, oracle bone 0.340; gap **−0.087** |

The freedom statistic does not pick out syllabograms in a script where they are known, and the one-sign-per-word Shijing combines its signs **more** freely than Akkadian syllabograms do. So "a syllabic core combines freely, word-signs sit in slots" is false as a statistical signature at this corpus size, and the Indus value (C 0.594, median F 0.722) is uninterpretable for the question asked.

## Why the intuition fails
Syllabograms are constrained by the phonotactics and morphology of the language inside words (in Akkadian, a CV sign is followed by a limited set of VC and CV signs that make real syllables), so their neighbour sets are far from random. Word-signs in a monosyllabic language, by contrast, are followed by whatever word comes next; the Shijing's characters, especially its particles, are nearly as free as chance (median F 0.77). Combinatorial freedom therefore measures where in the hierarchy a sign sits (inside a word versus between words), not whether it is phonetic. The round-53 failure and this one point the same way: at 8,726 tokens, the only structural property the corpus reliably exposes is **slot restriction**, not sign function.

## Description (not a verdict)
Core share C at θ = 0.648 (coverage of the f ≥ 10 set in brackets): Old Babylonian letters 0.768 (0.95), Old Assyrian letters 0.791 (0.97), Ur III 0.454 (0.91), Egyptian 0.654 (0.90), oracle bone 0.340 (0.85), Shijing 0.855 (0.58), **Indus 0.594 (0.86)**. The Indus corpus is intermediate, between oracle bone and Egyptian; nothing follows from that.

The Indus freedom table is nonetheless a usable artefact, because slot restriction is what it measures and slot restriction is what a Kober-style grid needs. Most restricted signs (F, tokens): 817 (0.23, 124), 679 (0.32, 13), 527 (0.36, 45), 090 "man" (0.40, 88), 520 "arrow" (0.41, 166), 861 (0.44, 157), 400 (0.44, 211), 820 (0.46, 151), 692 (0.48, 44). Freest: 645 (1.11, 10), 440 (1.09, 30), 742 (1.09, 24), 741 (1.02, 136), 031 "one stroke" (0.99, 132), 745 (0.98, 16). The restricted set is dominated by the known terminal and near-terminal signs; the free set by numeral-like and bracketing signs. These are inputs for a future distributional-grid round, not findings.

## Status of A3
Unchanged, OPEN. Rounds 52–54 together: alphabets and syllabaries are excluded; among large-inventory systems, no statistic tried so far (inventory, entropy, Heaps, repetition, PMI segmentation, combinatorial freedom) distinguishes a logosyllabic system from a one-sign-per-word system at 8,726 tokens on real controls. That sentence is the result of the structural track to date.

## What this means for the roadmap
Four consecutive METHOD-FAILs on Track 2 with real controls. Each was informative about the instrument, none about the script. The honest reading is that generic sign statistics have been exhausted on this corpus; what remains in Track 2 is (a) a lexicon-induction segmenter (53b), which attacks word structure with a stronger model, and (b) a grid built from slot restriction alone (54b), which does not claim to identify sign function. Both should be run once, and the methods paper should report the whole series.

## Data
`controls/`: OBL 348,163 tokens (296,174 syllabic, 51,989 logographic by ATF marking), OAL 174,415 (145,943 / 28,472), SEAL-akk 7,348 (under N; reported only). Flags: lower case = syllabic; `_…_`, braces, numerals, upper case = logographic. Other corpora read unchanged from rounds 52–52b.
