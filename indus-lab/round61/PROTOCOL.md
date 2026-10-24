# Round 61: Do the atlas's Indus signs look like their Brahmi letters, and more than other scripts could? (pre-registered measurement)

Written 24 October 2026, before `run61.py` exists. No round 61 distance has been computed. Disclosed in advance from round 48 (fonts, descriptors, v1 run):
- Round 48 ended METHOD-FAIL. Nearest-neighbour counts over a 25-script pool could not detect Phoenician → Aramaic or Greek → Gothic.
- Its v1 Indus numbers were seen: Brahmi E = 0.35, rank 20 of 25; rarefied rank 19.
- 3 of 20 Table 7 pairs had the author's letter as the global nearest; the median rank was 594 of 1,061.
- Round 61 uses a different and more powerful statistic: **paired** distances against a permutation of the pairing itself. It does this because round 48's reopen criterion 2 asked for a higher-powered statistic. Round 48's criterion 1 (epigraphic glyphs) is still not met; modern fonts are used again.

## Question (Arham)
In the atlas, each Indus sign is drawn next to a Brahmi letter. Arham's point is that the shapes are close, so the pairs are not random.
- **A.** Are the atlas's sign–letter pairs closer in shape than the same signs paired with the same letters at random?
- **B.** Could letters from other scripts be assigned to the same groups of signs and look just as alike? This compares Brahmi with 24 other scripts, including ones that cannot be related to Indus.

## Ledger status (rule 4)
**Measurement, cluster K8 (shape).** No factor, for three reasons:
- The pairs were partly chosen by eye for shape. Table 7 is the author's look-alike table, so A can come out positive without any history behind it.
- The glyphs are modern fonts, not ancient forms.
- Shape continuity would not identify a language.

## Inputs (pinned in round 48 `SHA256SUMS`)
- **Indus glyphs:** `ext/fonts/indus-font.ttf`, codepoint U+E000 + catalogue code.
- **Pairs:** every code in `round46-brahmi-coverage/expanded-map.json` whose value is a single letter: a, i, u, b, c, d, g, j, k, l, m, n, p, r, s, t, v, y. That is 18 letters and about 440 signs; the exact list is written to `pairs.tsv`. Each pair uses the Brahmi letter the atlas chart displays:
  - a 𑀅, i 𑀇, u 𑀉;
  - b 𑀩, c 𑀘, d 𑀤, g 𑀕, j 𑀚, k 𑀓, l 𑀮, m 𑀫, n 𑀦, p 𑀧, r 𑀭, s 𑀲, t 𑀢, v 𑀯, y 𑀬.
  - Multi-letter values are compounds and are excluded.
- **Other scripts:** round 48's 25 scripts, fonts and code ranges, unchanged.

## Distance
Round 48 descriptor **B**:
- 64×64 grid, skeleton dilated to a 3-pixel stroke;
- symmetric chamfer distance;
- minimised over the 8 rotations and reflections, the same freedom for every script.

It is fixed now and no other descriptor is tried. Code: `run48.py` `render`, `Glyph`, `dist_matrix(..., 'B')`.

## Part A: paired test
- **Statistic:** `S` = mean over pairs of d(sign, its letter).
- **Null:** 10,000 permutations of the letter labels among the signs, keeping how often each letter is used (seed 61001).
- **Reported:** p = share of permutations with S ≤ S_real, and z.
- **Per letter:** the mean paired distance and its permutation p, as description only.

## Part B: could another script do as well?
The atlas groups signs into 18 letter groups. For each group g and candidate letter x, cost(g, x) = sum of d(sign, x) over the signs in g.
- For each script X: draw 22 of its letters at random (22 = the smallest inventory, so size is equal for all), 200 draws, seeds 61101+.
- In each draw, find the **best possible** one-to-one assignment of the 18 groups to 22 letters (Hungarian algorithm). `Opt_X` = mean optimal cost over draws.
- `Atlas` = the cost of the atlas's actual Brahmi assignment.
- **Reported:**
  - the rank of Brahmi among 25 scripts by `Opt_X`;
  - for each script, the share of its draws whose optimal cost is at or below `Atlas` ("this script, with letters chosen to fit, looks at least as alike as the atlas Brahmi pairs").

## Controls
**A-controls.** These use the same paired test with known letter pairs, 10,000 permutations, seeds 61011–61014.
- **PC-A1:** Phoenician → Greek capitals, 19 pairs: alf Α, bet Β, gaml Γ, delt Δ, he Ε, zai Ζ, het Η, tet Θ, yod Ι, kaf Κ, lamd Λ, mem Μ, nun Ν, semk Ξ, ain Ο, pe Π, rosh Ρ, shin Σ, tau Τ.
- **PC-A2:** Phoenician → Imperial Aramaic, 22 pairs in alphabet order.
- **NC-A1:** Phoenician → Linear A U+10600–10615, in order.
- **NC-A2:** Phoenician → Old Hungarian U+10C80–10C95, in order.
- **Pass:** both PC p < 0.01, and both NC p ≥ 0.05. Otherwise Part A is **VOID**.

**B-control.** Phoenician's 22 letters are 22 one-sign groups.
- The actual Greek pairing (19 groups) and the actual Aramaic pairing (22) are compared with the optimal pairings of the 11 unrelated scripts (round 48 `UNRELATED`), using 22-letter draws and the same 19 or 22 groups.
- **Pass:** both actual pairings cost less than the median `Opt_X` of every unrelated script. Otherwise Part B is **METHOD-FAIL** and is reported only as description. A true descent must at least beat what fitting can do with unrelated scripts.

## Verdicts, fixed now
**Part A**

| Verdict | Condition |
|---|---|
| **PAIRS SHAPE-CLOSE** | p < 0.01 |
| **WEAK** | 0.01 ≤ p < 0.05 |
| **NOT CLOSER THAN RANDOM** | p ≥ 0.05 |

**Part B**

| Verdict | Condition |
|---|---|
| **BRAHMI STANDS OUT** | Brahmi ranks 1st of 25 by `Opt_X`, **and** for every unrelated script fewer than 5% of draws reach `Atlas` |
| **FITTABLE IN ANY SCRIPT** | any unrelated script has ≥ 50% of its draws at or below `Atlas` |
| **IN BETWEEN** | otherwise; the failing clause is named |

Interpretation fixed now:
- PAIRS SHAPE-CLOSE with FITTABLE IN ANY SCRIPT means the pairs look alike, but letters from unrelated scripts can be made to look as alike. The resemblance is then what chosen look-alikes give, not evidence of descent.

## Outputs
`run61.py`, `pairs.tsv`, `results.json`, `run61.log`, `REPORT.md`; a STATUS row; a ledger fact (no factor). No glyph images are committed.
