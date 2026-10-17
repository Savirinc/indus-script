# Round 36 — Rebus tournament: method REJECTED by its own Chinese validation (pre-registered)

12 October 2026. The Indus tournament was NOT run, as the protocol requires.

## What was tested
- **Idea:** each candidate language assigns sounds to picture signs mechanically (sign → that language's word for the picture), with no fitted parameters.
- **Score S1:** if rebus was used, signs that sound alike under the right language should be used in similar contexts.
- **Validation:** run on classical Chinese, where the true readings (Middle Chinese) are known, against 14 other languages, before touching the Indus inscriptions.

## Result

| Setting | Tagged signs | Corpus | True Middle Chinese key | Rank | Verdict |
|---|---:|---|---:|---|---|
| C-full | 51 pictographs | 86,270 characters | percentile 0.29 (ρ = −0.02) | 14th of 16 | FAIL |
| C-indus | 12 (Indus concept set) | 8,751 characters (Indus-sized) | percentile 0.45 | 10th of 15 | FAIL |
| Exploratory: Indus tags, full corpus | 12 | 86,270 characters | percentile 0.89 | 3rd | — |

In C-full the leader was Burushaski (0.94). In C-indus the only language above 0.95 was Japanese, a control. Rankings are noise.

## Why it failed (interpretation)
- In real text, how a picture sign is USED (its neighbours) is driven by its meaning and grammar, not by its sound. Rebus homophony leaves almost no trace in usage statistics, even in Chinese, where rebus genuinely shaped the script.
- In Chinese the rebus trace is in sign FORMATION: phonetic components inside compound characters. For the Indus script we cannot hear the compounds, so that channel cannot be used.

## The pictograph inventory, which stands on its own
- Of the 250 commonest Indus signs (95.6% of tokens), only 7 object signs (jar, fish, man, arrow, bird, two leaf forms) and 17 stroke numerals are clear pictures.
- This is far fewer than Chinese offers (51 at frequency ≥5 here). Any picture-to-sound method has very little to work with in this script.

## Decision
The S1 rebus tournament is rejected. No Indus language claim is made. Files: `PROTOCOL.md`, `tournament.py`, `indus_pictograph_tags.tsv`, the render sheets, `chinese_control_results.json`, and `data/` (word lists, provenance, coverage).
