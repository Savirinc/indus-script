# Round 50 — Indus-sign seal impressions on inscribed tablets: **INCOMPLETE, trending CLOSED (A = 0 in every source reached)**

Pre-registered in `PROTOCOL.md` (commit 80403e5) before any source was opened for this purpose. No amendments.

## Result
| Category | Count | Cases |
|---|---:|---|
| A: legible Indus signs on an impression on an inscribed tablet | **0** | none found |
| B: Gulf-type impression, iconography only | 1 | YBC 5447 (Hallo & Buchanan 1965) |
| C: uncertain signs | 0 | – |

The verdict word is **INCOMPLETE** because three listed sources could not be obtained (below). In every source that was read, the count of near-bilinguals is zero, so the route is trending CLOSED, not merely untested.

## The one case: YBC 5447
A consignment agreement dated to the tenth year of Gungunum of Larsa, about 1923 BCE (CDLI P306518, provenience probably Ur). Luma'a consigns wool, wheat and sesame to Hatin-Ibanum son of Apkallum, who swears to render account; witnesses Ur-Shulpa'e the seer and Erishti-ili, foreman of the fishermen. The tablet carries several impressions of one round "Persian Gulf" stamp seal of Buchanan's Type III, the Dilmun type, and Hallo argues the sealer is the debtor, whose name is not Babylonian and whose divine element may be a Gulf god. So the tablet does name the probable owner of a Gulf seal. But the seal's design is two seated figures drinking through a tube, a bucranium and cross-hatched squares. Buchanan's own note on the squares: they recall Indus sign shapes, but "Indus script, if present, seem no longer used as such." Type III seals carry no text. There is nothing to anchor.

Buchanan also records (n. 4) that in all Mesopotamian and Indus material only one ancient impression has ever been matched to a recovered seal, a rectangular Indus seal at Mohenjo-daro, and that uninscribed.

## Sources read and what they yielded
| Source | Reached | Impressions on inscribed tablets |
|---|---|---|
| Gadd 1932, PBA 18 (archive.org scan) | yes, in full | none; 18 seals, no sealings; seal no. 1 is an Indus-style seal with a cuneiform legend, not a tablet |
| Hallo & Buchanan 1965, AS 16 (ISAC open PDF) | yes, in full | YBC 5447 (category B) |
| CDLI catalogue, full dump (154 MB, 2026) | yes | `seal_information` of 0 tablets mentions Gulf, Dilmun, Tilmun, Indus or "stamp" for Ur, Larsa or Susa; the 53 Old Babylonian Ur tablets with seal data have cylinder legends, "illegible" or "anepigraphic" |
| UET 5 (via CDLI records) | yes | no stamp-seal impressions recorded |
| Mitchell 1986, *Bahrain through the Ages* pp. 278-285 | **no** (not online) | unknown |
| Legrain 1951, UE X | **no** (Stony Brook repository returns 403) | unknown; a cylinder-seal catalogue, unlikely to add stamp impressions |
| Laursen 2010; Laursen 2016; Laursen & Steinkeller 2017 | **no** (harappa.com and Wiley 403; book not open) | unknown; Laursen 2016 abstract concerns stamped tokens with cuneiform at Bahrain, not Indus signs |
| Amiet, Susa glyptic | **no** | unknown |

## What this means
- The "near-bilingual" idea was worth checking and it fails on the material that is open. Dilmun seals that were impressed on dated tablets are of the late, textless type. The Gulf seals that do carry Indus signs (Gadd's round seals, rounds 30-31) are the earlier type and none is recorded impressed on an inscribed tablet.
- The remaining hope is narrow: Mitchell 1986 or Laursen & Steinkeller 2017 might list an Ur sealing not in CDLI. Given that CDLI's seal fields for Ur are populated and show nothing, the prior is low.
- The one two-script object, Gadd no. 1 with its unreadable archaic cuneiform legend, remains what it was in round 34: suggestive and unusable.

## Reopen criteria
A copy of Mitchell 1986 or of Laursen & Steinkeller 2017 chapter on sealings; or any published tablet with a Type I/II Gulf seal impression. The census table `census.tsv` takes new rows unchanged.

## Reproduce
Sources and the CDLI dump are in the session scratchpad, not the repo (sizes and copyright). Gadd 1932: archive.org `in.gov.ignca.33779`. Hallo & Buchanan: ISAC `as16.pdf`. CDLI: `cdli-gh/data` `cdli_cat.csv` via Git LFS media URL; the search is a regex over `seal_information`, `provenience`, `period`, `museum_no`.
