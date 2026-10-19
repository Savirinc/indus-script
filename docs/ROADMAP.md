# Roadmap

*From 18 October 2026. The project does not wait for a bilingual; it builds the structural grid and the testing standard that a bilingual would plug into, and it tests every claim that appears. Each item says what it is, what it costs, and how it could fail.*

## Track 1. The standard of proof (now)

| Item | Deliverable | Status |
|---|---|---|
| Methods write-up | `docs/methods/METHODS-DRAFT.md`: introduction, data incl. twelve control corpora, methods 3.1–3.9, results 4.1–4.7 (keys, anchors, shape, loanwords, structural series 52–54), discussion, limitations, AI-assistance declaration, references | **Draft 0.2 complete (19 Oct 2026)**; awaiting owner's read-through before deposit |
| Deposit | Zenodo record with DOI for the repository snapshot and the paper | Waiting on owner's go |
| Preprint | arXiv (cs.CL, cross-list to physics.hist-ph if allowed) once an endorser is found; OSF Preprints as fallback | Not started |
| Journal | Digital Scholarship in the Humanities, PLOS ONE, or Journal of Open Humanities Data (data paper for the harness) | After preprint |
| Claim bench | `docs/TEST-YOUR-KEY.md`; respond to each new public decipherment claim with a pre-registered round | Live; Bonta 2023 waiting on a copy |

## Track 2. Structural analysis without sounds (rounds 52 onward)

*Status after rounds 52–54: four pre-registered rounds, four METHOD-FAILs on real controls. Generic sign statistics (inventory, entropy, Heaps, repetition, PMI segmentation, combinatorial freedom) do not distinguish logosyllabic from one-sign-per-word writing at 8,726 tokens. What they do establish: alphabets and syllabaries are excluded; the corpus is nearest the oracle-bone inscriptions; sign order is real; 3.5% of texts repeat a sign. 53b (lexicon induction) also failed its control by 0.001 on two corpora. The remaining Track 2 item is 54b (slot grid, no claim about sign function); otherwise the methods paper reports the series.*

The Linear B precedent: Kober's grids came before Ventris's values. Each round below is pre-registered and controlled, and each narrows what a true key could look like.

| Round | Question | Control | Could fail by |
|---|---|---|---|
| 52 | Logosyllabic vs alphabetic vs logographic: which system's statistical signature does the Indus inventory match? | Greek, Hebrew, Cherokee, Ur III Sumerian, Egyptian, oracle-bone Chinese, Shijing, all cut to Indus text lengths and size (no open Linear B corpus exists) | **Ran: METHOD-FAIL on the large-inventory split; alphabet and syllabary excluded.** 52b needs ≥ 3 excavated corpora per class |
| 52b | Same, three classes incl. archaic administrative systems (proto-cuneiform, proto-Elamite) from the CDLI dump; nearest-corpus classifier | Leave-one-corpus-out across 12 corpora | **Ran: METHOD-FAIL** (oracle bone and Cherokee misassigned). Finding: entropy-type statistics do not separate archaic accounting from phonetic writing. Series closed; Indus nearest oracle bone, far from all alphabets and syllabaries |
| 53 | Segmentation: can texts be split into recurrent words by unsupervised methods, and do the segments behave like morphemes? | Cuneiform seal legends, Ur III lines, OB/OA letters with gold word boundaries; Shijing as one-sign-per-word control | **Ran twice: METHOD-FAIL.** PMI (53) beats random on seal legends only; Dirichlet-process lexicon induction (53b) passes seal legends and misses OB/OA letters by 0.001 each. Segmentation is closed; the induced Indus lexicon is the known frequent sequences |
| 54 | Sign classes: does a free-combining syllabic core exist (the Kober method's premise for a logosyllabic script)? | Akkadian letters with gold syllabic/logographic marking; Shijing and oracle bone as no-core controls | **Ran: METHOD-FAIL.** Freedom does not separate syllabograms from logograms (AUC 0.46/0.65) and Shijing is freer than Akkadian. 54b, if run: a grid from slot restriction alone, no claim about sign function |
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
