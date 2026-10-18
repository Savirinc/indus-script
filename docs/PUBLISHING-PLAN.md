# Publishing plan

*Nothing in this plan happens without the owner's explicit go. Pushing to this repository is the only publication currently authorised.*

## Principle

The work is a negative result with a positive instrument: no published key survives a test that Linear B passes, and here is the test. That is publishable as methods, and useful to the field, provided it is framed as a standard rather than as a rival decipherment. Every venue below accepts negative results and reproducible code.

## Step 1. Make it citable (one afternoon)

1. **Zenodo.** Connect the GitHub repository to Zenodo; a tagged release (`v0.51`) produces a DOI that resolves to the exact snapshot. Add the DOI to `CITATION.cff` and the README. Cost: none. Licence shown: MIT for code, CC BY 4.0 for text.
2. **Software Heritage.** Request archival of the repository (free, permanent, gives a SWHID). Belt and braces for the code.

## Step 2. Preprint (a week after the draft is complete)

| Venue | Fit | Requirement |
|---|---|---|
| arXiv, cs.CL (computation and language), cross-list physics.hist-ph | Standard home for computational decipherment work (NeuroDecipher, Rao et al.) | First-time submitters need an endorser from the category; ask an author of a related arXiv paper |
| OSF Preprints | No endorsement needed; DOI; versioned | None |
| Humanities Commons CORE | Humanities audience | Free account |

Recommended: OSF first for a DOI on the day, arXiv when endorsed.

## Step 3. Peer review (after preprint)

| Venue | Why | Form |
|---|---|---|
| Digital Scholarship in the Humanities (Oxford) | Publishes computational epigraphy and negative results; reviewed by people who know the field | Article |
| Journal of Open Humanities Data | Data and software papers; the harness and pinned data sets are a natural fit | Short data paper |
| PLOS ONE | Accepts methods and negative results; open access; has published Indus statistics before (Rao et al.) | Article; APC |
| Cuneiform Digital Library Journal | For the Meluhha material of rounds 50–51 specifically | Short note |
| Workshops: LChange, SIGTYP (ACL) | Computational historical linguistics audience; fast turnaround | Short paper |

## Step 4. Community (after Step 1)

- **harappa.com** carries working papers on the Indus script and has hosted both Mahadevan and critics; a short summary with the DOI is appropriate there.
- The **Indology list** is where Witzel and others discussed earlier claims; a one-paragraph announcement with the DOI, no more.
- Direct notes to the authors whose keys were tested (Yajnadevam, Bonta), with the protocol and the invitation to run their own pipeline through the harness. This is outreach and requires the owner's explicit go.

## Framing rules for every venue

- Lead with the instrument and its calibration (Linear B passes), then the results, then the checklist.
- Name no one as wrong; show the shuffle distribution and where each key sits in it.
- State plainly that the project proposes no reading and does not decide Dravidian against Indo-Aryan.
- Declare the AI assistance in the methods section, with the protocols and seeds as the audit trail.
- Keep the Tamil Nadu prize out of the paper; it is context for why claims will multiply, not a motive.

## What is not published

Copyrighted scans used for reading (Rao 1982, Possehl 1996, Parpola 1994) are cited, not redistributed. Hashes of excluded files remain in `docs/excluded-files-manifest.json`.
