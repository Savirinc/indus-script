# Bayesian evidence ledger

*Created 22 October 2026 from the reports of rounds 09–57. Nothing new was run to build it. Rules: `reports/LEDGER-RULES.md`. This is a living document: rows are added, never deleted; withdrawals are logged.*

**State in one line:** no pre-registered test so far moves any hypothesis by ×3 or more. The current probabilities are the priors, and the priors rest on the literature plus unregistered structural measurements. The leading hypothesis is not clearly ahead (see Fragility).

---

## a. Certain facts
Measured, reproducible, each with the test that established it. No interpretation.

| ID | Fact | Established by |
|---|---|---|
| C1 | Core corpus (core regions, known direction, no damaged sign, exact repeats merged): 1,936 text types, 8,726 sign tokens, 582 sign types; 15.0 tokens per sign, median 2; 340 types occur ≤ 3 times; lengths 2–13; 15% of texts are 2 signs long. | `round30/foreign_context.py` FC.TRAIN; round 47 corpus block |
| C2 | A bigram model trained on Harappa texts predicts unseen Mohenjo-daro texts 8.2% better than a unigram model (3.1% in the reverse direction; 7.8% and 11.2% on stamp seals), after removing exact and one-edit copies; it beats 200 of 200 position-preserving shuffles in all four conditions. | Round 27 (not pre-registered); round 29 exact-order test (pre-registered, MIXED: position model failed, bigram exploratory +2.3–3.2 bits) |
| C3 | Eight Gulf-type round seals (Ur, Bahrain, Luristan) sit at mean percentile 0.916 in bigram surprisal against length-matched Indus-valley seals (p < 5 × 10⁻⁵); 0.926–0.943 under every transcription scenario. Five square seals found abroad: 0.606 (not anomalous, n = 5). | Rounds 30–31 (pre-registered) |
| C4 | 3.5% of Indus texts contain a repeated sign. Recomposing texts from the same signs at the same lengths gives 17.3%. Shuffling order within texts leaves it at 3.5%. Merging the 17 stroke numerals into one sign raises it to 17.7%. Comparison corpora at Indus size and lengths: oracle bone 3.0%; all twelve others 13.4–34.0% (Greek 34.0, Hebrew 33.8, Egyptian 27.6, Uruk IV 24.0, proto-Elamite 22.4, Shijing 18.9, Uruk III 17.8, Old Assyrian 17.7, Cherokee 13.9, Ur III 13.9, seal legends 13.9, Old Babylonian 13.4). | Rounds 52, 52b (descriptive outputs of METHOD-FAIL rounds; measurement is valid, classification is not) |
| C5 | On eight relabelling-invariant features at matched size and lengths, the Indus vector is nearest the Shang oracle-bone corpus (0.44 between-corpus sd), next Uruk III 2.05, Ur III 2.11; distance to every small-inventory script 4.4–7.1. Nearest corpus unchanged under every leave-one-out. | Round 52b (descriptive) |
| C6 | Shuffling sign order within Indus texts raises H2/H1 from 0.494 to 0.662 and lowers DP-segment length from 1.42 to 1.07. | Rounds 52, 53b |
| C7 | At matched size and lengths, H2/H1 is 0.469–0.512 for the archaic accounting systems (Uruk IV, Uruk III, proto-Elamite) and 0.477–0.685 for phonetic scripts (Ur III 0.477, seal legends 0.508, Egyptian 0.562, OB letters 0.634, OA letters 0.685). The ranges overlap. | Round 52b |
| C8 | The trigram shuffle instrument recognises the true Linear B key at Indus density (Greek z 11.5; best wrong language 5.7), and down to ~57–60% token coverage; it does not reach the bar at 28–39% coverage. | Rounds 47, 49 |
| C9 | A homophonic solver given the correct language recovers 83% of Linear B at 20 tokens per sign and collapses (8–30%) at 14 tokens per sign or fewer, where wrong keys outscore the true key. | Round 32 (pre-registered INFEASIBLE) |
| C10 | Published keys under C8: Yajnadevam Sanskrit percentile 0.29 (z −0.35); Fairservis Tamil 0.61 (z 0.20); Rao Sanskrit 0.26 (z −0.70); Bhaty (Yajnadevam with 435/436 → o) Sanskrit 0.30 (z −0.35). Refits of each author's own value inventory reach z 3.2–10.5 in any language tested, Finnish and Basque included. | Rounds 47, 49, 57 |
| C11 | 24 Proto-Dravidian rebus anchors beat 60 shuffles at pooled p 0.066 over 10 splits; Finnish words in the same slots 0.016; Basque 0.72. | Rounds 43, 45 |
| C12 | Under the Bhaty key, Bronze Age place names (ePSD2 GN/SN + her 23 names) match Indus readings at percentile 0.41 of key shuffles; matches per name 2.8 against 6.9 for scrambled skeletons and 4.4 for Finnish towns; Linear B place names under the same procedure z 4.2. | Round 57 |
| C13 | In Gadd 1932, Hallo & Buchanan 1965, Collon 1996 and the full CDLI catalogue, no impression bearing Indus signs exists on an inscribed cuneiform tablet; three Gulf-seal impressions on tablets exist, all textless. | Round 50 (census; Mitchell 1986 and Laursen & Steinkeller 2017 unread) |
| C14 | The 11 proposed Meluhhan loanwords show no family attribution (Finnish first in 70% of resamples) while the same instrument attributes 11 Mitanni Indo-Aryan words to Indo-Aryan in 100%. | Round 51 |
| C15 | Kuiper's glossed Rigvedic foreign words score Proto-Dravidian above Munda in 100 of 100 size-equalised subsamples; below the attribution bar against controls in 6 of 100. | Rounds 39–40 |
| C16 | Instruments that failed their positive controls on real data: shape matching from fonts (48); writing-system classifiers (52, 52b); PMI and DP word segmentation (53, 53b); combinatorial freedom as a syllabic signature (54); rebus homophony (36); substrate classifiers without meaning (37, 38). | Those rounds |
| C17 | At Indus text lengths and token total, the share of texts with a repeated syllable is: Sanskrit (Ṛgveda, Rāmāyaṇa, words, 24,626 dictionary names) 6.1–8.1% mean, lowest of 2,400 samples 4.5%; Old Tamil (Puṟanāṉūṟu lines, words) 5.8–9.3%; Old Tamil names (Sangam poets and patrons) 7.5% in written syllables but **3.2% in spoken syllables**, below the Indus 3.51%. Random two-way homophony brings every condition to ≤ 3.5–5.0%. Yajnadevam's published readings repeat 20.4%, against at most 10.1% in any real Sanskrit sample. | Round 58 (pre-registered measurement) |
| C18 | The 17 Indus stroke signs share (left, right) frames with one another less often than frequency-matched random sign sets (percentile 0.08), whereas count signs 1–9 in proto-Elamite and proto-cuneiform score 1.00 at Indus size and lengths. Stroke-count frequencies 1–8: 248, 700, 281, 73, 44, 30, 49, 6 (two strokes commonest; PE and proto-cuneiform: one commonest). Stroke signs are text-medial 77% (all signs 56%), final 7% (22%). Of the 68 texts with a repeated sign, 20 repeat only a stroke sign. Indus repetition with stroke signs removed: 2.64%. | Round 55 (pre-registered measurement) |
| C19 | Read with the atlas mapping (expanded Yajnadevam key) and split into Sanskrit dictionary words (DCS, 134,131 headwords of ≥ 3 letters, sounds grouped as the mapping's author groups them), the 4,543 inscribed records have 69.0% of their letters inside dictionary words; 20 structure-preserving scrambled keys give 67.6% (sd 2.1%), 4 of 20 at or above. | Readings atlas, 24 Oct 2026 (descriptive, unregistered; not scored) |
| C20 | Under the atlas key, true sign order gives more Sanskrit dictionary coverage than 20 within-inscription permutations (88.97% vs 86.91%, gain 0.0207, z 7.8; 1,689 distinct fully assigned inscriptions of ≥ 3 signs). The gain exceeds all 20 pre-registered scrambled keys (max 0.0189); post hoc, 4 of 120 wrong keys reach it (atlas z 1.93 among wrong keys). Real Rāmāyaṇa windows give a gain of 0.049; order-free strings give none. The key was fitted by its author to these inscriptions, which predicts this result whether or not the key is right. | Round 60 (pre-registered measurement; not scored) |
| C21 | On Linear B with the correct Greek lexicon, a 600k-step homophonic solver recovers ≥ 50% of tokens (median of 5 layouts) down to 16.5 tokens/sign with word boundaries and down to 21.0 tokens/sign with 1–3 words per text and no dividers; a Finnish lexicon recovers 2.4%. Mapped onto the Indus corpus (8,726 tokens), that is ≤ 528 and ≤ 414 signs; the defensible merge (Bourdeau's groups without the numeral merges) gives 541. Optimistic for Indus: language supplied, milder long tail (2–4% of signs seen ≤ 2 times vs 52%), smaller corpus. | Round 63b (pre-registered measurement, controls passed; round 63 VOID on a mis-specified control) |
| C22 | When 42% of Linear B words are written as single word signs (16% of tokens, the Indus share outside its top 100 signs) and the rest with one sound sign per syllable, a 600k-step solver given the Greek lexicon recovers the sound signs at 29.1 uses per sound sign without word dividers (median 0.855, against 0.863 with no word signs) and fails at 17.4 (0.19); a Finnish lexicon recovers 0.02. The Indus top 100 signs average 73 uses, top 200 average 40. Kind assumptions: single-use word signs, no homophones at the recovered level, language supplied. | Round 64 (pre-registered measurement, controls passed) |
| C23 | Under round 48 descriptor B (modern fonts), the 440 atlas pairs of Indus sign and single Brahmi letter are no closer in shape than the same signs with the same letters permuted (mean 0.0824 vs 0.0829, p 0.33, 10,000 permutations); the same test detects Phoenician→Greek (p 0.0001) and Phoenician→Aramaic (0.0018) at 19–22 pairs and rejects Linear A and Old Hungarian. Letters m, y, b, p are closer than random; t and a further. | Round 61 (pre-registered measurement; Part B METHOD-FAIL) |
| C24 | In the round 64 logosyllabic Linear B cipher, a truth-free statistic (order gain over shuffles ÷ the LM's own order gain) ranks the plaintext's own Greek lexicon first against 9 wrong languages in 4 of 5 layouts (0.60 vs ≤ 0.39), but an independent Ancient Greek IDS list only 1 of 5 (0.29); with that list the solver recovers 0.12 of sound tokens against 0.86. By raw likelihood Hawaiian, Sanskrit and Maori beat the true lexicon. | Round 65 (pre-registered measurement, solver control passed) |

**Measurements pending scripting** (counted in conversation on 22 October 2026, not yet in a committed report; they become facts only when scripted and committed):
- P1. The comb sign (156 and variants 150–161) is followed by the three-stroke sign 003 in 43 inscriptions (31 of them the whole text), by one stroke (031) 16 times, by two strokes (032) and four strokes (004) occasionally; 003 follows at least eight different signs. Find sites: Harappa 28, Mohenjo-daro 13, Lothal 1, Kalibangan 1.
- P2. One object in the 5,679-record catalogue comes from Afghanistan (Sh-69, Shortughai, 426-003).

## b. Exclusions (by logic, with scope)
Only what follows deductively from a measured fact. Low probability alone never excludes.

| ID | Excluded | Logic | Scope |
|---|---|---|---|
| X1 | A one-sign-per-value phonetic system with at most ~100 values (alphabet, abjad, pure syllabary) without homophony | 582 sign types (≈ 460 after the most generous allograph merging, round 33) cannot be the values of a ≤ 100-value system unless the same value has on average ≥ 4 interchangeable signs | Holds unless the sign list is ≥ 4× over-split; a homophonic syllabary is not excluded |
| X2 | The Indus corpus as a sign-for-unit bijective substitution of running text drawn like any of the twelve phonetic, accounting or literary control corpora | A bijection preserves the within-text repetition rate exactly; the Indus rate is 3.5% (C4) against 13.4–34.0% for those corpora at the same lengths | For texts generated like those twelve corpora; not for name lists, not for homophonic systems that avoid repeats, not for oracle-bone-like records (3.0%) |
| X3 | Using any relabelling-invariant statistic (rounds 27–31, 52–54) as evidence for a specific sound value or language | Such statistics are unchanged by any bijection of sign labels, so they take the same value under every key | All structural rounds |
| X4 | The near-bilingual seal-impression route, in the sources read | Census found zero category-A cases (C13) | The four sources read; Mitchell 1986, Laursen & Steinkeller 2017 unread |
| X5 | Using H2/H1, H1 or Heaps slope to decide linguistic vs non-linguistic | The statistic takes overlapping values on known members of both classes (C7) | At Indus size and text lengths |
| X6 | A reading of the seals whose output is the attested lexicon and morphology of Classical or Epic Sanskrit, Puranic Sanskrit, or Old (Sangam) or later Tamil, taken as the language of the seal-makers | The mature Indus corpus dates c. 2600–1900 BCE; the earliest attested Sanskrit (Ṛgveda) is c. 1500–1200 BCE, Classical Sanskrit c. 500 BCE onward, the earliest Tamil writing c. 3rd century BCE (earliest claimed dates 5th century BCE). No attested language keeps its words and endings unchanged across 700–2,000 years (Old to Modern English took ~1,000). A correct reading of 2600–1900 BCE text therefore cannot return dictionary forms of a language attested 700–2,000 years later; a key that does return them has shown that the reader supplied the words | Rests on a law-like generalisation about language change, not pure deduction from a measured fact; this is stated, not hidden. Excludes the *output* of such readings (Yajnadevam, Bhaty, Classical-Tamil readings), not the families: an unattested ancestor of Indo-Aryan, Dravidian or any other family is untouched (section f). Added 22 Oct 2026; no test run |
| X7 | A bijective (no homophones) key that reads each Indus sign as one syllable. **Excluded under both readings of the stroke signs** (rounds 58 and 55): Ṛgveda and Rāmāyaṇa in written syllables; Puṟanāṉūṟu lines in written syllables; Old Tamil words in written and spoken syllables. **Excluded only if stroke signs are ordinary signs** (round 58, Indus 3.51%): additionally Rāmāyaṇa spoken; Sanskrit words spoken; Sanskrit names written and spoken; Old Tamil names written. | Such a key preserves the per-text repetition rate exactly; in each listed condition none of 300 Indus-shaped samples repeats as rarely as the Indus corpus and the gap is ≥ 5 sd. With stroke signs read as numerals and removed, the Indus rate is 2.64% (round 55). The corpus does not decide between the two readings (round 55 M1: stroke signs show no numeral-like substitution, percentile 0.08, where proto-Elamite and proto-cuneiform numerals score 1.00), so both lines stand unranked. | Open under the numeral reading: every names condition in both languages, Ṛgveda/Rāmāyaṇa/Puṟanāṉūṟu in spoken syllables, Sanskrit words. Open under both readings: Old Tamil names in spoken syllables (3.2% and 2.0%, at or below the seals). Not excluded: any key with homophones (two signs per syllable suffice); any language family. The earlier caveat "merged numerals (17.7%) undo it" is **deleted** (23 Oct 2026): merging corresponds to a key giving all stroke counts one sound, which no reading proposes (round 55 protocol). |

## c. Hypotheses
Exhaustive and mutually exclusive, about what the signs encode. Language family is a separate question (section f).

| | Hypothesis | Layers (Occam count) | What it must explain |
|---|---|---|---|
| **N** | **Non-linguistic symbol system.** Signs do not map to words of any particular language: emblems, clan or office marks, tallies, ritual or accounting symbols (Farmer, Sproat & Witzel 2004). | 1: symbols with conventional order | ordered, transferable sequences (C2); low repetition (C4) |
| **R** | **Restricted linguistic system.** Signs stand for words of a spoken language (names, titles, offices, commodities, numbers), possibly with rebus for names, but only for these functions; no general means of writing arbitrary utterances. | 2: symbols + mapping to words | the absence of any long text; profile of names (C1, C4) |
| **L** | **Full script.** Signs encode linguistic units productively (logosyllabic or similar) and could write arbitrary utterances; the surviving corpus is genre-limited by what was durable. | 3: symbols + words + productive phonetic component | why no text exceeds 17 signs anywhere, in any material, over 700 years |
| **O** | **Other.** Mixtures (e.g. linguistic seals with non-linguistic tablet tallies), pseudo-script or imitation, several systems in one corpus, or something not considered. | variable | – |

N and R are not the hypotheses this project was hoping for. They are kept at full weight by rule.

## d. Priors (starting point; sum to 1)

| | Prior | Agreed range | Why |
|---|---:|---|---|
| L | 0.40 | 0.25–0.55 | Majority scholarly view (Parpola, Mahadevan, Possehl, Wells). Inventory and statistics sit with large-inventory systems and nearest a full writing system used for short records (oracle bone, C5). Against: no long text in 700 years; C7 shows the statistics usually cited for L do not discriminate. |
| R | 0.30 | 0.15–0.45 | The corpus is entirely seals, sealings, tags and tablets of 2–13 signs; 892 distinct texts on 1,005 unicorn seals; low repetition fits lists of distinct name elements (C4); most deciphered seal traditions record names and titles. |
| N | 0.20 | 0.10–0.35 | Farmer, Sproat & Witzel's argument is not refuted; the statistics used against it are void (C7, X5); real emblem and accounting systems produce ordered sequences. Against: cross-city transfer of fine sequential structure (C2) and the foreign-order effect (C3) are more natural if sequences encode words, though not exclusive to that. |
| O | 0.10 | 0.05–0.20 | Mixed corpora are common (Uruk tablets mix numerals, commodities and names); the incised tablets and seals may not be one system; pseudo-script exists in the Gulf set (C3, round 31). |

Unregistered measurements (C2, C4, C5, C6) and the literature informed these numbers. By rule 5 they cannot also be used as Bayes factors.

## e. Update log
Pre-registered tests only, grouped into independent evidence clusters (same data or same underlying signal = one cluster). Scale: weak ×3, moderate ×10, strong ×30, decisive ×100. "Gate" = could any outcome have moved some hypothesis by ×3 or more.

| Cluster | Rounds (pre-registered) | Outcome | Gate | Factor | Reason |
|---|---|---|---|---|---|
| K1 Cross-city order | 29 (27 unregistered) | MIXED | no | none | Ordered, transferable sequences are expected under N, R and L alike; the test cannot separate them. |
| K2 Gulf seals foreign in order | 30, 31 (same 8 seals) | SUPPORT (pct 0.916) | no | none | Foreign names (R, L) and foreign use of emblems or pseudo-script (N, O) both predict deviation; round 31 itself found one pseudo-inscription. |
| K3 Decipherability benchmark | 32 | INFEASIBLE | no | none | About what statistics can recover, not about what the signs encode. |
| K4 Gulf names | 35 | NON-INFORMATIVE | – | none | Real and fake names matched equally. |
| K5 Rebus and substrate classifiers | 36, 37, 38 | control failed | – | VOID | Rule 6. |
| K6 Anchor-rebus | 41–45 (same design, overlapping data) | ARTEFACT | no | none | A real anchor signal would bear on family; an artefact bears on nothing. |
| K7 Published phonetic keys | 47, 49, 57 (same instrument, same corpus) | NULL for all testable keys | no | none | Under N, P(all keys null) = 1. Under L or R, P(all published keys null) ≈ 0.9 or more, since few of a handful of published keys would be right even if the script were phonetic. Ratio ≈ 1.1, under ×3. |
| K8 Shape | 48 | METHOD-FAIL | – | VOID | Rule 6. |
| K8 (cont.) Shape of atlas pairs | 61 | Part A NOT CLOSER THAN RANDOM (controls passed); Part B METHOD-FAIL | no (measurement, declared in advance) | none | Shape continuity would not identify a language; fonts, not tracings. Adds C23. |
| K9 Near-bilingual census | 50 | INCOMPLETE | no | none | Absence of bilingual seal impressions is expected under every hypothesis. |
| K10 Writing-system signature | 52, 52b (same corpora) | METHOD-FAIL | – | VOID | Rule 6. Descriptive outputs are facts C4, C5, C7. |
| K11 Segmentation | 53, 53b (same gold corpora) | METHOD-FAIL (53b by 0.001) | – | VOID | Rule 6. 53b also falls under rule 7 (knife edge); void either way, no replicate needed. |
| K12 Combinatorial freedom | 54 | METHOD-FAIL | – | VOID | Rule 6. |
| K13 Sanskrit/Tamil syllable repetition | 58 | PARTIAL: 10 of 14 conditions excluded | no (measurement, declared in advance) | none | Excluding bijective Sanskrit/Tamil syllabic keys leaves L, R and N where they were: such keys are a small subclass of L and R. Adds X7 and C17 only. |
| K14 Stroke signs | 55 | M1 no class behaviour (controls passed); M2 5 of 14 conditions excluded under the numeral reading | no (measurement, declared in advance) | none | Numerals are expected under N, R and L alike. Rewrites X7 scope; adds C18. |
| K7 (cont.) Sign order under the atlas key | 60 (same key and corpus as 47, 57, 59) | ORDER SIGNAL, narrow (0 of 20 pre-registered wrong keys, 4 of 120 post hoc) | no (measurement, declared in advance) | none | A key fitted by its author to these inscriptions predicts an order gain under L, R or N alike. A machine-fitted held-out comparison is needed before any factor. Adds C20. |
| K7 (cont.) Traded-goods words under the Brahmi key | 59 (same key and instrument as 47, 57) | VOID: Linear B trade-word control z 2.11, pct 0.968 | yes (SUPPORT would have given ×3) | none | Rule 6. Descriptively, trade words in Sanskrit and Proto-Dravidian matched less often than scrambled strings and ordinary words; the same 65 texts read "gem" in Sanskrit and "monkey" in Proto-Dravidian. |
| K3 (cont.) Decipherability threshold with replicates | 63 (Linear B, same harness as 32) | VOID: positive control at 150k steps 0.271 (bar 0.70) | no (measurement, declared in advance) | none | Rule 6. Descriptively, thresholds ≈ 17.3 tokens/sign with word boundaries and ≈ 21.0 without; Indus merged (16.1) below both. About recoverability, not encoding; adds no fact while void. |
| K3 (cont.) Decipherability threshold, replication | 63b (fresh seeds) | OUT OF REACH, at the threshold (R1); controls passed | no (measurement, declared in advance) | none | About what can be recovered, not about what the signs encode. Adds C21. |
| K3 (cont.) Logosyllabic sound-sign recovery | 64 (Linear B, same harness) | SOUND PART RECOVERABLE (u* 29.1); controls passed | no (measurement, declared in advance) | none | Recoverability under an assumed script type; says nothing about which type Indus is. Adds C22. |
| K3 (cont.) Truth-free language discrimination | 65 (Linear B, same harness) | ONLY WITH THE TEXT'S OWN WORDS; solver control passed | no (measurement, declared in advance) | none | A right-language word list that is not the texts' vocabulary neither decodes nor stands out; Indus candidate lexicons are of that kind. Adds C24. |

Family-axis rounds (39–40, 51) are logged in section f, not here.

**Current probabilities = priors:** L 0.40, R 0.30, N 0.20, O 0.10.

## Fragility
- **Priors at the edges of their ranges:** L 0.25 with R 0.45 puts R ahead; N 0.35 with L 0.25 puts N ahead of L. The ranking flips inside the agreed ranges. **Neither L nor R is clearly ahead; N is behind but not excluded.**
- **Drop the most influential test:** no test moved anything, so nothing changes. That is the point of the exercise: after 58 rounds, the probability of what the signs encode rests entirely on priors.

## Honest summary
- The best surviving explanation is L at 0.40, by prior only. None of its lead comes from a scored positive match, and none from removing an objection by a scored test.
- What the scored tests have done is close routes and keys: every testable published key is NULL (K7), the anchor method is an artefact (K6), the bilingual route is empty in the sources read (K9), and five structural instruments are void. Those are failures recorded as results.
- A probability for L says nothing about which language or what any sign says.
- Occam, layers counted: N has 1 layer, R 2, L 3. No measured fact has yet forced the second layer by a scored test. The simplest hypothesis consistent with the scored record is N; the priors favour L and R on unscored structure and on what seal traditions usually are.

## f. Separate axis: language family (conditional on R or L)
Not scored yet; recorded so that family evidence is never counted toward L/R/N/O.

| Round | Outcome | Bears on |
|---|---|---|
| 39–40 | Rigvedic substrate leans Proto-Dravidian over Munda (100/100), below the bar against controls | Substrate language of the Punjab, not the script |
| 51 | Meluhhan candidates: no family attributable; gates passed | Family of Meluhhan speakers |
| 41–45, 47, 49, 57 | All family-specific keys and anchors NULL or ARTEFACT | Whether any family has been demonstrated in the script (no) |
| 58, 55 | Bijective syllabic keys excluded in 10 of 14 Sanskrit/Old Tamil conditions with strokes as signs, 5 of 14 with strokes removed (X7); Old Tamil names in spoken syllables repeat as rarely as the seals (3.2%) | Which *keys* are possible, not which family: both languages keep open conditions, and X6 removes only the attested forms |
