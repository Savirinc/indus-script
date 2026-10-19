# Roadmap

*From 18 October 2026. The project does not wait for a bilingual; it builds the structural grid and the testing standard that a bilingual would plug into, and it tests every claim that appears. Each item says what it is, what it costs, and how it could fail.*

## Track 1. The standard of proof (now)

| Item | Deliverable | Status |
|---|---|---|
| Methods write-up | `docs/methods/METHODS-DRAFT.md` → complete draft with introduction, anchor-rebus section, discussion, references | Draft 0.1; outlines marked |
| Deposit | Zenodo record with DOI for the repository snapshot and the paper | Waiting on owner's go |
| Preprint | arXiv (cs.CL, cross-list to physics.hist-ph if allowed) once an endorser is found; OSF Preprints as fallback | Not started |
| Journal | Digital Scholarship in the Humanities, PLOS ONE, or Journal of Open Humanities Data (data paper for the harness) | After preprint |
| Claim bench | `docs/TEST-YOUR-KEY.md`; respond to each new public decipherment claim with a pre-registered round | Live; Bonta 2023 waiting on a copy |

## Track 2. Structural analysis without sounds (rounds 52 onward)

The Linear B precedent: Kober's grids came before Ventris's values. Each round below is pre-registered and controlled, and each narrows what a true key could look like.

| Round | Question | Control | Could fail by |
|---|---|---|---|
| 52 | Logosyllabic vs alphabetic vs logographic: which system's statistical signature does the Indus inventory match? | Greek, Hebrew, Cherokee, Ur III Sumerian, Egyptian, oracle-bone Chinese, Shijing, all cut to Indus text lengths and size (no open Linear B corpus exists) | **Ran: METHOD-FAIL on the large-inventory split; alphabet and syllabary excluded.** 52b needs ≥ 3 excavated corpora per class |
| 52b | Same, three classes incl. archaic administrative systems (proto-cuneiform, proto-Elamite) from the CDLI dump; nearest-corpus classifier | Leave-one-corpus-out across 12 corpora | **Ran: METHOD-FAIL** (oracle bone and Cherokee misassigned). Finding: entropy-type statistics do not separate archaic accounting from phonetic writing. Series closed; Indus nearest oracle bone, far from all alphabets and syllabaries |
| 53 | Segmentation: can texts be split into recurrent words by unsupervised methods, and do the segments behave like morphemes? | Cuneiform seal legends, Ur III lines, OB/OA letters with gold word boundaries; Shijing as one-sign-per-word control | **Ran: METHOD-FAIL.** PMI segmenter beats random on seal legends only. 53b: MDL or Dirichlet-process lexicon induction, same gold, same rule |
| 54 | Sign classes: a distributional grid (which signs substitute for which in which slots), the Kober method | Linear B grid recovered blind | Grid not stable across Harappa/Mohenjo-daro splits |
| 55 | Numerals and measures: stroke signs and their partners, tested as a counting system on tablets | Proto-Elamite and Mesopotamian numeral behaviour | Stroke signs behave like ordinary signs |
| 56 | Non-linguistic null revisited: an emblem-combinatorics generator fitted to the corpus vs the bigram model (round 28 unfinished) | Uruk III proto-cuneiform and proto-Elamite (now extracted, `round52b/controls/`) as real non-phonetic controls, plus heraldic or brand-mark corpora | Both models fit equally, or the bigram model also fits proto-cuneiform |

## Track 3. External anchors (opportunistic)

| Route | What to watch | Trigger |
|---|---|---|
| Meluhhan names | New Irisagrig and Girsu publications on CDLI; any text with *lú me-luḫ-ḫa* | Twenty names → rerun round 35 with power |
| Sealed tablets | Mitchell 1986; Laursen & Steinkeller 2017; unpublished Ur and Susa sealings | Any Type I/II Gulf impression on an inscribed tablet |
| Long text | Excavation news from Ganweriwala, Rakhigarhi, Dholavira | A text over 20 signs |
| Shape | Epigraphic tracings of Ashokan Brahmi and of Indus signs under compatible licences | Rerun round 48 with a rank-based statistic |
| Bonta 2023 | A copy of the second edition | Run through round 49 harness unchanged |

## Track 4. Things this project will not do

- Propose sound values without external anchors. Round 32 shows it cannot be validated.
- Match pictures to scripture or signs to letters by eye and call it evidence.
- Pool corpora, use upstream translation columns, or let an AI model's agreement with another stand in for a control.
- Publish or circulate beyond this repository without the owner's explicit go.

## Decision rule for adding a round

A round is worth running if (a) its result would change a status word in `docs/CONJECTURES.md`, (b) a positive control exists for it, and (c) an impossible-language or decoy control can be given identical freedom. If any of the three is missing, the idea goes in this file under "not yet runnable" with what would make it runnable.

### Not yet runnable
- Proto-Shiva epithet test (E2): needs a decoy image set with comparable published descriptions.
- Sindhi substrate search (Witzel's suggestion): needs an etymological dictionary of Sindhi, which does not exist.
- Dholavira signboard analysis: ten signs; nothing statistical can be said about one text.
