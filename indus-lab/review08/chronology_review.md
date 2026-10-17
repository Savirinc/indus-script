# Independent chronology review, round 08

No prior code, chronology export, or raw data was changed. Run `python3 indus-lab/review08/chronology_review.py` to reproduce the supplementary audit.

## Concrete finding

The proposed 220/231 chronology comparison cannot currently support a claim that adding the internal stroke was a chronological innovation. Narrow-period, HARP-ID candidates contain only one row with 231 in 3C and none in 3B. The single case is H-1705 (source ID 939.1), a long rectangular seal; the candidate 3B assemblage contains no long rectangular seals. Date, object type and sample size are confounded.

| Candidate bin | All rows | ID stems | Rows with 220 | Stems with 220 | Rows with 231 |
|---|---:|---:|---:|---:|---:|
| 3B | 192 | 108 | 14 | 14 | 0 |
| 3C | 166 | 121 | 16 | 15 | 1 |

HARP-style excavation IDs are a provenance clue, not a certificate of secure dating. These are not counts of independently verified objects. Restricting further to square seals yields three 220 rows in 3C and one in 3B, and no 231 rows in either; there is no usable matched square-seal contrast in this subset.

## Coverage and potential false calendar mappings

The previous audit bins 1,930 of 2,717 Harappa rows. Of those, 915 have excavation identifiers outside the recognized HARP-style prefix, including every one of the 27 Period 4 rows. The prior script correctly calls the crosswalk provisional, but a matching label alone does not establish that a legacy object belongs to the HARP calendar interval. Keep all these records; withhold them from primary chronological inference until the source of the crosswalk is known.

The HARP-ID candidate group has 1,157 rows, with 1,015 assigned and 142 unassigned. It contains 55 rows with 220 and seven with 231. Four of the seven 231 rows are broad 3B/C, one general Period 3, one 3C, and one unassigned. None provides a narrow early-bin comparison. Period 5A and 5B remain unassigned; this review establishes no equivalence between those labels and the HARP Late Harappan phase.

## Record conflicts needing image/catalogue adjudication

- H-912 and H-1191 share the literal excavation ID `8650c448` and the same two face transcriptions (`+400-740-760-220-416+`, `+220-700-004+`). H-912 is labeled 3C-1/Stratum IV; H-1191 is labeled broad 3B/C. Treat as a possible duplicate or catalogue correction, not independent occurrences. Neither merge nor choose a date automatically.
- H-1682: source CSV says 3B/C; the primary report describes a 3B context. A broader metadata interval is not necessarily an error; retain both assertions with provenance.
- H-1734: source CSV lacks a period; the primary report places the stamped pointed-base-goblet group H-1727–H-1766 in 3C. This is a possible group-level date supplement, not a newly verified stratigraphic date for that individual sherd.

## Primary-source check and useful positive anchors

Kenoyer and Meadow (2010), *Inscribed Objects from Harappa Excavations 1986–2007*, Table 1 validates the HARP calendar ranges used in the prior pilot. Pages 4 and 12 discuss revised assignments and dating based partly on artifact style; avoid using those features both to date objects and to prove stylistic evolution. Page 10 identifies H-1688 around 2600 BCE; page 11 locates H-1692 in a 3B house-associated dustbin. These are useful object-specific anchors. Pages 7 and 11 support a 3C comparison group of stamped goblets and long rectangular seals. They do not validate every date in a derivative corpus.

Primary URL: https://www.harappa.com/sites/default/files/pdf/KenoyerMeadow%202010%20Inscribed%20Objects%20from%20Harappa.pdf

## Next admissible experiment

Use the photographed H-1688 and H-1692 anchors to test whether image descriptors recover independently documented changes in object form and carving, while keeping media different. For 220/231, continue photographic verification of the original substitution contexts; postpone any time-trend model until both variants occur on comparable object classes with independently supported dates. Report failure of current coverage as a result, not absence of the sign in ancient society.

The original local CISI 2 file was truncated and produced structural errors; its missing search results are unusable. The coordinator acquired an intact original scan. Inspection of printed page 339 (PDF page 374) verifies the published H-912 A/B and A/B bis images and its placement among incised tablets. H-1191 is outside this volume, so the proposed duplicate relationship and conflicting dates remain unresolved. An intact OCR derivative still returns no exact `8650` hit; this is an OCR/search limitation, not evidence that the excavation identifier is absent from the literature.

Original CISI 2 scan: https://archive.org/download/corpus-vol-2_202409/CorpusVol2.pdf

Recommended conservative patch to the main audit: retain the previous regex-derived bin as an explicitly unverified label crosswalk; assign calendar ranges only to HARP-ID candidate rows, still with provisional status; keep source-supported individual assertions in a separate override ledger that exposes rather than erases disagreements. The prefix rule is `re.match(r'^H(?:\d{2}|20\d{2})-', excavation_id)`. Calendar eligibility by this rule is only a first gate; secure context, redeposition, dating basis and independent physical-object identity are additional gates.
