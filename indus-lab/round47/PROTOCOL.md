# Round 47 — Is Yajnadevam's Indus→Brahmi/Sanskrit key Sanskrit-specific, or does it read any language? (pre-registered)

Written 17 October 2026, before any scoring, fitting or lexicon inspection beyond file formats. Committed before `run47.py` exists.

## Question
Yajnadevam (Bharath Rao) proposes that Indus signs are early Brahmi letters and that the inscriptions read as Sanskrit. Round 46 showed his 714-code key is executable and assigns a value to every sign in every complete single-line text. Coverage is not correctness: any complete key covers the corpus. The question here is whether the key's output is **Sanskrit-like beyond what shape-matched keys produce, and more Sanskrit-like than it is Finnish-, Basque- or Proto-Dravidian-like.** Round 45 showed that a Dravidian anchor set which beat its shuffles was beaten harder by Finnish. Every proposed key must now face that test.

Prior evidence: Bourdeau (round 34 digest) found an earlier version of this key indistinguishable from shuffles in consonant mode (63/200 as good), mildly above shuffles with vowels (10/100) but reading *Dravidian* even better than Sanskrit, and his bench could not recognise the true Linear B key. Round 32 showed fitted keys outscore true keys at Indus density. The expectation going in is therefore NULL or ARTEFACT. A SUPPORT verdict would be the surprise.

## Hypotheses
- **H1 (author's claim, operationalised):** readings under the real key are more Sanskrit-like than under structure-preserving shuffles of the same key, and this advantage is specific to Sanskrit: it does not appear for Finnish, Basque or Proto-Dravidian, and cannot be matched by a key of the same label inventory fitted to those languages with a modest search budget.
- **H0a (null):** the real key is not distinguishable from its shuffles.
- **H0b (artefact):** the real key beats its shuffles, but so does it for impossible languages, or fitted keys for impossible languages do as well. The signal is label phonotactics (CV shape, vowel insertion), not Sanskrit.

## Frozen inputs
| Item | Source | Pin |
|---|---|---|
| Key K_Y | `round46-brahmi-coverage/expanded-map.json` (714 codes → label), derived from lipi `xlits.csv` | lipi commit fc8813a; sha256 in round46 `manifest.json` |
| Vowel-insertion rule | `xlitize()` in lipi `src/pages/index.vue` at the same commit | reproduced verbatim in `run47.py`; lines quoted in REPORT |
| Corpus | `FC.TRAIN` from `round30/foreign_context.py`: core-region text types of `raw/inscriptions.csv`, deduplicated, reading order | inscriptions.csv sha256 c22d39c3…3429 |
| Sanskrit lexicon | Monier-Williams headwords (`<k1>` field of `mwtranscode/mw.txt`, SLP1), sanskrit-lexicon/MWS | commit recorded in `fetch_lexicons.sh`; CC BY-SA 4.0 |
| Finnish lexicon | Kotus *Nykysuomen sanalista* via hugovk/everyfinnishword `kaikkisanat.txt` | commit recorded in fetch script; LGPL-2.1 |
| Basque lexicon | Xuxen hunspell stems, `dictionaries/eu/index.dic` in wooorm/dictionaries, flags stripped | commit recorded; GPL |
| Proto-Dravidian lexicon | `external/dravidian_db_v1.1/pdr_04.csv`, `reconstruction` column, rows classified Proto-Dravidian, normalised with `round37/fingerprint.py:norm` | CC BY 4.0; already in repo |
| Greek (control only) | NeuroDecipher `linear_b-greek.cog`, Greek comparison forms | commit 480bad2 |
| Linear B texts (control) | same file, 919 word types, 70 syllabograms | same |

Lexicons are word **types**, lower-cased, deduplicated after collapsing (below). None of the Indus corpus's upstream Sanskrit/translation columns is read.

## Alphabet collapse (fixed before running)
Yajnadevam's labels use 20 symbols: `a s n r m t d y k l A i b v p j c u g h`. His `decipher.csv` groups k/kh, g/gh, c/ch, j/jh, t/th/ṭ/ṭh, d/dh/ḍ/ḍh, p/ph, b/bh, ś/ṣ/s/h, an/aṃ, as/aḥ. Every lexicon is collapsed to the same granularity so the key is judged at the resolution it claims:
- aspirates → plain; retroflex → dental; ś ṣ h ḥ → `s`; ṅ ñ ṇ ṃ → `n`; ṛ → `ri`, ḷ → `li`; long ā → `A`; ī → `i`, ū → `u`; e, o, ai, au kept as `e`, `o`, `ai`, `au` (the key never emits e/o; this penalises every key under every language equally).
- Finnish: ä→a, ö→o, y→u, å→o, h→s, f→p, c/q→k, w→v, x→ks, z/š→s, ž→j; geminates kept.
- Basque: tx/ts/tz→c, x/z→s, ñ→n, h→s, f→p, ll→l, rr→r, w→v.
- Proto-Dravidian: `norm()` output, then the same retroflex/aspirate merges; `norm` already drops length, so PDr has no `A`.
- Greek: standard romanisation (β b, γ g, δ d, ζ s, θ t, κ k, λ l, μ m, ν n, ξ ks, π p, ρ r, σ/ς s, τ t, φ p, χ k, ψ ps, digamma v), accents stripped, η→e, ω→o, υ→u.
- Everything is then restricted to `[a-zA]`; characters outside the set are dropped.

## Reading procedures
- **P-V (primary):** reading-order labels joined with Yajnadevam's inherent-vowel rule: after each label that does not end in `i`, `u`, `an` or `as`, insert `a` unless the next label is exactly `a`, `i` or `u`; append a final `a` under the same condition. This is his display rule, reproduced verbatim.
- **P-C (secondary):** consonant skeleton: delete `a A i u` from labels and from lexicon words; `an`→`n`, `as`→`s`. Bourdeau's consonant mode.
Texts containing any sign without a label are dropped and counted.

## Language model and statistic
Character trigram model with add-0.1 smoothing over the collapsed alphabet plus boundary symbols, exactly the `LM` class of `round41/anchored.py` (stdlib reimplementation; no numpy). Trained on a lexicon's word types. A text's reading is scored as one string with boundaries.

**Statistic** S(K, L) = −(total log₂ probability of all readings under LM_L) / (total reading characters) = bits per character. Lower is more L-like.

**Lexicon size matching (primary):** each lexicon is subsampled without replacement to the size of the smallest (expected: Proto-Dravidian, a few thousand types), 5 draws, seeds 47101–47105; S is averaged over draws. **Secondary:** full lexicons.

## Null distribution
**Structure-preserving shuffle:** signs are sorted by corpus token frequency and cut into bins of 20 consecutive signs; labels are permuted among signs within each bin. This keeps the label-frequency profile of the output (how often `an`, `r`, `m` … appear) and the label inventory, and destroys only *which* sign carries which label. 1,000 shuffles, seeds 47201–47200+1000. **Secondary:** unrestricted permutation of labels over signs, 1,000 shuffles.

For a key K and language L: percentile p(K, L) = share of shuffles with S ≥ S(K, L) (so 0.99 means the real key is more L-like than 99% of shuffles); z(K, L) = (mean_shuf − S(K, L)) / sd_shuf (positive = more L-like than shuffles).

## Positive controls (must run first)
Linear B with its true Ventris key, scored against Greek and against the four Indus-test languages, with the same shuffle null and statistic:
- **PC1:** bijective, 70 signs, texts = the 919 word types (round 32 condition A geometry, no lexicon oracle: Greek LM trained on the comparison forms of a random half of the words, the other half is the cipher; seed 47301).
- **PC2:** Indus density: round 32 `build()` with homophones (~400 sign IDs) and 1–3 words per text without dividers (round 32 condition D geometry, seeds 32001–32003), Greek LM trained on the held-out half.
- Pass criteria, each: p(true, Greek) ≥ 0.99 **and** z(true, Greek) exceeds z(true, L) for every other L by ≥ 2.
- If PC1 fails: **METHOD-FAIL**, stop, report. If PC2 fails but PC1 passes: the Indus test keeps its NULL/ARTEFACT power but a SUPPORT verdict is barred, because the scorer cannot certify a true key at Indus density.

## Matched-budget fitted controls
For each L in {Finnish, Basque, Proto-Dravidian, Sanskrit}: starting from a random permutation of K_Y's own label multiset over the signs, simulated annealing with swap moves maximises total LM_L log-probability of the P-V readings; 60,000 steps, temperature 3.0→0.05, 3 chains (seeds 47401–47412), best chain by objective. Score the fitted key with the same shuffle null: z(K_fit-L, L). This is a small budget compared with the author's development of K_Y, so it favours the author.

## Verdict rules (fixed)
Primary analysis = P-V, size-matched lexicons, structure-preserving null.
1. **METHOD-FAIL** if PC1 fails.
2. **NULL** if p(K_Y, Sanskrit) < 0.95.
3. **ARTEFACT** if p(K_Y, Sanskrit) ≥ 0.95 and either (a) z(K_Y, L) ≥ z(K_Y, Sanskrit) − 2 for any L in {Finnish, Basque, Proto-Dravidian}, or (b) z(K_fit-L, L) ≥ z(K_Y, Sanskrit) − 2 for Finnish or Basque.
4. **SUPPORT** (for "the key's output is Sanskrit-like in a language-specific way"; explicitly **not** a decipherment verdict) if PC1 and PC2 pass, p(K_Y, Sanskrit) ≥ 0.99, z(K_Y, Sanskrit) exceeds z(K_Y, L) by ≥ 2 for all three controls, and z(K_fit-Finnish, Finnish) and z(K_fit-Basque, Basque) both fall ≥ 2 below z(K_Y, Sanskrit).
5. **MIXED** otherwise.
Secondary analyses are reported but do not change the verdict.

## Diagnostics (reported, not verdict-bearing)
- M-304 trace: sign IDs, reading order, labels, P-V string, bits/char under each language.
- Ten texts chosen by a fixed rule (every 190th text of `FC.TRAIN` sorted order), same trace.
- Exploratory: z(K_Y, Sanskrit) restricted to texts whose signs are ≥ 50% Table-7 uniquely crosswalked IDs (18 IDs, round 46), to see whether the Brahmi-shape-anchored part of the key carries the signal. Low power expected; labelled exploratory.
- Exploratory: does refitting the Sanskrit key (K_fit-Sanskrit) beat K_Y under the author's own criterion?

## What this round cannot show
A SUPPORT verdict would mean the key's output has Sanskrit-specific phonotactics beyond its label inventory; it would not establish sound values, Brahmi descent or any translation (round 32's ceiling still applies). A NULL or ARTEFACT verdict refutes the specific claim that complete Sanskrit readability is evidence; it does not refute Indo-Aryan or any other language for the Indus script.

## Stopping and amendments
Fixed trial counts above; no additional shuffles or chains after seeing results. Any change before results goes in an Amendment section below with a reason. Runtime estimate: minutes, stdlib Python 3.9+.

## Amendment 1 (17 October 2026, before any scoring run)
**Change:** PC2's homophone target. Round 32's `build()` inflates to a fixed ~400 sign IDs, calibrated for a 919-word cipher. With the held-out half as cipher (1,674 tokens) that gives 366 IDs, i.e. 4.6 tokens per sign, three times sparser than the Indus corpus. PC2 now sets the target so that tokens per sign ID matches the kept Indus corpus (tokens ÷ sign types, computed from the data, expected ≈ 15 → ≈ 110 IDs). The round 32 fixed-400 geometry is still run and reported as **PC2b** but is not verdict-bearing.
**Reason:** the protocol's stated purpose for PC2 is "Indus density"; the inherited constant did not deliver it. Discovered from the unit check of the builder (`PC2 texts 227 ids 366 tokens 1674`), before any score was computed.
**Also noted:** collapsing Linear B syllable values to the shared alphabet merges 70 syllabograms into 63 values (a/a2, pu/pu2 …), so the "bijective" PC1 key is very slightly many-to-one. No change.
