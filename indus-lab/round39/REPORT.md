# Round 39 — Sound + meaning attribution: control PASSES; no family reaches the bar; Proto-Dravidian leads (pre-registered)

12 October 2026.

## Result
A_F = how much better each target word's closest look-alike with a RELATED MEANING in family F is, compared with ordinary Vedic words of the same consonant/vowel shape.

| Targets | Family | A_F | 95% CI | P(rank 1) | P(beats Basque and Finnish) |
|---|---|---:|---|---:|---:|
| **41 Dravidian loans (control)** | Proto-Dravidian | **+0.156** | +0.092..+0.216 | **0.99** | 1.00 |
| | Munda | +0.046 | −0.001..+0.104 | 0.01 | 0.88 |
| | Finnish / Basque | ≈ 0 | spans 0 | 0.00 | — |
| **124 glossed Kuiper foreign words** | Proto-Dravidian | **+0.064** | +0.027..+0.096 | **0.80** | 0.82 |
| | Finnish | +0.042 | +0.007..+0.080 | 0.14 | — |
| | Basque | +0.029 | −0.004..+0.066 | 0.03 | — |
| | Munda | +0.028 | −0.007..+0.060 | 0.03 | 0.21 |
| | Burushaski (37 forms) | +0.028 | +0.004..+0.051 | 0.00 | 0.19 |

## Pre-registered decision
- **Gate: PASS.** Requiring related meaning removes the chance matches that sank rounds 37–38. Finnish and Basque drop to ≈ 0 on the control.
- **Kuiper words: NO FAMILY ATTRIBUTABLE.**
  - Proto-Dravidian is the only family whose CI is clearly above 0 and that leads.
  - But P(rank 1) = 0.80 < 0.90 and P(beats controls) = 0.82 < 0.95.
  - Finnish's CI also excludes 0 narrowly, a reminder of residual chance.

## What changed from round 38
The Munda lean seen with sound alone (round 38, uninterpretable) does not survive when meaning is required. With meaning, Proto-Dravidian leads.

## Caveats that limit this
1. **Unequal dictionaries.** Proto-Dravidian has 6,088 glossed forms, Munda 712, Burushaski 37. The baseline removes CHANCE matches, but a small dictionary also contains fewer TRUE sources. Munda and Burushaski are underpowered; "Dravidian leads" partly reflects better documentation. JAMBU's full Munda tables (Git LFS) were not downloadable here.
2. **Coverage.** Only 124 of 386 Kuiper words could be glossed via CDIAL (most proper names drop out).
3. **The gate is a minimum requirement.** Turner found those loans by sound+meaning matching, so recovering them shows the method works on known etymologies, not that it has power on unknown ones.
4. **Exploratory top pairs, not evidence.**
   - Proto-Dravidian: phala ~ *pal- 'fruit'; mālā ~ *māl- 'garland'; apūpa ~ appa 'cake'.
   - Finnish chance pair: niṣka 'neck ornament' ~ niska 'neck'.

## Next decisive step on this route
Equalise the dictionaries: subsample Proto-Dravidian to Munda's size repeatedly, or obtain the full Munda and Burushaski data. Re-run with the same gate. If Proto-Dravidian still leads at equal dictionary size, the Dravidian lean is about the substrate, not about documentation.

Files: `PROTOCOL.md`, `semantic_attribution.py`, `results.json` (with top pairs).
