# Round 35 — Do the Gulf round seals write attested Gulf-period names? (pre-registered)

Written 11 October 2026 before any matching code was run. Inputs are fixed below.

## Hypothesis
H_names: the Gulf-type round seals write personal names of people of Dilmun, Magan or Meluhha. This is the hypothesis of Parpola, Vidale and Laursen. If it holds, and the attested names in cuneiform are a fair sample of such names, the seal sign sequences should be readable as ATTESTED names more easily than as fake names of the same shape.

## Name pool (fixed; from round35/names.tsv, compiled from CDLI ATF and Marchesi 2024 via the name search)
Included are people identified as of Dilmun, Magan or Meluhha (c. 2350–1700 BCE), plus the Dilmun gods' names (Inzak, Panipa), which may occur as name elements. Babylonian traders, Sumerian-named Mesopotamians and Kassite-period entries are excluded.

Syllables use cuneiform-style CV/V/VC/CVC values; DINGIR in names is read as *il*.

| Group | Names |
|---|---|
| Meluhha | na-na-za; sa-ma-ar; a-li-a-hi |
| Magan | ma-ni-um; na-du-be-li; we-du-um; a-tu |
| Dilmun | ri-mu-um; ia-ag-li-il; su-mu-le-il; u-la-pa-ni-pa; sa-mu-a; ri-ip-qa-tum; sa-ri-tam-bi; pa-qa-da; a-ba-si-di-a; ha-din-il; ia-ta-ra-tim; te-em-en-za-ag; mi-il-ki-il; in-za-ak-ga-mil; i-din-nin-in-za-ak; in-za-ki; ku-un-in-za-ki; ia-mi-u |
| Gods | in-za-ak; pa-ni-pa |

That is 27 forms.

## Seals (fixed)
- **Primary set:** the 8 round seals of round 30 (2153.1, 3863.1, 3897.1, 3898.1, 5227.1, 5228.1, 5229.1, 5232.1), plus the Dilmun round seal 415-803-001-717-354 (from Bourdeau's indusscript.net export, gulf.md; absent from our CSV). n = 9.
- Reading order follows the corpus direction field (R/L reversed). Because direction is uncertain on foreign seals, each seal may be read in either direction.
- **Sensitivity sets:**
  - drop 5228.1 (likely pseudo-script, round 31);
  - drop the stroke signs 001–004 and 031–033 (possible numerals or fillers).

## Model and fit (exact)
1. Each sign ID stands for one syllable.
2. Several signs may share a syllable, but a sign has only one syllable.
3. A seal is READ AS NAME X if a contiguous run of its signs (in either direction) spells name X exactly, and that run covers at least 60% of the seal's signs.
4. S(pool) = the maximum, over all sign→syllable keys, of the number of seals read as some name in the pool. It is computed exactly by backtracking over per-seal candidate readings with key consistency. Sign values shared across seals are the only constraint that gives the test teeth.

## Null and statistic
- Fake pools: 200 pools of 27 names each, with the same syllable-count distribution, and syllables drawn independently from the real pool's syllable frequencies (seed 35001+i).
- Statistic: S(real) against the distribution of S(fake). One-sided p = (1 + #{S_fake ≥ S_real}) / 201.
- Secondary: the identity of the best-reading assignment for the real pool (descriptive only; never a claimed decipherment).

## Power (run alongside; reported regardless)
- 100 synthetic seal sets. Each draws 9 real names at random (with replacement) and writes them with a random syllable→sign key over the same number of sign types, padded to the real seals' lengths.
- Padding: when the name is shorter than its seal (sticking to the ≥60% rule), a random filler sign is added on either side.
- The same test is run on each set. Power = share with p < 0.05.

## Decision (fixed)
- If power < 0.5: the test cannot discriminate at this sample size. Report the result as NON-INFORMATIVE whatever S(real) is, and park the name route until more inscribed Gulf seals or more native names exist.
- If power ≥ 0.5:
  - p < 0.05 → SUPPORT (seals readable as attested names beyond chance; still not a decipherment, because a free key was fitted);
  - p > 0.2 → NO SUPPORT;
  - otherwise INCONCLUSIVE.
