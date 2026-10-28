# Round 61: Do the atlas's Indus signs look like their Brahmi letters? Part A: NOT CLOSER THAN RANDOM. Part B: METHOD-FAIL

28 October 2026. The protocol was locked at 23d579b (24 October). Amendment 1 and the script were locked at 2adda94, before any distance was read. Fonts were verified against round 48 `SHA256SUMS` (26 files). The pool has 1,061 letters, none dropped. There are 440 pairs and no Indus glyph is missing (`pairs.tsv`).

## Part A: are the atlas's sign–letter pairs closer than random pairings? **NOT CLOSER THAN RANDOM**

| Test | Pairs | Mean paired distance | Permutation mean | p | z | Bar | |
|---|---:|---:|---:|---:|---:|---|---|
| PC-A1 Phoenician → Greek | 19 | 0.0691 | 0.0876 | 0.0001 | −3.90 | p < 0.01 | pass |
| PC-A2 Phoenician → Aramaic | 22 | 0.0655 | 0.0773 | 0.0018 | −2.99 | p < 0.01 | pass |
| NC-A1 Phoenician → Linear A | 22 | 0.0745 | 0.0738 | 0.58 | +0.22 | p ≥ 0.05 | pass |
| NC-A2 Phoenician → Old Hungarian | 22 | 0.0787 | 0.0756 | 0.81 | +0.89 | p ≥ 0.05 | pass |
| **Atlas Indus → Brahmi** | **440** | **0.0824** | **0.0829** | **0.33** | **−0.45** | | |

All four controls pass. The test sees real descent with only 19–22 letter pairs and rejects unrelated pairings. With 440 pairs, 20 times as many, the atlas pairs are no closer in shape than the same signs given the same letters at random.

**Per letter (descriptive, 18 tests, uncorrected):**

| Direction | Letters (number of signs, p) |
|---|---|
| Closer than random | m (49, p < 0.001), y (42, < 0.001), b (13, 0.001), p (8, 0.008); n (17, 0.049) borderline |
| Neither | c, l, i, g, j, k, v, d, s |
| **Further than random** | **a (40, p 0.999), t (53, p 1.000)**, r (58, 0.93), u (6, 0.92) |

A few letters were evidently chosen with shape in mind: m, y, b and p, where the Brahmi letter does resemble its signs. Several large groups go the other way. The 53 signs read t and the 40 read a are *less* like 𑀢 and 𑀅 than random signs are. Over the whole key the two directions cancel. The look-alike pairs on display in the atlas are a selection, not the rule.

## Part B: could another script be fitted as well? **METHOD-FAIL**
**B-control fails.** The real Phoenician → Greek pairing costs 1.31. Every one of the 11 unrelated scripts, with its letters assigned optimally, does better: medians 0.86–1.04. The same holds for Phoenician → Aramaic (1.44 against 1.04–1.30).

Optimal assignment is so powerful that it beats even true descent. So Part B cannot judge Brahmi, and its numbers are description only:
- The atlas assignment costs 36.3. Every script, Brahmi included, reaches a lower cost in 100% of its draws (means 22.8–27.9).
- By optimal fit Brahmi ranks **19th of 25**. The best-fitting script is Linear A, then Old South Arabian and Old Hungarian.
- This agrees with round 48's description (Brahmi rank 20 of 25), which was seen in advance.

## What it means
- **Shape leg of the Brahmi lead.** Round 48 left it untestable. Round 61 used a statistic that the controls show is powerful, and found **no shape resemblance beyond chance across the atlas's 440 sign–letter pairs**. Where resemblance exists (m, y, b, p), it is offset by groups that look less alike than chance (t, a).
- **What still limits this.** The glyphs are modern fonts (round 48 reopen criterion 1, epigraphic tracings, is still unmet). Shape would not identify a language even if it had passed.
- **The Brahmi file now reads:**
  - coverage, not correctness (46);
  - sound leg NULL (47, 57);
  - running-text syllabic keys excluded (58);
  - traded goods VOID (59);
  - order signal predicted by fitting (60);
  - **shape: atlas pairs not closer than random (61)**.

## Ledger
Measurement, cluster K8, no factor. Adds fact C23.

## Reproduce
`cd indus-lab/round61 && ../../ext/venv/bin/python run61.py` (about 11 s). This needs Pillow, numpy, scipy and fontTools in `ext/venv`, plus fonts from `round48/fetch_fonts.sh`.
