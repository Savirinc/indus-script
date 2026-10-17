# Round16 — focused methods audit and correction of our novelty claims

Repository snapshot: dbourdeau/cyphersolver commit843165c369a9c35658b1a7656860e06abd7a5de3. Read-only audit; no computational reruns. File hashes and exact review scope are in methods-files.json. This is a focused audit of dictionary, language-model and language-control methods, **not an audit of the whole repository, all links or every prediction**.

## Main correction

The user is right: the source project already implemented important parts of the route we have been exploring. It has dictionary-based key fitting, held-out inscription scoring, shuffled controls, synthetic planted-key experiments, matched lexicons, character language models, known-script validation and wrong-language/genre decoys. Ourround15 synthetic cipher demonstration is an engineering baseline under easier assumptions, not a new decipherment strategy. We should have mapped this prior work before presenting another model-building round as forward research progress.

## What the inspected implementations do

### Dictionary keys: bench.py; linb_control.py

The dictionary bench reduces proposed phonetic values to coarse consonant or vowel-aware skeletons and finds a high-coverage segmentation into dictionary entries, allowing selected ending consonants. Its denominator is the material covered by the supplied key, so partial-key coverage must be reported separately. Vowels, diacritics and some consonantal distinctions are collapsed; this substantially increases accidental matches. Frequency-banded key shuffles provide a useful within-key comparison but are not a semantic reading test.

The published LinearB control output reports11–41 of100 shuffled keys scoring at least as well as the real key, depending on settings. That fails a strict known-answer discrimination gate. This result is in the saved output and consistent with the code's stated test; I have not rerun the third-party datasets.

### Dictionary fitting on held-out data: fit_holdout.py; matched_holdout.py

fit_holdout.py fits250 common signs to freely chosen syllabic/consonantal values, scores M77-only lines not exactly matching the training lines, tests shuffled training, and includes a synthetic Dravidian planted-key generator. This is already the broad idea of hiding a known language behind artificial signs and checking recoverability.

Specific implementation limitations: hill climbing maximizes covered-consonant count, while the reported score is a covered/total ratio; changing values can change the denominator. Values are many-to-one, and adjacent identical characters are collapsed. Missing sign values split runs. Synthetic lines concatenate generated words then truncate to target line length; unsupported material may be skipped. The simulation is a chosen encoder, not an archaeological writing model. Exact-line holdout removes direct string duplicates but is not a proof of independent object or production-family sampling.

matched_holdout.py samples equal-sized lexicons stratified by consonant count, uses multiple draws and a synthetic positive control, and compares standardized held-out gains over shuffled keys. The source includes an explicitly inconclusive interpretation and acknowledges dependence on lexicon construction. I inspected the full implementation but did not acquire/rerun its external wordlists or independently validate its saved numerical outcomes.

### Character LM scorer: lmkey.py; predict_test205.py

The scorer is an add0.5-smoothed character n-gram wordlist model. It joins supplied sign values without word dividers, gives each decoded line an average log score per character, and averages across eligible lines. It deletes unknown sign values rather than maintaining unknown spans, another reason key coverage matters.

Set205 chooses order2–5 on odd-numbered LinearB lines and evaluates the known Ventris key on even-numbered lines against100 frequency-banded shuffled keys. The saved output selects order5: no shuffled key matches the Greek-model score, whereas9/100 match it under the Sanskrit model. This validates discrimination of that **supplied known key against these shuffles**, not recovery of unknown values. Odd/even lines can share formulas, scribes or objects; this is not a strong independent excavation holdout. Greek orthographic adjustments are supplied from known LinearB conventions.

### Blind key fitting: keyfit.py; predict_test207.py

Each language supplies its90 most common consonant-plus-vowel units. Every sign may independently take any unit, including the same unit as other signs. Annealing runs30000 steps under an order3 model on odd lines; an order5 model scores even lines. A separately fitted within-line-shuffled corpus provides the reference. Two seeds are tried.

Saved result: Sanskrit gives the largest gain for both seeds; Greek is last for seed1 and third for seed2. The fitted Greek key agrees with none of the30 most common Ventris values. Thus a method that recognizes the correct key when supplied does not necessarily recover it or identify the correct language when allowed to fit freely.

The failure is informative but bounded: Fit.run returns the terminal state, not the best visited state; the inventory is limited to90 frequent units, with no checked guarantee the true values are representable; many-to-one collapse is unrestricted; the fitting and evaluation orders differ; only two seeds are reported. Lexicons and genre differ between languages. Therefore this experiment rejects this specific free-fit procedure as a reliable identification gate, not all possible language-model approaches or decipherment in principle.

### Name structure and decoys: predict_test197.py; predict_test198.py; lang_names.py

Set197 compares structural summaries with Tamil-Brahmi/Prakrit candidates and Japanese/Turkish decoys. Set198 explicitly changes candidate material to name lists to address the inscription-versus-list genre confound. Its saved output puts Japanese first on the full sample and both halves, ahead of Sanskrit and OldTamil lists. The source retracts the earlier language interpretation while retaining the original historical record.

These comparisons remain heuristic: units differ among scripts/languages (morae, syllables, grapheme clusters, signs); Indus bodies/endings are an inferred analysis; four summary distances are combined by mean ranks; the 'head share' implementation uses the last two elements in known-language lists versus one final body sign in Indus. The Japanese win is not evidence of Japanese Indus. It is evidence that this comparison does not uniquely select the proposed SouthAsian candidates.

## PREDICTIONS and PROGRESS: what was checked

Read the relevant197/198 and205–207 registrations/results, and PROGRESS's tier definitions, stopping rule, and loop summaries. The documents preserve failed tests and withdrawals and distinguish structural performance from phonetic values. They also record repeated later corrections for duplicate inflation and weak transfer in image associations. Their numerical summaries are project-reported, not independently reproduced here.

The site's247-set headline differs from the current checkout, which contains prediction scripts through350. Do not combine these as one contemporaneous snapshot. The existence of headings saying 'registered before testing' does not itself prove commit chronology; this focused audit did not inspect every historical commit. Repeated adaptive use of the same corpus/splits does not create a fresh independent holdout each round. The progress/prize thresholds are project-defined research targets, not an established external decipherment standard.

## Consequence for ourround15

Our hidden-sound exercise uses a random **bijective phoneme substitution**, known word boundaries, known segmentation, a disclosed inventory including held-out sounds, a preselected related reference and a same-language full-vocabulary control. The project above already examined more flexible sign-to-unit fitting and demonstrated its wrong-language failure on LinearB. Our higher toy recovery is not evidence that we solved that difficulty: the bijection removes collapse, boundaries constrain decoding, and the vocabulary/language are much more favourable.

The meaning-blind retrieval baseline similarly establishes only phonetic retrieval among known related languages; it neither eliminates dictionary bias nor supplies an Indus language test. Keep these experiments as transparent engineering controls and explicitly downgrade any novelty framing.

## Concrete gate before further model work

First map our proposed experiment to the existing code and result that already addresses it. A new run must identify one changed assumption and a falsifiable reason that change should fix a documented failure. The next model gate must recover an independently known script under matched freedom and reject wrong-language/genre-matched controls, with errors and key recovery shown, before being treated as evidence about Indus. Freeze a prospective evaluation set rather than reusing the same familiar corpus as if unseen. If no genuinely different discriminating test exists, shift effort to independent evidence and source verification rather than another fit.

No additional models were run in this audit.

## Follow-up: completed work beyond the webpage's set247 snapshot

Read all247 lines of PROGRESS.md and NOTES.md lines2600–3269, covering the complete post247 narrative, final limitations/next-step sections and appended corrections. Also read predict_test350.py and the final PREDICTIONS registration. These are documentary audits; the implementations of sets248–349 were not all reviewed or rerun.

**Latest completed state is set349, not350.** PROGRESS ends at loop174/set349; NOTES ends its completed sequence with the same result. The cumulative reported tally is1,581 held and1,492 failed hypotheses (3,073). Set350 has a registration and script for learned distributional-class referent units but no result section and no results/predict_test350.md in this checkout. Treat it as pending/unreported. NOTES pass numbers differ from prediction-set numbers: its363rd pass corresponds to set349. The website's2,727 hypotheses/247 sets are an older reporting cutoff.

The later work already addresses several tempting 'next steps':

- **Restoring damaged signs:** set255's original-scan check was blocked because14 examined gaps remained illegible. Set258's two available independent CISI readings missed the predicted top5. Set282's apparent12/15 top1 success was withdrawn after eight completed lines proved present in training. Copy-excluding retraining and additional cases ultimately give29/75 restored signs, versus23/75 for a simple neighbour baseline (sets283–285,314). This is limited sign-restoration evidence, not reading sound or meaning, and the incremental advantage is small.
- **Predicting pictures from text:** raw performance improved through many representation/threshold changes, but the project repeatedly found nonportable associations, dominant-picture confounds, partial-text leakage and mould duplicates. Cross-city apparent successes were withdrawn (set299); transfer from tablet-derived units to seals failed (set319). A statistical picture association is not a portable lexical meaning.
- **Copy correction materially changed the story:** the site/type-stratified coverage figure13.64% collapsed to1.09% when distinct texts were counted; the reported shuffle-based FDR rose to50.3% (set337). A revised manufactured-copy/impression treatment and tighter alpha produced2.80% (set339). Subsequent skip-pair and graphic-family expansion reached4.57% (set348). These changing denominators/units mean the historical maxima cannot be presented as current decipherment coverage.
- **The latest4.57% is weak association coverage, not translated text.** Set349 reports199 correct picture matches among3,948 held-out match observations (about5%), compared with a shuffled median91. These are repeated split-half match observations, not3,948 independent archaeological objects. The project's 'confirmed' language means above its randomization control; it does not imply95% reliable sign meanings. Multiple train/test splits of the same repeatedly analysed data do not make this prospective confirmation.
- **Corrected picture vault:** set341 collapses359 moulded tablets to152 designs and reports46 correct held-out pictures among165 predicted cases, against a shuffle median5. This replaces the earlier excess+64 with+41. Preserve the task-specific denominator and copy correction; do not mix this approximately28% prediction precision with the5% unit-match precision above.
- **Further model/grammar variants often failed:** learned object-class context, grammar priors, extra candidate inventories, several new grammatical rules and word-frequency priors did not deliver registered gains. The source reports structural scores plateauing around4.635 bits/sign, with line length supplied to parts of the score. Its adopted WORD task remains poor and phonetic-value componentP remains0. Rich structural regularity has not become a decipherment.
- **Stopping rules already triggered twice:** sets277 and324 reached ten no-progress loops; new owner-authorized runs resumed. A swarm needs the same discipline: another loop is not evidence of advancement, and restarting should state its genuinely new assumption or data.

Final NOTES sections contain stale statements alongside explicit corrections. In particular, 'obtain the fullICIT' is withdrawn by the final note: the broader5,680-record source was already present, while the analysis loader discarded1,999 damaged records. The note identifies unused legible stretches in those damaged texts. This is a coverage/filter distinction, not a newly discovered external corpus. The final note also says early dumps lack separated faces; do not project that onto our independently grouped full-export face records without checking schema. Likewise the early duplicate-count limitation does not describe every late corrected analysis.

For our work the immediate consequence is to stop proposing damaged-text restoration, picture prediction, graphic-family clustering, or additional LM fitting as unexplored routes. They require a specified improvement over these baselines, an independently checked observation, and a new evaluation gate. Higher-resolution original evidence and correct object/production identity remain concrete needs; the project itself records where scan quality and duplicated manufacture blocked interpretation.

## Files actually reviewed

Full code: keyfit.py, lmkey.py, linb_control.py, fit_holdout.py, matched_holdout.py, predict_test197.py, predict_test198.py, predict_test205.py, predict_test207.py, predict_test350.py. Full saved outputs: results/predict_test197.md, results/predict_test198.md, results/predict_test205.md, results/predict_test207.md, results/linb_control.md. Full document: PROGRESS.md. Targeted portions only: bench.py (normalization/scoring/shuffle methods and fit/control declarations), lang_names.py (source declarations and relevant name loaders), PREDICTIONS.md (197/198,205–207,347–350), NOTES.md (opening overview and lines2600–3269). Several other files were downloaded but not read fully; downloading is not an audit. All reviewed direct downloads were compared with the checkout snapshot; subsequent additions were read directly from that checkout.
