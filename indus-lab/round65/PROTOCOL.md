# Round 65: Can the fit tell the right language from wrong ones, without knowing the answer? (pre-registered measurement)

Written 28 October 2026, before `run65.py` exists. Disclosed in advance:
- **Rounds 63b and 64 have been seen in full.** In the round 64 setting (Linear B made logosyllabic: 42% of words as single word signs, no dividers, one sound sign per syllable, S = 70), the solver given the Greek lexicon recovers the sound signs (median 0.855), and a Finnish lexicon recovers 0.02.
- **Round 45** found Finnish fitting better than Dravidian, and **round 47** found refits to Finnish and Basque beating a published key. The fit score of a wrong language can look as good as the right one.
- No fit has yet been run with any lexicon other than the round 63 Greek cognate list and Finnish in this setting. The IDS word lists named below have only been opened to list their characters and a sample of 10 forms each (to write the spelling rule).

## Question
In round 64 we knew the answer, so accuracy against the truth was the score. On Indus there is no truth. The question here: **given only the cipher and several candidate languages, does a statistic computed without the answer rank the true language first?** If it does, the same procedure can be pointed at Indus with Dravidian, Indo-Aryan, Munda and other candidates. If it does not, no language claim for Indus can be checked by fitting, and that is what is missing.

## Ledger status (rule 4)
**Measurement, cluster K3 (continued).** It is about the power of a method on a known script and moves no probability about Indus. If the solver control passes it adds fact C24.

## Cipher (round 64 set P, unchanged)
`run64.build(q = 0.42, regime = 'R2', S = 70, seed, opaque = True)`, imported unchanged. Layouts: seeds **65001–65005** (extra 65006–65010, see Robustness).

**Decoy cipher.** The same segments with the sign order shuffled within every segment (`random.Random(seed + 700)`, one shuffle per segment occurrence, applied in segment-list order). Sign frequencies, segment lengths and segment count are kept. Only the order is destroyed.

## Candidate languages
Every lexicon below is turned into Linear B syllables by one spelling rule (below), except G-same.

| Code | Lexicon | Role |
|---|---|---|
| **G-same** | Round 63/64 Greek cognate list (`run63.lexicon('greek')`): the plaintext's own words | Ideal right language (as rounds 63–64) |
| **G-IDS** | Ancient Greek, IDS `Language_ID` 167: independent vocabulary list | **Realistic right language:** the language is right but the words are not the inscriptions' words, as it would be for Indus |
| G-mod | Modern Greek, IDS 168 | Descendant: descriptive only, not in the ranking |
| Wrong (9) | Finnish 128, Basque 219, Hungarian 131, Hawaiian 235, Maori 236, Spanish 176, Latin 169, Sanskrit 211, Persian 214 | Wrong languages, from 5 families. Hawaiian and Maori are open-syllable languages that fit a CV syllabary easily, so they are the hardest decoys. |

**Spelling rule (all IDS lists).**
1. Split each form at spaces, hyphens and full stops. Each piece is a word.
2. Lower-case. Delete `ʰ`, `'`, `ʔ`. Unicode NFD and drop combining marks (so ā → a, ü → u, ő → o).
3. Map characters: æ ɑ ə → a; ɛ → e; ɔ ø → o; b → p; g → k; f → p; v → w; l → r; h → (none); c → k; q → k; x → ks; y → j; ŋ ɲ → n; ð → d; θ → t; ɣ → k; ʃ → s; ʒ → z.
4. Keep only a–z. Syllabify with round 63's `syllabify` (the round 32 `to_lb` loop: word-final consonants dropped, syllable-final s/n/r/m dropped).
5. Keep non-empty results. Take the distinct words, sorted, and if more than 1,500 remain, keep a sample of 1,500 (`random.Random(65900)`).

The bigram LM for every language is round 32's `fit_lm`, unchanged.

## Fits
For each layout × each of the 12 lexicons × {real cipher, decoy cipher}, run the round 32 v2 solver, imported unchanged: 4 chains (seeds 65300–65303) at 600k steps, keeping the best objective. That makes 120 fits.

## Statistics (none uses the truth)
For a key k, let **LL(k)** = the bigram LM log-likelihood of the decoded segments (`Scorer.total` × counts, without the emission term) ÷ cipher tokens.

- **D_L** = LL on the real cipher − LL on the decoy cipher, each at its own best key. It measures how much better language L explains the real sign order than a shuffled order.
- **I_L** = the same gain on L's own lexicon:
  1. group L's words into segments of 1–3 words (`random.Random(65800)`, as in R2) and concatenate them;
  2. shuffle the order within each segment (`random.Random(65801)`);
  3. I_L = LL of the real segments − LL of the shuffled segments, per token, under L's own LM.

  It is the order information that language L's LM can see at all.
- **Primary: R_L = D_L ÷ I_L.** This is the share of language L's maximum order gain that it achieves on the cipher. Dividing by I_L removes the advantage of languages whose bigram LM is simply more peaked.
- Descriptive:
  - D_L;
  - raw LL on the real cipher (the round 45 trap);
  - the best objective;
  - accuracy against the truth (real cipher, G-same and G-IDS only meaningful).

## Positive control (solver, rule 6)
G-same on the real cipher must recover the sound signs: **median sound-token accuracy ≥ 0.70** over layouts 65001–65005 (round 64 got 0.855 here). If it fails, the round is VOID.

## Negative control
The wrong languages, Finnish and Basque among them, are the impossible languages. The verdict below fails if any of them ranks first.

## Verdict, fixed now
Ranking set: G-IDS and the 9 wrong languages (10 in all). G-same is ranked separately against the same 9 wrong languages. "First" means the highest R_L in that layout.

| Verdict | Condition |
|---|---|
| **DISCRIMINATES** | G-IDS is first in ≥ 4 of 5 layouts. An independent vocabulary list of the right language can be told from wrong languages, from the inside. |
| **ONLY WITH THE TEXT'S OWN WORDS** | G-IDS is first in ≤ 2 of 5, but G-same is first in ≥ 4 of 5. Discrimination works only if the LM already contains the inscriptions' words. For Indus this does not apply. |
| **CANNOT DISCRIMINATE** | G-same is first in ≤ 3 of 5. Even the exact plaintext lexicon is not picked out. |
| **VOID** | The positive control fails. |

**Robustness (rule 7).** If G-IDS (or, for the second line, G-same) is first in exactly 3 of 5, run layouts 65006–65010 for every lexicon. The 4-of-5 condition then becomes ≥ 7 of 10, and the ≤ 2-of-5 condition becomes ≤ 5 of 10. If G-IDS lands at 6 of 10 after this, the verdict is **IN BETWEEN** and is reported as such.

## What this can and cannot show
- **Kinder than Indus:**
  - the cipher is round 64's (word signs single-use, separable);
  - the right language is among the candidates;
  - the sound inventory is Linear B's.
- **Harder than a real candidate test:** each candidate gets only an IDS concept list of about 1,500 words, not a text corpus.
- **Cannot:** show which language Indus is, or that any candidate list for Indus is good enough. A pass licenses running the same procedure on Indus under a new protocol.
- **Can:** show whether a truth-free statistic picks the right language in the setting where round 64 showed the sounds are recoverable.

## Outputs
`run65.py`, `results.json`, `run65.log`, `REPORT.md`; STATUS, ledger (C24 and a K3 row), CLAUDE.md, README and CITATION (0.65.0). Expected compute: 120 fits at 600k on 8 processes, about 25 minutes.
