# Round 37 — Substrate fingerprint: UNINTERPRETABLE (positive control failed; pre-registered)

12 October 2026.

## What was tested
- A classifier learned what makes Kuiper's 386 non-Indo-European Rigvedic words sound different from ordinary Rigvedic vocabulary (1,701 CDIAL headwords).
- It then scored which language family's words share that "foreign" sound profile: Proto-Dravidian, Munda, Burushaski, and Basque and Finnish as controls.
- The gate: the same pipeline, run on 45 Indo-Aryan words that Turner marks as borrowed from Dravidian, had to point to Dravidian.

## Result (ΔF = how "foreign-like" each lexicon scores relative to held-out Vedic words)

| Target words | Normalisation | 1st | 2nd | 3rd | Verdict |
|---|---|---|---|---|---|
| Dravidian loans (control) | primary | Finnish +1.58 (P rank 1 = 0.68) | Proto-Dravidian +1.44 (0.32) | Munda +0.91 | **CONTROL FAIL** |
| Dravidian loans (control) | criterion-blind | Proto-Dravidian +1.30 (0.52) | Finnish +1.30 (0.46) | Munda | fail |
| Kuiper foreign words | primary | Finnish +1.77 (0.99) | Proto-Dravidian +1.42 | Burushaski +1.17* | uninterpretable |
| Kuiper foreign words | criterion-blind | Finnish +1.48 (0.87) | Proto-Dravidian +1.32 | Munda +0.98 | uninterpretable |

*Burushaski: only 39 forms.

## Why it failed
- Every non-Indo-Aryan lexicon scores "foreign-like" (all ΔF > 0). The classifier learned "does not sound like Sanskrit", not "sounds like donor X".
- Finnish, with simple CV syllables and many vowel-final words, is the most un-Sanskrit-sounding lexicon, so it wins regardless of the true donor.
- Sound-profile resemblance cannot attribute a loan to its source family at this resolution.

## What survives (descriptive only)
- In both runs Proto-Dravidian ranks first among the *South Asian* candidates, ahead of Munda.
- But the control shows that this ranking is not trustworthy evidence. It is reported only so it is not lost.

## Lesson for the next design
- Donor attribution needs word-level matching (each foreign word against its closest form in each family, compared with shuffled-word baselines), which is how etymologists work. A whole-lexicon sound profile is not enough.
- The Dravidian-loan positive control built here is reusable for that test.

## Files
- `PROTOCOL.md` (with deviations logged before scoring), `fingerprint.py`, `results.json`.
- `kuiper_parsed.txt`: the parsed list, with citation to Kuiper 1991. The book itself is not redistributed.
- `dravloans.txt`.
