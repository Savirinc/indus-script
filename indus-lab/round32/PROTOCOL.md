# Round 32 — Can a known script be machine-deciphered under Indus-like conditions? (pre-registered)

Written 11 October 2026 before any solver code was run.

## Why
Every statistical "reading" of the Indus script fits equally well whatever language it assumes, unless the method is first shown to recover a KNOWN script under comparable conditions. Round 20's Tamil control was deliberately favourable: an alphabet, word boundaries, and the answer vocabulary supplied as the reference.

This round uses a real deciphered logo-syllabic script, Linear B, with its known language (Mycenaean Greek). It degrades the conditions step by step toward the Indus situation and asks whether sign values can still be recovered.

## Data (external, frozen)
- `j-luo93/NeuroDecipher` commit 480bad2487820e3737fecfdd108214efa769e34b, `data/linear_b-greek.cog`.
- 919 Linear B word types; 70 syllabogram types; 3,451 sign tokens; mean 3.76 signs per word.
- Each word is paired with Greek comparison forms (classical/normalised, with digamma as `f`).
- Plaintext truth = the Unicode syllabogram value (e.g. KO, NO, SO).
- For scale: the Indus core corpus has 1,936 text types and over 400 sign types. So this benchmark is SMALLER in text and much smaller in sign inventory.

## Solver (fixed)
1. Every sign is renamed to a random ID (the cipher).
2. A mapping sign → syllable value is searched by simulated annealing. The candidate values are the 70 true Linear B values. This is generous: for Indus the value inventory is unknown.
3. Objective: the log-likelihood of all cipher word tokens, decoded, under a syllable-bigram language model with BOS/EOS and add-0.1 smoothing over the 70 values, trained on the condition's reference lexicon.
4. Four chains × 150,000 proposals. The temperature falls linearly from 3.0 to 0.05.
5. The best chain is chosen by OBJECTIVE, never by accuracy.
6. Moves:
   - bijective conditions: swap the values of two signs;
   - many-to-one conditions: reassign one sign's value (80%) or swap (20%).

## Metrics
- **Primary:** token accuracy, the share of cipher sign tokens decoded to their true value.
- **Secondary:** type accuracy over signs with ≥5 tokens.
- **Baseline:** frequency-rank matching (signs sorted by frequency are assigned values sorted by frequency in the reference lexicon). This is classical frequency analysis.

## Reference lexicons
- **ORACLE:** the true Linear B spellings of all 919 words. This is an upper bound.
- **COGNATE:** every Greek comparison form converted to Linear B-style syllabic spelling by fixed rules:
  - letters map as β→p, γ/κ/χ→k, θ/τ→t, φ/π→p, λ/ρ→r, ξ→ks, ψ→ps, f→w, η→e, ω→o;
  - open CV syllables; a consonant before another consonant takes the next vowel;
  - syllable-final s/n/r/m are dropped before a consonant, and all word-final consonants are dropped;
  - syllables not in the inventory are kept and simply match nothing.

  This plays the role of "a related, later-attested language whose spelling conventions we must guess".
- **COGNATE-SHUFFLED:** COGNATE with syllables shuffled within each word, seed fixed (negative control).
- **HELD-OUT:** COGNATE forms of a random half of the words; the other half is the cipher. There is no vocabulary overlap, only phonotactics. This mimics knowing the language family but not the words on the seals.

## Conditions (all run, all reported)

| ID | Lexicon | Script | Boundaries | Indus-likeness |
|---|---|---|---|---|
| A | ORACLE | bijective, 70 signs | words | upper bound |
| B | COGNATE | bijective | words | favourable |
| B0 | COGNATE-SHUFFLED | bijective | words | negative control |
| C | COGNATE | homophones inflate to ~400 sign IDs (each value split into 1–11 allographs ∝ frequency; tokens assigned at random) | words | Indus-size inventory |
| D | COGNATE | as C | 1–3 words per text, no dividers | Indus-like |
| E | HELD-OUT | bijective | words | family only, no shared vocabulary |
| F | HELD-OUT | as C | as D | **closest Indus analogue** |

Seeds: cipher key 32001, homophone assignment 32002, text grouping 32003, half-split 32004, solver chains 32010–32013.

## Decision rule (fixed)
- If condition A is not at least 90%, the solver is broken. Fix it and rerun everything, documenting the fix.
- B0 must stay near baseline. If B0 is within 10 points of B, sequence content is not driving recovery.
- **Indus feasibility verdict** is based on D and F:
  - **FEASIBLE-WITH-LEXICON** if D ≥ 70% token accuracy.
  - **FEASIBLE-FROM-FAMILY** if F ≥ 70%.
  - **INFEASIBLE** if D and F are both < 40%.
  - Otherwise **MARGINAL**.
- If INFEASIBLE: purely statistical decipherment of the Indus script from its own corpus plus a related-language lexicon is not a viable route, even before adding the extra Indus difficulties (unknown language, unknown value inventory, likely logograms, names). Decoding would then need external anchors (a bilingual, or names in known-language records).
- A FEASIBLE result would justify building a Proto-Dravidian (and alternative-language) reference lexicon and running the same pipeline on Indus, with the same controls.
