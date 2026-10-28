# indus-script — a pre-registered test bench for Indus script decipherment claims

**Arham Partap Jain · Savir Platforms · public since 17 October 2026 · 63 rounds (56 reserved; 61 locked, 62 offered)**

> **Status, 19 October 2026: no Indus sign has an established sound or meaning in this project, and none is claimed. Every published key that can be tested on the corpus reads no better than a random re-assignment of its own values. The structural results that survive controls are listed below. The methods, data pins and failed tests are all here.**

This repository is not a decipherment. It is the instrument that decipherments have to pass, built in public, with the protocols written before the results. If you have a reading of the Indus script, [you can test it here in minutes](docs/TEST-YOUR-KEY.md). If you want to know what is actually known about the script and what is conjecture, read [`docs/CONJECTURES.md`](docs/CONJECTURES.md). If you want the plan, read [`docs/ROADMAP.md`](docs/ROADMAP.md).

---

## 1. Why this exists

The Indus script, about 4,000 inscriptions from 2600–1900 BCE averaging five signs each, has been "deciphered" dozens of times since 1925: as Dravidian, as Sanskrit, as Munda, as Sumerian, as Egyptian, as not writing at all. None of these readings is accepted, and none has ever been tested the way a scientific claim is tested: against a null model that could have said no.

Every one of them follows the same shape. A key is fitted to the corpus, the readings come out "meaningful", and the meaningfulness is presented as proof. The question this project asks of each key is simpler and harder: **do your readings look more like your language than the readings produced by shuffling your own values among your own signs?** For a real key, as for Linear B, the answer is yes by a wide margin. For every Indus key tested so far the answer is no.

The working rules, in force since round 29 and written into [`CLAUDE.md`](CLAUDE.md):

1. **Pre-register.** Hypothesis, statistic, null, positive control, negative control, decision thresholds, seeds and stopping rule go into `PROTOCOL.md` and are committed before any code runs. Changes afterwards are amendments with a stated reason, before results.
2. **Positive control first.** A known script (Linear B) degraded to Indus conditions must pass. If it fails, the Indus result is uninterpretable.
3. **Negative control.** An impossible language (Finnish, Basque) is given identical freedom. If it fits as well, the result is an artefact.
4. **Report failures.** Every round ends in the verdict word its protocol defined, and a one-row entry in [`docs/STATUS.md`](docs/STATUS.md).

## 2. What is established (survived controls)

| Finding | Rounds | Strength |
|---|---|---|
| The sign order is real: bigram structure transfers between Harappa and Mohenjo-daro | 27, 29 | Structural; says nothing about sound |
| Gulf round seals from Ur, Bahrain and Luristan are foreign in sign order (percentile 0.916, p < 5e-5) | 30, 31 | Robust to transcription doubts; cannot separate foreign names from pseudo-script |
| Statistics alone cannot recover sound values at ~15 tokens per sign; about 40 externally anchored signs would be needed | 32 | Linear B benchmark |
| Even given the right language, the corpus would need ≤ 528 signs if word boundaries were known and ≤ 414 without them; the best defensible sign merge gives 541 | 63b | Linear B ladder, 5 draws per level; optimistic for Indus |
| The trigram shuffle test recognises the Linear B key at Indus density (z 11.5) and works for partial keys down to ~60% coverage | 47, 49 | The instrument's calibration |
| The round 39 sound-and-meaning instrument recovers a known donor (Mitanni Indo-Aryan words in cuneiform) from an 11-word sample | 51 | Calibration for loanword tests |
| Rigvedic foreign vocabulary leans Proto-Dravidian over Munda, below the attribution bar | 39, 40 | About the substrate, not the script |

## 3. What has been refuted or closed

| Claim or route | Rounds | Result |
|---|---|---|
| Yajnadevam 2024, 714-code Sanskrit key, "100% of inscriptions read" | 46, 47 | **NULL.** Readings under the author's own vowel rule sit at percentile 0.29 of the key's own shuffles (z −0.35). A 15-second refit of his labels beats his key by 6 sd in Sanskrit, and does the same in Finnish and Basque. The Sanskrit enters at the manual glossing stage. |
| Fairservis 1992, Dravidian key, 95 signs | 49 | **NULL.** Tamil z 0.20; Finnish fits his key better. |
| Rao 1982, Indo-Aryan key, 56 signs transcribed from his book | 49 | **NULL.** Sanskrit z −0.70; Finnish z 2.06. |
| Parpola 1994 (27 signs), Kak 1988 (7), Mahadevan 2014 (5) | 49 | **Not testable** on this corpus: too little coverage or too few signs; the Linear B control fails at their coverage. |
| Dravidian rebus anchors predicting held-out texts (p ≈ 0.06) | 41–45 | **ARTEFACT.** Finnish anchors did better (p = 0.016). |
| Indus signs "look like" Brahmi letters | 48 | **METHOD-FAIL.** Four shape descriptors cannot recover Phoenician → Aramaic or Greek → Gothic from fonts, so look-alike tables are not evidence for or against. Brahmi ranked 20th of 25 scripts descriptively. |
| Rebus tournament; substrate fingerprint; sound-only matching | 36–38 | Positive controls failed; uninterpretable. |
| Gulf seals read as attested Dilmun/Meluhha names | 35 | Non-informative: 27 names, fake names match as often as real. |
| Indus-sign seals impressed on inscribed cuneiform tablets (a near-bilingual) | 50 | **None exist** in any published catalogue (Gadd 1932, Hallo & Buchanan 1965, Collon 1996, full CDLI). The three Gulf-seal impressions on tablets are textless Dilmun types. |
| Meluhhan loanwords in Sumerian/Akkadian | 51 | **No family attributable.** Eleven candidates; Finnish ranks first. Possehl's 1996 catalogue holds no loanwords, only Sumerian terms qualified "of Meluhha". The one word an ancient list calls Meluhhan, *šamru* "thorn tree", matches Sanskrit *śamī* and Proto-Dravidian "thorn" equally, at a similarity one random plant word in five achieves. |
| Indus signs behave like an alphabet or a syllabary (the premise of every letter-value key) | 52 | **Excluded** at matched corpus size and text length: the control recovers alphabets perfectly and the Indus statistics sit among large-inventory systems, nearest oracle-bone Chinese and Ur III Sumerian. The finer logosyllabic-vs-logographic split was **METHOD-FAIL** (not separable with one or two corpora per class). |
| Conditional entropy and inventory statistics show the signs encode language (Rao et al. 2009) | 52b | **Does not discriminate.** At matched size, Uruk III proto-cuneiform and proto-Elamite (largely non-phonetic accounting) match Ur III Sumerian and Egyptian on conditional entropy, unigram entropy and Heaps slope. The Indus corpus is nearest the Shang oracle-bone inscriptions by 4–5× over any other of twelve corpora and far from every alphabet and syllabary; class beyond that is **METHOD-FAIL**. |
| Texts can be cut into words by adjacent-sign cohesion (PMI segmentation) | 53 | **METHOD-FAIL** at 8,726 tokens: the segmenter beats random boundaries only on cuneiform seal legends, and scores the Shijing (one sign per word) above Akkadian letters. The "monosyllabic" versus mixed-system question stays open; a lexicon-induction segmenter is the next attempt. |
| A syllabic core can be detected by free combination (signs that combine with anything are syllabograms) | 54 | **METHOD-FAIL.** On Akkadian letters, where syllabograms are known, the statistic does not find them (AUC 0.46 and 0.65), and the Shijing's one-sign-per-word characters combine more freely than Akkadian syllabograms. Freedom measures slot position, not sign function. |
| Texts can be cut into words by lexicon induction (Dirichlet-process unigram model) | 53b | **METHOD-FAIL by 0.001** on two of four gold corpora. Descriptively the Indus corpus segments like the one-sign-per-word Shijing or below it, and the induced lexicon is just the known frequent sequences; but the Shijing is not separated from Akkadian letters on segment length, so no verdict is possible. |
| Bhaty 2024: seals name Bronze Age places (Moka = Magan/Makran, Hattusa, Umma, Susa, Daman…) under Yajnadevam's key with one vowel changed | 57 | **NULL.** Every place known to Mesopotamia, plus all her names, matches her readings no more often than shuffles of her own key (percentile 0.41), and less often per name than scrambled consonant strings or Finnish towns. Linear B place names pass the same test (z 4.2). |
| Any Sanskrit or Tamil key that reads one sign as one syllable, with no two signs sharing a sound (most popular decipherments) | 58, 55 | **Excluded for running text, open for names.** Real Sanskrit verses and Old Tamil poem lines and words, written syllable by syllable, repeat a syllable more often than the seals repeat a sign (6–9% against 3.5%), so a key of this kind cannot turn the seals into them. That holds whether or not the stroke signs are numbers. Lists of names are excluded only if the strokes count as ordinary signs; Old Tamil names in spoken syllables are never excluded. Keys where several signs share a sound are not covered. |

Full detail per round: [`docs/STATUS.md`](docs/STATUS.md). Each round's folder has the protocol, code, results and report.

## 4. Why every key "reads": the information-theoretic reason

Shannon's unicity distance says a key is unique only when the text is long enough relative to the key's information and the language's redundancy. The Indus corpus has 582 sign types, 8,720 tokens, a median of two tokens per sign, and texts averaging 4.5 signs that are almost all different from each other, which is the profile of names. Under those conditions a refit of Yajnadevam's own labels produces text more "Sanskrit" than real Sanskrit by the same measure (2.87 vs 2.99 bits per character). When wrong keys outscore real language, the corpus is below the unicity distance by definition. Dictionaries do the rest: a 186,000-word Sanskrit lexicon or a Tamil fish/star pun turns any short string into something, which is why Dravidianists see stars and Sanskritists see gods in the same five signs. The full argument is in [`docs/methods/METHODS-DRAFT.md`](docs/methods/METHODS-DRAFT.md).

## 5. Use, attribution and permission

- **Code** is MIT licensed. You may use it for anything, including testing your own key. The licence requires that the copyright notice travel with the code.
- **Text** (protocols, reports, methods draft, this README) is CC BY 4.0: reuse with attribution.
- **Data** keep their upstream licences; see [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). Copyrighted scans and an unlicensed font are not redistributed; their hashes are in `docs/excluded-files-manifest.json`.
- **If you use the harness or the results, please cite the repository** ([`CITATION.cff`](CITATION.cff); GitHub's "Cite this repository" button) **and tell us** by opening a Discussion or an Issue. We keep a list of uses in [`docs/USED-BY.md`](docs/USED-BY.md). An open licence cannot legally require notice, so this is a request, and attribution is the enforceable part.
- Commercial or closed use of future releases may move to a source-available licence that requires permission; if that happens it will be announced here and will not affect versions already released.

## 6. Test your own key

Put your sign values in a three-column file (catalogue sign ID, value, note), run `indus-lab/round49/run49.py`, and in about twenty minutes you will know whether your readings beat your own shuffles, whether Finnish beats you, and whether the Linear B control passes at your coverage. Instructions: [`docs/TEST-YOUR-KEY.md`](docs/TEST-YOUR-KEY.md). The outcome words are NULL, ARTEFACT, SUPPORT, MIXED or NOT TESTABLE, and they are defined before you run.

## 7. Layout

```
docs/STATUS.md                 one row per round, 09–54, with verdicts
docs/CONJECTURES.md            every open conjecture, with what would refute it
docs/ROADMAP.md                what comes next and why
docs/PUBLISHING-PLAN.md        where this work can be deposited and reviewed
docs/TEST-YOUR-KEY.md          how to run your key through the harness
docs/USED-BY.md                known uses of this work
docs/methods/METHODS-DRAFT.md  the write-up (draft 0.2, complete; rounds 27–54)
docs/EXTERNAL-EVIDENCE.md      Meluhha names, Ur seal, source gateways
docs/atlas/                    714-sign Indus/Brahmi proposed-mapping atlas (PDF), compiled by the owner with GPT assistance after S. R. Rao's mapping idea; a hypothesis document, not evidence
docs/handover/                 earlier handover documents, kept verbatim
indus-lab/roundNN/             one folder per round: PROTOCOL.md, code, results, REPORT.md
indus-lab/raw/                 corpus exports (read-only)
indus-lab/external/            Dravidian Database v1.1 (CC BY 4.0)
indus-lab/run.py               the original evidence lab (SQLite, recurrence, substitutions)
data/derived/                  CDLI Dilmun/Meluhha extracts, Kuiper word list
setup/                         pinned external clones, env paths, smoke test
CITATION.cff                   how to cite
CLAUDE.md                      working rules for AI assistants in this repo
```

## 8. Reproduce

```sh
python3 verify_manifest.py                                   # file integrity (sha256 of every tracked file)
cd indus-lab/round47 && bash fetch_lexicons.sh && python3 run47.py        # 8 min, stdlib; prints VERDICT NULL
cd indus-lab/round49 && python3 run49.py                                 # 20 min, stdlib; all published keys
cd indus-lab/round48 && bash fetch_fonts.sh && ../../ext/venv/bin/python run48.py select   # 20 s; needs ext/venv (pillow fonttools brotli numpy scipy)
cd indus-lab/round51 && ../../ext/venv/bin/python run51.py               # 1 min; needs numpy, rapidfuzz, JAMBU data materialised
cd indus-lab/round46-brahmi-coverage && python3 audit.py && python3 expand.py
cd indus-lab && python3 run.py                                           # evidence lab, regenerates results/
```

Rounds 29–45 need `numpy`, `rapidfuzz`, about 1 GB of pinned external clones and the Kuiper 1991 OCR text (not bundled):

```sh
pip install -r setup/requirements.txt
bash setup/setup_external.sh          # pinned commits into ./ext
# save Kuiper (1991) archive.org OCR text as data/kuiper.txt
bash setup/smoke_test.sh              # expect: indus -1 -46.888  and  lb -1 -19.093
```

Rounds 09–28 were produced by earlier sessions and may need scipy, Pillow, fontTools or PyMuPDF. Check each round's imports.

## 9. Data honesty

- The corpora are modern transcription exports (ICIT via lipi, Bourdeau's TSVs, Tejesh Raut's explorer). Rows are catalogue records, not deduplicated objects. Three different exports exist; never pool them silently.
- `inscriptions.csv` carries upstream Sanskrit and translation columns. They are one author's outputs and are never used as ground truth, training targets or confirmation.
- Sign IDs are catalogue identifiers, not values.
- A seal and its modern impression are one text. Repeated texts across copies are not independent evidence.
- Modern Tamil and Classical Sanskrit are both far younger than the seals; any match to either is a match to a descendant.

## 10. How to contribute

Open an Issue with a key file, a counter-argument to a protocol, a transcription correction, or a source we could not reach (Mitchell 1986; Laursen & Steinkeller 2017; Bonta 2023 2nd ed.). Pull requests that add a round must include `PROTOCOL.md` committed before the code, as the existing rounds do. Agreement between people or models is not evidence; a passed control is.

## 11. Acknowledgements

Data and code lineages this work stands on: the Indus Website export and Bourdeau's `cyphersolver` transcriptions; Yajnadevam's `lipi` repository; Tejesh Raut's explorer; the Dravidian Database (Kolipakam et al.); lexibank IDS; the JAMBU/CDIAL data; Kotus; Xuxen; NeuroDecipher; ePSD2 (Oracc); Noto fonts; and the public scans on the Internet Archive that made Rao 1982, Possehl 1996, Collon 1996 and Glassner 1996 readable. Analyses were designed and run with an AI assistant; the protocols, seeds and code are the record of what was done.
