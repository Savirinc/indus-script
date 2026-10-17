# Round 44 — Copper-tablet picture test (pre-registered; conditional on round 43 REPLICATED)

Written 12 October 2026. At the time of writing, round 43 was still running (8 of 10 Indus splits done). No copper text has been decoded with any key.

## Idea
Mohenjo-daro copper tablets pair a short text with a picture, and the same picture tends to recur with the same text (round 24). If the 24 Dravidian anchors plus the fitted key capture real sound values, the decoded text should resemble the Proto-Dravidian word for the pictured animal more than the words for other animals.

## Material
- Round 24 eligible objects (`round24/predictions.json`). Texts are reversed into the core-corpus reading order; round 24 stores them in the opposite direction.
- **Categories used:** those with a Krishnamurti 2003 reconstruction in `pdr_04.csv` whose meaning names the animal.

  | Category | Word(s) |
  |---|---|
  | Elep | *yĀn-ay 'elephant' |
  | Hare | *moy-al, *muc-Vl 'hare' |
  | Buff | *er-umV- 'buffalo'; *kaṭ-V- 'wild buffalo'; *paḍḍ-V 'female buffalo' |
  | Goat:8 | *mē-nkkV 'goat'; *yĀṭu 'goat, sheep' |
  | Bull1:W | *ēṯu 'ox, bull' |

- **Excluded:**
  - Tigr: its only text is the round-24 flagged conflict family 407-061-845-240-798, also labelled Gaur.
  - Gaur, Rhin: no Krishnamurti word.
  - Loop, Comp, Anth: not animals with one word.
- Words are normalised with round 37 `norm`. The unspecified vowel V is deleted.

## Key
- Fitted once with round 41's `fit`: real 24 anchors, seed 41050, 60,000 steps.
- Training set: all core texts EXCEPT those identical to any eligible copper text, in either orientation.
- Secondary: fit seeds 44001–44004, reported for robustness only.

## Statistic
- sim(d, w) = 1 − (minimum edit distance between w and any substring of the decoded string d) / len(w). Take the maximum over a category's alternate words.
- Category score for animal a = the mean of sim over that category's distinct texts.
- **S** = the mean over the 5 categories of [score(own animal) − mean score(other 4 animals)].
- **Null:** all 5! = 120 assignments of animal-word sets to categories. p = #{assignments with S ≥ S_real} / 120 (the identity is included).

## Decision
- **PASS:** p ≤ 0.05 (the true assignment ranks in the top 6 of 120).
- Otherwise **FAIL**.

## Stated limits, in advance
- There are only 5 categories and about 9 distinct texts, so power is low; a FAIL is weak evidence against.
- Many scholars hold that copper-tablet texts are not animal names, so the test can fail even if the language is Dravidian.
- Labels are noisy: the Buff texts are near-identical to a Gaur-labelled text.
- A PASS would be the first non-statistical, meaning-level hit and would warrant an independent re-check, not a claim of decipherment.
