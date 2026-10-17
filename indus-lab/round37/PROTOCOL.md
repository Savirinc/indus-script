# Round 37 — Substrate fingerprint: which language family do the Rigveda's foreign words resemble? (pre-registered)

Written 12 October 2026 before any scoring code was run. The source files were inspected for format only.

## Question
Kuiper (1991) listed 383 Rigvedic words that "have little or no chance of being of Indo-European origin". They are the oldest written residue of the language(s) spoken in the northwest before or alongside Vedic. The question: does their sound pattern resemble Dravidian, Munda, Burushaski, or none of the available families? No family is assumed in advance.

## Data (frozen)
- **FOREIGN:** Kuiper 1991, ch. V numbered list (archive.org OCR text). Parsed automatically; OCR errors normalised by the fixed mapping in `fingerprint.py`.
- **INHERITED:** CDIAL Old Indo-Aryan headwords (JAMBU `cdial.csv`, language "Indo-Aryan", position "1:", attested only, i.e. no leading `*`) whose CDIAL entry has a PIE etymology in JAMBU `etymologies.csv`. Split 50/50 (seed 37001) into TRAIN and HELDOUT.
- **DRAVLOAN (positive control):** CDIAL OIA headwords that JAMBU `cross-family-comparisons.csv` marks as relation "loan", direction "entry-from-compared", compared with a DEDR entry. Any confidence.
- **Target lexicons scored:**
  - PDR: Dravidian Database `pdr_04.csv`, reconstructions;
  - MUNDA: JAMBU `munda/forms.csv`, all languages incl. Proto-Munda;
  - BUR: Burushaski, JAMBU Berger plus IDS Burushaski if present;
  - EUS: Basque (IDS);
  - FIN: Finnish (IDS);
  - IA-HELDOUT: inherited half.
  - Each lexicon is de-duplicated after normalisation.

## Normalisation (applied identically to every set)
- Lower-case; long and short vowels merged (a, e, i, o, u).
- Aspiration dropped; retroflex merged with dental; all sibilants → s; nasals → n.
- Glottal stops and length marks dropped.
- Voiced and voiceless stops kept distinct (b, d, g, j vs p, t, k, c); other letters kept if they are a–z.
- Reason for the merges: the OCR of Kuiper's text loses diacritics, so they must be lost for every set equally.

## Method
- **Features:** character unigrams and bigrams over `^word$`, plus word-length bins (≤3, 4–5, 6–7, ≥8).
- **Classifier:** L2 logistic regression (λ = 1.0, class-balanced), trained on FOREIGN vs INHERITED-TRAIN.
- **Fingerprint** F(lexicon) = mean predicted log-odds of "foreign" over the lexicon's words. ΔF = F(lexicon) − F(IA-HELDOUT).
- **Uncertainty:** 500 bootstrap resamples of the training words (both classes) give rank probabilities.
- **Criterion-blind variant (secondary, reported always):** additionally map b→p, d→t, g→k, j→c (voicing removed), because Kuiper used b- and voicing-type criteria to select words.

## Positive control (runs first; gates interpretation)
- The same pipeline with DRAVLOAN in place of FOREIGN.
- **PASS** if PDR has the highest ΔF among {PDR, MUNDA, BUR, EUS, FIN} in ≥ 90% of bootstrap resamples, in the primary normalisation.
- If the control FAILS, the FOREIGN result is reported as uninterpretable.

## Decision for FOREIGN (only if the control passes)
- A family MATCHES if it ranks first in ≥ 90% of resamples AND exceeds both EUS and FIN in ≥ 95%.
- It is CRITERION-ROBUST if the same holds in the criterion-blind variant.
- Otherwise: no single family matches; report the profile.

## Limits stated in advance
- Foreign words were reshaped to Vedic sound habits. Kuiper's list is one scholar's judgement and mixes layers (some pre-Indian, some Central Asian).
- Lexicons differ in size and type (reconstructions vs modern forms).
- A match would show the Rigvedic substrate's sound pattern resembles a family. It would NOT show that the Harappans spoke it, though it is the closest evidence available without a decipherment.

## Deviations (made before any score was computed)
1. INHERITED: JAMBU `etymologies.csv` gives PIE etymologies for only 2 entries, so INHERITED = Rigveda-attested CDIAL OIA headwords (tag "RV") minus Kuiper's words and the Dravidian loans. It is contaminated by unrecognised foreign words (Kuiper: a few % of RV vocabulary), which biases toward NO difference.
2. Proto-Dravidian alternatives ("X ~ Y", "X, Y") use the first form only.
3. Burushaski has only 39 forms available (Berger subset; IDS has no Burushaski). Its results are reported but flagged as low-sample.
