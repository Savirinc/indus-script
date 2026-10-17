# Full NOTES.md audit

Audited 2026-10-10 at repository commit `843165c369a9c35658b1a7656860e06abd7a5de3`. Source: `targets/indus/NOTES.md`. This is a full textual reading and critical synthesis, not a rerun or independent verification of the recorded experiments.

## Exact coverage

All 3,269 lines / 245,109 bytes were read in ten sequential, nontruncated tool outputs: lines 1–350, 351–700, 701–1050, 1051–1400, 1401–1750, 1751–2100, 2101–2450, 2451–2800, 2801–3150, 3151–3269. No skipped main text, tables, limitations, final corrections or appendices. This includes the earlier notes not previously read in full.

SHA-256: `06b12d6604670b3eee8ce4ed06ff45bfc7f2a46e1a622313564f63369f62936d`.

## What the document actually is

An evolving research log, not a stable catalogue of established facts. Its 363 numbered passes contain preliminary interpretations, later reversals, model tuning, repeated sample comparisons and cumulative registered-test counts. The newest recorded tally is 1,581 held plus 1,492 failed = 3,073; this is an experiment ledger, not 1,581 independently established facts and not a percentage deciphered. A withdrawn interpretation can remain in that cumulative count. Some experiments are explicitly degenerate, underpowered or ill-posed. Early summaries and the final generic Next steps block are not reliably current.

The strongest methodological contribution is the willingness to expose negative controls, failures and corrections. The largest limitation is that the narrative repeatedly turns positional associations into semantic nouns—names, heads, persons, receipts, labels—before those interpretations have external confirmation. Read those as working labels unless the claim is explicitly archaeological.

## Corrections that materially change the story

| Thread | Earlier claim | Later correction / current reading |
|---|---|---|
| Corpus access | Full ICIT unavailable without an account; missing thousands of objects | Final correction says F already contains 5,680 records, 19,946 sign slots, 18,067 legible; 177 sampled book IDs present. The smaller 3,681-object analysis sample was a filter dropping 1,999 damaged records. This supports broad coverage of that edition, not all archaeological objects worldwide. |
| Direction | Reverse R/L records but not L/R; M77 mirrored; F line order listed | Initial L/R reversal corrected; fourth pass retracts M77 mirroring; pass38 says F multiline order should be reversed but old default retained for reproducibility. Count-token reversals also appear unmarked. Direction is a measurement issue, not solved by one global rule. |
| Copper anchors | Seven firm sign=image equations; parts of texts name pictured animals | Pass46 withdraws them as text anchors: reverse-side substitutions derived from Parpola drawings, not signs occurring in the relevant inscriptions. Pass47 distinguishes paired reverse images/signs over a shared inscription. Final Next steps still calls them firmest anchors: stale. |
| Bench reliability | Published keys no better than shuffles, interpreted negatively | Pass10 consonant bench fails Linear Elamite; pass17 vowel bench fails Linear B. Null results cannot reject keys when the test misses a correct key. Later character-LM scorer passes a limited Linear B gate, but free fitting still ranks Sanskrit over Greek and recovers0/30 values. Scoring a supplied key and discovering a key are different tasks. |
| Dravidian specificity | Two grammar tests favor only Dravidian outright | Conditional on names/suffixes/persons/stars. Later donor-name comparisons do not decide Tamil versus Prakrit, and genre-matched decoys destroy language ranking. No established language identification. |
| Fish-star numerals | Numeral series matches Tamil star names; 12 and1 enriched | Duplicated Lothal impressions and formula strokes inflate those counts; six-fish remains an early enrichment, not a phonetic reading. Later transcriptions agree2-fish is commonest. Numeral-series restriction and language exclusivity do not hold as first stated. |
| Openers/site | Three headings are regional variants | Pass17 withdraws city effect: small-site impressions and copies drove it; M77 merges817/861. Substitution supports a slot, not distinct offices or regional dialects. |
| Name semantics | Recurrence/capture-recapture establishes personal names, office+person | Pass171 shows count texts also have the open profile; UrIII comparison measures individuality, not personhood. Pass175 retracts office/core separation largely as length artifact. Personal-name reading remains plausible, not proved. |
| Counts/receipts | Tablets count local seal owners; fixed idioms versus variable counts | Pass44 places supposed receipt number inside the name; later seal-owner link fails. Multiple passes move between idioms and variable counts. Observed numeral-sign dependence is safer than a specific administrative translation. |
| S gains | Opening-sign context improves prediction | Final correction: first component predicts position0 from itself. Gain withdrawn; firstpos/first2 have same leakage. Corrected S returns4.635. |
| Restoration |12/15 frozen top1 correct | Eight completions were already training lines. Withdrawn, retrained copy-free. Later29/75 vs neighbor baseline23 is the reported comparison, not validation of meanings. Photos remain too poor for some checks. |
| Picture prediction | Large and growing percentage of referents established | Same-mould copies, partial transcriptions, catch-all Mult codes, nested units, site/type composition inflate results. Coverage rises as high23.77%, then falls after stratification/deduplication. Latest4.57% configuration has reported5% held-out precision. Coverage is not accuracy, and neither is decoded meaning. |
| Portability | Referent units identify pictured things | Final observation: made↔moulded transfer0/3 and1/37; seals fail. Local text-picture association does not establish a portable word meaning. |
| Other findings | Rare-word freedom=sound signs; classes validated; alternative endings settled | Known-answer controls withdraw phonetic inference; numeral clustering gate fails; closer interpretation is repeatedly withdrawn/reintroduced under different conditions. Carry versions, units and eligibility rules with each claim. |

The motif-string None bug has a documented targeted audit: twelve earlier scripts reportedly gave unchanged verdicts after normalization. This is evidence of a recorded repair, not grounds to declare every metadata field audited. Font-based visual families remain modern editorial encodings; some IDs share glyphs, and M77 merges57 ICIT signs.

## Where it is stuck

1. **Semantics remains underdetermined.** The log obtains sign order, numeral conventions, positional families and predictive associations; it does not recover a securely validated sound system, language or translation. Calling a final sign a suffix or a phrase a name is an interpretation of structure.
2. **Measurements are incomplete or edition-dependent.** Object faces, damaged runs, direction, mould/impression families and exact cross-edition equivalence affect both denominators and independence. Photographic confirmation and archaeological provenance cannot be replaced by another shuffle of the same transcription.
3. **External anchors are weak.** Picture associations are sparse, medium-specific and sensitive to copy handling. Low held-out precision survives statistically significant aggregate tests. No recorded bilingual bridges form to sound and meaning.
4. **Evaluation is adaptively reused.** The same A/B/F corpora, samples, metrics and picture vault drive hundreds of decisions. Registering the next test before executing it documents chronology but does not erase exposure to the corpus or create fresh external validation. Several replication samples share objects/upstream transcription and derive maps from matched texts.
5. **Controls establish only their tested capability.** LinearB lexical scoring does not validate Indus sign segmentation, an unknown language, allograph selection or picture-as-meaning. A model can learn recurrence and pass sign prediction while translating nothing.

## What “exhausted” can responsibly mean

The loop-end passage after pass149 says every content field has been used and internal tests cannot reach meanings. Later passes in the same file add many analyses and predictive improvements, including previously unused find-spot fields. The literal universal claim is contradicted by the subsequent work. The defensible interpretation is narrower: that particular hypothesis queue and representation showed diminishing returns, and the owner’s ten-no-progress stopping criterion was met at several checkpoints. The criterion was revised and loops restarted; per-subset replications eventually stopped counting as progress.

This is practical advice to seek higher-value evidence, not a proof that every possible algorithm or internal analysis has failed. Conversely, restarting an agent swarm or adding more registered tests does not itself add independent information. Further work needs a specific falsifiable gain rather than a promise of eventual decipherment through iteration.

## Concrete next evidence contract

Freeze the existing corpus and all discovered patterns as development data. Create an object/face/design provenance manifest and a versioned claim ledger recording superseded interpretations. Do not label a fresh random split of these familiar data untouched.

For a first external test, choose a small predeclared graphic distinction (for example plain versus marked fish or plain versus internally stroked jar). Freeze morphology, positional predictions, eligibility, abstention policy and thresholds before independent photographic recoding. Blind coders should not see preferred meanings or sequence predictions. Score agreement, errors, uncertainty and positional predictions on grouped object families; hold out whole mould/impression families and linked faces. Same-mould recognition is a production-family control, not proof that two drawn signs are the same sign.

Use photographs to test measurement and morphology first. A semantic claim additionally needs independent context that discriminates competing readings, and transfer to new designs/contexts—not merely association with the same repeated picture. Collect new evidence prospectively with a custodian when feasible; newly viewed photographs of already known texts must be labelled measurement validation, not an untouched decipherment holdout. No reruns were performed for this audit.
