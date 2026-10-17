# Held-out initial correspondence test

Protocol fixed before executing this experiment. Existing dataset has previously been inspected: this is not an untouched external validation corpus.

Question: can a conditional initial-segment table trained on Tamil cognates predict the initial segment of a related-language cognate for excluded concepts better than copying the Tamil initial?

Use round21's supplied cognacy classifications. For each Tamil/target-language pair, retain a concept only if all shared cognate groups together imply exactly one initial on each side. Discard ambiguous cases, recording their count. No selection by model success. Thus this tests already-classified cognates, not identification of unknown cognates.

Five folds by integer SHA256(concept ID) modulo five. All records for a concept are held out together. Train initial-to-initial frequency table on other concepts. Predict modal target initial; ties prefer the unchanged source initial, then lexical ordering. For an unseen source initial, copy it. Compare with copying for every example and the training set's unconditional modal target initial.

Controls: for each target language and fold, shuffle training target initials 100 times (fixed seeds), preserving source and target marginals. Use the same fitting/prediction rule. Report descriptive distribution of accuracy, not a significance test across dependent folds/languages. This shuffle breaks source-target association and is distinct from the copy baseline.

Report all 19 Tamil-to-other-language directions, pooled concept-language-record micro accuracy and per-language results. Concepts represented in more languages contribute more pooled records; these are not independent statistical samples. Score only the first segment, never whole-word accuracy. No tuning, proto-form prediction, sound-change direction, chronology, Meluhhan attribution or Indus sign assignment. Regularity among descendants alone does not establish an ancestral pronunciation.

Reporting clarification after execution: the phrase "equal-concept micro accuracy" originally used above was imprecise. The implementation has always pooled concept-language records. This wording correction did not change the experiment or results.
