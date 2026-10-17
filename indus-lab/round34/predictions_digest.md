# PREDICTIONS.md digest (indus target, commit 843165c)

Scripts used: `parse.py`, `join.py`, `stats.py` and `cat.py` in this folder. Per-hypothesis verdicts were taken from the bold `**ID holds.**` / `**ID fails.**` lines in `results/predict_test*.md` and joined to the hypothesis wording in the ledger. That resolved 3,034 of 3,064 hypotheses; the other 30 sit in sets with odd file references.

## 1. Ledger structure and recount

- **How a prediction is recorded.** Each block starts with a `# Nth set, registered before testing (date): topic (k hypotheses)` header. Next come the conventions (samples A = the ICIT-derived corpus, B = the M77 additions, F = the fuller ICIT corpus; permutation counts; usually p < 0.05). Then each hypothesis is a bold ID (`**WA1**`, `**SP3**`…) with a one-line criterion.
- **How the outcome is recorded.** A `## Results of the Nth set (added after the test; predict_testN.py, results/predict_testN.md)` section follows. It gives a prose verdict and ends with a running total: "Tally, counting parts: H held, F failed (N registered)". The result files hold a machine-readable verdict line for each hypothesis.
- **Size.** 336 headers cover 350 numbered sets, because sets 147–170 were registered in groups. There are 3,064 bold hypothesis IDs.
- **Dates.** Every set is dated 23–25 September 2026, so about 3,000 hypotheses were written and tested in three days. That means an automated agent loop. The ledger refers to an "owner" who reviews and sets goals.

**Do the numbers match 2,364 / 1,224 / 1,140?** Yes, but only as an old snapshot. That exact total appears once, at line 7,625, at the end of set 175 ("1224 held, 1140 failed (2364 registered)"). The ledger then runs on through set 350:

| Source | Held | Failed | Registered |
|---|---|---|---|
| Site claim (= ledger tally after set 175) | 1,224 | 1,140 | 2,364 |
| Result-file verdicts, sets 1–175 | 1,214 | 1,135 | 2,349 |
| Latest ledger tally (set 349) | 1,581 | 1,492 | 3,073 |
| Result-file verdict lines, all sets | 1,571 | 1,487 | 3,058 |
| Set 350 (registered, not yet tested) | – | – | +3 |

The small gaps (about 10–15) come from "counting parts", where sub-parts of a hypothesis are counted separately, plus a few untestable items such as P2 in set 1. The "other" outcomes:

- **Untested or not testable:** a handful.
- **Progress rules:** 166 hypotheses are the loop's own "Progress rule" items (e.g. "DF3: DF1 and DF2 hold"). They are logical combinations of other hypotheses in the same set, yet they are counted as predictions in the tally (68 held, 92 failed).
- **Fail by design:** some validation sets mark their rule as failing on purpose (e.g. TW3, "recorded as failing").

Overall hold rate: **51%**. It is 52% before the decipherment loops (sets 1–175) and 50% in the loops (176–350).

## 2. Topics

Each hypothesis was given one topic from keywords in its own text, checked in the priority order shown; if nothing matched, the set's title was used. The numbers are approximate, and topics overlap: "count" is common, so the numerals bucket is inflated.

| Topic | n | Held | Failed | Hold % |
|---|---|---|---|---|
| Numerals / strokes / counts | 632 | 320 | 305 | 51 |
| Name structure / heads / grammar / sign order | 565 | 285 | 275 | 51 |
| Endings, affixes, morphology (740, 520, closers, 400/90/151) | 515 | 239 | 273 | 47 |
| Language-model benchmark (S bits/sign, SIGN, WORD, smoothing) | 438 | 227 | 200 | 53 |
| Sign meaning: pictures, referent units, depiction, "picture vault" | 234 | 111 | 121 | 48 |
| Chronology / region / site / physical object | 179 | 106 | 73 | 59 |
| Other structural | 158 | 90 | 68 | 57 |
| Copper tablets | 121 | 63 | 58 | 52 |
| Published readings and keys (Parpola, Mahadevan, Fairservis, Kak, Yajnadevam, Farmer–Sproat–Witzel) | 103 | 45 | 57 | 44 |
| Language comparison (Dravidian/Tamil, Prakrit/Sanskrit, Sumerian, typology) | 67 | 40 | 27 | 60 |
| West Asian / Gulf / Ur III | 40 | 23 | 17 | 57 |
| Damaged-text restoration | 12 | 7 | 4 | 64 |

Most of the work is structural or distributional; about 85% is about structure, models and statistics. Sets 176–350 are "decipherment loops". From about loop 58 onward they are dominated by tuning one method, which ties text units to the picture on pictured tablets (the "referent units").

## 3. Statistical discipline

**What is good:**
- **Fixed criteria.** Thresholds and tests are written with each hypothesis, and the results section says when the run deviated ("Deviation, fixed before recording…").
- **Post-test notes are labelled.** About 378 passages say "after the test", "noted after" or "unregistered". Leads found after a test are re-registered before they count.
- **Replication on held-out data.** The structural sets that re-ran findings on held-out data (46, 56, 66, 73, 86, 101, 107, 110, 113, 116) held **139 of 170 (82%)**. That is real evidence that the core grammar is not noise.
- **Known-answer controls.** Linear B / DAMOS is used repeatedly as a control. A method must recover Greek before it is allowed to judge Indus keys. Control hypotheses held 74% of the time.
- **Admitting artefacts.** The ledger records its own mistakes, e.g. LS7 "holds but is a multiple-comparison artefact", the mould-copy inflation in set 336, and the wrong field in set 135.

**What is weak:**
1. **No correction across hypotheses.** There is no Bonferroni or Holm correction anywhere, and nothing across sets. FDR (about 140 mentions) is used only *inside* the referent-unit method, to control false units for one setting at a time. About 3,000 tests at α = 0.05 would give about 150 "holds" even if every null were true.
2. **The 51% hold rate says nothing about decipherment.** If every one-sided p < 0.05 test had a true null, about 5% would hold. Here roughly half do, because many hypotheses ask whether real text beats within-line shuffles. Any structured corpus passes that test. Many hypotheses are also written right after exploring the same data ("Lead from the seventy-first set (post-test, unregistered)"). So the hold rate mainly measures how well the agent guesses direction and threshold. Generic examples that hold for any natural-language corpus:
   - PR8 ("20%+ of sign types occur once")
   - PR9 (mean line length under 5)
   - PR12 (conditional entropy under 80% of unigram entropy)
   - PR13 (Zipf slope between −1.3 and −0.7)
3. **Null predictions win by low power.** Some hypotheses say "two-sided p ≥ 0.05 counts as holding" (e.g. PA9, PR5, TM6, WA8). With n = 18 (the West Asian lines) these hold by default. Margins can also be razor-thin: WA6 held at 6.52 bits against a 6.5 threshold.
4. **Many configurations tried.** The referent-unit loops (about sets 287–350) try roughly 60 configurations: unit types, alphas from 0.01 down to 0.002, stratifications, pools. Each is a fresh "hypothesis", and the headline coverage moves 0.79% → 23.8% → (a mould-copy flaw found) → 1.09% → 4.57%. Split-half checks (TW1, p = 0.005) help, but the search over configurations is never corrected for. The held-out precision is only 5%, about twice chance.
5. **Benchmark rescued after failing.** The language-type bench failed (set 195, 1 of 5). It was then "repaired" with a "tolerant profile", and all eight held (set 196, LT1–LT3). That is a classic forking path, even though it was labelled.
6. **Double counting and tiny thresholds.** The 166 progress-rule items double-count. Many benchmark hypotheses are improvements of 0.003–0.01 bits, with the setting tuned on the training split. These are engineering checks, not predictions.
7. **Pre-registration cannot be checked here.** The clone is shallow: a single commit, 843165c, dated 2026-10-10, adds every file. The ledger's claim that each set was committed before its script was written cannot be checked from this checkout. The full upstream history would be needed.

**Strong example:** sets 179 and 205–206. First, the method is shown to "see sound" on Linear B (SP1, p = 0.001). The same method then rejects the published keys (SP2–SP6). After that, a character-model scorer passes a gate that is specific to the language (GA1/GA2: Ventris's values beat all 100 shuffles in Greek but not in Sanskrit). These are falsifiable, controlled tests with power, and they could have come out the other way.

**Weak example:** PR8/PR13 (properties of any text), WA6 (a 0.02-bit margin), LT1–LT3 (passed after the criteria were loosened) and DF1/DF3 (one rung of a tuning ladder).

## 4. Specific topics

**Sign values and sounds** (about 23 hypotheses that mention sound or substitution, 10 held and 13 failed, plus the key tests):
- **The headline negative.** No sound value has passed. PROGRESS.md gives P = 0 and the held-out "U vault" = 0. Tier-1 "meaning" is 0.008%, which is 4 copper-tablet signs.
- **Rare names spelled by sound.** N4 held, but it was withdrawn after the P25 control: Linear B shows the same rare-word effect, so it is just a frequency effect. K12, N5, N8 and SL1–SL2 (a "sound-sign shortlist") failed.
- **Strokes used for sound abroad.** AD9 held: in West Asian lines, strokes stand before signs that are never counted at home, read as "strokes used for sound". WA7 held in reverse: 14 of 18 West Asian lines contain numerals, against 56% at home. These are weak support for rebus values of strokes, on n = 18.
- **Substitutions are not semantic.** SE4 and SE8 failed. SE1 held (same-category substitutions above chance).
- **Language-level comparisons.** Indus name statistics are not closer to Old Tamil than to Sanskrit: LN6, LN7, LT2 and LT3 failed. In set 175 (TB), name structure sits closer to early Prakrit donor names than to Tamil-Brahmi names (TB2, TB3 and TB5 held; TB1 and TB7 failed). Only the dominant single ending looks Tamil-like (TB6), and the ledger says the source formats make that comparison unfair.

**Sign 091 ("twins"):** no prediction targets it. The ledger uses ICIT numbering. ICIT 91 is not in `icit_m77_map.tsv`. ICIT 91 does open 3 of the 18 West Asian lines ('91 840 413 831', '91 32 1 33', '91 31 455 220'), but no hypothesis tests that. "Context twins" in set 100 (AL1–AL20) means pairs of signs that occur in near-identical contexts, not a sign. Those twins are not split by city or period (AL1, AL4 and AL5 failed); likely variant pairs are 435/436, 526/527 and 705/706. The sign the user means needs its catalogue mapped before it can be checked.

**West Asian, Gulf and Dilmun texts** (40 hypotheses, 23 held / 17 failed). Set 136, on 18 lines:
- **Held:** foreign lines rarely end in the ending slot (WA1: 17% against 57%); their opening signs never open home names (WA3: 39%); fewer end in home heads (WA4: 67% against 95%); fewer contain home name units (WA5); they are harder to predict (WA6).
- **Failed:** WA2, WA7 and WA10.
- **Earlier and related:** foreign tokens are "freer" (Y2 and RF2 held); cylinder seals leave out the endings (U24 held).
- **Ur III seal legends** as a control with a known reading (set 150): mixed, 3 of 7 held.
- **Dilmun:** not mentioned.

**Meluhha names:** **no registered prediction.** The work is exploratory only:
- `meluhha.py` and `results/meluhha.md` compare the Meluhhan names Nanaza and Samar with the Indus name slot (a doubled opening sign in only 2.2% of slots).
- `meluhha_oracc.py` collects 161 ORACC attestations.
- NOTES.md concludes that matching them "needs sound values nobody has".

**Sequences starting 415-803-001 (ICIT "415 803 1"):**
- O3 failed: 415 does not behave as 400 + 1.
- V3 held: 400/415 alternate in the same names.
- NA14 failed: fish heads after 415 do not take 520 more often.
- "415 803 1" occurs in two West Asian lines ('415 803 1 717 354', '415 803 1 328 4 2'). It is cited as evidence of stroke use abroad but not tested itself.
- In set 291 (SN1), the seal units "415 803", "415 803 1" and "803 1" tied to the gaur (bison) did **not** survive (FDR 43%; SN1 and SN2 failed).

**Copper-tablet equations** (121 copper hypotheses, 63 held / 58 failed):
- **CT5 failed with a count of zero.** The "firm" equations (341 rhinoceros, 749/778 goat, 753 hare) never occur in the text of copper labels that carry their own picture. They come from Parpola's drawings, where the sign is on the reverse. They were withdrawn as text anchors (CT6 and CT15 failed as well).
- **PL3 failed** as registered. The post-test explanation: in 8 of Parpola's 10 linked copper groups, a reverse-side picture is swapped for a single sign over the same front-side inscription. These are "reverse-side substitutions", not readings.
- **The moulded-tablet anchors held** (CT9: 31 cases, p = 0.0001).
- Sets 94–97 (copper tablets and their pictures; how copper labels are built; the name findings with copper tablets removed) went 13/7, 8/12 and 18/2.

## 5. Most informative outcomes

**HELD** (each narrows what a reading may claim):
1. **Q1/Q2 (set 2):** the class ending (740/520) is set by a name's *last* sign, and an inner fish does not set it. This replicated on held-out data and argues for head-final compounds, against head-initial Sumerian or Elamite.
2. **P6 (set 16):** numerals before 520 are almost all the long "3" (sign 33). So 33-520 is a fixed expression, not free counting.
3. **P11/P12 (set 16):** tablets vary at the numerals (29%), seal names at the words (13%). Tablets behave like records of counts.
4. **Held-out replication sets 107, 110, 113 and 116 (74 of 80 held):** the grammar of formulas, closers and genres is robust.
5. **LT4–LT7 (set 196):** fish-headed names take 520 at Mohenjo-daro, at Harappa, at the other sites, and in early and late Harappa alike.
6. **MF1–MF3 and MF7 (set 185):** marks added to the fish change its grammatical job. The roof-hat fish 235 stands before another fish 40% of the time against 15% for the plain fish, i.e. it is attributive. This is morphology inside the sign.
7. **WA1 and WA3–WA6 (set 136), with AD9:** West Asian texts break the home grammar in the way foreign names would, and strokes there look like sound signs.
8. **SP1, GA1/GA2 and KY4:** these methods recover Linear B → Greek in a way specific to the language. The Indus negatives are only meaningful because these validated tools produced them.
9. **TW1 and DF1 (sets 348–349):** a held-out tablet's text predicts its picture (199 against a shuffle median of 91, p = 0.005), with about 4.6% of tokens "fixed by the picture". This is real but loose, with 5% precision.
10. **MH1, MH2 and MH8 (set 145):** Mahadevan's "255 435 690 740" phrase splits into two units, AB|CD, and occurs at three sites after nine different signs: a title or name part used by many people. Runner-up: TB2, TB3 and TB5, where the structure of Indus names sits nearer early Prakrit than Tamil-Brahmi.

**FAILED** (each rules something out):
1. **SP2–SP7 (set 179):** no published key passes the substitution-phonetics test that Linear B passes (Fairservis, Parpola, Yajnadevam, Mahadevan 2014, Kak). Two pass on sample A and then fail on B, which is the signature of overfitting.
2. **KY3 and the KY results (set 206):** published keys do not beat their own shuffles in their claimed language. Fairservis has 12 of 100 shuffles as good, Yajnadevam 7 of 100, and Parpola and Mahadevan are worse than 99. Only Kak's 7-sign key gets p = 0.03, on 1,000 shuffles.
3. **KF1–KF4 (set 207):** fitted blind, Linear B fits Sanskrit best and Greek worst. So claims that the Indus script "fits Dravidian" or "fits Sanskrit" by fitting a free key are uninformative.
4. **DK1–DK3 and DK6 (set 180), with LS1, LS2 and LS4 (set 181):** no rebus key built from what the signs depict passes, in Dravidian, Sanskrit or Sumerian. A search over 503 languages finds no family signal (Dravidian sits at the 44th percentile).
5. **PA1, PA10, PR1 and PR20:** Parpola's "six or seven + fish" (star groups) is not the main pattern in ICIT. The commonest is 2 + fish (113 of 195); 6 or 7 appears in about 5%.
6. **CT5 and PL3:** the copper "equations" are swaps of the reverse-side picture, not sign values inside the text.
7. **PC1–PC4 (set 252) and BW1:** a sign's drawing does not match the picture on its object (fish signs are *rarer* on fish tablets), and the seal bull units are not words for the bull. Reading the signs as pictures of their meaning is not supported.
8. **P1 and P3 (set 1), with NA1–NA19 (set 72):** no Dravidian-style rational plural, and the ending does not agree with a number. The "31 of 34" lead was produced by repeated seals.
9. **LN6, LN7, LT2 and LT3, with TB1 and TB7:** the length and closure profiles of Indus names do not sit closer to Old Tamil than to Sanskrit or Prakrit.
10. **TM1–TM8 (set 144):** the ending slot does not change between early and late levels. RS1–RS4 (set 255) also failed: blind restorations could not be checked against the CISI photographs because none of the gaps is legible.

**Bottom line:** the ledger is unusually careful about registering predictions and using controls. It firmly establishes a reproducible grammar and morphology of the texts, and it convincingly rejects every published phonetic key it tests. It has produced no sound value and no reading. Its hold count of about 1,224 (now 1,581) is inflated by tests on generic properties, null hypotheses with little power, progress-rule duplicates and tuning ladders, and it has no correction across hypotheses. The count should not be cited as evidence of decipherment.
