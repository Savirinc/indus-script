# Round 38 — Word-level donor attribution of the Rigveda's foreign words (pre-registered)

Written 12 October 2026 before any scoring code was run. Inputs are the frozen sets from round 37: Kuiper list (386), Dravidian-loan control (45), Rigvedic background (1,701), and lexicons PDR, MUNDA, BUR, EUS, FIN. Round 37's normalisation is reused unchanged (primary only).

## Idea
A borrowed word has a real look-alike (its source) in the donor language's dictionary. Any word also has chance look-alikes in any big dictionary. So for each target word w and family F:
- m_F(w) = best similarity between w and any word in F, where similarity = 1 − normalised Levenshtein distance on the normalised strings.
- b_F(w) = mean of m_F over 5 background Vedic words of the same normalised length, drawn at random (seed 38001) from the Rigvedic background set, excluding w. This is the chance level for words like w.
- d_F(w) = m_F(w) − b_F(w).
- **A_F = mean d_F over the targets.** A real donor gives A_F > 0; a non-donor gives A_F ≈ 0 (chance only).

## Uncertainty
1,000 bootstrap resamples of target words (seed 38002) give a 95% CI for each A_F, P(F ranks first), and P(A_F > A_EUS and A_F > A_FIN).

## Positive control (gate)
Targets = the 45 Dravidian loans. **PASS** if PDR ranks first in ≥ 90% of resamples AND its 95% CI is above 0. If FAIL, the Kuiper result is uninterpretable.

## Decision for Kuiper's foreign words (only if the control passes)
- A family is the BEST-SUPPORTED DONOR if it ranks first in ≥ 90% of resamples, its CI is above 0, and it beats both EUS and FIN in ≥ 95%.
- A family is a SECONDARY CONTRIBUTOR if its CI is above 0 and it beats both controls in ≥ 95% without ranking first.
- Otherwise: no family attributable.
- **Exploratory, never counted as evidence:** the 30 best-matching word pairs per family, for human etymological review.

## Limits
- No meaning is used, so chance look-alikes remain; the baseline corrects their average, not their noise.
- Lexicons are of unequal size and type. The baseline is computed per lexicon, so size effects are subtracted.
- Kuiper's words are Vedic-adapted forms. Burushaski has only 39 forms, so it has low power.
