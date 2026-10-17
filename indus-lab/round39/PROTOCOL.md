# Round 39 — Sound AND meaning donor attribution of the Rigveda's foreign words (pre-registered)

Written 12 October 2026 before any scoring code was run. Rounds 37–38 failed their Dravidian-loan control because sound alone lets short CV words chance-match any CV-rich language. Round 38's descriptive lean (Munda) was seen; nothing below was chosen with reference to it. All choices are stated here before scoring.

## Sets (from rounds 37–38, same normalisation)
- **Glosses:**
  - targets and background: CDIAL headword glosses (JAMBU `cdial.csv`, column 4);
  - Kuiper words: glossed by matching their normalised form to normalised CDIAL Old Indo-Aryan headwords; all glosses of all matches are pooled; unmatched Kuiper words are dropped and the count reported.
- **Lexicons with glosses:**

  | Lexicon | Source | Gloss |
  |---|---|---|
  | PDR | Dravidian Database `pdr_04.csv` | `meaning` (rows with a meaning) |
  | MUNDA | JAMBU `munda/forms.csv` | column 4 |
  | BUR | Berger | column 4 |
  | EUS, FIN | IDS | concept name of the form's Parameter |

## Meaning relatedness (fixed rule)
1. Gloss → lower-case word tokens.
2. Drop stop/generic words: a an the of to in on at and or with for by from as is be being used made etc esp e g i also sp species kind sort type part thing name names person man woman one small large big great little good bad very much many some any other certain particular.
3. Crude stemming: strip a final "es"/"s"/"ing"/"ed"/"ly" if the remainder is ≥3 letters.
4. Two glosses are RELATED if they share at least one remaining stem.

## Score
- For target w (gloss G) and family F: m_F(w) = max sound similarity (1 − normalised Levenshtein) between w and any F-word whose gloss is RELATED to G; 0 if none.
- **Baseline:** b_F(w) = mean m_F over 5 background Vedic words with the SAME consonant/vowel shape as w (e.g. CVCVCV; fallback same length), each using its own gloss. Drawn with seed 39001; the target itself is excluded.
- d_F(w) = m_F(w) − b_F(w). **A_F = mean d_F.**
- 1,000 bootstrap resamples over targets (seed 39002).

## Gate (positive control)
- 41 Dravidian loans must give PDR rank 1 in ≥ 90% of resamples with its 95% CI above 0. Otherwise the result is uninterpretable.
- Caveat stated in advance: Turner attributed those loans by sound+meaning matching to DEDR, so passing shows only that the method recovers known etymologies, a NECESSARY condition, not proof of power on unknown donors.

## Decision for Kuiper's words
- **BEST-SUPPORTED DONOR:** rank 1 in ≥ 90%, CI above 0, beats both EUS and FIN in ≥ 95%.
- **SECONDARY:** CI above 0 and beats both controls in ≥ 95%.
- Otherwise: none attributable.
- **Exploratory only:** the top 30 sound+meaning pairs per family.

## Interpretation limits
- A positive result says which family has more sound+meaning look-alikes for the Rigveda's foreign vocabulary than chance. It is a quantitative tally of the etymological signal, not proof of the Harappan language.
- Kuiper's list includes proper names, which mostly drop out because they lack glosses.
