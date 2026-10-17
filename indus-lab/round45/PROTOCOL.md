# Round 45 — Bias check: do impossible languages also "fit"? (pre-registered)

Written 13 October 2026 before any fitting.

## Question
In round 43, the 24 Dravidian sound values beat about 95% of their shuffles on held-out Indus texts (pooled p = 0.066). Is that specific to Dravidian, or does the method reward any real language's words in these slots?

## Control languages
Finnish and Basque. Neither can have been the Harappan language. Both have IDS word lists in this workspace (lexibank_ids), already used as controls in rounds 37–40.

## Anchors (rule fixed now)
Use the first IDS form for each concept: fish; man (vs. woman); arrow; pot, cooking vessel (for 740 jar); leaf (803, 806); bird (269); one … eight (the same numeral signs as rounds 42–43). Normalise with round 37 `norm`.

| Concept | Finnish | Basque |
|---|---|---|
| fish | kala | a'raɲ |
| man | mies | 'gison |
| arrow | nuoli | 'fleša |
| pot | pata | tʰi'piɲa |
| leaf | lehti | 'oṣto |
| bird | lintu | 'čori |
| 1 | üksi | bat |
| 2 | kaksi | 'biga |
| 3 | kolme | 'hiru |
| 4 | nelyæ | lau |
| 5 | wiisi | boṣt |
| 6 | kuusi | ṣei |
| 7 | seitsemæn | 'saspi |
| 8 | kahdeksan | 'sorc̷i |

## Model
This is the round 41–43 model, unchanged except that each language supplies its own pieces:
- **LM:** a character trigram model over all of that language's IDS forms, each normalised.
- **Inventory:** the 150 most frequent syllable chunks of that lexicon.
- **Fixed, as before:** anchor signs, permutation groups (numerals among numerals, pictures among pictures), the same 10 splits (seeds 43001–43010), the same 60 permutation seeds (43100–43159), fit seed 41050, 60,000 steps.

## Statistics
The same as round 43, computed per language:
- pooled p over the 60 shared permutations;
- the mean per-split percentile of the real anchors among their shuffles.

Dravidian reference (round 43): pooled p = 0.066, mean percentile ≈ 0.95.

## Decision
- **ARTEFACT:** either control language reaches pooled p ≤ 0.15. Then the method rewards word shapes, rounds 41–43 are not evidence for Dravidian, and the anchor-rebus branch is parked.
- **DRAVIDIAN-SPECIFIC:** both controls have pooled p > 0.30, AND the Dravidian mean percentile exceeds each control's by ≥ 0.20. Then the round 41–43 lean counts as real, and the round 44 copper-tablet test runs next.
- **INCONCLUSIVE:** anything else.
