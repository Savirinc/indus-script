# Direct-link coverage audit

Date:2026-10-10. Source inventory: `page-links.json`. Local read source: clone `/tmp/indus-cyphersolver-audit`, commit `843165c369a9c35658b1a7656860e06abd7a5de3`. Fragments were deduplicated to page URLs; no recursive whole-site crawling was performed.

The supplied inventory contains 54 link entries, 26 unique destinations after fragment removal, of which 17 are local HTML pages. The team has fully read extracted main prose for all 16 linked local pages other than the main Indus page, which was additionally read by the coordinator. This completes the 17-local-page direct-link prose scope; it does not imply recursive reading of their own links.

## Local page ledger

| Page | Coverage | Scope |
|---|---|---|
| [atlas.html](https://dbourdeau.github.io/cyphersolver/atlas.html) | Full extracted main prose read | 1,055 extracted characters. Scripts/styles/navigation/header/footer excluded; images not re-examined; linked sources not recursively opened. |
| [catalogue.html](https://dbourdeau.github.io/cyphersolver/catalogue.html) | Full extracted main prose read | 92,785 extracted characters, including all card text on this page; destinations linked by those cards were not recursively opened. |
| [esterhazy1744.html](https://dbourdeau.github.io/cyphersolver/esterhazy1744.html) | Full extracted main prose read | 6,870 extracted characters. Scripts/styles/navigation/header/footer excluded; images not re-examined; linked sources not recursively opened. |
| [famous.html](https://dbourdeau.github.io/cyphersolver/famous.html) | Full extracted main prose read | 11,129 extracted characters. Scripts/styles/navigation/header/footer excluded; images not re-examined; linked sources not recursively opened. |
| [ferdinand3.html](https://dbourdeau.github.io/cyphersolver/ferdinand3.html) | Full extracted main prose read | 18,643 extracted characters. Scripts/styles/navigation/header/footer excluded; images not re-examined; linked sources not recursively opened. |
| [geertruidenberg.html](https://dbourdeau.github.io/cyphersolver/geertruidenberg.html) | Full extracted main prose read | 11,280 extracted characters. Scripts/styles/navigation/header/footer excluded; images not re-examined; linked sources not recursively opened. |
| [glossary.html](https://dbourdeau.github.io/cyphersolver/glossary.html) | Full extracted main prose read | 5,134 extracted characters. Scripts/styles/navigation/header/footer excluded; images not re-examined; linked sources not recursively opened. |
| [hesse1672.html](https://dbourdeau.github.io/cyphersolver/hesse1672.html) | Full extracted main prose read | 10,659 extracted characters. Scripts/styles/navigation/header/footer excluded; images not re-examined; linked sources not recursively opened. |
| [highlights.html](https://dbourdeau.github.io/cyphersolver/highlights.html) | Full extracted main prose read | 37,451 extracted characters, including all card text on this page; destinations linked by those cards were not recursively opened. |
| [index.html](https://dbourdeau.github.io/cyphersolver/index.html) | Full extracted main prose read | 170,053 extracted characters, including all card text on this page; destinations linked by those cards were not recursively opened. |
| [indus.html](https://dbourdeau.github.io/cyphersolver/indus.html) | Coordinator main-page audit; extracted here | 36,157 extracted characters. Not claimed as a second full read by this link auditor. |
| [keys.html](https://dbourdeau.github.io/cyphersolver/keys.html) | Full extracted main prose read | 1,814 extracted characters. Scripts/styles/navigation/header/footer excluded; images not re-examined; linked sources not recursively opened. |
| [lineara.html](https://dbourdeau.github.io/cyphersolver/lineara.html) | Full extracted main prose read | 43,565 extracted characters. Scripts/styles/navigation/header/footer excluded; images not re-examined; linked sources not recursively opened. |
| [rupert.html](https://dbourdeau.github.io/cyphersolver/rupert.html) | Full extracted main prose read | 17,033 extracted characters. Scripts/styles/navigation/header/footer excluded; images not re-examined; linked sources not recursively opened. |
| [secret.html](https://dbourdeau.github.io/cyphersolver/secret.html) | Full extracted main prose read | 1,897 extracted characters. Scripts/styles/navigation/header/footer excluded; images not re-examined; linked sources not recursively opened. |
| [sieniawski1708.html](https://dbourdeau.github.io/cyphersolver/sieniawski1708.html) | Full extracted main prose read | 15,745 extracted characters. Scripts/styles/navigation/header/footer excluded; images not re-examined; linked sources not recursively opened. |
| [writeups.html](https://dbourdeau.github.io/cyphersolver/writeups.html) | Full extracted main prose read | 141,585 extracted characters, including all 292 entry summaries and final Only in the notes catalogue. Linked destinations not recursively opened. |

Extraction uses HTML tag stripping and entity decoding, with `<main>` preferred where present. This is a prose inspection, not browser interaction or a rendered visual audit. Complete extracted text is saved in `link-prose/`; saving/extracting text alone is not counted as reading. One combined read was truncated; Rupert and Sieniawski were re-read separately in full. LinearA was read in two complete chunks. Index was read in six contiguous character chunks: [0:18000], [18000:50000], [50000:80000], [80000:110000], [110000:140000], [140000:170053]. Highlights was read in [0:20000] and [20000:37451]. Archaeology reader confirmed catalogue in six nontruncated chunks [0:18000], [18000:36000], [36000:54000], [54000:72000], [72000:90000], [90000:92785], replacing an initially truncated attempt. Methods reader confirmed writeups in eight nontruncated contiguous chunks: [0:20000], [20000:40000], [40000:60000], [60000:80000], [80000:100000], [100000:120000], [120000:140000], [140000:141585].

## External direct links

| Destination | Status |
|---|---|
| https://github.com/erc-dharma | Organization overview and visible repository summaries read; no claim to read all62 repositories. |
| https://archaeologymag.com/2025/01/prize-offered-to-decipher-indus-valley-script/ | Full article main prose read (title/byline/date/body). Reader comments, related-story carousel and share links excluded from evidentiary use. |
| https://github.com/mayig/indus-valley-script-corpus | README and actual root LICENSE read in this auditor’s repository audit; see repositories.md. |
| https://github.com/dbourdeau/cyphersolver | Coordinator clone/methods audit; this follow-up does not claim every target file was read. |
| https://github.com/dbourdeau/cyphersolver/tree/main/targets/indus | Coordinator/methods reviewer covers targeted files; see methods.md and methods-files.json. |
| https://github.com/erc-dharma/tfb-eiad-epigraphy | Coordinator reports README read; not independently re-read here. |
| https://old.harappa.com/script/indusscript.pdf | Covered by source-review workflow; this link audit makes no additional full-PDF claim. Consult sources-review.md. |
| https://tamildigitallibrary.in/ | Initial browser-search timeout superseded by successful HTTP 200 retrieval (415,084 bytes). Archaeology reader fully read the 4,516-character extracted homepage prose; saved as link-prose/tamil-library-root.txt. Specific 2025/2026 volumes were not acquired/read in this step. |
| mailto:dnbourdeau@gmail.com | Contact link, no document to read; no message sent. |

## Findings relevant to the user’s request

The neighbouring cipher write-ups frequently succeed because an original key, interlinear decipherment, parallel plaintext or known-language crib survives. That is a useful contrast with the Indus problem, not evidence that identical tools recover Indus meanings. The six recent cipher write-ups were read as process comparisons; their historical claims and numerical results were not independently rerun here.

The LinearA page is a particularly relevant methodological comparison: it distinguishes arithmetic/commodity constraints from sound values and unknown language, records failed language-matching controls, and says unavailable external material limits progress. Its claimed fractions and readings are still the author’s analysis; this link audit did not validate them against original tablets or scholarly consensus.

The index and writeups page still label the Indus write-up with 2,364 registered tests (writeups: 1,224 held / 1,140 failed), while the main Indus page has a later count. Its dated feed also revises earlier cipher claims. These are versioned author reports, not cumulative independent confirmations. Highlights presents the author’s selected cipher successes and their reported controls; no solver or historical claim was independently reproduced in this read.

The famous-ciphers overview contains broad judgments and some simplified/stale Indus statements (including a longest-text figure differing from the prize article). Do not use this navigation survey as an archaeological authority or silently reconcile incompatible counts. Definitions and inscription units must be checked against primary catalogues.

The prize article is secondary reporting of the reward and proposed Tamil-mark comparisons, not an official submission protocol, adjudication rubric or proof of historical continuity. Its comments contain unsupported decipherment claims and are not research evidence. DHARMA is a useful scholarly comparator source; its much later inscriptions are not direct Indus translations.

## Explicit exclusions

No recursive traversal of the261/292 write-up cards,972-target catalogue, repository links inside those linked pages, all DHARMA repositories, article comment links, or site JavaScript app interactions. No claim of reading all papers/books cited anywhere in the website. All four formerly sampled navigation pages have now been read in full extracted prose. The Tamil Digital Library homepage was read after successful fallback retrieval; this does not cover its books or deeper catalogue.
