# Round 35 — Gulf round seals vs attested Gulf-period names: NON-INFORMATIVE (pre-registered)

11 October 2026.

## Inputs
- 27 names of people of Dilmun, Magan and Meluhha (c. 2350–1700 BCE), plus the Dilmun gods Inzak and Panipa. Compiled from the CDLI corpus (downloaded from GitHub) and Marchesi 2024 (Failaka); see `names.tsv` and `names_sources.md`.
- 9 round seals: the 8 from round 30, plus Bourdeau's Dilmun seal 415-803-001-717-354.

## Result
With a free sign→syllable key, the best number of seals readable as an attested name:

| Set | Real names | Fake names (200 pools) | p |
|---|---:|---|---:|
| Primary (9 seals) | 8 | 9 in 96% of pools | 1.0 |
| Without 5228.1 (likely pseudo-script) | 8 | 8 in 100% | 1.0 |
| Without stroke signs | 8 | 8 in 96.5% | 0.97 |

**Power check.** Synthetic seals that truly spell names from the list (random key, padded to the real seal lengths) were detected in **0 of 40** replicates. The minimum p was 0.07. The protocol's in-script power loop (100×100) exceeded the time cap, so it was rerun smaller (40×40) as `power.py`; this is disclosed.

**Decision (fixed in advance): NON-INFORMATIVE.** Nine short seals and a free key can be read as almost any list of names. The test cannot tell true names from fakes even when the names are planted. This is the same identifiability wall as round 32, at a much smaller scale.

## What the name search itself established
- **Dilmun:** named people (kings Rimum, Yagli-El, Sumu-lêl, Samu'a; Failaka seal owners) bear Amorite or Akkadian names. The only surviving native vocabulary is the god names Inzak/Enzak, Panipa and Tamb.
- **Magan:** the ruler Nadubeli and his messenger Wedum have Akkadian names.
- **Meluhha:** the only candidate native names remain Nanaza and Samar (P453801 / CUSAS 40, Šu-Suen 6). This matches Laursen & Steinkeller 2017 and Bourdeau.
- **Consequence:** even if the round seals write names, those names were probably Amorite or Akkadian. Matching them would give sound values for the Indus signs as used abroad, not for the Harappan language. That would still be the sign-value anchor that round 32 says is missing.

## What would make this route testable
- **More seals.** Transcribe Laursen 2010's ~29 Gulf seals and Al-Sindi 1999. An exploratory power run at 20–30 seals was started and stopped for time, so the needed number is not estimated.
- **A key element fixed from outside.** For example, test whether the twins sign (091) behaves like a theophoric element such as Inzak across several seals.
- **A bilingual.** None is known.

## Files
`PROTOCOL.md`, `name_match.py`, `power.py`, `results.json`, `power_results.json`, `names.tsv`, `names_sources.md`.
