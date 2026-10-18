# indus-script: working rules

Owner: Arham Partap Jain. Mission: decipher the Indus script, honestly. State as of 18 Oct 2026: **48 rounds, no sign has an established sound or meaning.** Read this file, then `docs/STATUS.md`.

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
Rounds 09–45 follow the original lab. The Brahmi coverage audit (called "Round 29" in its own handover, which collided with the existing round 29) is **round 46**; its pre-registered test is **round 47** (NULL); the shape-resemblance test is **round 48** (METHOD-FAIL). Next is 49.

## Established (survived controls)
1. Rounds 30–31: Gulf round seals are foreign in sign order (percentile 0.916, p<5e-5).
2. Round 32: statistics alone cannot recover sounds at ~15 tokens/sign; ~40 anchors needed.
3. Rounds 39–40: Rigvedic substrate words lean Proto-Dravidian over Munda; below attribution bar; about the substrate, not the script.
4. Rounds 27/29: bigram structure transfers between cities.
5. Round 47: the trigram-LM shuffle test recognises the Linear B key at Indus density (z 11.5) and rejects Yajnadevam's key (z −0.35). Reusable harness: `round47/run47.py`.

## Parked (don't redo without a new idea)
- **Yajnadevam Brahmi/Sanskrit key (46–47): PARKED.** Key covers the corpus but its output is not Sanskrit-like beyond its own shuffles (z −0.35); a 15 s refit to Finnish/Basque beats it. Reopen only with a frozen automated pipeline given equal freedom for impossible languages, or external anchors.
- **Indus–Brahmi shape resemblance (48): UNTESTABLE with fonts.** Four shape descriptors all failed to recover Phoenician→Aramaic or Greek→Gothic, so look-alike tables are not evidence either way. Reopen only with epigraphic tracings (Ashokan Brahmi, Indus sign lists) and a pre-registered rank-based statistic; declare the v1 Indus numbers (Brahmi E 0.35) as previously seen. Shape tooling: `round48/run48.py` (needs `ext/venv`: pillow, fonttools, numpy, scipy).
Rebus tournament (36), substrate fingerprint (37), sound-only matching (38), Gulf seals vs names (35), anchor-rebus branch (41–45, Finnish artefact), Tamil pattern matching (20), correspondence decoders (22–23), copper-tablet labels (24–26).

## Open leads
1. **External anchors.** More Gulf/Dilmun seal transcriptions (Laursen 2010; Al-Sindi; Kjærum Failaka) need PDFs from Arham; then re-run round 35 with power and test the 415-803-001 opening.
2. **Methods write-up.** Rounds 32, 45 and 47 together discredit a common class of decipherment claims. Do not publish without Arham's OK.
