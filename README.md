# indus-script

An open, pre-registered research lab for the Indus script. Forty-nine rounds of experiments, their protocols, code, data snapshots and reports, including the ones that failed.

**Status, 17 October 2026: no Indus sign has an established sound or meaning in this project. No translation is claimed.** The current line of work tests whether the proposed Indus-to-Brahmi/Sanskrit mapping published by Yajnadevam (Bharath Rao, 2024) survives the same controls that already caught a false positive for Dravidian.

## What this repo is for

Most published "decipherments" fit a key to the corpus and then read the result as proof. This repo exists to do the opposite: write the hypothesis, statistic, null model, positive control and decision threshold *before* running anything, run a known-language control and an impossible-language control alongside, and report the verdict whatever it is. Every round is a folder with a `PROTOCOL.md`, scripts, result JSON and a `REPORT.md` that ends in the verdict word the protocol defined.

If you land here wanting to test your own reading of the script, the method and the harness are reusable. Start at `docs/STATUS.md`.

## What has survived controls

1. **Gulf round seals are foreign in sign order** (rounds 30–31). Eight round seals from Ur, Bahrain and Luristan sit at the 0.916 percentile of bigram surprisal against matched Indus seals, p < 5e-5, robust to transcription doubts. This cannot distinguish a foreign language from foreign names or pseudo-script.
2. **Statistics alone cannot recover sound values at this corpus size** (round 32). Linear B degraded to Indus conditions (about 15 tokens per sign) collapses: wrong keys outscore the true key. Roughly 40 externally anchored signs would be needed.
3. **Sign order transfers between Harappa and Mohenjo-daro** (rounds 27, 29). The script has real bigram structure. This says nothing about sound.
4. **Rigvedic foreign vocabulary leans Proto-Dravidian over Munda** (rounds 39–40), not a dictionary-size artefact, below the attribution bar. This concerns the substrate language, not the script.

## What failed, and why that matters

- **Dravidian rebus anchors** (rounds 41–43) beat about 95% of shuffled keys, p ≈ 0.06. Then round 45 ran the identical test with Finnish and Basque anchors. **Finnish beat its shuffles more strongly than Dravidian did** (p = 0.016). Verdict: artefact. The method rewards word shape, not the true language. This is the control every proposed key must now face.
- Rebus tournament (36), substrate fingerprint (37), sound-only matching (38): positive controls failed, results uninterpretable.
- Gulf seals against attested Meluhhan names (35): zero statistical power.
- Tamil pattern matching (20), correspondence decoders (22–23), copper-tablet picture labels (24–26): weak or null.

## The Brahmi lead (round 46, current)

Yajnadevam's 2024 paper includes a Table 7 standardising 38 Indus signs into Brahmi letters, and his `lipi` repository carries a full 714-code mapping to Sanskrit sounds. Round 46 reproduced the mapping's *coverage*: after the author's canonical substitutions, every sign in all 2,477 complete single-line records receives a value. Coverage is not correctness. A frequency-matched random map would cover the corpus too. `docs/atlas/` renders all 714 proposed correspondences for inspection; `docs/table7-yajnadevam-2024-p23.png` is the table itself. Fourteen of the 38 Table 7 entries still have no verified catalogue ID.

**Round 47 (pre-registered, run, verdict NULL):** the key's readings, under the author's own vowel rule, are no more Sanskrit-like than 1,000 structure-preserving shuffles of the same key (z = −0.35, percentile 0.29). The same test recognises the Linear B key at Indus density by 11.5 standard deviations and separates Greek from four wrong languages. A 15-second re-permutation of the author's own labels reaches z 5.5 for Sanskrit, 5.4 for Finnish and 9.8 for Basque. The Sanskrit in the published readings enters at the manual glossing stage, not in the key. Lead parked; see `indus-lab/round47/REPORT.md` for what would reopen it.

**Round 48 (pre-registered, run, verdict METHOD-FAIL):** the other leg of the lead, that Indus signs *look like* Brahmi letters, was put to a null test: 581 Indus glyphs against 1,061 letters from 25 scripts, nearest-shape enrichment under a complexity-stratified permutation null. None of four shape descriptors recovered known relationships (Phoenician → Aramaic, Greek → Gothic) on the positive controls, so nothing is concluded about Indus. The symmetric lesson is that eyeballed look-alike tables are not evidence either: no instrument at this resolution can tell descent from chance among simple stroke shapes. `indus-lab/round48/REPORT.md` lists what would make the question testable.

**Round 49 (pre-registered, run):** the round 47 instrument applied to every other published key available in machine-readable form. Fairservis 1992 (Dravidian, 95 signs): **NULL**, his values read no more like Tamil than random reassignments of the same values, and Finnish fits his key slightly better. Parpola 1994 (27 signs), Kak 1988 (7) and Mahadevan 2014 (5) are **not testable**: the Linear B control shows the method loses power below about 60% token coverage, and five-sign keys cannot be separated from wrong ones on 8,700 tokens. Rao 1982 (Indo-Aryan, 56 signs transcribed from his book): **NULL**, and Finnish likes his key more than Sanskrit does. Bonta 2023 is pending a copy. Every published key that can be tested is indistinguishable from its own shuffles.

## Layout

```
docs/STATUS.md                 one row per round, 09–49, with verdicts
docs/EXTERNAL-EVIDENCE.md      Meluhha names, Ur seal, Commons, source gateways
docs/atlas/                    714-sign Indus/Brahmi proposed-mapping atlas (PDF)
docs/handover/                 earlier handover documents, kept verbatim
docs/excluded-files-manifest.json   hashes of the 77 files not redistributed
indus-lab/roundNN/             one folder per round: PROTOCOL.md, code, results, REPORT.md
indus-lab/raw/                 corpus exports (read-only)
indus-lab/external/            Dravidian Database v1.1 (CC BY 4.0)
indus-lab/run.py               the original evidence lab (SQLite, recurrence, substitutions)
data/derived/                  CDLI Dilmun/Meluhha extracts, Kuiper word list
setup/                         pinned external clones, env paths, smoke test
CLAUDE.md                      working rules for AI assistants in this repo
```

## Reproduce

Standard library only, under a minute each:

```sh
python3 verify_manifest.py                              # file integrity
cd indus-lab/round46-brahmi-coverage && python3 audit.py && python3 expand.py
cd indus-lab && python3 run.py                          # evidence lab, regenerates results/
cd indus-lab/round47 && bash fetch_lexicons.sh && python3 run47.py   # 8 min, prints VERDICT NULL
cd indus-lab/round48 && bash fetch_fonts.sh && ../../ext/venv/bin/python run48.py select   # 20 s; needs ext/venv with pillow fonttools brotli numpy scipy
cd indus-lab/round49 && python3 run49.py   # 20 min; keys from dbourdeau/cyphersolver@04457698 in ext/cyphersolver_keys/
```

Rounds 29–45 need `numpy`, `rapidfuzz`, about 1 GB of pinned external clones and the Kuiper 1991 OCR text (not bundled):

```sh
pip install -r setup/requirements.txt
bash setup/setup_external.sh          # pinned commits into ./ext
# save Kuiper (1991) archive.org OCR text as data/kuiper.txt
bash setup/smoke_test.sh              # expect: indus -1 -46.888  and  lb -1 -19.093
```

Rounds 09–28 were produced by earlier sessions and may need scipy, Pillow, fontTools or PyMuPDF. Check each round's imports. `indus-lab/round36/data/build_rebus.py` has hard-coded paths from the machine it ran on.

## Data honesty

- The corpora are modern transcription exports (ICIT via lipi, Bourdeau's TSVs, Tejesh Raut's explorer). Rows are catalogue records, not deduplicated objects. Three different exports exist; never pool them silently.
- `inscriptions.csv` carries upstream Sanskrit and translation columns. They are the author's outputs. They are never used as ground truth, training targets or confirmation.
- Sign IDs are catalogue identifiers, not values.
- A seal and its modern impression are one text. Repeated texts across copies are not independent evidence.
- Copyrighted scans, photographs and an unlicensed font are excluded; see `THIRD_PARTY_NOTICES.md` and the excluded-files manifest.

## Licence

Code, protocols and reports: MIT. Data: per-source, see `THIRD_PARTY_NOTICES.md`.
