# indus-script: working rules

Owner: Arham Partap Jain. Mission: decipher the Indus script, honestly. State as of 23 Oct 2026: **rounds to 58 (56 reserved), no sign has an established sound or meaning.** Read this file, then `docs/STATUS.md`.

## Stay inside this repo
All work happens in this repository. New rounds go in `indus-lab/roundNN/`. Do not create files elsewhere except the scratchpad for throwaway runs. Do not touch `~/Indus Script Decipher`; it is the pre-repo archive.

## Rules (non-negotiable)
- **Pre-register:** write `roundNN/PROTOCOL.md` (hypothesis, statistic, null, positive control, negative control, decision thresholds, seed, trial count, stopping rule) before any fitting or before looking at test material. Later changes go in an "Amendment" section with a reason, before results.
- **Positive control first:** Linear B (`ext/neurodecipher/data/linear_b-greek.cog`) or another known script, degraded to Indus conditions. If it fails, the Indus result is uninformative.
- **Negative control:** an impossible language (Finnish, Basque from lexibank IDS). Round 45 is the reason: Finnish fitted better than Dravidian.
- **Report failed tests.** `REPORT.md` with the protocol's verdict word, then one row in `docs/STATUS.md`.
- Never use the upstream Sanskrit/translation columns of `indus-lab/raw/inscriptions.csv` as evidence. Never edit anything in `indus-lab/raw/` or `indus-lab/external/`.
- Agreement between agents is not independent evidence.
- Park a branch when it yields no discriminating prediction, and say what evidence would reopen it.
- Coverage is not correctness. Statistics invariant under relabelling cannot identify sounds.
- No outreach, purchases, upstream edits or public posting beyond this repo without Arham's explicit OK. Pushing to this repo is authorised.

## Bayesian evidence ledger (from 22 Oct 2026)
Every new test is planned against `reports/LEDGER.md` under the twelve rules in `reports/LEDGER-RULES.md`: fixed Bayes-factor scale (×3/×10/×30/×100), prereg with a factor for each outcome, prereg and script `chmod 444` with sha256 in the commit message, gate (≥ ×3 possible or it is a measurement), one score per evidence cluster, VOID on failed positive control, replicate seeds near thresholds, fragility check after each update. Update the ledger when a round closes.

## Working style
- One sentence on what you're doing, then do it. Short progress notes on long runs.
- Lead with the verdict and a small table, then what it means, then ONE recommended next step.
- Be direct when something fails. No over-claiming, no wandering.

## Data facts
- Main corpus: `indus-lab/raw/inscriptions.csv`, 5,679 rows, SHA256 `c22d39c3…3429`, text in column 34. Core text types 1,936. 582 sign types, ~8,700 tokens, ~15 tokens/sign.
- Loader: `indus-lab/round30/foreign_context.py` → `FC.TRAIN` (reading order, 3-digit sign IDs).
- Explorer snapshot (round 46): `indus-lab/round46-brahmi-coverage/texts.js`, 5,445 records. Do not pool with the CSV.
- Proposed Sanskrit map: `round46-brahmi-coverage/xlits.csv` (lipi commit fc8813a); expanded 714-code map in `expanded-map.json`.
- Copper-tablet texts in `round24/predictions.json` are stored reversed relative to `FC.TRAIN`.
- Numerals: 001/031 one, 002/032 two, 003/013/033 three, 004/014/034, 005/015/035, 016/036, 017, 018. Pictographs: 220 fish, 090 man, 520 arrow, 740 jar, 803/806 leaf, 269 bird.
- Proto-Dravidian: `indus-lab/external/dravidian_db_v1.1/pdr_04.csv`; use `round37/fingerprint.py:norm` on `reconstruction`, not the `simplified` column.
- Shared code: `round41/anchored.py` (trigram LM, annealing fit, heldout, split, permute), `round37/fingerprint.py`, `round32/benchmark.py` (Linear B).
- Gotchas: system Python has no numpy; round 48 uses `ext/venv` (git-ignored) for Pillow/numpy/scipy; macOS Accelerate prints spurious matmul warnings (values verified). Clear `lm.cache` per fit or long runs OOM; `python3 -I` breaks sibling imports, run scripts from their round folder; each 60k-step fit ≈ 4 s.
- Setup: `pip install -r setup/requirements.txt`, `bash setup/setup_external.sh`, supply `data/kuiper.txt`, `source setup/paths.sh` (exports `$DATA_ARGS` = KUIPER JAMBU DRDB IDS LINB in that order).

## Round numbering
Rounds 09–45 follow the original lab. The Brahmi coverage audit (called "Round 29" in its own handover, which collided with the existing round 29) is **round 46**; its pre-registered test is **round 47** (NULL); the shape-resemblance test is **round 48** (METHOD-FAIL); the published-key tournament is **round 49** (Fairservis and Rao NULL, others not testable); the sealed-tablet census is **round 50** (INCOMPLETE, A = 0); the Meluhhan-loanword attribution is **round 51** (NO FAMILY ATTRIBUTABLE, gates passed); the writing-system signature test is **round 52** (METHOD-FAIL on logosyllabic vs logographic; alphabet and syllabary excluded). Round **52b** (three classes incl. proto-cuneiform/proto-Elamite) also METHOD-FAIL; series closed; the segmentation test is **round 53** (METHOD-FAIL: PMI segmenter beats random only on seal legends). The syllabic-core freedom test is **round 54** (METHOD-FAIL on both controls). **Round 53b** (Dirichlet-process segmenter) METHOD-FAIL by 0.001 on OB/OA letters. **Round 57** (Bhaty 2024 place names under Yajnadevam's key, 435/436 → o) NULL, control passed; round 56 stays reserved. **Round 58** (Sanskrit/Old Tamil syllable repetition at Indus lengths, pre-registered measurement under the ledger): PARTIAL, 10 of 14 conditions EXCLUDED for bijective syllabic keys (ledger X7); Old Tamil names in spoken syllables (3.2%) not excludable; homophony undoes it. **Round 55** (stroke signs, measurement): no numeral-like substitution (percentile 0.08; PE/proto-cuneiform controls 1.00); with strokes removed only 5 of 14 stay EXCLUDED (running text in written syllables, Old Tamil words); names conditions open in both languages. X7 now stated for both readings; merged-numeral caveat deleted as misplaced. Ledger X6 added (no literal Classical/Epic Sanskrit or Sangam/later Tamil reading). Track 2 generic statistics are exhausted (52, 52b, 53, 53b, 54 all METHOD-FAIL on real controls); next is the methods paper, or 54b (slot grid) at most.

## Established (survived controls)
1. Rounds 30–31: Gulf round seals are foreign in sign order (percentile 0.916, p<5e-5).
2. Round 32: statistics alone cannot recover sounds at ~15 tokens/sign; ~40 anchors needed.
3. Rounds 39–40: Rigvedic substrate words lean Proto-Dravidian over Munda; below attribution bar; about the substrate, not the script.
4. Rounds 27/29: bigram structure transfers between cities.
5. Round 47: the trigram-LM shuffle test recognises the Linear B key at Indus density (z 11.5) and rejects Yajnadevam's key (z −0.35). Reusable harness: `round47/run47.py`.
6. Round 49: the same instrument on partial keys works down to ~60% token coverage (Linear B passes 2/3 subsets) and not at ~28% (1/3). Keys under 25 signs cannot be tested on this corpus.
7. Round 51: the round-39 sound+meaning instrument recovers a known donor (Mitanni Indo-Aryan words in cuneiform) from an 11-word sample (IA rank 1 in 100%).
8. Rounds 52–52b: at matched size and text length the Indus corpus is not alphabet- or syllabary-like (control passed; distances 3–10× those to large-inventory systems); nearest Shang oracle-bone inscriptions by 4–5× over any of twelve corpora, stable under leave-one-out. Only 3.5% of texts repeat a sign (oracle bone 3%; everything else 13–34%): a constraint on any key. Conditional entropy, H1 and Heaps slope do NOT separate proto-cuneiform/proto-Elamite from Sumerian/Egyptian (Rao et al. 2009's statistic fails on real controls); A1 cannot be settled by this family of statistics. Archaic controls extracted in `round52b/controls/` for round 56. Harness `round52/run52.py`; controls in `round52/controls/` (SUX regenerated by `fetch_controls.sh` + `extract52.py`).

## Parked (don't redo without a new idea)
- **Yajnadevam Brahmi/Sanskrit key (46–47): PARKED.** Key covers the corpus but its output is not Sanskrit-like beyond its own shuffles (z −0.35); a 15 s refit to Finnish/Basque beats it. Reopen only with a frozen automated pipeline given equal freedom for impossible languages, or external anchors.
- **Indus–Brahmi shape resemblance (48): UNTESTABLE with fonts.** Four shape descriptors all failed to recover Phoenician→Aramaic or Greek→Gothic, so look-alike tables are not evidence either way. Reopen only with epigraphic tracings (Ashokan Brahmi, Indus sign lists) and a pre-registered rank-based statistic; declare the v1 Indus numbers (Brahmi E 0.35) as previously seen. Shape tooling: `round48/run48.py` (needs `ext/venv`: pillow, fonttools, numpy, scipy).
- **Writing-system class (52, 52b): METHOD-FAIL twice; series CLOSED.** Do not run a 52c: more corpora improve the control but the features measure record type and inventory, not system class. Logosyllabic vs logographic not separable with 1–2 corpora per class; the 99% Mahalanobis region built from resampling variance was mis-specified. Reopen as 52b only with ≥ 3 excavated corpora per large-inventory class and a nearest-corpus bootstrap. No open Linear B running-text corpus exists (DĀMOS CC BY-NC-SA, no export).
- **Word segmentation (53, 53b): METHOD-FAIL twice; CLOSED.** DP lexicon induction (`round53b/run53b.py`, ~5 min) passes seal legends (0.196) and misses OB/OA letters by 0.001; Indus induced lexicon = known frequent sequences (861-002, 817-002, 820-002, X-740, 920-060-741), multi-sign token share 0.54, S 1.42 vs Shijing 1.50. Do not rerun with other seeds.
- **PMI word segmentation (53): METHOD-FAIL.** Pairwise cohesion cannot find words at 8,726 tokens even on Sumerian/Akkadian lines with gold boundaries; Shijing scores longer segments than Akkadian letters. Gold-boundary extracts in `round53/controls/` (` | ` word separators) are ready for 53b. Indus description: S 1.26, M 0.57, shuffle 1.05/0.19.
- **Combinatorial freedom as syllabic signature (54): METHOD-FAIL.** AUC 0.46/0.65 on Akkadian gold; Shijing freer than Akkadian syllabograms. Freedom = slot position, not function. Indus freedom table in `round54/results.json` (most restricted 817, 090, 520, 400, 861, 820; freest 741, 031, 440, 742) is grid input only. Akkadian extracts with syllabic/logographic flags in `round54/controls/`.
- **Published keys (49):** Fairservis 1992 NULL; Rao 1982 NULL (key transcribed in `round49/keys/rao1982.tsv` from the archive.org scan); Parpola 1994, Kak 1988, Mahadevan 2014 NOT TESTABLE (too little coverage or too few signs). Harness `round49/run49.py` scores any key file (sign, value, confidence, gloss) unchanged; Bonta 2023 runs through it as soon as a copy exists (`data/sources/`).
Rebus tournament (36), substrate fingerprint (37), sound-only matching (38), Gulf seals vs names (35), anchor-rebus branch (41–45, Finnish artefact), Tamil pattern matching (20), correspondence decoders (22–23), copper-tablet labels (24–26).

## Public-facing documents (keep in sync when a round closes)
`README.md` (summary tables §2–3), `docs/CONJECTURES.md` (status words per conjecture), `docs/ROADMAP.md` (tracks and next rounds), `docs/PUBLISHING-PLAN.md`, `docs/TEST-YOUR-KEY.md`, `docs/USED-BY.md`, `CITATION.cff` (bump version = round count). GitHub Discussions are enabled; answer key submissions with a pre-registered round.

## Open leads
1. **External anchors.** Round 50 found no Indus-sign impression on any inscribed tablet in open sources (Collon 1996 catalogue: 3 Late Gulf textless impressions); Mitchell 1986 and Laursen & Steinkeller 2017 remain unread (not online). More Gulf/Dilmun seal transcriptions (Laursen 2010; Al-Sindi; Kjærum Failaka) still need PDFs; then re-run round 35 with power and test the 415-803-001 opening.
1b. **Meluhhan loanwords (round 51): CLOSED on the published record.** Possehl 1996a obtained (archive.org `indian-ocean-in-antiquity`): no loanword list, only Sumerian terms qualified "of Meluhha"; Glassner's šamru added; strict set also null. Harness `round51/run51.py` + `candidates.tsv`.
2. **Methods write-up: DRAFT 0.2 complete** at `docs/methods/METHODS-DRAFT.md` (rounds 27–54: key tests 47/49, anchors 41–45, shape 48, loanwords 51, structural series 52–54, unicity argument, checklist, AI declaration, references). Next edits only on Arham's review notes. Text licence CC BY 4.0. Do not publish or circulate without Arham's OK; Zenodo DOI first when he says go.
3. **Pending key.** Bonta 2023 2nd ed. (Academia.edu, gated; no open copy found): transcribe to key format with page refs, commit, run `round49/run49.py` unchanged.
