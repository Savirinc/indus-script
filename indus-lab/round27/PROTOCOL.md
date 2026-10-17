# Cross-city prediction protocol

Fixed before execution, 11 October 2026. The underlying corpus has been explored in earlier rounds; this is a new computational split, not a pristine external dataset.

Question: does first-order sign-order information learned in one city improve prediction of distinct inscriptions in another city, beyond overall sign frequencies and shuffled order?

Use frozen inscriptions.csv; only cisi, site, type, dir., text, material. Select Harappa and Mohenjo-daro. Require one clean directed line, +DDD-DDD+, no 000, direction R/L or L/R, and at least two signs. Reverse stored strings for R/L, preserve L/R. Compare both city directions for all eligible object types and, separately, SEAL:S only. Do not consult Sanskrit or translation fields.

Within each city/subset collapse identical reading-order strings to one type, retaining all object IDs. Exclude from testing every string that occurs in the training city, so exact shared strings cannot supply test successes. Different near-duplicates may remain. Inputs are corpus transcriptions, not independently established physical objects or phonetic symbols.

Baseline: source-city unigram model, additive 0.5 smoothing over source vocabulary plus UNK and EOS. Sign-order model: source bigrams including BOS and EOS, interpolated with that unigram using a fixed total prior mass of 5 per preceding-sign context. Map test-only signs to UNK; never infer their identity. Report bits per predicted token overall, internal positions (excluding first sign and EOS), first sign and EOS separately. Lower is better. Also report test vocabulary coverage and per-inscription losses.

Controls: 200 independently seeded within-inscription permutations of source texts, preserving every text's length and sign multiset; same model and scoring. Reverse-source-order control. No parameter tuning or model selection from test results. Report all four conditions, not only favourable ones. A shuffle-tail fraction is descriptive, not a significance claim across dependent inscriptions/related variants. These controls do not prove linguistic encoding or identify a language.

Success would support transferable sign-order conventions under the stated selection and model. It cannot establish sign sounds, words, grammar, specific meanings, chronological influence, or a Dravidian origin. Near-duplicates, editorial normalisation and production templates could explain some transfer; SEAL:S controls only one broad object class.
