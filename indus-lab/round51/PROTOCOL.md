# Round 51 — Which language family do the proposed Meluhhan loanwords in Sumerian and Akkadian resemble?

Pre-registered 2026-10-18 before any candidate word was scored. Changes go in an "Amendments" section with the reason.

## Question
Mesopotamian scribes wrote down a handful of words for goods that came from Meluhha, and several scholars have proposed that some of these words are borrowings from the Meluhhan (Indus) language. Those words are the only Harappan speech plausibly recorded in a readable script. Do they resemble one candidate family by sound *and* meaning more than chance predicts, once impossible-language decoys and a shape-matched baseline are in place?

## Hypotheses
- **H1:** the candidate set is attributable to one family (Dravidian, Indo-Aryan, Munda or Burushaski) by the round 39 criteria.
- **H0:** no family beats the shape-matched baseline and the decoys (Finnish, Basque).

## Candidate set: compilation rule (fixed before compilation)
Include a Sumerian or Akkadian word if, and only if, a named scholar has explicitly proposed in print that it was borrowed from Meluhha or from the Indus/Harappan language. Sources searched, in order: Parpola 1994 *Deciphering the Indus Script* (archive.org scan, read visually where OCR fails); Southworth 2005 *Linguistic Archaeology of South Asia* (archive.org scan); Witzel 1999 *Substrate Languages in Old Indo-Aryan* §1.9 if reachable; Possehl 1996 if reachable; Bedigian's sesame etymologies; Wikipedia's "Meluhha" and "Harappan language" pages used only as pointers that must be traced to one of the above or to the cited primary article. Each entry records: Mesopotamian form (Sumerian or Akkadian, normalised), meaning, proposer, page, and the proposer's suggested source form (recorded, **not** used in scoring). Words whose only "Meluhhan" claim is the toponym itself (Meluhha, Magan) are listed but scored separately, because their meaning is a place, not a thing. The list is frozen by commit before `run51.py` is executed.

## Instrument (round 39, adapted)
- Lexicons with glosses: **PDR** (Dravidian DB `pdr_04.csv`, reconstruction + meaning), **IA** = Old Indo-Aryan headwords of CDIAL (JAMBU `cdial.csv`, gloss column) excluding reconstructed forms, **MUNDA** (JAMBU munda forms), **BUR** (Berger), decoys **FIN** and **EUS** (lexibank IDS forms with concept names). Normalisation: round 37 `norm` for all.
- Background for the baseline: Sumerian lemmas from ePSD2 (`gloss-sux.json`, CC0; 14,817 citation forms with guide words), nouns only, excluding the candidate words. Each target's baseline is the mean best-match of 5 background lemmas with the same CV shape (fallback: same length), seed 51001.
- Meaning relatedness, score, A_F, bootstrap (1,000 resamples, seed 51002): exactly as round 39.

## Positive controls (gate), both must pass or the result is uninterpretable
- **G1 Indo-Aryan loans in cuneiform.** The Mitanni Indo-Aryan words preserved in Hittite and Hurrian texts, fixed here: aika "one", tera "three", panza "five", satta "seven", na(wa) "nine", wartanna "turn (of the track)", babru "brown", parita "grey", pinkara "reddish", maryannu "chariot warrior", aššuššanni "horse trainer" (Mayrhofer 1966; Witzel 2001). Pass if IA ranks first in ≥ 90% of resamples with CI above 0.
- **G2 Dravidian loans in Sanskrit.** Round 39's 41 Turner Dravidian loans against the same lexicons, with CDIAL background as in round 39. Pass if PDR ranks first in ≥ 90% with CI above 0.
G1 is the one that matters: it shows the instrument can see a known donor through cuneiform spelling. Its sample is 11 words, close to the size of the candidate set, so it also calibrates the power available.

## Decision (as round 39)
- **BEST-SUPPORTED DONOR:** rank 1 in ≥ 90% of resamples, CI above 0, beats both decoys in ≥ 95%.
- **SECONDARY:** CI above 0 and beats both decoys in ≥ 95%.
- **NO FAMILY ATTRIBUTABLE** otherwise.
- **UNINTERPRETABLE** if G1 or G2 fails.
Toponyms scored separately and reported, not verdict-bearing.

## Limits stated in advance
The candidate set will be small (expected 8 to 20 words), so confidence intervals will be wide and a null is the likely outcome even if a real signal exists. Sumerian and Akkadian spellings distort foreign sounds (no distinct voiced/voiceless stops in Sumerian writing, no retroflexes, no aspirates), which lowers all similarities equally across families. A positive result would show which family the loan-givers' words resembled, which bears on the language of the Indus traders in the Gulf, not necessarily on the language written on the seals. Scholars' proposed source forms are recorded for transparency but excluded from scoring so that the test does not simply confirm their etymologies.
