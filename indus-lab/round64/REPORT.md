# Round 64: Sound signs in a logosyllabic Linear B: SOUND PART RECOVERABLE

28 October 2026. Protocol and script locked at 9c27606 before any run. 90 runs at 600k steps, 8 processes. No amendments. No robustness draws were triggered.

## Verdict: SOUND PART RECOVERABLE (u\* = 29.1 uses per sound sign)

| Control | Bar | Result |
|---|---|---|
| Positive: Greek, no word signs, one word per text, S = 70 | median ≥ 0.70 | **0.863**, pass |
| Negative: Finnish, 42% word signs, no dividers, S = 70 | median ≤ 0.15 | **0.020**, pass (draws 0.00–0.08) |

In every logosyllabic set, 16.2% of tokens are word signs: 386 single-use word signs. Total sign inventories run from 456 to 556, against 582 for Indus. Each cell gives the median sound-token accuracy over 5 layouts.

| Sound-sign target S | Uses per sound sign u | **P: word signs, no dividers, opaque rule** | K: word signs, word per text | V: word signs, naive solver | B: no word signs, no dividers (u differs) |
|---:|---:|---:|---:|---:|---:|
| 70 | 29.1 | **0.855** (0.74–0.87) | 0.865 | 0.864 | 0.863 (u 49.3) |
| 100 | 17.4 | 0.194 (0.11–0.49) | 0.261 | 0.146 | 0.861 (u 30.0) |
| 130 | 13.9 | 0.118 | 0.186 | 0.069 | 0.826 (u 23.8) |
| 160 | 11.7 | 0.116 | 0.106 | 0.090 | 0.298 (u 19.9) |

**Indus mapping, by the locked rule:** the Indus top 286 signs average at least 29.1 uses each, so **N\* = 286**. The top 100 average 73 and the top 200 average 40.

## What it means
1. **Word signs at the Indus share do not stop the sound signs being cracked.** At 29 uses per sound sign, with one sign per syllable, a logosyllabic Linear B is solved as well as the pure syllabary (0.855 against 0.863), with or without word dividers.
2. **The line lies between 17 and 29 uses per sound sign. The ladder cannot place it more finely.**
   - At 17.4 uses, every logosyllabic set fails.
   - The pure syllabary B still works at 23.8 and fails at 19.9.
   - So u\* = 29.1 is a cautious figure. The true threshold is lower, somewhere between 17.4 and 29.1.
3. **For Indus, this changes the picture from round 63b.**
   - Rounds 63 and 63b treated all 582 signs as sound signs and found too few uses per sign.
   - If the script is logosyllabic and its sound signs lie among its common signs, those signs are used far more often: 73 times each for the top 100 and 40 for the top 200. Both are above this round's line.
   - **On the logosyllabic assumption, the size of the corpus is not what blocks decipherment.**
4. **The opaque rule matters little** (P against V at S = 70: 0.855 against 0.864). In this simulation word signs are rare and do not disturb the sound statistics much.

## Limits (stated in the protocol, and what they do to the result)
- **Kinder than Indus:**
  - Every simulated word sign is used once, so separating word signs from sound signs is easy. Indus may have frequent word signs (740, the jar, for example) and rare sound signs.
  - The language is supplied.
  - The number of sound values (about 70) is known.
- **The recovered level has no homophones.** S = 70 means one sign per syllable. Once homophones are added (S ≥ 100), this small corpus is no longer enough. Indus may have homophones.
- **The Indus figures are an extrapolation.** The Indus top 100 (73 uses) lies beyond what the Linear B corpus can simulate (at most 29 uses). The direction (more uses is easier) is supported. The size of the gain is not measured.
- **N\* = 286 uses a mean.** Within the top 286 Indus signs, the rarest have far fewer than 29 uses. N\* says how many sound signs the corpus could carry *on average*, not that sign 286 is readable.

## Bearing on the mission
If the Indus script is logosyllabic, which is the majority scholarly view and consistent with round 52, then decipherment from the existing corpus is **not ruled out by its size**. That moves the bottleneck to two other questions:
1. **Which language?** Here the solver was given Greek. The Finnish control shows that a wrong language does not recover the truth. It does not show whether a wrong language would *look* as good as the right one from the inside, without knowing the answer. Rounds 45 and 47 found that wrong languages often do.
2. **Which signs are sound signs?** In the simulation, a frequency rule separated them almost perfectly. In Indus it will not.

## Ledger
Measurement, cluster K3, no factor. Adds fact C22.

## Reproduce
`cd indus-lab/round64 && ../../ext/venv/bin/python run64.py`. This needs numpy (`ext/venv`), NeuroDecipher data and lexibank IDS. Set `R64_PROCS` to change the number of processes.
