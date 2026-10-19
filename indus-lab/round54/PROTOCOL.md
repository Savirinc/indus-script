# Round 54 — Is there a syllabic core? A free-combination test for the logosyllabic reading (pre-registered)

Written 19 October 2026, before `extract54.py` or `run54.py` exist and before any neighbour statistic has been computed on any corpus. Committed before code.

## Question
Conjecture A3 says the Indus script is logosyllabic: a minority of signs with syllabic values that combine with almost anything and carry most of the tokens, plus a majority of word-signs and determinatives that sit in restricted contexts. Rounds 52–52b excluded alphabets and syllabaries but could not separate this from a system in which each sign is a word. The defining feature of a syllabic core is **combinatorial freedom**: a syllabogram's neighbours are whatever the words of the language put next to it, so its neighbour set is nearly as diverse as a random reordering would make it; a word-sign or determinative keeps company with few partners. This round asks whether the Indus corpus contains a free-combining core of the kind Akkadian syllabograms form, and whether that core is distinguishable from what a logographic corpus shows.

## Statistic
For a sample of N = 8,726 tokens in Indus-shaped texts (round 52 sampler, windows from units), for each sign type s with count f(s) ≥ 10: R(s) = number of distinct right-neighbour types within texts, L(s) likewise on the left. Null: sign order permuted within each text (unigram counts and text lengths kept), 30 permutations; E[R(s)], E[L(s)] are the permutation means. **Freedom** F(s) = (R(s) + L(s)) / (E[R(s)] + E[L(s)]). Near 1: as free as chance; well below 1: restricted.

**Core share** C = share of tokens, among tokens of types with f ≥ 10, carried by types with F ≥ θ. The coverage of the f ≥ 10 set is reported beside it.

## Gold labels (Akkadian)
In CDLI ATF for Akkadian, syllabic signs are lower case, Sumerograms are enclosed in `_ … _` (possibly spanning words), determinatives are in braces, numerals are numerals. A sign **type** is labelled PHON if ≥ 70% of its tokens are syllabic, LOGO if ≥ 70% are Sumerogram, determinative or numeral, else unlabelled. Corpora: OBL (Old Babylonian letters), OAL (Old Assyrian letters), SEAL-akk (seal legends with `lang akk`). Labels are used only for the positive control and for θ.

## Positive control
On OBL and OAL, each over 50 samples, the AUC of F separating PHON from LOGO types must average ≥ 0.75 in both. θ is the F value maximising balanced accuracy on the pooled OBL + OAL types, fixed before Indus is scored. If either AUC < 0.75: METHOD-FAIL.

## Negative control
CHN (Shijing, one sign per word) and OBI (oracle bone) have no syllabic core in the Akkadian sense. If the smaller of C_OBL and C_OAL does not exceed the larger of C_CHN and C_OBI by at least 0.20 (means over 50 samples), the statistic does not discriminate a syllabic core from freely combining word-signs (function words), and the round is METHOD-FAIL with that stated. SUX (Ur III, mixed) and EGY (tomb inscriptions, mixed) are reported as intermediate references.

## Verdict (Indus corpus, scored once, after θ is fixed)
Let C_akk = min(C_OBL, C_OAL) and C_logo = max(C_CHN, C_OBI), with sample sd.
- `CORE-PRESENT`: C_Indus ≥ C_akk − 2 sd and C_Indus > C_logo + 2 sd.
- `NO-CORE`: C_Indus ≤ C_logo + 2 sd and C_Indus < C_akk − 2 sd.
- `BETWEEN`: otherwise.
- `METHOD-FAIL`: either control fails.
Also reported: the Indus F distribution, the signs with highest F and their token share, and the same for the lowest.

## Reading of outcomes, stated now
- CORE-PRESENT narrows A3 towards a mixed system with a syllabic component and makes the one-sign-per-word reading less likely; it says nothing about which syllables.
- NO-CORE weakens A3's syllabic component and favours word-signs throughout (names and titles as logograms, A2), or a system too short-texted to show its syllabary.
- BETWEEN: no status change.
Confounds: Indus texts are shorter than Akkadian lines even after windowing (windows are matched, so this is controlled); the f ≥ 10 filter admits a smaller share of Indus tokens (582 types) than of Akkadian (250), which is why C is conditional on f ≥ 10 and the coverage is reported.

## Samples, seeds, pins
B = 50 samples per corpus, seed 54001 + corpus index × 1000 + sample index; 30 permutations per sample, seed derived. `extract54.py` writes `controls/{OBL,OAL,SEAL}.txt` with per-token flags (`SIGN/p`, `SIGN/l`, `SIGN/-`); SUX, EGY, OBI, CHN are read from rounds 52–52b unchanged. `run54.py` standard library only; `results.json`, `run54.log`, `REPORT.md`. One run; code fixes before results are amendments.
