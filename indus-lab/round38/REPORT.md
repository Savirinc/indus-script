# Round 38 — Word-level donor attribution: UNINTERPRETABLE (positive control failed; pre-registered)

12 October 2026.

## Result
A_F = how much better each target word's closest look-alike in family F is, compared with length-matched ordinary Vedic words.

| Targets | 1st | 2nd | 3rd | Verdict |
|---|---|---|---|---|
| 41 known Dravidian loans (control) | Finnish +0.050 (P rank 1 = 0.62) | Proto-Dravidian +0.040 (0.33) | Munda +0.018 | **CONTROL FAIL** |
| 386 Kuiper foreign words | Munda +0.030 (0.88; beats both controls 0.95) | Proto-Dravidian +0.020 (0.09) | Basque +0.017 | uninterpretable |

## Diagnosis (post hoc)
- Proto-Dravidian DOES contain the true sources of the control loans; exact matches include *valli*, *pota*, *mala*, *muta*.
- Finnish produces exact matches too, by chance: *mina* (Finnish 'minä' 'I'), *muta* ('mud').
- Dravidian loans have simple CV(C)V shapes, and so do Finnish words. Ordinary Vedic words (the baseline) have more clusters, so a length-matched baseline does not remove a syllable-SHAPE advantage.
- With meaning ignored and sounds coarsened (retroflex, aspiration and vowel length merged), short CV words match any CV-rich language. Rounds 37 and 38 failed for the same underlying reason.

## What it would take
Real etymology matches sound AND meaning. A meaning-constrained version would only count look-alikes whose glosses share a semantic field. Glosses are available from CDIAL (for Kuiper words present in CDIAL), the Dravidian Database, Munda sources and IDS. It should also use a shape-matched baseline (same consonant-vowel pattern). That test would be new; it would need its own pre-registration and the same Dravidian-loan gate. The Munda lean seen here must not be used to tune it.

Files: `PROTOCOL.md`, `attribution.py`, `results.json` (includes the top 30 look-alike pairs per family for review).
