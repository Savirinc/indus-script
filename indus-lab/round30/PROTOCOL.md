# Round 30 — Are Indus inscriptions from West Asian contexts statistically foreign? (pre-registered)

Written 11 October 2026 before any round-30 scoring code was run. The foreign rows were listed (site, type, text) to define groups. No foreign text was scored before this protocol was fixed. In-region texts were scored in earlier rounds, so they are not pristine.

## Published claim under test
Parpola (2005 Tōhō Gakkai lecture, pp. 47–48; also 1994): some Near Eastern Indus seals use "common Indus signs but in sequences completely dissimilar from those occurring on native Harappan texts". He reads this as Harappans abroad writing local-language names.
Vidale 2004 (p. 265): sequences on the western round seals are "unparalleled in Punjab and Sindh".
Laursen 2010 (p. 116, citing Parpola): only Susa, Luristan and Girsu among the round seals are well paralleled. The unsupported ones cluster in his Bahrain/Mesopotamia group. Square Indus seals abroad (e.g. Kish, Umma) are not flagged.
These are qualitative judgments. They have not been tested against a held-out baseline with matched lengths.

## Data
Frozen `raw/inscriptions.csv` (SHA256 c22d39c3…3429). Fields used: id, region, site, type, dir., text. No Sanskrit or translation field is used.
Eligible text: one clean line `+DDD-…+` with no 000 and at least 2 signs, direction R/L (reversed) or L/R (kept). This is the same rule as round 27.

**In-region (training and control pool):** regions Inter-Riverine, Lower Indus, Gujarat/Kutch, Eastern Headwaters, Upper Indus. Baluchistan-sphere and Shortughai rows are excluded from all groups.

**Foreign group F:** eligible rows from regions Mesopotamia and Persian Gulf, sites Susa, Luristan and Tepe Yahya, and Central Asian sites other than Shortughai. Expected n≈16.
- F_C = SEAL:C (circular stamp seals), expected n≈8. This is the PRIMARY group.
- F_S = SEAL:S plus the Umma sealing (TAG:L), expected n≈5. Secondary group.
- Remaining types (tablet, pot graffito, cylinder) count toward F only.

Exploratory group U_C: eligible SEAL:C rows of unknown provenance. Analysed separately and never pooled with F.

## Model and leakage control
Round-27 bigram model (`fit`, `evaluate`) unchanged. It is trained on all in-region eligible text TYPES (all object types). For every scored text, foreign or control, the training set excludes that exact type and every one-edit neighbour (substitution, deletion or insertion). Test-only signs map to UNK.

## Metrics (per text)
- M1 (PRIMARY): bigram bits per predicted token, all positions including first sign and end marker.
- M2: unigram bits/token (sign-frequency surprise only).
- M3: order surprisal. Conditional bits of the true order given the text's sign multiset under the bigram model (exact DP from round 29), minus log2(number of distinct orders). Negative means more predictable than a random order. Defined only for texts with at least 2 distinct orders and length ≤9.

## Test
Control pool for the primary test: in-region SEAL:S texts. Each control is scored with its own leave-neighbourhood-out model.
For a foreign text of length L, its percentile is the fraction of same-length controls with a lower loss, ties counted half. If fewer than 30 controls have length L, use L±1, then L±2.
The group statistic is the mean percentile. Null: 20,000 draws, each replacing every foreign text with a random control of matched length and recomputing the mean percentile (the control's percentile is computed within the same pool). One-sided p = share of null draws ≥ observed.

## Decisions (fixed)
- P1 (primary): F_C on M1. SUPPORT the published claim if p < 0.01 and mean percentile ≥ 0.70. CONTRADICT if p > 0.20. Otherwise INCONCLUSIVE.
- P2 (specificity): F_S on M1. The literature predicts no anomaly (p > 0.05). If F_S is also anomalous at p < 0.01, a generic "found abroad / catalogued differently" effect becomes the leading explanation over the seal-type-specific claim.
- P3 (mechanism, descriptive): for F_C, report M2 and M3 percentiles. Anomaly concentrated in M2 points to unusual signs. Anomaly in M3 points to unusual ORDER, which is the published claim. No decision threshold; this is descriptive.
- Secondary: a sensitivity run of P1 against an all-types in-region control pool.

## Power checks (run with the test; reported regardless)
200 simulations each, n=8 texts drawn as matched controls and then:
- (a) pseudo-writing: every sign replaced by a draw from the in-region unigram distribution;
- (b) order-only anomaly: signs kept, order shuffled.
Report the share of simulations reaching P1's support threshold. If power for (b) is below 0.5, a non-supporting P1 result on order is reported as low-power, not as a contradiction.

## Interpretation limits
SUPPORT means these texts are statistically atypical of Indus-valley sign usage. It cannot by itself distinguish:
- a different language written in Indus signs,
- personal names or titles,
- pseudo-script by non-literate copyists,
- a regional sub-convention,
- transcription problems on worn seals.
None of these assigns a sound. The value of a SUPPORT result is that it localises where a cuneiform-named-person anchor (Dilmun or Meluhha personal names) could most plausibly attach. That is a separate, later test.
