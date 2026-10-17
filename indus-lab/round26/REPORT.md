# Elephant transcription provenance

11 October 2026. This checkpoint traces digital representations; it does not recover the original editor's rationale.

## Result

All eleven elephant records have identical stored sign sequences in the frozen CSV, the freshly retrieved Lipi CSV and the supplied SQL sign-position rows. Therefore our extraction and subsequent models did not introduce the five-versus-four distinction. The SQL was parsed as text only, never executed.

The frozen CSV's immediate source was field-cady/indus_valley_script_corpus, whose README attributes its data to Lipi. The older SQL comes from yajnadevam/indus-website. Agreement among these related digital representations is not independent archaeological confirmation. Their exact historical editing relationship is not fully established here. Repository history was not audited beyond the pinned current snapshots.

The separate Mayig digitisation at commit ad2f1e218a34b8c33c57de0d6cb8d99272765bbb contains 179 Mohenjo-daro objects between M-1 and M-184, with gaps. None of the eleven elephant objects is covered. It cannot adjudicate this discrepancy. Its README describes a work in progress and subjective uncertainty annotations: https://github.com/mayig/indus-valley-script-corpus . Field-cady's source attribution: https://github.com/field-cady/indus_valley_script_corpus .

## Photographic evidence retained

Pinned Lipi image crops of M-527 A and M-1486 A bis are included. They reproduce published CISI photographs rather than supplying independent new observations. The M-527 crop shows a plausible short isolated mark at the left; M-1486 A bis also contains a plausible short mark near the adjacent larger sign. Separation from neighbouring strokes, highlighting and preservation remain concerns. No fresh exact sign count is certified from these crops. See round25 for the full plates and independent visual assessment.

The Lipi repository includes a claimed decipherment. Its Sanskrit/translations and decipherment claim were not used as evidence in this audit. The comparison uses object IDs and numeric transcriptions only.

## Operational decision

Every record in comparison.json is explicitly marked phonetic_constraint_usable=false for this particular presence/absence comparison. This does not reject the whole inscription or assert that either transcription is wrong. It prevents an unverified extra-mark distinction from being converted into a sound, word or grammatical contrast.

Reopening condition: an independently documented transcription rationale or sufficiently clear object evidence must settle whether the short mark is a separate sign, part of another sign, damage, or omitted in a digital transcription. Until then, preserve alternatives without assigning probabilities or semantic meanings. The original CSV remains unchanged.

This lead is now bounded and parked for phonetic inference. Further pattern fitting on these eleven duplicated digital strings will not resolve the missing epigraphic evidence. It can be revisited when a new source provides it.

## Reproduce

Run `python indus-lab/round26/audit_sources.py` from the archive root. Included input_records.json preserves the compared fields from the two CSVs; sql_sign_rows.txt contains only the relevant sign-position tuples. Pinned repository commits and source hashes are in provenance.json. All eleven comparisons must agree across each representation. This verifies faithful digital copying, not the ancient reading.
