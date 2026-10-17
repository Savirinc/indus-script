# Indus research 14 — comparative-language baseline

10 October 2026. A completed benchmark on known languages; no Indus sign reading or language identification.

## What we built and ran

We acquired the openly licensed DravLex comparative dataset, preserved its source files, license and commit, and ran a fixed phonetic-similarity baseline. The source has 2,127 forms across 20 Dravidian languages and 100 concepts. We excluded 141 forms explicitly labelled as loans, leaving 1,986 forms.

The program compared 18,990 cross-language pairs with the same supplied meaning. Expert cognacy labels define 6,913 positive and 12,077 negative pairs. Similarity is normalized edit distance over phonetic segments. No parameters were fitted and no threshold was tuned.

| Measure | Observed | Mean of 100 shuffled controls |
|---|---:|---:|
| Primary pooled AUC | 0.8184 | 0.5853 |
| Equal-concept average AUC | 0.8680 | 0.4991 |

An AUC measures ranking: within an eligible concept, a documented cognate pair outranks a non-cognate pair approximately 87% of the time on average, giving half credit for ties. This is not 87% translation accuracy. The macro calculation covers 95 concepts having both classes.

The control shuffles relationship labels among forms within each concept, retaining label counts. It respects shared-form pair dependence better than shuffling each pair independently. Pooled control performance exceeds 0.5 because concepts differ in both score distributions and cognate prevalence. Therefore we report both metrics and no inferential p-value.

## What this establishes—and what is missing

The baseline detects expected sound resemblance in annotated known-language data. Expert cognacy decisions themselves use sound evidence, so this is a sanity check, not independent proof of ancestry. All languages are Dravidian; the test cannot identify an unknown language's family. Supplied meanings and pronunciations are major advantages unavailable for Indus inscriptions. Loan annotations may also be incomplete. No untouched confirmation set is claimed.

The next benchmark should remove known meanings and then hide the sound-to-symbol mapping. A useful system must recover consistent correspondences across multiple words and reject unrelated or randomized alternatives. A strong result on known meanings alone is insufficient for Indus.

## The wider evidence resource

We inspected the current JAMBU compiled data at commit 665850cdd1451391dc939063b5ccc972e646f6f6. This snapshot has 991,379 form rows and 578 language-table entries, substantially different from the 2023 publication's counts. These are database rows, not that many independent ancient words. 535,922 rows carry the status `unlinked`; that field must not be treated as a verified etymological relationship. The inventory records the file hash and current category counts.

JAMBU assembles historical and comparative sources across South Asian languages. Its paper distinguishes inherited relationships from broader uses of the word cognate and describes both attested forms and reconstructed ancestors. It supplies a foundation for future comparisons, not a list of Indus words. We performed read-only inspection, not a source ingestion or rebuild. Full JAMBU data is not redistributed in this bundle; the commit and audit results are retained.

## First disputed lexical leads

| Form | Meaning | Cited attestation | Treatment |
|---|---|---|---|
| phala | fruit | Rigveda 4.57.6 | Dravidian, Munda and Indo-Aryan explanations compete |
| kuṇḍa | vessel/pit | Rigveda 8.17.13 | Proposed Dravidian comparison; Iranian comparanda and meaning differences require review |
| lāṅgala | plough | Rigveda 4.57.4 | Proposed Austroasiatic/intermediary connection alongside wider comparisons |

These are examples discussed in the literature, not confirmed Harappan survivals. Witzel treats hymn 4.57 as a later addition; a book number is not a borrowing date. Parpola also argues that some substrate vocabulary could reflect Central Asian contact before entry into the Indus region. Each claim needs separate attestation, donor, borrowing-date and geography fields. No word has been assigned to an Indus sign.

## Reproduction

Run `python3 indus-lab/round14/benchmark/run.py`. It uses the bundled DravLex snapshot and Python's standard library. Protocol, per-concept scores, all control results, source hashes, license and lexical claim records are included.

Sources:

- DravLex, Kolipakam et al.; Lexibank conversion, CC BY 4.0: https://github.com/lexibank/dravlex ; commit 37578075e5ccb09c43022f7f1282125e748de84d.
- Arora et al. 2023, JAMBU: https://aclanthology.org/2023.sigmorphon-1.8/ ; data: https://github.com/moli-mandala/data .
- Witzel, Substrate Languages in Old Indo-Aryan, section 1.6 and plough discussion: https://www.researchgate.net/publication/241460738_Substrate_Languages_in_Old_Indo-Aryan_Rgvedic_Middle_and_Late_Vedic .
- Parpola 2010, A Dravidian solution to the Indus script problem, pp.10–12: https://www.harappa.com/sites/default/files/pdf/Parpola-2010-Coimbatore.pdf .
