# Round 60 report: sign order under the atlas key

**Verdict (pre-registered): ORDER SIGNAL, by a narrow margin.** Both controls passed.
- With the atlas key, the scribes' order of the signs gives more Sanskrit dictionary words than reorderings of the same signs.
- The gain is larger than for every one of the 20 scrambled keys in the protocol. In a disclosed post-hoc check, 4 of 120 wrong keys reached it.
- This round is a measurement and moves no probability.
- A key fitted by its author to these same inscriptions is expected to show an order signal whether or not it is right. That alternative is not excluded (see "What this does and does not show").

Protocol: `PROTOCOL.md` (sha256 4588f85e…, commit fd5cde5). Script: `run60.py` (sha256 7ea524af…, commit 1d57517), run once. Log: `run60.log`.

## Data
1,689 distinct inscriptions, every sign with an atlas value, 3 or more signs, mean length 5.04 signs.

## Controls
| Control | Result | Bar | |
|---|---|---|---|
| Positive: Rāmāyaṇa windows of the same lengths | true order 86.6% vs permutations 81.7% (reversed 80.1%); G 0.049, z 16.7, pct 1.00; 20 syllable substitutions: max G 0.009 | pct 1, z ≥ 3, G above all substitutions | PASS |
| Negative: order-free syllable strings | G −0.003, z −1.13 | \|z\| < 3 | PASS |

The instrument detects real word order in Sanskrit, and the detection disappears when the syllables are substituted. It sees no order where none exists.

## Indus
| Key | True order | Permutations (mean) | Reversed | Order gain G | z | pct |
|---|---|---|---|---|---|---|
| Atlas key | 88.97% | 86.91% | 84.91% | **0.0207** | 7.84 | 1.00 |
| 20 scrambled keys (protocol) | 84.0–90.8% | | | −0.025 to **0.0189** | −7.5 to 5.2 | 0.00–1.00 |

- Scrambled keys with G at or above the atlas key: 0 of 20. Under the rule this is ORDER SIGNAL. The extra-key robustness step was not triggered, and z = 7.84 lies outside the redraw band.
- Five of the 20 wrong keys also show a significant order gain on their own (pct 1.00, z 3.1–5.2), and 46906 comes close to the atlas key (0.0189 vs 0.0207). The dictionary therefore finds order-dependent words even through keys known to be wrong. This is the reason the protocol compares against them.
- The order gain is about 40% of the gain in real Sanskrit (0.021 vs 0.049). The true order also beats reversal by 0.041.

**Post-hoc, descriptive only** (`posthoc60.py`, written after the verdict, seeds 47001–47100; it does not change the verdict):
- 4 of 100 further scrambled keys reach the atlas key's gain, which makes 4 of 120 overall (max 0.0252).
- Among the 120 wrong keys, mean G is −0.0003 and sd 0.0109. The atlas key sits at z 1.93, roughly the top 4%.

**Per inscription** (`order_ledger.csv`): the true order beats the permutation mean in 1,068 of 1,689 inscriptions, loses in 516 and ties in 105.

## What this does and does not show
- **Shows:** under this key, the order the scribes used reads as Sanskrit a little better than shuffled orders, and better than most wrong keys manage. This is the first measurement in the lab where the atlas key separates from its scrambles in the expected direction. Round 47 (language model, NULL), round 59 and the atlas coverage (C19) did not.
- **Does not show:** that the key is right.
  - The key's author assigned values while reading these inscriptions in their true order and looking for Sanskrit. A key fitted that way should make common true-order sequences into words.
  - Round 49 found that refits of an author's value inventory reach z 3–10 in any language.
  - The margin over wrong keys is about the top 4%, and the round is not scored.
- **What would separate the two:** a key fitted by machine, on half the inscriptions, to maximise Sanskrit coverage in the true order, then measured on the other half.
  - If such a fitted key, known to have no history behind it, matches or beats the atlas key's order gain, the signal is explained by fitting.
  - If it falls well short, the atlas key's gain needs another explanation.
  - That would be a separate pre-registered round.
