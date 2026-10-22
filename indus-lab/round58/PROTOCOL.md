# Round 58: Can any one-syllable-per-sign Sanskrit or Tamil key be right? (pre-registered measurement)

Written 22 October 2026. No script for this round exists yet, and no repetition rate has been computed on any Sanskrit or Tamil text. Disclosed in advance:
- the source formats were inspected (one Ṛgveda hymn file from DCS, the DCS dictionary header and gloss field, the first page of Puṟanāṉūṟu on Tamil Wikisource);
- the Indus value is already known (3.51%, fact C4, round 52), as are the values for the twelve earlier control corpora (13.4–34.0%).

## Ledger status (rule 4)
**This is a measurement, not a scored test.** None of its outcomes moves L, R, N or O. A key that writes Sanskrit or Tamil one syllable per sign belongs to L or R, but so do keys in every other language and every logosyllabic reading. Excluding this one class therefore leaves the L/R/N balance where it is. The possible outputs are a new exclusion, X7, with a stated scope (ledger section b), and new facts. No Bayes factor is attached.

## Question
Under a key that gives each Indus sign one syllable value and gives no two signs the same value (a bijection, i.e. no homophony), a seal text has a repeated sign exactly when its reading has a repeated syllable. The within-text repetition rate is therefore the same on both sides of any such key, whatever the values are.

In the Indus corpus, 3.51% of texts of two or more signs contain a repeated sign. The question: **does real Sanskrit or real Tamil, cut into pieces of exactly the Indus lengths, ever repeat syllables as rarely as that?** If it never does, under every way of cutting and syllabifying it below, then no bijective one-syllable-per-sign reading in that language can be correct. Black-swan logic applies: one measurement settles the whole class, without testing any key.

The yardstick is the same as in fact C4 and exclusion X2. This round extends X2 to the two languages that most published keys use. It also adds the conditions X2 left open: single words and lists of names.

## Data (sources pinned by sha256 in `SHA256SUMS` before the run)
| Code | Language stage | Text | Unit ("one text" to cut from) | Source, licence |
|---|---|---|---|---|
| RV | Vedic Sanskrit, c. 1500–1200 BCE | Ṛgveda, all DCS files | DCS sentence; word forms joined without spaces | Digital Corpus of Sanskrit, CoNLL-U (OliverHellwig/sanskrit on GitHub), CC BY 4.0 |
| RAM | Epic Sanskrit | Rāmāyaṇa, all DCS files | DCS sentence, joined as RV | as RV |
| SKW | Sanskrit words | RV + RAM word tokens; compound members (Case=Cpd) re-joined to the next token | one word | as RV |
| SKN | Sanskrit names | DCS dictionary lemmas whose first sense (text before the first ';') begins "name of" (any case), excluding first senses containing any of: work, metre, meter, plant, Sāman, hymn, chapter, section, treatise, commentary, verse, letter, particular, text | one name (lemma stem) | DCS `lookup/dictionary.csv`, CC BY 4.0 |
| PUR | Old Tamil (Sangam), c. 1st cent. BCE – 3rd cent. CE | Puṟanāṉūṟu, all poems on Tamil Wikisource | one poem line (between `<br />`); words joined without spaces | ta.wikisource.org, public-domain text, page CC BY-SA |
| TMW | Old Tamil words | PUR word tokens (whitespace-split) | one word | as PUR |
| TMN | Old Tamil names | Puṟanāṉūṟu poet and patron lines (`பாடியவர்:`, `பாடப்பட்டோன்:`, `பாடப்பட்டோர்:`, `பாடப்பெற்றோர்:`), split on commas, parentheses removed, de-duplicated | one full name, multi-word names and titles joined (e.g. "சேரமான் பெருஞ்சோற்று உதியன் சேரலாதன்" is one unit) | as PUR |

The DCS forms are sandhi-split. Written Sanskrit joins words by sandhi, which changes some word-boundary syllables. This is a limitation, but a small one for a repetition count. Text cleaning: keep IAST letters (Sanskrit) or the Tamil block U+0B80–0BFF (Tamil); drop digits, punctuation, wiki markup and editorial brackets.

Only the derived unit files (`controls/*.txt`, one unit per line, syllables space-separated) and SHA256SUMS are committed. Raw downloads stay outside the repo. Copyright: all sources are openly licensed (CC BY 4.0, CC BY-SA, or public domain), as in round 52.

## Two syllabifications (both declared now; rule 8: two variants, no others)
- **S1, orthographic syllable (akṣara, Brahmi-style).** A consonant cluster goes with the following vowel. Anusvāra ṃ and visarga ḥ attach to the preceding syllable. A word-final consonant (Sanskrit virāma, Tamil puḷḷi) is its own unit. Tamil: each written grapheme (uyirmey, vowel, or puḷḷi consonant) is a unit; ஃ is a consonant. This is how Brahmi-derived scripts write, and it is what Yajnadevam-type keys assume.
- **S2, phonological syllable.** Between vowels, the first consonant of a cluster closes the previous syllable and the rest open the next. Word-initial clusters are onsets; word-final consonants, ṃ and ḥ are codas. This gives fewer, larger units: the most generous case for a key, since a larger inventory means fewer repeats.

Sanskrit segments (IAST): vowels a ā i ī u ū ṛ ṝ ḷ e ai o au (ai and au are read greedily as diphthongs). Aspirates kh gh ch jh ṭh ḍh th dh ph bh are single consonants. Vowel length is kept distinct in both languages (more distinct units, so fewer repeats, which again favours the key).

**Syllabifier check (must be 40/40 before any rate is computed; a mismatch is fixed by an Amendment, then the full check is re-run).** Format: word, S1, S2.

Sanskrit: agnim a·gni·m ag·nim; yajñasya ya·jña·sya yaj·ñas·ya; purohitam pu·ro·hi·ta·m pu·ro·hi·tam; indraḥ i·ndraḥ in·draḥ; kṛṣṇa kṛ·ṣṇa kṛṣ·ṇa; rāmāyaṇam rā·mā·ya·ṇa·m rā·mā·ya·ṇam; saṃskṛtam saṃ·skṛ·ta·m saṃs·kṛ·tam; aśvaḥ a·śvaḥ aś·vaḥ; devam de·va·m de·vam; vāk vā·k vāk; hotāram ho·tā·ra·m ho·tā·ram; ṛtvijam ṛ·tvi·ja·m ṛt·vi·jam; bhaktiḥ bha·ktiḥ bhak·tiḥ; vaiśvānaraḥ vai·śvā·na·raḥ vaiś·vā·na·raḥ; auṣadhī au·ṣa·dhī au·ṣa·dhī; sūktam sū·kta·m sūk·tam; jyotiḥ jyo·tiḥ jyo·tiḥ; mitrāvaruṇā mi·trā·va·ru·ṇā mit·rā·va·ru·ṇā; gāyatrī gā·ya·trī gā·yat·rī; brahman bra·hma·n brah·man.

Tamil (shown in transliteration; the check runs on Tamil script): aṟam a·ṟa·m a·ṟam; poruḷ po·ru·ḷ po·ruḷ; iṉpam i·ṉ·pa·m iṉ·pam; tamiḻ ta·mi·ḻ ta·miḻ; kaṇṇi ka·ṇ·ṇi kaṇ·ṇi; koṉṟai ko·ṉ·ṟai koṉ·ṟai; vēntaṉ vē·n·ta·ṉ vēn·taṉ; pāṭal pā·ṭa·l pā·ṭal; cēramāṉ cē·ra·mā·ṉ cē·ra·māṉ; auvaiyār au·vai·yā·r au·vai·yār; nilam ni·la·m ni·lam; vicumpu vi·cu·m·pu vi·cum·pu; tī tī tī; nīrum nī·ru·m nī·rum; aimperum ai·m·pe·ru·m aim·pe·rum; ñāyiṟu ñā·yi·ṟu ñā·yi·ṟu; peruñcōṟṟu pe·ru·ñ·cō·ṟ·ṟu pe·ruñ·cōṟ·ṟu; utiyaṉ u·ti·ya·ṉ u·ti·yaṉ; pāal (பாஅல்) pā·a·l pā·al; muṭinākarāyar mu·ṭi·nā·ka·rā·ya·r mu·ṭi·nā·ka·rā·yar.

## Procedure
Conditions: 7 sources × 2 syllabifications = **14 conditions, all reported.**

The Indus side is `FC.TRAIN` from `round30/foreign_context.py`, exactly as in rounds 52 and 52b: 8,726 tokens, repetition rate 0.0351 on texts of two or more signs.

An Indus-shaped sample is built with round 52's `indus_sample` rule, unchanged. Lengths are drawn from the Indus length multiset until the token total equals the Indus total. Each length ℓ is cut as a random window from a random unit with at least ℓ syllables, and a window never crosses a unit boundary.

One addition, for the short-unit sources (SKW, SKN, TMW, TMN) only: if no unit has ℓ or more syllables, the window is cut from a concatenation instead. For words, that is consecutive words of the same sentence or line. For names, it is randomly drawn further names (a "name + name" text, like a seal reading name and title). The share of windows that needed this is reported for each condition.

Statistic: `repeat` from round 52's `features()`, unchanged. It is the share of texts of length ≥ 2 that contain any unit twice.

B = 300 samples per condition, seed 58001 + condition index × 1000 + sample index (condition order as in the table, S1 before S2).

## Controls (rule 6)
1. **Pipeline check:** the script recomputes the Indus rate and must get 0.0351 (to 4 decimals). Run round 52's sampler on round 52b's SEAL control with its seed, and the first sample must reproduce the stored `repeat` value exactly.
2. **Sampler check (impossible-difference control):** feed the Indus texts themselves through the same sampler as if they were a control corpus. The mean over 300 samples must lie within 0.01 of 0.0351. Otherwise the sampler adds repeats by itself, and the round is VOID.
3. Syllabifier check 40/40, as above.

## Decision rule per condition (fixed now)
Let I = 0.0351. For each condition, over its 300 samples, compute mean m, sd s, and the count k of samples with repeat ≤ I.
- **EXCLUDED:** k = 0 and (m − I)/s ≥ 5.
- **NOT EXCLUDED:** k ≥ 3 (at least 1% of samples are as low as the Indus corpus).
- **BORDERLINE** (anything else): replicate with 10 fresh blocks of 300 samples (seeds 59001 + condition × 1000 + block × 300 + sample). Final verdict EXCLUDED only if ≥ 8 of 10 blocks meet the EXCLUDED rule, otherwise NOT EXCLUDED (rule 7).

## What gets written to the ledger
- **X7** lists exactly the EXCLUDED conditions, worded as: "a bijective (no-homophony) key reading Indus signs as [S1/S2] syllables of [source]". Conditions that are not excluded are listed as open.
- **Headline wording, fixed now:**
  - If all 14 are EXCLUDED: "No bijective one-syllable-per-sign key in Vedic or Epic Sanskrit or Old Tamil can be correct, whether the seals hold running text, single words or names."
  - If only some are EXCLUDED: name them; nothing broader is claimed.
  - If none are EXCLUDED: "Sanskrit and Tamil at seal lengths can repeat as rarely as the Indus corpus; X2's repetition argument does not reach these languages." That is a failure of the idea, reported with that word.
- **Scope stated with X7 in every case:**
  - (a) Homophonic keys are not excluded. Yajnadevam's key does assign several signs to one value. Whether his particular key passes is a separate, direct check (descriptive item 2 below), not part of X7.
  - (b) It applies to the ICIT sign list as used by all published keys. If the 17 stroke numerals are one sign, the Indus rate is 17.7% (fact C4), and the comparison is reported against that value too.
  - (c) It says nothing about Dravidian, Indo-Aryan or any family (ledger section f).

## Descriptive items (no verdict, reported)
1. **Random homophony.** For each condition, the mean repeat rate after each syllable token is written at random with one of k interchangeable signs, k ∈ {2, 3, 4, 6, 8, 12}. Also reported: the k needed to reach 0.0351, and the implied sign inventory (k × syllable types in the samples), set against the 582 Indus sign types. This is one model of homophony among many. A scribe who deliberately avoids repeating a sign needs only k = 2, and that is stated.
2. **Yajnadevam's key, as published.** The repetition rate of his readings is measured directly in reading space, using the round-47 `read_v` rendering split into S1 units. It is set against the 14 condition distributions. Descriptive only; this round scores nothing.
3. All 14 conditions also compared against the numerals-merged Indus value of 0.177.

## Files
`PROTOCOL.md` (this file; `chmod 444` and sha256 in the commit message once the owner has read it), `fetch58.py` and `extract58.py` (download and build `controls/`; committed with SHA256SUMS before the run), `run58.py` (`chmod 444`, sha256 in its commit message, committed before it is run), then `results.json`, `run58.log`, `REPORT.md`. Afterwards: a docs/STATUS.md row and the LEDGER (X7, facts, fragility check).

## Amendment 1 (22 October 2026, before `run58.py` was run and before any repetition rate was computed)
Reason: the extraction did not match the source. No rule in this protocol changes.
1. **Two page formats.** Tamil Wikisource carries Puṟanāṉūṟu in two wikitext formats. Some pages put a poem on one `#` line broken by `<br />`. Others put it in a `<poem>` block with one line per text line. The first build read only the first format: 136 lines and 130 names, from 21 of 48 pages. Both formats are now read.
2. **Metadata excluded.** A line holding a metadata label is never a poem line. The labels are the poet and patron labels above, திணை (*tiṇai*) and துறை (*tuṟai*). Poet and patron lines still feed TMN.
3. **Duplicate pages excluded.** The template pages `புறநானூறு/1`, `/2` and `/3` repeat poems 1–3, so they are left out. The page `புறநானூறு/பாடல்371-380` is a redirect and contributes nothing.
4. **Download pacing.** `fetch58.py` now waits 1.5 s between Wikisource requests and backs off on HTTP 429, after the server rate-limited the first download.

What was seen before this amendment: the unit counts and twelve example names from each name list, printed by the builder. No repetition statistic of any kind.

Final unit counts: RV 21,253 sentences; RAM 38,004; SKW 59,257 sentences (words grouped); SKN 24,626 names; PUR 4,729 lines; TMW 4,729 lines (words grouped); TMN 262 names. Spelling variants of one person are kept as separate entries, since the rule de-duplicates exact strings only. Some patron entries are descriptive phrases rather than bare names. Both are noted as limitations and not cleaned by hand. Characters dropped by the syllabifiers: 0. Syllabifier check: 40/40.
